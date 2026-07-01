"""
Unified, read-only connectors for the daily-insights routine.
=============================================================
One import surface for every backend the routine explores. All connectors are
**read-only by contract** — query helpers reject anything that is not a
SELECT/WITH (ClickHouse, Neon) and only ever call list/retrieve on Stripe and
Mixpanel's read API.

Credentials come from the repo-root `.env` (loaded with the same hand-rolled
loader the rest of the repo uses — NOT python-dotenv). Nothing here is specific
to a single analysis; it's the plumbing the rotating exploration sits on.

Backends & env vars (see docs/data-sources/*.md):
  ClickHouse : CLICKHOUSE_URL, CLICKHOUSE_USERNAME, CLICKHOUSE_PASSWORD
  Neon       : NEON_DATABASE_URL
  Stripe     : STRIPE_SECRET_KEY
  Mixpanel   : MIXPANEL_SERVICE_ACCOUNT_USERNAME/_SECRET, MIXPANEL_PROJECT_ID

Quick check:  python -m insights.connections     (smoke-tests all four)
"""
from __future__ import annotations

import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"

_READONLY_RX = re.compile(r"^\s*(with|select)\b", re.IGNORECASE)


def load_env(path: Path = ENV_PATH) -> None:
    """Populate os.environ from .env (does not overwrite existing vars)."""
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, val = line.partition("=")
        key, val = key.strip(), val.strip().strip('"').strip("'")
        os.environ.setdefault(key, val)


def _assert_readonly(sql: str) -> None:
    if not _READONLY_RX.match(sql):
        raise ValueError("Only SELECT / WITH queries are allowed (read-only contract).")
    # cheap guard against multi-statement injection of a write
    lowered = sql.lower()
    for bad in (";insert", ";update", ";delete", ";drop", ";alter", ";create", ";truncate"):
        if bad in lowered.replace(" ", ""):
            raise ValueError(f"Refusing multi-statement query containing {bad!r}.")


# ── ClickHouse ────────────────────────────────────────────────────────────────
def clickhouse_client():
    import clickhouse_connect

    load_env()
    url = os.environ["CLICKHOUSE_URL"]
    # URL is https://host:port ; clickhouse_connect wants host/port/secure split
    m = re.match(r"https?://([^:/]+):?(\d+)?", url)
    host = m.group(1)
    port = int(m.group(2)) if m.group(2) else 8443
    return clickhouse_connect.get_client(
        host=host,
        port=port,
        username=os.environ["CLICKHOUSE_USERNAME"],
        password=os.environ["CLICKHOUSE_PASSWORD"],
        secure=url.startswith("https"),
        connect_timeout=30,
        query_limit=100_000,
        settings={"readonly": 1},
    )


def ch_df(sql: str, parameters: dict | None = None):
    """Run a read-only ClickHouse query, return a pandas DataFrame."""
    _assert_readonly(sql)
    client = clickhouse_client()
    try:
        return client.query_df(sql, parameters=parameters or {})
    finally:
        client.close()


# ── Neon (Postgres: jelou-ai-assistant) ─────────────────────────────────────────
def neon_conn():
    import psycopg

    load_env()
    return psycopg.connect(os.environ["NEON_DATABASE_URL"], connect_timeout=30)


def neon_df(sql: str, params: tuple | None = None):
    import pandas as pd

    _assert_readonly(sql)
    with neon_conn() as c, c.cursor() as cur:
        cur.execute("SET TRANSACTION READ ONLY")
        cur.execute(sql, params or ())
        cols = [d[0] for d in cur.description]
        rows = cur.fetchall()
    return pd.DataFrame(rows, columns=cols)


# ── Stripe ──────────────────────────────────────────────────────────────────────
def stripe_client():
    import stripe

    load_env()
    stripe.api_key = os.environ["STRIPE_SECRET_KEY"]
    return stripe


# ── Mixpanel (Query API via service account) ─────────────────────────────────────
MIXPANEL_QUERY_BASE = "https://mixpanel.com/api/query"


def mixpanel_jql(script: str, params: dict | None = None):
    """Run a JQL script against the project. Returns parsed JSON (list)."""
    import requests

    load_env()
    auth = (
        os.environ["MIXPANEL_SERVICE_ACCOUNT_USERNAME"],
        os.environ["MIXPANEL_SERVICE_ACCOUNT_SECRET"],
    )
    data = {"script": script, "project_id": os.environ["MIXPANEL_PROJECT_ID"]}
    if params:
        import json

        data["params"] = json.dumps(params)
    r = requests.post(f"{MIXPANEL_QUERY_BASE}/jql", auth=auth, data=data, timeout=60)
    r.raise_for_status()
    return r.json()


def mixpanel_segmentation(event: str, from_date: str, to_date: str,
                          on: str | None = None, unit: str = "day", type_: str = "general"):
    """Segmentation API: event volume (or uniques) over a date range.
    from/to are 'YYYY-MM-DD'. `on` is a property expression to segment by."""
    import requests

    load_env()
    auth = (
        os.environ["MIXPANEL_SERVICE_ACCOUNT_USERNAME"],
        os.environ["MIXPANEL_SERVICE_ACCOUNT_SECRET"],
    )
    params = {
        "project_id": os.environ["MIXPANEL_PROJECT_ID"],
        "event": event,
        "from_date": from_date,
        "to_date": to_date,
        "unit": unit,
        "type": type_,
    }
    if on:
        params["on"] = on
    r = requests.get(f"{MIXPANEL_QUERY_BASE}/segmentation", auth=auth, params=params, timeout=60)
    r.raise_for_status()
    return r.json()


# ── Smoke test ────────────────────────────────────────────────────────────────
def smoke_test() -> dict:
    """Ping every backend; return {name: (ok, detail)}."""
    results = {}

    try:
        df = ch_df("SELECT count() AS n FROM silver.chatbot_companies WHERE _peerdb_is_deleted = 0")
        results["clickhouse"] = (True, f"chatbot_companies rows: {int(df['n'][0]):,}")
    except Exception as e:
        results["clickhouse"] = (False, f"{type(e).__name__}: {e}")

    try:
        df = neon_df("SELECT count(*) AS n FROM chat_sessions")
        results["neon"] = (True, f"chat_sessions rows: {int(df['n'][0]):,}")
    except Exception as e:
        results["neon"] = (False, f"{type(e).__name__}: {e}")

    try:
        s = stripe_client()
        acct = s.Account.retrieve()
        results["stripe"] = (True, f"account: {acct.id} ({getattr(acct, 'default_currency', '?')})")
    except Exception as e:
        results["stripe"] = (False, f"{type(e).__name__}: {e}")

    try:
        out = mixpanel_jql("function main(){ return Events({from_date:'2026-06-01',"
                           "to_date:'2026-06-01'}).groupBy([], mixpanel.reducer.count()); }")
        n = out[0]["value"] if out else 0
        results["mixpanel"] = (True, f"events on 2026-06-01: {n:,}")
    except Exception as e:
        results["mixpanel"] = (False, f"{type(e).__name__}: {e}")

    return results


if __name__ == "__main__":
    load_env()
    print("Smoke-testing all backends...\n")
    for name, (ok, detail) in smoke_test().items():
        mark = "OK  " if ok else "FAIL"
        print(f"  [{mark}] {name:12} {detail}")

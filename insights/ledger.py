"""
Insights ledger — the memory that makes "new" mean new.
=======================================================
Two artifacts, kept in sync:
  - insights.jsonl        machine record, one JSON object per insight (append-only).
  - INSIGHTS_LOG.md       human-readable log, newest first.

Novelty model. Every insight has a `topic_key` = normalized (theme, angle-ish,
metric, segment). The routine calls `classify(topic_key, value)` before writing:
  - "new"    — topic_key never seen.
  - "update" — seen, but the value moved beyond the relative threshold (default 15%).
  - "stale"  — seen and essentially unchanged → do NOT report it again.

This is what lets the job "find new insights" instead of re-printing the same
numbers daily: the rotation varies WHAT gets looked at; the ledger vetoes
anything already known and unchanged.

CLI:
  python -m insights.ledger list [N]     # last N insights
  python -m insights.ledger keys          # all known topic_keys
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
JSONL_PATH = SCRIPT_DIR / "insights.jsonl"
LOG_PATH = SCRIPT_DIR / "INSIGHTS_LOG.md"

UPDATE_THRESHOLD = 0.15  # relative move required to re-surface a known topic


def normalize_key(*parts: str) -> str:
    raw = "::".join(str(p) for p in parts if p)
    raw = raw.lower()
    raw = re.sub(r"[^a-z0-9]+", "-", raw).strip("-")
    return raw


def load_insights() -> list[dict]:
    if not JSONL_PATH.exists():
        return []
    out = []
    for line in JSONL_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return out


def known_keys() -> dict[str, dict]:
    """Latest record per topic_key."""
    latest: dict[str, dict] = {}
    for rec in load_insights():
        k = rec.get("topic_key")
        if k:
            latest[k] = rec  # jsonl is append-order → last wins
    return latest


def _to_number(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.search(r"-?\d+\.?\d*", v.replace(",", ""))
        if m:
            return float(m.group())
    return None


def classify(topic_key: str, value=None, threshold: float = UPDATE_THRESHOLD) -> tuple[str, dict | None]:
    """Return ('new'|'update'|'stale', prior_record_or_None)."""
    prior = known_keys().get(topic_key)
    if prior is None:
        return "new", None
    old = _to_number(prior.get("value"))
    new = _to_number(value)
    if old is None or new is None:
        # non-numeric — treat as stale unless the one-liner text changed a lot
        return "stale", prior
    if old == 0:
        return ("update" if new != 0 else "stale"), prior
    if abs(new - old) / abs(old) >= threshold:
        return "update", prior
    return "stale", prior


def append_insight(rec: dict) -> dict:
    """Append one insight. rec should carry at least: title, one_liner, topic_key.
    Fills date/status/id if missing. Writes both jsonl and the markdown log."""
    rec = dict(rec)
    rec.setdefault("date", datetime.now().date().isoformat())
    rec.setdefault("topic_key", normalize_key(rec.get("theme", ""), rec.get("metric", ""),
                                              rec.get("segment", "")))
    if "status" not in rec:
        status, prior = classify(rec["topic_key"], rec.get("value"))
        rec["status"] = status
        if prior is not None:
            rec["prior_value"] = prior.get("value")
    rec.setdefault("id", f"{rec['date']}-{rec['topic_key'][:40]}")

    with JSONL_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    _prepend_markdown(rec)
    return rec


def _prepend_markdown(rec: dict) -> None:
    badge = {"new": "🆕 NEW", "update": "🔁 UPDATE", "stale": "· stale"}.get(rec.get("status"), "")
    src = ", ".join(rec.get("sources", [])) if isinstance(rec.get("sources"), list) else rec.get("sources", "")
    block = [
        f"### {rec['date']} — {badge} — {rec.get('title', '(untitled)')}",
        "",
        f"{rec.get('one_liner', '')}",
        "",
        f"- **Metric:** {rec.get('metric','?')} = **{rec.get('value','?')}**"
        + (f"  (was {rec['prior_value']})" if rec.get("prior_value") is not None else ""),
        f"- **Theme/angle:** {rec.get('theme','?')} — {rec.get('angle','')}",
        f"- **Segment:** {rec.get('segment','overall')}  ·  **Sources:** {src}",
    ]
    if rec.get("confidence"):
        block.append(f"- **Confidence:** {rec['confidence']}")
    if rec.get("caveat"):
        block.append(f"- **Caveat:** {rec['caveat']}")
    block.append("\n---\n")
    new_block = "\n".join(block)

    header = "# Insights log\n\nNewest first. Written by the daily routine; each entry is a NEW finding or a\nmaterial UPDATE to a prior one. Seeded with pre-existing findings so they are not\nre-reported.\n\n---\n\n"
    if LOG_PATH.exists():
        existing = LOG_PATH.read_text(encoding="utf-8")
        if existing.startswith("# Insights log"):
            body = existing.split("---\n\n", 1)[-1]
            LOG_PATH.write_text(header + new_block + "\n" + body, encoding="utf-8")
            return
    LOG_PATH.write_text(header + new_block + "\n", encoding="utf-8")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "list"
    if cmd == "keys":
        for k in sorted(known_keys()):
            print(k)
    else:
        n = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        recs = load_insights()[-n:]
        for r in recs:
            print(f"[{r.get('status','?'):6}] {r.get('date')}  {r.get('title')}  "
                  f"({r.get('metric')}={r.get('value')})")
        print(f"\n{len(load_insights())} total insights; {len(known_keys())} distinct topics.")

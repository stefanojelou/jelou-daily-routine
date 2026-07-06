"""
Digest delivery — push the day's NEW/UPDATE insights out.
=========================================================
Delivery precedence (first that is configured wins; always also writes a file):
  1. Slack Incoming Webhook  — set SLACK_WEBHOOK_URL in .env  (most reliable for cron)
  2. Email via SMTP          — set SMTP_HOST/PORT/USER/PASS + DIGEST_EMAIL_TO
  3. File only               — data/digests/<date>-insights.md  (+ stdout)

We deliberately DON'T depend on the Slack/Gmail MCP here: interactive OAuth does
not reliably survive into headless/scheduled runs. A webhook URL is a static
secret that always works. If neither channel is set, the digest still lands as a
committed markdown file so nothing is lost.

Usage (from the routine):
    from insights.digest import send_digest
    send_digest(date, assignment, new_and_updated_insights)
"""
from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path

from insights.connections import load_env

SCRIPT_DIR = Path(__file__).resolve().parent
# Tracked in git so the GitHub Action can email the newest digest on push.
DIGEST_DIR = SCRIPT_DIR / "digests"


def _format_markdown(date: str, assignment: dict, insights: list[dict]) -> str:
    new = [i for i in insights if i.get("status") == "new"]
    upd = [i for i in insights if i.get("status") == "update"]
    lines = [
        f"# Daily insights — {date}",
        "",
        f"**Explored:** {assignment.get('theme','?')} → _{assignment.get('angle','')}_  "
        f"(lens: {assignment.get('segment','overall')})",
        "",
    ]
    if not insights:
        lines += ["_No new or materially-changed insight surfaced today. The angle was explored "
                  "and came up dry — logged for coverage._", ""]
    if new:
        lines.append(f"## 🆕 New ({len(new)})")
        for i in new:
            lines.append(f"- **{i.get('title')}** — {i.get('one_liner')}  "
                         f"_({i.get('metric')} = {i.get('value')})_")
        lines.append("")
    if upd:
        lines.append(f"## 🔁 Updated ({len(upd)})")
        for i in upd:
            lines.append(f"- **{i.get('title')}** — {i.get('metric')} moved to "
                         f"**{i.get('value')}** (was {i.get('prior_value')}). {i.get('one_liner')}")
        lines.append("")
    lines += ["---", "Full log: `insights/INSIGHTS_LOG.md` · backlog: `insights/questions.md`"]
    return "\n".join(lines)


def _format_slack(date: str, assignment: dict, insights: list[dict]) -> dict:
    new = [i for i in insights if i.get("status") == "new"]
    upd = [i for i in insights if i.get("status") == "update"]
    header = f":mag: *Daily insights — {date}*"
    ctx = (f"Explored: *{assignment.get('theme','?')}* → {assignment.get('angle','')} "
           f"(lens: {assignment.get('segment','overall')})")
    blocks = [
        {"type": "header", "text": {"type": "plain_text", "text": f"Daily insights — {date}"}},
        {"type": "context", "elements": [{"type": "mrkdwn", "text": ctx}]},
        {"type": "divider"},
    ]
    if not insights:
        blocks.append({"type": "section", "text": {"type": "mrkdwn",
                      "text": "_No new or materially-changed insight today — angle explored, came up dry._"}})
    for i in new:
        blocks.append({"type": "section", "text": {"type": "mrkdwn",
                      "text": f":new: *{i.get('title')}*\n{i.get('one_liner')}\n"
                              f"`{i.get('metric')} = {i.get('value')}`"}})
    for i in upd:
        blocks.append({"type": "section", "text": {"type": "mrkdwn",
                      "text": f":arrows_counterclockwise: *{i.get('title')}*\n"
                              f"{i.get('metric')} → *{i.get('value')}* (was {i.get('prior_value')})\n"
                              f"{i.get('one_liner')}"}})
    return {"text": header, "blocks": blocks}


def _safe_print(s: str) -> None:
    """Print without crashing on a legacy Windows console codepage."""
    try:
        print(s)
    except UnicodeEncodeError:
        import sys
        sys.stdout.buffer.write(s.encode("utf-8", "replace"))
        sys.stdout.buffer.write(b"\n")


def _write_file(date: str, md: str) -> Path:
    DIGEST_DIR.mkdir(parents=True, exist_ok=True)
    p = DIGEST_DIR / f"{date}-insights.md"
    p.write_text(md, encoding="utf-8")
    return p


def send_digest(date: str, assignment: dict, insights: list[dict], dry_run: bool = False) -> dict:
    """Deliver the digest. Returns {channel, ok, detail, file}."""
    load_env()
    md = _format_markdown(date, assignment, insights)
    path = _write_file(date, md)
    result = {"file": str(path), "channel": "file", "ok": True, "detail": f"wrote {path.name}"}

    if dry_run:
        result["detail"] += " (dry-run: no external send)"
        _safe_print(md)
        return result

    webhook = os.environ.get("SLACK_WEBHOOK_URL")
    if webhook:
        try:
            import requests
            r = requests.post(webhook, data=json.dumps(_format_slack(date, assignment, insights)),
                              headers={"Content-Type": "application/json"}, timeout=30)
            r.raise_for_status()
            result.update(channel="slack", ok=True, detail="posted to Slack webhook")
            return result
        except Exception as e:
            result.update(channel="slack", ok=False, detail=f"Slack failed: {e}; kept file")
            return result

    if os.environ.get("SMTP_HOST") and os.environ.get("DIGEST_EMAIL_TO"):
        try:
            import smtplib
            from email.mime.text import MIMEText
            msg = MIMEText(md, "plain", "utf-8")
            msg["Subject"] = f"Daily insights — {date}"
            msg["From"] = os.environ.get("SMTP_USER", "insights@jelou")
            msg["To"] = os.environ["DIGEST_EMAIL_TO"]
            with smtplib.SMTP(os.environ["SMTP_HOST"], int(os.environ.get("SMTP_PORT", 587))) as srv:
                srv.starttls()
                if os.environ.get("SMTP_USER"):
                    srv.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
                srv.send_message(msg)
            result.update(channel="email", ok=True, detail=f"emailed {os.environ['DIGEST_EMAIL_TO']}")
            return result
        except Exception as e:
            result.update(channel="email", ok=False, detail=f"email failed: {e}; kept file")
            return result

    result["detail"] += " (no SLACK_WEBHOOK_URL / SMTP configured — file only)"
    return result


if __name__ == "__main__":
    # demo with a synthetic insight
    from insights.rotation import assignment_for
    a = assignment_for()
    demo = [{"status": "new", "title": "Demo insight", "one_liner": "This is a dry-run sample.",
             "metric": "demo_metric", "value": "42%"}]
    print(send_digest(datetime.now().date().isoformat(), a, demo, dry_run=True))

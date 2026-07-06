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

import html as _html
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

    def block(i: dict, updated: bool = False) -> list[str]:
        b = [f"### {'🔁 ' if updated else '🆕 '}{i.get('title','(untitled)')}", ""]
        b.append(i.get("one_liner", ""))
        b.append("")
        metric = f"**{i.get('metric','?')} = {i.get('value','?')}**"
        if updated and i.get("prior_value") is not None:
            metric += f"  _(was {i['prior_value']})_"
        b.append(f"- **Metric:** {metric}")
        src = i.get("sources")
        if isinstance(src, list):
            src = ", ".join(src)
        if src:
            b.append(f"- **Sources:** {src}")
        if i.get("confidence"):
            b.append(f"- **Confidence:** {i['confidence']}")
        if i.get("caveat"):
            b.append(f"- **Caveat:** {i['caveat']}")
        b.append("")
        return b

    if new:
        lines.append(f"## 🆕 New ({len(new)})")
        lines.append("")
        for i in new:
            lines += block(i)
    if upd:
        lines.append(f"## 🔁 Updated ({len(upd)})")
        lines.append("")
        for i in upd:
            lines += block(i, updated=True)

    # context footer: what else was in scope today + where to dig
    twist = assignment.get("twist")
    qs = assignment.get("questions") or []
    lines.append("---")
    if twist:
        lines.append(f"**Creativity twist applied:** {twist}")
    if qs:
        lines.append("**Backlog questions in scope:** " + "; ".join(qs))
    lines.append("Full log: `insights/INSIGHTS_LOG.md` · backlog: `insights/questions.md`")
    return "\n".join(lines)


def _format_html(date: str, assignment: dict, insights: list[dict]) -> str:
    """Email-safe HTML (inline styles only — email clients strip <style>/CSS files).
    Jelou palette from docs/dashboard-app/design.md."""
    e = _html.escape
    new = [i for i in insights if i.get("status") == "new"]
    upd = [i for i in insights if i.get("status") == "update"]

    def row(label: str, value_html: str) -> str:
        return (f'<div style="font-size:13px;line-height:1.45;color:#727c94;margin:3px 0">'
                f'<b style="color:#161c2b">{label}:</b> {value_html}</div>')

    def card(i: dict, updated: bool) -> str:
        badge = ("🔁" if updated else "🆕")
        metric = f'{e(str(i.get("metric","?")))} = {e(str(i.get("value","?")))}'
        if updated and i.get("prior_value") is not None:
            metric += f' <span style="color:#959daf">(was {e(str(i["prior_value"]))})</span>'
        src = i.get("sources")
        src = ", ".join(src) if isinstance(src, list) else (src or "")
        rows = [row("Metric", f'<span style="color:#00a2cf;font-weight:700">{metric}</span>')]
        if src:
            rows.append(row("Sources", e(str(src))))
        if i.get("confidence"):
            rows.append(row("Confidence", e(str(i["confidence"]))))
        if i.get("caveat"):
            rows.append(row("Caveat", e(str(i["caveat"]))))
        return (
            '<div style="border:1px solid #e3e5ec;border-radius:12px;padding:16px 18px;'
            'margin:0 0 14px;background:#ffffff">'
            f'<div style="font-weight:700;font-size:16px;color:#0f1f33;margin-bottom:6px">'
            f'{badge} {e(str(i.get("title","(untitled)")))}</div>'
            f'<div style="font-size:14px;line-height:1.55;color:#303b56;margin-bottom:10px">'
            f'{e(str(i.get("one_liner","")))}</div>'
            + "".join(rows) + "</div>"
        )

    parts = [
        '<div style="max-width:640px;margin:0 auto;padding:20px;background:#eef1f4;'
        'font-family:-apple-system,BlinkMacSystemFont,\'Segoe UI\',Roboto,Helvetica,Arial,sans-serif">',
        f'<div style="font-size:22px;font-weight:800;color:#0f1f33">Daily insights '
        f'<span style="color:#727c94;font-weight:600">— {e(date)}</span></div>',
        f'<div style="font-size:13px;color:#727c94;margin:4px 0 18px">Explored: '
        f'<b style="color:#303b56">{e(str(assignment.get("theme","?")))}</b> → '
        f'{e(str(assignment.get("angle","")))} · lens: {e(str(assignment.get("segment","overall")))}</div>',
    ]
    if not insights:
        parts.append('<div style="font-size:14px;color:#303b56;background:#fff;border:1px solid #e3e5ec;'
                     'border-radius:12px;padding:16px">No new or materially-changed insight today — '
                     'the angle was explored and came up dry (logged for coverage).</div>')
    if new:
        parts.append(f'<div style="font-size:13px;font-weight:700;color:#00b3c7;margin:6px 0 8px">🆕 NEW ({len(new)})</div>')
        parts += [card(i, False) for i in new]
    if upd:
        parts.append(f'<div style="font-size:13px;font-weight:700;color:#d39c00;margin:14px 0 8px">🔁 UPDATED ({len(upd)})</div>')
        parts += [card(i, True) for i in upd]

    foot = ['<div style="font-size:12px;color:#8a93a6;border-top:1px solid #e3e5ec;margin-top:8px;padding-top:12px">']
    if assignment.get("twist"):
        foot.append(f'<div><b style="color:#727c94">Twist applied:</b> {e(str(assignment["twist"]))}</div>')
    qs = assignment.get("questions") or []
    if qs:
        foot.append('<div style="margin-top:4px"><b style="color:#727c94">Backlog in scope:</b> '
                    + e("; ".join(qs)) + '</div>')
    foot.append('<div style="margin-top:8px">Full log: <code>insights/INSIGHTS_LOG.md</code> · '
                'backlog: <code>insights/questions.md</code></div></div>')
    parts += foot
    parts.append("</div>")
    return "\n".join(parts)


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
    # HTML sibling for the email Action (rendered body; .md stays the plain-text fallback)
    (DIGEST_DIR / f"{date}-insights.html").write_text(
        _format_html(date, assignment, insights), encoding="utf-8")
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

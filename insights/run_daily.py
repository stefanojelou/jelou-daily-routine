"""
Daily brief generator — assembles everything the routine needs for one run.
============================================================================
This is the deterministic half of the daily job. It does NOT do the exploration
(that's the Claude agent's job — see DAILY_ROUTINE.md); it produces the *brief*:
today's rotating assignment + the ledger context (what's already known, so the
agent knows what "new" means) + a connectivity check.

  python -m insights.run_daily            # print today's brief
  python -m insights.run_daily --date 2026-07-04
  python -m insights.run_daily --check    # brief + live connectivity smoke test

The agent then: reads this brief → queries via insights.connections → for each
finding calls insights.ledger.classify() and appends only new/updated ones →
insights.digest.send_digest().
"""
from __future__ import annotations

import argparse
from datetime import datetime

from insights.ledger import known_keys, load_insights
from insights.rotation import assignment_for, render_markdown


def build_brief(date=None, check=False) -> str:
    a = assignment_for(date)
    parts = [render_markdown(a), ""]

    known = known_keys()
    parts.append(f"## Already known — do NOT re-report unless the number moved (>15%)\n")
    if known:
        for rec in sorted(known.values(), key=lambda r: r.get("date", ""), reverse=True):
            parts.append(f"- [{rec.get('date')}] **{rec.get('title')}** "
                         f"({rec.get('metric')} = {rec.get('value')}) — key: `{rec.get('topic_key')}`")
    else:
        parts.append("- (ledger empty)")
    parts.append(f"\n_{len(load_insights())} insights logged, {len(known)} distinct topics._\n")

    if check:
        from insights.connections import smoke_test
        parts.append("## Connectivity\n")
        for name, (ok, detail) in smoke_test().items():
            parts.append(f"- [{'OK' if ok else 'FAIL'}] {name}: {detail}")

    return "\n".join(parts)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--date")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    d = datetime.strptime(args.date, "%Y-%m-%d").date() if args.date else None
    brief = build_brief(d, check=args.check)
    try:
        print(brief)
    except UnicodeEncodeError:
        import sys
        sys.stdout.buffer.write(brief.encode("utf-8", "replace"))

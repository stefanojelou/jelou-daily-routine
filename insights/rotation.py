"""
Rotation engine — the "creative" core of the daily routine.
============================================================
The point of the daily job is to find something NEW, so it must not run the same
analysis every day. This module turns a date into a fresh **exploration
assignment** by combining four independent rotating axes plus the live question
backlog:

  1. THEME     — a domain focus (7 of them). Cycles ONE STEP PER RUN (business-day
                 index), not per weekday — so a weekdays-only schedule still covers
                 all 7 themes over ~1.5 weeks instead of stranding the weekend ones.
  2. ANGLE     — a specific facet within the theme, rotated by ISO week number so
                 the same theme digs a different facet on its next visit.
  3. SEGMENT   — a slice-the-data lens (by channel, cohort, geo, device, ...),
                 rotated on a co-prime cycle so THEME×ANGLE×SEGMENT rarely repeats.
  4. TWIST     — a creativity prompt (join two sources, invert the funnel, find
                 the outlier, ...) to push past the obvious cut.
  + QUESTIONS  — N items pulled from insights/questions.md (the living backlog),
                 rotated so unexplored questions surface over time.

Selection is DETERMINISTIC given the date (seeded by a hash of the ISO date), so
a run is reproducible and testable, yet varied across dates. The ledger
(insights/ledger.py) then enforces novelty on top of this — an assignment that
happens to repeat still won't re-report a known number unless it moved.

CLI:
  python -m insights.rotation                 # today's assignment
  python -m insights.rotation 2026-07-04       # a specific date
  python -m insights.rotation --week 2026-07-04  # show the whole week
"""
from __future__ import annotations

import hashlib
import random
import sys
from datetime import date, datetime, timedelta
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
QUESTIONS_PATH = SCRIPT_DIR / "questions.md"

# ── Axis 1: themes ──────────────────────────────────────────────────────────────
# 7 themes, each naming the backends it leans on and the events/tables to reach
# for. Selected by a business-day run-index (see _run_index) so the cycle advances
# one theme per actual run — the weekday labels below are just mnemonic legacy.
THEMES = {
    0: {  # Monday
        "key": "acquisition",
        "name": "Acquisition & signup funnel",
        "sources": ["mixpanel", "clickhouse"],
        "focus": "How self-serve users arrive and get through signup. Mixpanel "
                 "funnel onboarding_started → step_* → signup_completed; initial_utm_* "
                 "channels; device/browser (mobile vs desktop); home_variant; "
                 "has_template at signup. Cross to silver.chatbot_companies for signup counts.",
        "angles": [
            "Channel quality: which initial_utm_source/medium converts land→signup best (and worst)?",
            "Mobile vs desktop: where in the funnel do mobile signups drop that desktop don't?",
            "home_variant / has_template at onboarding_started: does landing context change conversion?",
            "Step-level leakage: which signup step (email/password/profiling) sheds the most users?",
        ],
    },
    1: {  # Tuesday
        "key": "activation",
        "name": "Activation & time-to-milestone",
        "sources": ["mixpanel", "neon", "clickhouse"],
        "focus": "Speed from signup to first meaningful action. Time deltas from "
                 "signup_completed to first node_used / skill_created / "
                 "tester_session_started / agent_message_sent; first workflow execution "
                 "(gold.workflow_executions_weekly); first Neon chat_session.",
        "angles": [
            "Time-to-first-value: distribution of hours from signup to first node_used / skill_created.",
            "Which first milestone (tester vs agent chat vs node) best predicts a 2nd-week return?",
            "Same-day activators vs delayed: does day-0 activation beat day-1..7 on retention?",
            "The dead-on-arrival cohort: signed up, never fired a single activation event — how big, what channel?",
        ],
    },
    2: {  # Wednesday
        "key": "templates",
        "name": "Templates: intent vs. action",
        "sources": ["mixpanel", "neon", "stripe"],
        "focus": "Template funnel and whether templates drive or merely mark serious "
                 "users. Mixpanel template_installed / template_preview_opened; Neon "
                 "template_instantiations; reconcile intent (preview/install click) vs "
                 "completion vs downstream activation/pay. (Prior: lift is a fragile marker.)",
        "angles": [
            "Preview→install→activate: the template micro-funnel and where it leaks.",
            "Which specific templates correlate with activation, and which are dead ends?",
            "Template installers vs non-installers: agent-usage depth once activated (not just pay).",
            "Time-from-install-to-first-use: do installs sit unused (shelfware)?",
        ],
    },
    3: {  # Thursday
        "key": "monetization",
        "name": "Monetization & pay-drivers",
        "sources": ["stripe", "mixpanel", "neon"],
        "focus": "What precedes paying. Stripe charges/subscriptions/credit purchases "
                 "(real = amount>0); the action sequence before first payment; intent "
                 "signals upgrade_cta_clicked / credit_topup / page_visited_settings_billing. "
                 "Revenue truth is Stripe, NOT Mixpanel.",
        "angles": [
            "The last action before first payment: what do payers do in the 48h pre-charge?",
            "Credit top-up vs subscription: which entry point retains/expands better?",
            "upgrade_cta_clicked → actual charge: conversion of the intent signal, by source.",
            "Payer vs never-pay lookalikes: matched on activation, what separates the two?",
        ],
    },
    4: {  # Friday
        "key": "retention",
        "name": "Retention & churn cohorts",
        "sources": ["neon", "clickhouse", "stripe"],
        "focus": "Who comes back and who leaves. Week-N activity retention by signup "
                 "cohort; credit-buyer churn deepening; resurrection (dormant→active); "
                 "cohort-by-signup-month curves. (Prior: credit-buyers ~42% churn.)",
        "angles": [
            "Week-over-week retention curve by signup-month cohort — is a recent cohort better/worse?",
            "Resurrection: dormant companies that came back in the last window — what triggered it?",
            "Churn leading indicators: activity-decay pattern in the 2 weeks before a company goes silent.",
            "Single-session-and-gone: share of signups with exactly one active day, by channel/plan.",
        ],
    },
    5: {  # Saturday
        "key": "usage_depth",
        "name": "Agent & workflow usage depth",
        "sources": ["clickhouse", "neon"],
        "focus": "Depth and health of usage among the active. gold.workflow_executions_weekly, "
                 "root_skill_executions / root_tool_executions, error_rate_pct, "
                 "avg/p95 duration; agent_message_sent depth; power-user distribution.",
        "angles": [
            "Power-law of usage: what share of executions come from the top 1%/10% of companies?",
            "Error rate vs retention: do companies hitting high workflow error_rate_pct churn faster?",
            "Skills vs tools mix: does building skills (vs only tools) mark a stickier user?",
            "Depth cliff: distribution of nodes/skills per company — where do most users stall?",
        ],
    },
    6: {  # Sunday
        "key": "wildcard",
        "name": "Cross-source anomaly & wildcard",
        "sources": ["clickhouse", "neon", "stripe", "mixpanel"],
        "focus": "Free exploration. Find the biggest WoW mover across ANY source, or "
                 "join two sources that aren't usually combined (e.g. Mixpanel acquisition "
                 "channel × Stripe payment; Neon assistant cost × ClickHouse executions). "
                 "Chase whatever looks strange.",
        "angles": [
            "Biggest week-over-week mover across all sources — quantify and explain it.",
            "An unusual join: acquisition channel (Mixpanel) × downstream revenue (Stripe).",
            "Assistant build cost (Neon) vs realized workflow executions (ClickHouse): ROI per company.",
            "A metric that contradicts a prior insight in the ledger — actively try to break one.",
        ],
    },
}

# ── Axis 3: segment lenses (rotate on a co-prime cycle) ───────────────────────────
SEGMENTS = [
    "overall (no split — establish the baseline)",
    "by acquisition channel (initial_utm_source / _medium)",
    "by signup-cohort month",
    "by plan (SELF_SERVICE vs the rest)",
    "by geography (Mixpanel region / mp_country_code)",
    "by device/browser (mobile vs desktop — Mixpanel only)",
    "by first-template vs no-template",
    "by activity tier (power / mid / one-and-done)",
]

# ── Axis 4: creativity twists ─────────────────────────────────────────────────────
TWISTS = [
    "Invert it: study the users who DIDN'T do the action and ask why.",
    "Join two sources that don't usually meet, and see if the story holds across both.",
    "Find the outlier company and reverse-engineer what makes it different.",
    "Compare the most recent cohort to an older one — has the behavior shifted?",
    "Follow the time dimension: how long between step A and step B, and does speed predict outcome?",
    "Size the leak: turn a drop-off into an absolute count of lost companies, not just a %.",
    "Segment until the average breaks: keep splitting until one slice behaves very differently.",
    "Stress a prior insight: pick one from the ledger and try to find data that contradicts it.",
]


def _rng(d: date) -> random.Random:
    """Deterministic RNG seeded by the ISO date (reproducible across machines)."""
    seed = int(hashlib.md5(d.isoformat().encode()).hexdigest(), 16)
    return random.Random(seed)


# Monday anchor; business days since this advance the theme cycle by 1 per run.
_RUN_EPOCH = date(2026, 1, 5)


def _run_index(d: date) -> int:
    """Count of business days (Mon-Fri) from the epoch to d — a monotonic run
    counter so themes cycle one-per-run under a weekdays-only schedule."""
    lo, hi, sign = (_RUN_EPOCH, d, 1) if d >= _RUN_EPOCH else (d, _RUN_EPOCH, -1)
    full_weeks, rem = divmod((hi - lo).days, 7)
    count = full_weeks * 5
    wd = lo.weekday()
    for _ in range(rem):
        if wd < 5:
            count += 1
        wd = (wd + 1) % 7
    return sign * count


def _load_questions() -> list[str]:
    if not QUESTIONS_PATH.exists():
        return []
    qs = []
    for line in QUESTIONS_PATH.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("- ") and not s.startswith("- ~~"):  # ~~struck~~ = answered
            qs.append(s[2:].strip())
    return qs


def assignment_for(d: date | None = None, n_questions: int = 3) -> dict:
    d = d or datetime.now().date()
    theme = THEMES[_run_index(d) % len(THEMES)]
    rng = _rng(d)

    iso_week = d.isocalendar()[1]
    angle = theme["angles"][iso_week % len(theme["angles"])]
    # segment on a co-prime step vs week so combos spread out
    segment = SEGMENTS[(d.toordinal() * 3) % len(SEGMENTS)]
    twist = TWISTS[rng.randrange(len(TWISTS))]

    questions = _load_questions()
    rng.shuffle(questions)
    picked_q = questions[:n_questions]

    return {
        "date": d.isoformat(),
        "weekday": d.strftime("%A"),
        "theme_key": theme["key"],
        "theme": theme["name"],
        "sources": theme["sources"],
        "focus": theme["focus"],
        "angle": angle,
        "segment": segment,
        "twist": twist,
        "questions": picked_q,
    }


def render_markdown(a: dict) -> str:
    qlines = "\n".join(f"  - {q}" for q in a["questions"]) or "  - (backlog empty)"
    return f"""# Exploration assignment — {a['date']} ({a['weekday']})

**Theme:** {a['theme']}  ·  **Primary sources:** {', '.join(a['sources'])}

**Focus.** {a['focus']}

**Today's angle (rotates weekly):**
> {a['angle']}

**Segment lens (rotates daily):** {a['segment']}

**Creativity twist:** {a['twist']}

**Pull from the question backlog:**
{qlines}

---
_Deterministic for this date. The ledger enforces novelty on top: don't re-report a
known number unless it moved materially — see insights/INSIGHTS_LOG.md._
"""


if __name__ == "__main__":
    args = [x for x in sys.argv[1:] if not x.startswith("--")]
    if "--week" in sys.argv:
        base = datetime.strptime(args[0], "%Y-%m-%d").date() if args else datetime.now().date()
        monday = base - timedelta(days=base.weekday())
        for i in range(7):
            a = assignment_for(monday + timedelta(days=i))
            print(f"{a['weekday']:9} {a['date']}  {a['theme']}")
            print(f"          angle : {a['angle']}")
            print(f"          segment: {a['segment']}\n")
    else:
        d = datetime.strptime(args[0], "%Y-%m-%d").date() if args else None
        print(render_markdown(assignment_for(d)))

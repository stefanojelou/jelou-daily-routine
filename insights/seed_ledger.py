"""
One-shot: seed the ledger with pre-existing findings so the routine treats them
as KNOWN (won't re-report unless the number moves). Safe to re-run — it skips
topic_keys already present. Run once: python -m insights.seed_ledger
"""
from __future__ import annotations

from insights.ledger import append_insight, known_keys, normalize_key

SEED = [
    dict(
        date="2026-06-24", status="new",
        title="Template payment 'lift' is a fragile marker, not a driver",
        theme="Templates: intent vs. action", angle="does install drive conversion",
        segment="by first-template vs no-template", sources=["neon", "stripe"],
        metric="excluded template pay-rate", value="15.8%",
        one_liner="After excluding internal accounts, template users pay at 15.8% (6/38) vs 1.6% "
                  "non-template (~9.8x), BUT 5 of the original 11 payers were internal and only 6 "
                  "real payers remain — 4 of them paid the same week they touched a template. "
                  "Templates mark serious users; they don't drive conversion.",
        confidence="medium (N=6 real payers; Wilson CI lift as low as 3.8x)",
        caveat="Small N; lifetime not June. Install funnel leaks 61% (28/71 install rate).",
    ),
    dict(
        date="2026-06-24", status="new",
        title="Credit-buyers churn hard with weak repurchase",
        theme="Retention & churn cohorts", angle="credit-buyer churn",
        segment="by activity tier", sources=["stripe", "neon"],
        metric="credit-buyer 30d churn", value="42%",
        one_liner="Of 48 real credit-buyers with a >=30d window, 42% fully churned (no later payment, "
                  "no June activity). Repeat-buy 31% but median time-to-2nd-buy = 0 days (same-day "
                  "top-ups = running out fast). 29% ever bought a paid subscription.",
        confidence="medium",
        caveat="subscriptions table is mostly $0 auto-subs; use paid-invoice signal.",
    ),
    dict(
        date="2026-06-18", status="new",
        title="Real payers are rare — free tier inflates PAID invoices",
        theme="Monetization & pay-drivers", angle="who actually pays",
        segment="overall", sources=["stripe"],
        metric="real payers (amount_paid>0)", value="123",
        one_liner="Counting only amount_paid>0, there are ~123 real payers vs 8,705 invoices marked "
                  "PAID (the free tier books $0 PAID invoices). Always filter amount>0 for revenue.",
        confidence="high",
    ),
    dict(
        date="2026-06-18", status="new",
        title="Free-limit cut ~June 11 changed the payment picture",
        theme="Monetization & pay-drivers", angle="pricing-change effect",
        segment="by signup-cohort month", sources=["stripe"],
        metric="free-limit change date", value="2026-06-11",
        one_liner="The free usage limit was cut ~June 11 2026. subscription_update invoices fire many "
                  "per company — dedup to the first paid subscription before counting conversions.",
        confidence="high",
    ),
    dict(
        date="2026-05-18", status="new",
        title="Structural mismatch: mobile acquisition vs desktop activation",
        theme="Acquisition & signup funnel", angle="mobile vs desktop",
        segment="by device/browser", sources=["mixpanel"],
        metric="acquisition-activation device mismatch", value="qualitative",
        one_liner="Headline structural finding: users are acquired largely on mobile but the builder "
                  "activation happens on desktop. Device/user-agent exists ONLY in Mixpanel, never in "
                  "the internal DBs — quantify with the Jelou Apps project.",
        confidence="medium",
        caveat="Needs Mixpanel device split to size precisely.",
    ),
    dict(
        date="2026-05-18", status="new",
        title="~36% of template users are active in week 2",
        theme="Retention & churn cohorts", angle="week-2 retention",
        segment="by first-template vs no-template", sources=["neon"],
        metric="week-2 activity retention (template users)", value="36%",
        one_liner="Roughly 36% of template-using signups show activity in their second week — the "
                  "baseline retention number this investigation started from.",
        confidence="medium",
    ),
]


def main() -> None:
    have = known_keys()
    added = 0
    for rec in SEED:
        rec.setdefault("topic_key", normalize_key(rec["theme"], rec["metric"], rec["segment"]))
        if rec["topic_key"] in have:
            print(f"skip (already present): {rec['topic_key']}")
            continue
        append_insight(rec)
        added += 1
        print(f"seeded: {rec['title']}")
    print(f"\n{added} seeded; {len(known_keys())} distinct topics now known.")


if __name__ == "__main__":
    main()

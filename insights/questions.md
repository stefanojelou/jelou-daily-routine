# Open question backlog

The daily routine pulls a few of these each run (rotated) and appends new ones as
findings raise fresh questions. Answered questions get struck through (`- ~~...~~`)
so they drop out of rotation but stay as a record.

Format: one question per `- ` bullet. Keep them specific and data-answerable.

## Acquisition
- Which acquisition channel (initial_utm_source) has the best signup→activation→pay full-funnel yield, not just signup volume?
- ~~Is the mobile-vs-desktop activation gap widening or narrowing across recent signup cohorts?~~ (2026-07-06: gap is near-total — mobile ~0.3% build vs desktop ~29-31%.)
- Do signups that arrive with `has_template=true` at onboarding_started convert better than blank-start signups?
- What share of `onboarding_started` never reach `signup_completed`, and where do they die?

## Activation
- What is the median time from signup_completed to first agent_message_sent, and how does it differ for eventual payers?
- Which single activation milestone most strongly predicts week-2 return?
- ~~How large is the dead-on-arrival cohort (signed up, zero activation events), and which channel produces it most?~~ (2026-07-06: ~55% of signups are mobile and only ~0.3% ever build; paid channels are 77% mobile → 5-7% build-activation vs 15% organic.)
- Do the mobile signups ever come back on desktop later (cross-device activation), or are they permanently lost? (split by distinct_id)
- Is there a mobile-appropriate first action (chat/tester) we could make the mobile activation goal instead of the desktop-only canvas?
- What is the CAC-adjusted view: does paid spend on mobile-heavy channels (Meta, Google) ever recover given ~5% build-activation?

## Templates
- Does installing a template shorten time-to-activation, or just correlate with users who'd activate anyway?
- Which specific templates lead to real downstream usage vs sit unused (shelfware)?
- What fraction of template *preview* opens convert to an actual install?

## Monetization
- What is the most common action sequence in the 48h before a company's first real (amount>0) charge?
- Do credit top-up buyers or first-time subscribers retain/expand better over the following month?
- What is the realized conversion from `upgrade_cta_clicked` to an actual paid charge, by source?

## Retention
- Are recent signup-month cohorts retaining better or worse than older ones at week 2 and week 4?
- What activity-decay pattern precedes a company going silent (any early-warning signal)?
- Among resurrected (dormant→active) companies, what event marks the comeback?

## Usage depth
- ~~What share of all workflow executions come from the top 1% / 10% of companies?~~ (2026-07-07: agent_message_sent proxy — top 1% of companies = 28.7%, top 10% = 61.7%, Gini 0.70; 48% of companies sent ≤2 msgs in 90d. Confirm on true ClickHouse executions when wired.)
- Do companies with high workflow error_rate_pct churn faster than clean-running ones?
- Does building SKILL-type nodes (vs only tools) mark a stickier user?
- Are the top-1% "power" companies (30 accounts, ~29% of agent volume) the same ones that pay, and what's the revenue risk if any churns? (needs Stripe)
- Does the Ecuador concentration (50.5% of agent usage) match revenue concentration, or do other markets monetize better per active company? (needs Stripe)
- Within the top-decile companies, how many distinct active users per company — is depth driven by a few power-users or broad team adoption?
- What separates the 65% of builders who add <5 nodes then stop from the 6% who add ≥40 — is there an early node-count threshold that predicts becoming a power account?

## Cross-source / wildcard
- Which company has the highest assistant build cost (Neon) relative to realized executions (ClickHouse)?
- ~~Is there an acquisition channel that is cheap to sign up but never pays (a low-quality source)?~~ (2026-07-09: at the pre-pay/build-activation proxy, Facebook_Mobile_Reels is the clearest low-quality source — 151 signups, 0.7% ever build. Confirm on realized pay once Stripe is wired.)
- Does the Facebook_Desktop_Feed placement (30% build vs organic 16%) scale — is there enough desktop-placement inventory on Meta to shift spend into, or is it a small accidental slice?
- What is the realized pay-through (credit_topup / Stripe) by placement — do cpc/ppc (Google, ~6-7% build) ever recover CAC despite low build rates, or are they as dead as Meta mobile?
- Is the ~90% signup_completed drop since Jul 3 a broken tracking event or a real signup-funnel outage? Cross-check against server-side signups / DB user-created rows once wired.
- If signup_completed is broken, since exactly when, and are onboarding_started / first-session events still firing for brand-new distinct_ids (which would confirm tracking-only, not a real outage)?
- Do new distinct_ids still appear in node_used / agent_message_sent after Jul 3 (i.e. are new users still arriving despite the flat signup event)? (2026-07-09: node_used/agent_message_sent/tester_session_started all recovered to normal volume Jul 6-8 while signups stayed floored — points to a broken signup_completed event, not a real new-user outage. Still needs new-vs-returning distinct_id split to confirm.)
- Since exactly which deploy/commit did signup_completed break (Jul 2→3 boundary)? Bisect against release history once repo/CI access is available.

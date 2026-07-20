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
- ~~What is the median time from signup_completed to first agent_message_sent, and how does it differ for eventual payers?~~ (2026-07-17: median is under 1h — 56% of ALL signups message within 1h, 60% by 1d, 65% by 30d (clean May18–Jun30 cohort, N=3,697). Eventual credit-toppers too small-N (51) to split by speed reliably; revisit with Stripe payers.)
- Agent-message activation (65%) dwarfs build activation (13%) on the same cohort — which one actually predicts week-2/week-4 return and credit_topup? Is messaging a low-bar vanity activation or the real leading indicator?
- Mobile signups converse at ~60% (near desktop 69%) but build at ~2.9%. Do mobile-signup messagers RETAIN (wk2+), or do they message once and vanish — i.e. is mobile conversation real activation or a dead-end without the builder?
- Which single activation milestone most strongly predicts week-2 return?
- ~~How large is the dead-on-arrival cohort (signed up, zero activation events), and which channel produces it most?~~ (2026-07-06: ~55% of signups are mobile and only ~0.3% ever build; paid channels are 77% mobile → 5-7% build-activation vs 15% organic.)
- Do the mobile signups ever come back on desktop later (cross-device activation), or are they permanently lost? (split by distinct_id)
- Is there a mobile-appropriate first action (chat/tester) we could make the mobile activation goal instead of the desktop-only canvas?
- What is the CAC-adjusted view: does paid spend on mobile-heavy channels (Meta, Google) ever recover given ~5% build-activation?
- Given 86% of build-activators fire within 24h of signup, does the ~14% "slow" cohort (day 1-14) retain/pay any differently than the same-session builders — i.e. is a delayed first build a worse or equal signal?
- Does the same first-hour front-loading hold for the OTHER milestones (skill_created, tester_session_started, agent_message_sent), or is node_used uniquely same-session — and which milestone has the longest tail worth a re-engagement nudge?

## Templates
- Does installing a template shorten time-to-activation, or just correlate with users who'd activate anyway?
- Which specific templates lead to real downstream usage vs sit unused (shelfware)?
- ~~What fraction of template *preview* opens convert to an actual install?~~ (2026-07-13: 18% overall — 27 of 147 unique previewers install any template within 30d; per-template 0–36%.)
- Why do "Appointment scheduling" (0/13) and "Schedule with Microsoft Outlook Calendar" (0/6) convert 0% preview→install while "Schedule with Google Calendar" converts 12% — broken install path, missing integration, or genuinely unwanted?
- Most installs come from ~40 custom/Spanish templates NOT in the previewable gallery (Agente Shopify 39, Tienda Jelou Shop 14) — how are those discovered/installed if not via the preview gallery, and should the top custom ones be promoted into the gallery?
- Of the 27 gallery-preview installers, how many go on to build (node_used) vs the ~40 off-gallery installers — does gallery provenance predict activation?

## Monetization
- What is the most common action sequence in the 48h before a company's first real (amount>0) charge?
- ~~Do credit top-up buyers or first-time subscribers retain/expand better over the following month?~~ (2026-07-14: not answerable in Mixpanel yet — subscription_changed only started firing ~Jun 24 2026, so all 14 subscribers have <3wk immature windows. Credit-toppers alone: agent-activity retention decays 46%→14%→6% over wk0-2. Revisit once subscription cohorts mature / Stripe is wired.)
- What is the realized conversion from `upgrade_cta_clicked` to an actual paid charge, by source?
- Now that subscription_changed is live (~Jun 24 2026), re-run credit-topup vs subscription retention once the subscriber cohort has a mature ≥4-week window (≈late Jul).
- Do the ~79%-organic credit-toppers differ from the ~21% media ones in top-up amount, repeat-topup rate, or agent-activity retention — i.e. does channel predict credit-buyer quality?
- Are credit-toppers and subscribers genuinely disjoint populations, or a funnel? (lifetime funnel showed 3% topup→sub and 14% sub→topup, but both are confounded by subscription_changed's Jun-24 start — re-test on the co-existing window.)
- What do credits actually get spent on (agent_message_sent vs campaign_sent vs other) — validate agent_message_sent as the right post-topup retention proxy.

## Retention
- Are recent signup-month cohorts retaining better or worse than older ones at week 2 and week 4?
- What activity-decay pattern precedes a company going silent (any early-warning signal)?
- Among resurrected (dormant→active) companies, what event marks the comeback?
- Peru is the #4 agent-volume market yet returns at ~3% wk1 (vs Ecuador 38%). Is that near-zero retention driven by one/few churned accounts, or broad across Peruvian companies? (needs company_id dedup — no JQL groupByUser in Mixpanel MCP; revisit when DB/Stripe wired.)
- Why does Ecuador retain agent usage ~2.3x better than Colombia/Mexico (38% vs 16-17% wk1)? Product-language/localization, sales-touch, account size, or self-serve-vs-managed mix by market?
- Does the geographic retention gap (EC ≫ CO/MX ≫ PE) hold on node_used (builder) cohorts too, or is it specific to agent messaging?
- Does per-market agent-usage retention track per-market revenue (credit_topup / Stripe) — i.e. is Ecuador's stickiness monetized, and is Peru's volume worthless? (needs Stripe)

## Usage depth
- ~~What share of all workflow executions come from the top 1% / 10% of companies?~~ (2026-07-07: agent_message_sent proxy — top 1% of companies = 28.7%, top 10% = 61.7%, Gini 0.70; 48% of companies sent ≤2 msgs in 90d. Confirm on true ClickHouse executions when wired.)
- Do companies with high workflow error_rate_pct churn faster than clean-running ones?
- ~~Does building SKILL-type nodes (vs only tools) mark a stickier user?~~ (2026-07-16: reframed to the skill lifecycle — skills are created prolifically but rarely deployed. 761 users / 542 companies created 2,894 skills in 90d, but only ~1 in 4 companies (28%; 12% on a strict 30d ordered funnel) ever adds a skill to the canvas; 57% of creators are one-and-done. Not a device artifact — creation is 92% desktop. Open: do the ~25% who DEPLOY retain/monetize better than create-only users?)
- Do skill-DEPLOYERS (skill_used) retain and monetize better than create-only users? Needs $user-profile company_id join to agent_message_sent / credit_topup (agent_message_sent has no event-level company_id).
- Why is the create→canvas step leaking 72–88%? Are skills being created AI-assisted in bulk (2,894 skills / 761 users) as throwaway experiments, or is the canvas-drop UX the blocker? Cross-check with node_config / tester events.
- Does a created-but-never-deployed skill predict churn faster than never-creating a skill at all (i.e. is abandoned exploration a worse signal than no exploration)?
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
- ~~If signup_completed is broken, since exactly when, and are onboarding_started / first-session events still firing for brand-new distinct_ids (which would confirm tracking-only, not a real outage)?~~ (2026-07-20: onboarding_started is NOT still firing normally — it ALSO collapsed on Jul 3, prod last-7d -67% (420 vs 1,264), so the break is the whole new-user onboarding funnel, not just the signup_completed event. Weakens the pure-tracking read; could be a real top-of-funnel/acquisition outage OR a shared onboarding-flow instrumentation regression. Still needs a new-vs-returning distinct_id split + server-side counts to fully close.)
- Now 17 days sustained (Jul 3→20) with no recovery — has anyone confirmed whether real new users are still arriving? Split node_used/agent_message_sent by NEW vs returning distinct_id post-Jul-3 to settle real-outage vs tracking once and for all.
- The onboarding_started→signup_completed same-day ratio itself halved (43%→19%) on top of the -67% onboarding drop — is the extra completion loss a second, distinct regression on signup_completed specifically, or a real drop in people finishing signup?
- The untagged 'undefined' home_variant fell hardest (-91% vs home_a/home_b ~-70%) — does that localize the break to a specific entry path (app-direct / a particular referral / a landing page that doesn't set home_variant)?
- Do new distinct_ids still appear in node_used / agent_message_sent after Jul 3 (i.e. are new users still arriving despite the flat signup event)? (2026-07-09: node_used/agent_message_sent/tester_session_started all recovered to normal volume Jul 6-8 while signups stayed floored — points to a broken signup_completed event, not a real new-user outage. Still needs new-vs-returning distinct_id split to confirm.)
- Since exactly which deploy/commit did signup_completed break (Jul 2→3 boundary)? Bisect against release history once repo/CI access is available.
- Weekly agent_message_sent UNIQUE users slid 488 (wk Jun 22) → 391 (Jun 29) → 215 (Jul 6) even though node_used total stayed healthy (~1.5-1.7k/wk). Is agent-MAU genuinely shrinking, or is it a knock-on of the signup_completed collapse (fewer new users → fewer first agent messages), or a second tracking regression? Split new-vs-returning distinct_ids to disentangle.
- agent_message_sent was only instrumented ~May 18 2026 (0 unique users before). What was the pre-May-18 agent-usage event (if any), and can earlier agent history be recovered for longer retention cohorts?

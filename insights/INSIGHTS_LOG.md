# Insights log

Newest first. Written by the daily routine; each entry is a NEW finding or a
material UPDATE to a prior one. Seeded with pre-existing findings so they are not
re-reported.

---

### 2026-07-10 — 🆕 NEW — Time-to-first-value is a first-hour event — 66% of activators build within 1h of signup

Build-activation is a first-HOUR event, not a first-week one. Of the 1,103 signups (of 8,126, prod, Feb 1-Jul 10) who ever add a node within 14d, 38% do it within 10 min of signup, 66% within 1 hour, and 86% within 24 hours; only ~8% arrive after day 3. Median time-to-first-value is under ~30 min while the mean (17.9h) is dragged up by a thin tail — the mean is misleading. The window to convert a signup into a builder is essentially the same session: if they don't build on day 1 (86% cutoff), they almost never do. This is a desktop story — mobile signups activate at ~0 by construction (node_used is a desktop drag-drop), so the timing curve describes the desktop cohort. Actionable: onboarding nudges must fire in-session/first-hour; day-2+ email drips miss the window.

- **Metric:** first-hour share of build-activators (signup->node_used) = **66**
- **Theme/angle:** Activation & time-to-milestone — Time-to-first-value: distribution of hours from signup to first node_used
- **Segment:** by device (desktop-driven; mobile ~0 by construction)  ·  **Sources:** mixpanel
- **Confidence:** high (N=8,126 signups; 1,103 activators within 14d; cumulative-window CDF at 10m/1h/1d/3d/7d/14d)
- **Caveat:** Cohort on all prod signups Feb 1-Jul 10; node_used is the desktop builder proxy so mobile is ~0 by construction and the curve is desktop-driven. Recent signups (<14d) have partial windows (minor understatement of late arrivals). Median inferred by interpolation between the 10-min (38%) and 1-h (66%) buckets; Mixpanel ttc returns only the mean. Signup_completed collapse (Jul 3-9) affects only the newest ~1% of the window, not the distribution shape.

---

### 2026-07-09 — 🆕 NEW — Acquisition placement decides quality: FB Mobile Reels builds at 0.7%, FB Desktop Feed at 30%

Channel quality by placement (initial_utm_medium), signup->build (node_used, 14d, cohort on signup, outcome any-device), prod 120d. Organic/direct = 16% (978/6,184), the healthy baseline. Google paid is ~half: cpc 7% (54/732), ppc 6% (23/367). Meta is NOT uniformly bad — it splits by the device the placement targets: Facebook_Mobile_Reels 0.7% (1/151) and Facebook_Mobile_Feed 3% (2/79) are dead-on-arrival, while Facebook_Desktop_Feed 30% (9/30) beats organic. Same advertiser, opposite outcomes — the placement is a device proxy, and mobile placements feed a desktop-only builder.

- **Metric:** Facebook_Mobile_Reels 14d build-activation = **0.7%**
- **Theme/angle:** Acquisition & signup funnel — Channel quality by placement (utm_medium) — which acquisition placement's signups actually build
- **Segment:** by acquisition medium/placement (initial_utm_medium)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (organic N=6,184, cpc N=732, ppc N=367 solid; Meta placements small-N: Reels 151, Mobile Feed 79, Desktop Feed 30 — directional)
- **Caveat:** utm_medium present on only ~21% of signups (undefined=organic/direct). Activation proxied by node_used (desktop drag-drop). Meta-placement rates are small-N; the mobile-vs-desktop contrast within Meta is the robust signal, not any single placement's exact %. Pay-through needs Stripe (deferred).

---

### 2026-07-09 — 🔁 UPDATE — Signup collapse persists 6 days — now confirmed signup-specific (others recovered)

The ~90% signup_completed collapse flagged Jul 8 has NOT recovered: Jul 3-9 daily signups ran 17,3,4,3,10,13,0 vs a June baseline of ~68-103/day. Last-7d (Jul 3-9) = 50 signups vs prior-7d 542 = -91% WoW (worse than the -67% reported yesterday). Crucially, node_used, agent_message_sent and tester_session_started all dipped only for the Jul 4-5 weekend and fully recovered to normal volume Jul 6-8 (node 264/306/292, agent 315/376/219, tester 239/312/272) — signups alone stayed floored. That isolates the break to signup_completed specifically and leans toward a broken signup event / tracking regression over a genuine new-user outage (downstream activity continues). 6-day sustained; all signup-based cohort metrics remain unreliable until resolved.

- **Metric:** signup_completed last-7d WoW = **-91%**  (was -67% (Jul 4-7 avg 5/day))
- **Theme/angle:** Cross-source anomaly & wildcard — Biggest week-over-week mover — signup event health
- **Segment:** overall  ·  **Sources:** mixpanel
- **Confidence:** high (production daily; cross-checked vs 3 other core events, all recovered)
- **Caveat:** Jul 9 is a partial day (0 so far). Mixpanel alone still can't fully separate a broken signup_completed event from a real signup outage, but the clean recovery of node_used/agent/tester while signups stayed dead strongly favors a tracking regression. Needs server-side signup counts / DB user-created rows to close out.

---

### 2026-07-08 — 🆕 NEW — Signups flatlined ~90% since Jul 3 — anomaly isolated to signup_completed

Production signup_completed collapsed from a stable ~61/day June baseline to 3,4,3,10/day on Jul 4-7 (~92% below trend; last 7d 188 vs prior 7d 571 = -67% WoW). Isolated to signups: node_used, agent_message_sent, campaign_sent and tester_session_started only dipped for the Jul 4-5 weekend and fully recovered Jul 6-7. Not env-tag drift (all-env $overall collapsed identically) and not a shift to the marketing project (3842156 has zero signup_completed). Most likely a broken signup_completed instrumentation/event or a genuine new-signup outage.

- **Metric:** signup_completed daily volume, Jul 4-7 avg = 5/day (vs June ~61/day; -67% last-7d WoW) = **5.0**
- **Theme/angle:** Cross-source anomaly & wildcard — Biggest week-over-week mover across all sources
- **Segment:** overall (activity-tier lens N/A — new signups have no tier yet)  ·  **Sources:** mixpanel
- **Confidence:** high (production, daily; cross-checked vs other events, environments, and second project)
- **Caveat:** Cannot yet distinguish a broken signup_completed event (tracking regression) from a real signup-funnel outage from Mixpanel alone; server logs / funnel checks needed. Current partial-window days under-report slightly but cannot explain a 5-day flatline given other events recovered. While unresolved, all signup-based cohort metrics in this project are unreliable.

---

### 2026-07-07 — 🆕 NEW — Agent usage is a home-market story — Ecuador is half of all activity

By geography, agent_message_sent (prod, 90d) is dominated by Jelou's home market: Ecuador alone = 12,548 events (50.5%), then Colombia 2,879 (11.6%), Mexico 2,451 (9.9%), Peru 1,873 (7.5%), Brazil 1,411 (5.7%). The top 3 countries are ~72% and the top 5 ~85%. The US is only 469 (1.9%). Usage concentration is geographic as well as per-company — expansion beyond the Andean core is still thin.

- **Metric:** Ecuador share of agent messages = **50.5% (top3 ~72%)**
- **Theme/angle:** Agent & workflow usage depth — Power-law of usage — geographic concentration
- **Segment:** by geography (mp_country_code)  ·  **Sources:** mixpanel
- **Confidence:** high (N=24,853 events, production, 90d, event mp_country_code)
- **Caveat:** mp_country_code is Mixpanel geo-IP at event time, not billing country; VPNs/travel add minor noise. Reflects where activity happens, not necessarily company HQ.

---

### 2026-07-07 — 🆕 NEW — Agent usage follows a steep power-law — top 10% of companies drive 62%

Over the last 90d, 24,853 agent_message_sent events (prod) span 2,987 companies but are heavily concentrated: the top 1% of companies (30) generate 28.7%, the top 5% (150) 50.6%, and the top 10% (299) 61.7% of all messages (Gini 0.70). The tail is shallow — 48% of companies sent <=2 messages in 90 days and 31% sent exactly one. Builds echo it: of 1,789 companies that added a node, 65% added <5 nodes total and only 6% added >=40. Depth lives in a thin slice of accounts.

- **Metric:** top-10pct company share of agent messages = **61.7% (top1%=28.7%, top5%=50.6%, Gini 0.70)**
- **Theme/angle:** Agent & workflow usage depth — Power-law of usage: what share of executions come from the top 1%/10% of companies
- **Segment:** by company  ·  **Sources:** mixpanel
- **Confidence:** high (N=24,853 events / 2,987 companies, production, 90d; company_id user-property breakdown, checksum within 0.3%)
- **Caveat:** company_id from the $user profile; 449 events (1.8%) had no company_id (undefined) and are excluded from concentration. Internal/test accounts not separately excludable by id — a few low-id companies may be internal, which would slightly inflate the top slice. agent_message_sent is the agent-usage proxy; true workflow-execution internals (durations, error_rate) need ClickHouse (deferred).

---

### 2026-07-06 — 🔁 UPDATE — Correction: mobile-signup build-activation is 2.9% (not 0.3%) vs desktop 27%

Run #1 measured node_used with $os=mobile, but node_used is a desktop-only drag action (31,722 desktop vs 128 mobile events), so that ~0.3% was near-tautological. Cohorting on SIGNUP device and counting node_used within 14d on ANY device: mobile signups activate at 2.9% (132/4,536) vs desktop 26.9% (953/3,548). The ~9x structural gap and the paid-is-77%-mobile story hold; the magnitude was overstated ~10x.

- **Metric:** mobile 14d build-activation (node_used) = **2.9%**  (was 0.3%)
- **Theme/angle:** Retention & churn cohorts — Dead-on-arrival cohort by device — who never activates
- **Segment:** by device ($os)  ·  **Sources:** mixpanel
- **Confidence:** high (N=4,536 mobile signups; cohort-by-signup-device, any-device node_used, 14d)
- **Caveat:** Recent signups (<14d) have a partial window (minor understatement). Paid ~6% is likely similarly understated (~8% cohort-corrected) but still ~half of organic.

---

### 2026-07-06 — 🆕 NEW — Paid acquisition is 77% mobile → activates at ~5-7% vs 15% organic

Signups with a utm_source (paid, 1,695/8,084 = 21%) are 77% mobile (1,302), vs ~50% mobile for organic. Because mobile can't build, paid channels convert to real building (node_used, 14d) at roughly half the organic rate: Google Ads 7% (52/725), Google 'adwords' 6% (22/370), Meta fb 4% (12/283) / ig 6% (10/172) — vs 15% organic (974/6,389). Paid spend is largely buying dead-on-arrival mobile signups.

- **Metric:** paid-channel 14d build-activation = **~6%**
- **Theme/angle:** Retention & churn cohorts — Activation by acquisition channel (paid vs organic)
- **Segment:** by acquisition channel (utm_source)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (Google N=1,106, Meta N=455; organic baseline N=6,389)
- **Caveat:** utm_source only on ~21% of signups; 'undefined' treated as organic/direct. X/x-ads excluded from headline (N<120, noisy at 15-24%). Activation proxied by node_used; mechanism (paid→mobile→can't build) confirmed by device split.

---

### 2026-07-06 — 🆕 NEW — Mobile signups are dead-on-arrival — 0.3% ever build vs 29% on desktop

55% of production signups (4,417/8,084 over 5 mo) arrive on mobile (Android+iOS), but virtually none activate the builder: only 13 mobile users ever added a node to the canvas within 14d (0.3%), vs ~29% on desktop (Windows 29%, Mac 31%). Mobile doesn't activate via testing either (~1.5%). This quantifies the previously-qualitative mobile/desktop mismatch: the builder canvas is desktop-only, so a majority of signups structurally cannot activate on the device they signed up on.

- **Metric:** mobile 14d build-activation (node_used) = **0.3%**
- **Theme/angle:** Retention & churn cohorts — Dead-on-arrival cohort by device — who never activates
- **Segment:** by device ($os)  ·  **Sources:** mixpanel
- **Confidence:** high (N=4,417 mobile signups; production only; 14d window)
- **Caveat:** node_used = 'Node Added to Canvas' is a desktop drag-drop UI, so this measures builder activation specifically; mobile app-session rate is ~96% (they open, they just can't build). Cross-device users (sign up mobile, build later on desktop) would be split by distinct_id and could modestly understate mobile.

---

### 2026-07-01 — 🆕 NEW — Template installs aren't shelfware — but 21% of installers vanish

Templates are installed mid-session (median ~1.4h to next builder session; 84% of installs are followed by more building within 7d) — they are NOT abandoned on a shelf. The real leak is a tail: 21% of template-installing companies (12/57, >=7d window) never open the builder again after their first install — a concrete re-engagement target.

- **Metric:** template-install abandonment (never return after 1st install) = **21%**
- **Theme/angle:** Templates: intent vs. action — Time-from-install-to-first-use: do installs sit unused (shelfware)?
- **Segment:** by signup-cohort month  ·  **Sources:** neon, clickhouse
- **Confidence:** medium (N=57 companies with >=7d window; test cos excluded)
- **Caveat:** 'Use' proxied by any chat_session after install; near-zero median time-to-next-session means installs happen inside active build sessions, so this measures engagement continuation, not template execution specifically.

---

### 2026-05-18 — 🆕 NEW — ~36% of template users are active in week 2

Roughly 36% of template-using signups show activity in their second week — the baseline retention number this investigation started from.

- **Metric:** week-2 activity retention (template users) = **36%**
- **Theme/angle:** Retention & churn cohorts — week-2 retention
- **Segment:** by first-template vs no-template  ·  **Sources:** neon
- **Confidence:** medium

---

### 2026-05-18 — 🆕 NEW — Structural mismatch: mobile acquisition vs desktop activation

Headline structural finding: users are acquired largely on mobile but the builder activation happens on desktop. Device/user-agent exists ONLY in Mixpanel, never in the internal DBs — quantify with the Jelou Apps project.

- **Metric:** acquisition-activation device mismatch = **qualitative**
- **Theme/angle:** Acquisition & signup funnel — mobile vs desktop
- **Segment:** by device/browser  ·  **Sources:** mixpanel
- **Confidence:** medium
- **Caveat:** Needs Mixpanel device split to size precisely.

---

### 2026-06-18 — 🆕 NEW — Free-limit cut ~June 11 changed the payment picture

The free usage limit was cut ~June 11 2026. subscription_update invoices fire many per company — dedup to the first paid subscription before counting conversions.

- **Metric:** free-limit change date = **2026-06-11**
- **Theme/angle:** Monetization & pay-drivers — pricing-change effect
- **Segment:** by signup-cohort month  ·  **Sources:** stripe
- **Confidence:** high

---

### 2026-06-18 — 🆕 NEW — Real payers are rare — free tier inflates PAID invoices

Counting only amount_paid>0, there are ~123 real payers vs 8,705 invoices marked PAID (the free tier books $0 PAID invoices). Always filter amount>0 for revenue.

- **Metric:** real payers (amount_paid>0) = **123**
- **Theme/angle:** Monetization & pay-drivers — who actually pays
- **Segment:** overall  ·  **Sources:** stripe
- **Confidence:** high

---

### 2026-06-24 — 🆕 NEW — Credit-buyers churn hard with weak repurchase

Of 48 real credit-buyers with a >=30d window, 42% fully churned (no later payment, no June activity). Repeat-buy 31% but median time-to-2nd-buy = 0 days (same-day top-ups = running out fast). 29% ever bought a paid subscription.

- **Metric:** credit-buyer 30d churn = **42%**
- **Theme/angle:** Retention & churn cohorts — credit-buyer churn
- **Segment:** by activity tier  ·  **Sources:** stripe, neon
- **Confidence:** medium
- **Caveat:** subscriptions table is mostly $0 auto-subs; use paid-invoice signal.

---

### 2026-06-24 — 🆕 NEW — Template payment 'lift' is a fragile marker, not a driver

After excluding internal accounts, template users pay at 15.8% (6/38) vs 1.6% non-template (~9.8x), BUT 5 of the original 11 payers were internal and only 6 real payers remain — 4 of them paid the same week they touched a template. Templates mark serious users; they don't drive conversion.

- **Metric:** excluded template pay-rate = **15.8%**
- **Theme/angle:** Templates: intent vs. action — does install drive conversion
- **Segment:** by first-template vs no-template  ·  **Sources:** neon, stripe
- **Confidence:** medium (N=6 real payers; Wilson CI lift as low as 3.8x)
- **Caveat:** Small N; lifetime not June. Install funnel leaks 61% (28/71 install rate).

---


# Insights log

Newest first. Written by the daily routine; each entry is a NEW finding or a
material UPDATE to a prior one. Seeded with pre-existing findings so they are not
re-reported.

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


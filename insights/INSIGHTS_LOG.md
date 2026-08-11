# Insights log

Newest first. Written by the daily routine; each entry is a NEW finding or a
material UPDATE to a prior one. Seeded with pre-existing findings so they are not
re-reported.

---

### 2026-08-11 — 🆕 NEW — Template choice predicts activation -- flagship English/commerce templates activate 54-83%, the Spanish biometrics duplicate is a dead end (25% tester / 11% node) vs its English twin (58% / 55%)

Directly answering the assigned angle -- which specific templates activate vs which are dead ends -- the template a user installs materially predicts whether they then EXERCISE the build: install->tester_session_started (30d, prod, 180d) ranges from 25% to 83% across templates, well outside noise for the high-volume cells, against a 47% overall baseline (56/118 installers; install->node is the same 47%, 55/118). The workhorses -- the flagship English/commerce templates that also carry the install VOLUME -- all activate at or above baseline on BOTH signals: Shopify store with native checkout 57% tester / 57% node (N=21), Jelou Shop store with in-chat payment 59% / 33% (N=17), Identity Verification or Biometrics 58% / 55% (N=12), Agente Shopify 54% / 50% (N=13). The DEAD END is the Spanish-localized biometrics duplicate 'Validacion de identidad con Biometria' (N=8): 25% tester / 11% node -- ~half the baseline and ~2x below its English twin 'Identity Verification or Biometrics' (58% / 55%) despite being essentially the same template concept. The same locale split repeats on scheduling: English 'Schedule with Google Calendar' activates 83% tester / 60% node (N=6) while Spanish 'Asistente de Agendamiento' manages 40% / 17% (N=5). Time twist: two templates activate SAME-SESSION -- Google Calendar (~2.2h to first tester) and Jelou Shop in-chat payment (~2.4h) -- vs ~3-6 days for the Shopify/Identity workhorses; speed-to-first-tester marks the stickiest templates. So the honest read: the flagship English/canonical gallery templates activate solidly (~55-83%), while several Spanish-localized near-duplicates and one-off payment demos under-activate (<=33%). Marks not drives -- the template name marks WHO installs it (English flagships -> more sophisticated/international builders; Spanish duplicates -> LatAm casual cohort, consistent with the ledger's geography retention gap), not that the template itself causes activation. Per-template N is small (6-21) so cell rates are directional; the workhorse cells (N=12-21) and the 25-83% spread are the robust reads.

- **Metric:** Spanish biometrics template install->tester 30d activation (vs EN twin 58, baseline 47) = **25**
- **Theme/angle:** Templates: intent vs. action — Which specific templates correlate with activation, and which are dead ends -- per-template install->tester/node (30d) + English-vs-Spanish-variant contrast + time-to-first-tester twist
- **Segment:** by template (per-template install->activation)  ·  **Sources:** mixpanel
- **Confidence:** medium
- **Caveat:** Mixpanel funnels template_installed -> tester_session_started (and -> node_used), prod (environment=='production'), countType=unique, 30-day conversion window, last 180d (template_installed carries only ~180d history). Overall base 118 installers, 47% -> tester (56), 47% -> node (55) -- matches the Jul-31 overall 43% tester / 44% node. Per-template install->tester (N>=5): Schedule with Google Calendar 83% (5/6), Agente de preguntas frecuentes 83% (5/6), Jelou Shop store w/ in-chat payment 59% (10/17), Identity Verification or Biometrics 58% (7/12), Shopify store native checkout 57% (12/21), Agente Shopify 54% (7/13), Asistente de Agendamiento 40% (2/5), Tienda Jelou Shop con pago en chat 33% (2/6), 'Validacion de Identidad con Biometria' (uppercase variant) 33% (2/6), 'Validacion de identidad con Biometria' (lowercase variant) 25% (2/8). install->node for the same: Shopify native 57% (12/21), Agente de preguntas frecuentes 83% (5/6), Tienda Jelou Shop 71% (5/7), Identity Verification EN 55% (6/11), Agente Shopify 50% (7/14), Jelou Shop in-chat 33% (5/15), Schedule w/ Google Calendar 60% (3/5), Asistente de Agendamiento 17% (1/6), 'Validacion de identidad con Biometria' lowercase 11% (1/9). Two Spanish biometrics name-variants (casing) exist; combined ~29% tester (4/14) -- the lowercase variant (N=8-9) is the clean dead end on BOTH signals (25%/11%), the uppercase (N=6) is noisier (33%/50%). Unit is distinct_id, NOT company_id-deduped. Per-template N=6-21 so rates are directional; the 47% baseline (N=118), the 25-83% spread, and the four workhorse cells (N=12-21, all 54-59%) are the robust reads; N=1 one-offs (payment 'Demo *' templates, TEST/final-test/testing internal templates, customer-named agents) excluded from the narrative as internal/noise. avg-time-to-tester is over converters only and tail-dragged. ASSIGNED SEGMENT LENS was device/browser (mobile vs desktop): NOT applied because template_installed->tester_session_started/node_used is a desktop-only builder surface (node_used is the desktop-only drag-drop; mobile activation ~0 by construction per the playbook funnel rule), so a mobile-vs-desktop activation split would be a tautology, not behavior. Deferred: reconciled pay-through by template (Stripe) and server-side template_instantiations/deploy (Neon/ClickHouse) -- so this is intent-to-exercise (tested/built more), not revenue. Extends Jul-13 (per-template PREVIEW->install) and Jul-31 (overall install->use + geography) with the never-before-measured per-template install->ACTIVATION cut. Marks not drives; reverse causation (committed builders self-select the flagship English templates) is at least as likely as the template driving activation.

---

### 2026-08-10 — 🆕 NEW — Building and testing predict a 2nd-week return far better than conversing -- node-first 74% / tester-first 66% return next week vs agent-first 46%

Directly answering the assigned angle -- which first milestone (node build, tester session, or agent chat) best predicts a 2nd-week return -- the ranking is clean and wide, and it is BUILDING or TESTING, not conversing. On weekly Mixpanel retention curves (prod) that cohort users on each milestone event and measure whether they RETURN the following week to a common, neutral signal (app_session_started = came back to the app at all), matched to the identical Jun 17-Jul 20 2026 window (the span where all three events co-exist), node_used-first users return at 74.5% (1,225/1,644 births), tester_session_started-first at 66.0% (748/1,133), and agent_message_sent-first at only 45.7% (951/2,080) -- a ~29pt gap between the best predictor (build) and the weakest (conversation), with test in between. The SAME ranking holds when the return signal is instead the canonical usage event agent_message_sent (node-first 32% / tester-first 27% / agent-first 24%, over the fuller May 25-Jul 20 window), so the ordering is not an artifact of the return-event choice. The counter-intuitive part: agent_message_sent is the WIDEST activation net (65% of all signups ever fire it, per the Jul-17 ledger) yet its users are the LEAST likely to come back -- a first agent message marks a shallow, one-and-done-prone population (many mobile/casual), while the deeper build and test milestones mark committed users. Robustness: tester_session_started was only instrumented ~Jun 17 2026 so its cohort births are near-true-first (no event-age confound) and it STILL beats agent-first by ~20pt -- so the build/test-beats-conversation conclusion does NOT rest on node_used's long pre-window history (the confound flagged in the Jul-21 entry). This extends Jul-21 (builder 43% vs agent 24% SELF-retention) by adding tester as a third milestone and running a fair head-to-head with a COMMON return event. Actionable read: the highest-value activation to drive first is a build or a tester session, not merely a first chat -- and the wide-net agent-first cohort is where the week-1 leak concentrates. Marks not drives -- reverse causation (already-committed users build/test more) is at least as likely as the milestone itself causing the return.

- **Metric:** node-first wk1 app-session return (matched window; vs tester 66 / agent 46) = **74**
- **Theme/angle:** Activation & time-to-milestone — Which first milestone (node/tester/agent-chat) best predicts a 2nd-week return -- head-to-head with a common return event
- **Segment:** by first-milestone type (node vs tester vs agent)  ·  **Sources:** mixpanel
- **Confidence:** medium-high
- **Caveat:** Mixpanel weekly retention CURVES, prod (environment=='production'), chartType=curve. Cohort ('first') = a user's first occurrence of the milestone event within the window; 'return' = firing the return event in the FOLLOWING calendar week (week-1 column). PRIMARY (neutral) return event = app_session_started, matched window Jun 17-Jul 20 2026 (the fair common window because tester_session_started was only instrumented ~Jun 17 2026 -- zero first-time users before that); week-1 rates aggregated across daily cohorts = sum(week1 counts)/sum(first): node 1,225/1,644=74.5%, tester 748/1,133=66.0%, agent 951/2,080=45.7% (all daily cohorts through Jul 20 have a fully-elapsed week-1 window as of Aug 10, so week-1 is mature). SECONDARY (self/usage) return event = agent_message_sent over May 25-Jul 20: node-first 32.4% (19.57/60.36 avg), tester-first 27.1% (11.62/42.85), agent-first 24.1% (21.55/89.44) -- note agent-first here is SELF-retention (return event == birth event) which if anything flatters the agent cohort, yet it is still last. Unit is distinct_id, NOT company_id-deduped. Event-age caveat: node_used and agent_message_sent have pre-window history (agent instrumented ~May 18, node older), so node-first/agent-first births are 'first in-window', not necessarily first-ever -- but tester (clean, launched ~Jun 17) reproduces the build/test>>conversation ordering, so the headline does not depend on it. app_session_started is a broad 'came back to the app' signal that could include some low-intent/background opens, but it is applied identically to all three cohorts so the RANKING is fair; the exact levels are re-engagement, not necessarily deep usage. Assigned segment lens was 'by signup-cohort month'; a true signup-month cohort is unmeasurable (signup_completed collapsed since Jul 3), so cohorts are on the milestone event itself (the standard ledger workaround) and the ranking is visibly stable across June and July daily cohorts. Marks not drives; reverse causation likely. Deeper 'did the returning user do something valuable' and reconciled pay-through remain deferred (Neon/ClickHouse/Stripe).

---

### 2026-08-07 — 🆕 NEW — Organic completes onboarding->signup at 50%, ~1.3-2x every paid channel (Google ~40, FB 34, X ~26, Instagram 24) -- and the profile-utm cut saying the OPPOSITE (media ~94%) is a back-stamping artifact

Today's assigned angle -- which channel converts land->signup best/worst -- has a clean, ledger-consistent answer at the onboarding->signup COMPLETION step (a funnel step never isolated by channel before; prior channel findings all measured signup->ACTIVATION), but ONLY once you avoid a back-stamping trap. On onboarding_started->signup_completed (prod, June 2026 clean pre-collapse window, unique, 1-day conversion) broken down by the EVENT-level utm_source captured on the onboarding_started event itself: organic/direct (no utm) completes at 50% (970/1,951), Google search paid ~40% (cpc/ppc combined 588/1,487; Google Ads 38%, adwords 41%), Facebook 34% (51/149), X/Twitter ~26% (30/115), and Instagram the WORST sizeable channel at 24% (22/90) -- so every paid channel completes signup at 0.5-0.8x the organic rate, and paid social (esp. Instagram) at roughly HALF. The utm_medium cut agrees (paid_social 26% 30/114; Instagram_Reels 23%, Instagram_Feed 23%, Facebook_Mobile_Feed 20%; vs cpc 38% / ppc 41%). THE TRAP: breaking the SAME funnel down by the initial_utm_source USER-PROFILE property gives the exact OPPOSITE ranking -- organic 32% vs media 93-96% (adwords 94%, Google Ads 96%, fb 93%, ig 93%) -- which is a selection artifact: initial_utm_source is persisted to the $user profile mainly at/after identify/signup, so only ~751 users carry it at profile level vs ~1,862 onboarding_started events carrying an event-level utm; the profile property is preferentially present on COMPLETERS, inflating media completion to near-100%. The event-level cut (captured at entry) is the unbiased one, and its direction is a floor: any organic->media contamination in the 'undefined' event bucket would only drag organic's 50% DOWN. Twist (time): signup completes within minutes of onboarding across all channels (same-session), and organic converts both fastest (~111s mean-to-complete) and highest, so speed and completion both favor organic. Net: media/paid is worse at BOTH ends of the funnel -- it finishes signup at ~half organic's rate AND (once signed up) builds less (Jul-6/9) -- the one place it beats organic is widest-net messaging (Jul-30). Marks not drives; a plausible contributor is media's ~77% mobile skew (Jul-6), but signup_completed is NOT device-constrained, so this is a real completion gap, not a desktop-only tautology like the build metric.

- **Metric:** organic onboarding->signup 1d completion (event-utm; vs Google ~40 / paid-social ~26) = **50**
- **Theme/angle:** Acquisition & signup funnel — Channel quality: onboarding->signup COMPLETION by acquisition channel (event-level utm) -- best/worst channel at finishing signup + a profile-utm back-stamping-artifact warning; time-to-complete twist
- **Segment:** by acquisition channel (utm_source/utm_medium, event-level)  ·  **Sources:** mixpanel
- **Confidence:** medium-high
- **Caveat:** Mixpanel funnel onboarding_started->signup_completed, prod (environment=='production'), unique users, 1-day conversion window, June 1-30 2026 (the clean pre-collapse month; the signup collapse began Jul 3 so recent windows are unusable). Breakdown is on the EVENT-level utm_source/utm_medium present on the onboarding_started entry event (NOT the initial_utm_source $user profile property, which is back-stamped onto completers -- see one-liner). Bases: overall 3,813->1,674 (44%); organic/undefined 1,951->970 (50%); Google Ads 757->290 (38%), adwords 730->298 (41%); fb 149->51 (34%); ig 90->22 (24%); X combined (x ads 54->15, x 39->9, x%20ads 22->6) 115->30 (26%). utm_source present on only ~49% of onboarding_started events (1,862/3,813); 'undefined' event bucket = organic/direct. Per-channel small-N (fb 149, ig 90, X 115) are directional; organic (1,951) and Google (1,487) are solid. onboarding_started is the app-project (3842718) entry to the signup flow, the closest 'land' proxy in Mixpanel -- a true landing-page-view lives on the marketing project (3842156) and a clean cross-project land->signup funnel needs distinct_id reconciliation (deferred). distinct_id, NOT company-deduped. 1-day window slightly under-counts late completers (would lift all rates a little, not change the ranking). avg-time-to-complete is noisy per channel (Google Ads 767s tail-dragged) so the 'speed predicts outcome' twist is directional. Marks not drives; reconciled pay-through by channel still needs Stripe (deferred).

---

### 2026-08-06 — 🆕 NEW — Day-34 signup collapse is an ~80% onboarding-entry drop, NOT a dead signup tag -- per-user onboarding->signup still converts 28% (was 44%), installed base 100% healthy

Answering the backlog's standing question -- 34 days into the Jul-3 signup collapse (now Aug 6), are real new users still arriving, and is this a broken signup_completed tag or a real outage? -- the per-USER funnel reframes the Jul-9 'isolated broken signup tag' hypothesis. signup_completed is STILL floored (last-7d Jul30-Aug5 = 39 events vs a June ~490/wk baseline = ~-92%, daily ~5-11), yet the collapse is NOT an isolated dead final-step tag: on a per-user onboarding_started->signup_completed 1-day funnel (prod, unique), completion only fell 44% pre (1,674/3,814, Jun) to 28% post (189/686, Jul10-Aug5) -- signup_completed still FIRES for ~1 in 4 onboarding-starters, not ~0 as a dead tag would imply. The ~90% daily-event collapse decomposes cleanly into TWO compounding factors: (1) ~80% fewer unique users ENTER onboarding (onboarding_started 127/day unique in Jun -> 25/day post), the dominant term, plus (2) a further ~36% relative drop in per-user completion (44%->28%); 0.20 x 0.64 ~= 0.13 of prior ~= -87%, matching the observed -92% daily drop. Crucially the installed base is 100% HEALTHY -- app_session_started runs at its full June baseline (Aug 3-5: 6,386/6,290/6,611 vs June ~6,000/weekday), and agent_message_sent/node_used are at normal weekday levels -- ruling out any Mixpanel-wide or product outage. And real new users ARE still arriving and activating: over Jul10-Aug5, 685 onboarding-starters converted to an agent message within 7d at 17% (117 users) vs 29% (1,089/3,815) pre-collapse -- reduced but a live, normally-activating trickle, NOT a zero. Net: this is a genuine ~80% top-of-funnel new-user CONTRACTION (fewer people reaching onboarding) plus a modest partial degradation of the completion step, on a fully-healthy existing base -- NOT the cleanly-isolated broken signup_completed tag the Jul-9 ledger suspected. Whether the ~80% onboarding-entry drop is real lost acquisition vs a shared upstream onboarding_started instrumentation break cannot be fully separated in Mixpanel, but the live 17% onboarding->agent activation proves a real (smaller) new-user flow persists. Marks not drives.

- **Metric:** per-user onboarding->signup 1d completion, post-collapse (vs 44% pre) = **28**
- **Theme/angle:** Acquisition & signup funnel — Signup collapse diagnosis at day 34 -- broken-tag vs real top-of-funnel contraction (per-user onboarding->signup completion + installed-base health + new-user activation)
- **Segment:** by funnel step (onboarding-starter -> signup)  ·  **Sources:** mixpanel
- **Confidence:** medium-high
- **Caveat:** Prod, environment=='production'. signup_completed daily-total last-7d (Jul30-Aug5)=39 vs June ~490/wk (~70/day) = ~-92%; daily values Aug1-5 = 4,1,2,7,11 (Aug6 partial, excluded). Per-user funnels are unique-user, 1-day conversion window, onboarding_started->signup_completed: PRE Jun 1-30 = 3,814->1,674 (44%); POST Jul 10-Aug 5 = 686->189 (28%). onboarding_started unique/day: 3,814/30=127 (Jun) vs 686/27=25 (post) = -80%. onboarding->agent_message_sent 7d unique: PRE 3,815->1,089 (29%), POST 685->117 (17%). app_session_started at June baseline (Aug3-5 ~6.3-6.6k/day) confirms product+pipeline healthy and rules out a project-wide outage. KEY LIMITATION: Mixpanel alone cannot fully separate a REAL ~80% acquisition/onboarding-entry drop from a shared UPSTREAM instrumentation break that under-fires onboarding_started itself (both would show the two events falling together); server-side user-created rows (Neon, deferred) are needed to close that. What IS newly settled: the 28% per-user completion (not ~0) weakens the Jul-9 'isolated broken signup_completed tag' read, and the live 17% onboarding->agent activation + 100% app_session_started prove real new users still arrive and activate (answers the backlog question: NOT a total new-user outage). distinct_id, not company_id-deduped. Windows differ in length (30d pre vs 27d post) so per-day normalization used for the -80%. Today's assigned template lens (first-template vs no-template) does not apply to a signup-funnel diagnostic and was not used; the twist (study who did NOT do the action) is honored by analyzing onboarding-starters who never complete signup.

---

### 2026-08-05 — 🆕 NEW — Building is a steeper power-law than conversing -- top 10% of building companies drive 72% of node-adds (Gini 0.79) vs 63%/0.71 for agent messages

Today assigned angle (top 1%/10% company share of executions) on the BUILD/execution surface, previously unquantified. On node_used (prod, 90d; 1,197 companies with a company_id, 18,783 attributed node-adds), the top 1% of companies generate 26.2%, top 5% 56.3%, and top 10% 72.1% of all node-adds, Gini 0.789. That is materially MORE concentrated than the conversation surface: re-running agent_message_sent on the same window (2,997 companies, 28,538 attributed msgs) gives top 1% 29.3% / top 5% 52.0% / top 10% 63.3%, Gini 0.712 -- essentially unchanged from the Jul-7 read (top10 61.7->63.3, Gini 0.70->0.71, a <3% relative move = stable, NOT material) so the power-law held through the signup collapse. The NEW parts: (1) the build surface top-decile share (72%) is ~9pt higher than agent (63%) and its Gini (0.79 vs 0.71) is higher -- building depth lives in an even thinner slice of accounts than conversation does, matching the ledger read that building is narrow-but-deep while conversation is wide-but-shallow; and (2) the assigned twist (segment until the average breaks): the mean company is a statistical fiction on both surfaces. Mean node-adds/company = 15.7 but the MEDIAN company added just 3 (45% added <=2 nodes, 29% exactly one); the bottom 50% of building companies together contribute only 4.8% of node-adds, and the single top company (914 node-adds) outweighs the bottom 600 companies COMBINED. Agent is the same shape, gentler (mean 9.5, median 3, bottom-50% = 8.5%, top company 1,069 > bottom 914 combined). So reporting a per-company average for usage depth is meaningless -- the distribution is dominated by a ~10% power-user core on both surfaces, more so on the builder.

- **Metric:** node top-10pct company share of executions (vs agent 63.3) = **72.1**
- **Theme/angle:** Agent & workflow usage depth — Power-law of usage: top 1%/10% company share of executions -- build (node_used) vs agent (agent_message_sent) surface contrast + mean-vs-median (average breaks) twist
- **Segment:** by company (build surface vs agent surface); tail split  ·  **Sources:** mixpanel
- **Confidence:** high
- **Caveat:** Company-level concentration on total-event breakdown by the company_id $user profile property, prod, last 90d (3 months). node_used = Node Added to Canvas (desktop-only drag-drop build action). Bases: node_used 1,197 companies / 18,783 company-attributed events (547 events, ~2.8%, had no company_id -> excluded); agent_message_sent 2,997 companies / 28,538 attributed events (607 undefined, ~2.1%, excluded). top-k uses round(n*frac): node top1%=12 cos, top5%=60, top10%=120; agent top1%=30, top5%=150, top10%=300. Gini computed on the excl-undefined per-company distribution. Unit is company_id from the $user profile, NOT distinct_id -- this is a genuine per-COMPANY concentration (unlike most ledger retention entries which are distinct_id). Internal/test accounts are not separately excludable by id, so a few low-id internal companies may sit in the top slice and mildly inflate concentration (e.g. company 331 = 1,069 agent msgs, 135 = 914 node-adds -- plausibly internal/heavy). agent_message_sent is the conversation proxy (may include builder-copilot); node_used the build proxy. Both are Mixpanel event-count proxies for usage depth; true workflow-execution internals (run counts, durations, error_rate_pct -- today assigned ClickHouse/Neon primaries) remain deferred, so power-law of actual workflow RUNS could differ from node-add concentration. The assigned plan lens (SELF_SERVICE vs rest) is not usable: self_service_cohort tags only 1.2% of active users (ledger Jul-28), so concentration cannot be split by plan; used build-vs-agent surface and the tail (mean-vs-median) as the differentiating cuts instead. Confirms & extends Jul-7 (agent top10 61.7%, Gini 0.70; builds only as "65% <5 nodes") -- adds the build-surface decile shares/Gini and the cross-surface contrast. Marks concentration; does not by itself explain WHY depth concentrates (account size, sales-touch, use-case). >15%-move novelty check: agent moved <3% (stable, not re-logged as new); the build-surface decile concentration is the genuinely new number.

---

### 2026-08-04 — 🆕 NEW — Directly answering the assignment: recent cohorts are NOT deteriorating -- weekday wk1 retention held flat ~23-27% May->July despite the signup collapse

The assigned question -- WoW retention by signup-month cohort, is a recent cohort better or worse? -- has a reassuring answer once you (a) cohort on first agent message rather than the broken signup_completed event and (b) strip out the weekend-composition effect (companion finding). Monthly wk1 self-retention on WEEKDAY births is essentially flat: May 22.8% (147/644), June 27.0% (564/2,090), July 25.7% (270/1,051) -- no decay, if anything a slight lift into June that holds through July. So cohort QUALITY (next-week return) has been stable-to-improving across three months even as acquisition VOLUME cratered ~90% on Jul 3: the smaller July intake is retaining as well as the pre-collapse cohorts, not worse. The naive all-births monthly read looked like improvement (20%->24%->26%) but ~half of that apparent gain was July simply having fewer low-retaining weekend activations (weekends nearly vanished during the collapse), so the honest read is FLAT weekday retention, not a real quality improvement. Net for the retention narrative: there is no recent-cohort retention cliff on top of the acquisition cliff -- the problem remains getting users in and past week 1, not a degrading week-1 return rate. Marks not drives; distinct_id not company-deduped.

- **Metric:** weekday wk1 agent self-retention, July cohort (May 22.8 / Jun 27.0 / Jul 25.7) = **25.7**
- **Theme/angle:** Retention & churn cohorts — WoW retention by signup-month cohort -- is a recent cohort better/worse (weekday-adjusted monthly trend)
- **Segment:** by signup-month cohort (weekday births, overall)  ·  **Sources:** mixpanel
- **Confidence:** medium-high
- **Caveat:** Same retention curve/source as the companion finding (agent_message_sent self-retention, prod, weekday births only to remove weekend composition). Monthly wk1: May (May 25-31 births) 147/644=22.8%, June 564/2,090=27.0%, July (through Jul 28, mature wk1) 270/1,051=25.7%. May is truncated to the clean post-rollout window (>=May 25) so its base is smaller and edge-affected. Cohort birth = first agent_message_sent, deliberately NOT signup_completed (collapsed since Jul 3, so a true signup-month cohort is unmeasurable for July); this is a usage-activation-month cohort, the closest measurable proxy. July intake is self-selected (acquisition down ~90%), so 'July retains as well' partly reflects a higher-intent surviving intake, not necessarily that the funnel improved. wk2/wk3 monthly rates are noisier and less mature for July and not used for the headline. distinct_id not company-deduped. Answers the assigned angle (no recent-cohort retention decay); the acquisition-volume collapse (ledger Jul-8/9/20) is the live problem, not week-1 return quality.

---

### 2026-08-04 — 🆕 NEW — Weekend-activated users are a retention dead zone -- 6% return the next week vs 26% for weekday activations (4x gap)

Today's assigned angle (WoW retention by signup-month cohort -- are recent cohorts better/worse?) surfaced a sharper cut than the month axis: the DAY OF WEEK a user first sends an agent message is a ~4x retention marker, and it's the cleanest baseline split yet. On birth-week self-retention of agent_message_sent (prod, births May 25-Jul 28 2026, cohorted on FIRST agent message -- which sidesteps the Jul-3 signup_completed collapse -- N=4,361 births, all wk1 windows mature), users whose first agent message lands on a WEEKDAY return the following week at 25.9% (981/3,785), essentially flat across Mon-Fri (23-29%). Users whose first message lands on a WEEKEND return at just 6.2% (36/576) -- Sat 6.0%, Sun 6.5% -- a 4.1x gap that is astonishingly consistent (every one of ~9-10 Sat and Sun cohorts sits at 6-7%, every weekday at 23-29%). This is NOT a bucketing artifact: a weekend birth's wk1 window is the next full calendar week (and starts sooner after birth, which would if anything flatter weekend return, not depress it), and the split reproduces cleanly WITHIN a single month (June alone: weekday 27.0% vs weekend 4.1%, 6.6x). Weekend births are also genuinely engaged in-session -- their same-week (wk0) second-message rate is a normal 65-77%, so they are real active first sessions, not bots -- they simply never come back. Weekend activations are ~13% of all activations (~576 over the window, ~150/month) and convert to almost zero retained users, refining the ledger's week-1 cliff (Jul-24: 75% one-week-and-done) by naming WHO falls off hardest: the weekend cohort is ~one-and-done by construction. Actionable: a weekday-timed activation, or a Monday re-engagement nudge aimed specifically at weekend first-users, is the lever; whatever onboarding/support/live-response exists on weekdays is largely absent when weekend users hit their first wall. Marks not drives; distinct_id not company-deduped.

- **Metric:** weekend-birth wk1 agent self-retention (vs 25.9% weekday) = **6.2**
- **Theme/angle:** Retention & churn cohorts — WoW retention by cohort -- day-of-week of first activation as a retention marker (weekday vs weekend births)
- **Segment:** by day-of-week of birth (weekday vs weekend)  ·  **Sources:** mixpanel
- **Confidence:** medium-high
- **Caveat:** Mixpanel weekly retention CURVE on agent_message_sent, SELF-retention (same event as birth and return), prod, daily birth cohorts May 25-Jul 28 2026 aggregated to weekday/weekend; wk1 = the following calendar week (all included cohorts mature -- births through Jul 28 have a complete wk1 window as of Aug 4; Jul 29-Aug 4 births excluded as immature). Cohort birth = FIRST agent_message_sent in-window (agent_message_sent instrumented ~May 18, so births >=May 25 are clean of the rollout burst); cohorting on usage-birth rather than signup_completed deliberately sidesteps the Jul-3 signup_completed collapse (signup is broken/floored since Jul 3; agent activity recovered and is healthy). N: weekday births 3,785 (wk1 ret 981), weekend births 576 (wk1 ret 36); every Sat/Sun daily cohort independently 6-7% and every weekday 23-29%, so the split is not small-N noise. NOT a weekly-bucketing artifact (weekend wk1 is a full following week and starts sooner post-birth, biasing weekend return UP not down) and reproduces within June alone (weekday 27.0% vs weekend 4.1%). Unit is distinct_id, NOT company_id-deduped -- a company could still be active via another user. Mechanism unidentified: weekend first-users may be a more casual/tire-kicker population, or may hit first-session friction with no weekday support/live-response to recover them (Mixpanel can't distinguish); mp timezone is event-time UTC-ish so day-of-week is server-side, not necessarily the user's local weekend. 'Marks' the retention gap; does not by itself 'drive' it. The cross-source join twist (Neon/Stripe) is deferred -- no DB creds this run.

---

### 2026-08-03 — 🆕 NEW — The last action before a credit purchase is an agent conversation, not a billing-page visit -- top-ups are ~2x more often reactive/in-chat than deliberate

On a Flows-into-credit_topup path (prod, 6mo, N~128 unique toppers, unique), the single most common IMMEDIATE predecessor of a top-up is agent_response_received (55, 44%) -- users topping up mid-conversation -- vs the deliberate billing path page_visited_settings_billing->button_billing_agregar_creditos (24-25, ~19%). Two-back, 52 users went agent_message_sent->agent_response_received->topup with NO billing page in the last two steps. So credit top-up is predominantly a REACTIVE, hit-the-wall-in-chat event (~2x the billing-page path), reframing the Jul-23 read that the billing page IS the pay-intent signal: it is a clean intent signal but captures only ~1 in 5 actual top-up moments. Device lens: top-ups are 85% desktop (Windows 77 + Mac 27 of 128; mobile just 23/18%) despite mobile being ~half of signups and conversing at 60% -- payers are the desktop-heavy engaged cohort.

- **Metric:** share of credit_topup whose last action is an agent conversation (vs billing page) = **44**
- **Theme/angle:** Monetization & pay-drivers — The last action before first credit_topup (Flows-into-topup): conversation vs billing-page path + device lens; stresses the Jul-23 billing-page-is-the-intent-signal finding
- **Segment:** by last-action path (conversation vs billing) + device  ·  **Sources:** mixpanel
- **Confidence:** medium
- **Caveat:** Mixpanel Flows into credit_topup, prod, last 6mo, countType=unique, stepsBefore up to 2; N~128 unique toppers (event history since ~May 2026, 0 before), ~126 with a traceable predecessor. Immediate-predecessor counts: agent_response_received 55 (44%), button_clicked_billing_agregar_creditos 34 (27%, the mechanical add-credits click), app_session_started 17 (13%), page_visited_settings_billing 3, node_used 3, tester_enviar_mensaje 3, others 2 each. Two-step: agent_message_sent->agent_response_received->topup 52; page_visited_settings_billing->add-credits-button->topup 24. Flows adjacency = immediately-preceding events in the user stream (a tighter read than a time-bounded 48h window; not strictly clipped to 48h). agent_response_received is the agent replying (system-side) but is the tail of a user-initiated message->response pair, so the 52-chain reflects real conversation not automation. credit_topup fires PRE-checkout = intent-to-pay, credits only, NOT reconciled revenue (subscriptions/MRR Stripe-only, deferred). Unit is distinct_id, NOT company_id-deduped. Sub-splits (device x path) are small-N; the 52-vs-24 conversation>>billing contrast and the 85%-desktop skew are the robust reads. Context (not a finding): Jul unique toppers fell 58->22 but agent monthly actives fell 1596->663 over the same step (both ~-60%), so top-up-per-active held ~3.5% -- Jul topup drop is downstream of the known signup/activity decline, not a monetization-specific collapse. Marks not drives.

---

### 2026-07-31 — 🆕 NEW — Template installs aren't shelfware -- run within a day (70%) but under half ever get formally tested (43%); home market exercises them hardest

Today's assigned angle -- do template installs sit unused as shelfware? -- has a two-sided answer in Mixpanel once you separate 'run it' from 'test/deepen it'. On 105 unique template-installing users (prod, last 180d; template events carry ~180d history), installs are NOT shelfware in the run-it sense: 70% (73/105) send an agent message within 30d of installing, and they do it FAST -- mean time-from-install-to-first-agent-message ~19-27h (essentially same/next day). But the DEPTH exercise lags badly: only 43% (45/104) ever start a tester session and only 44% (46/104) add another node within 30d of install, and both take ~3-4 days on average. So the leak isn't abandonment-on-a-shelf (~30% never even converse), it's under-testing: an installed template gets talked to within a day but under half of installers ever formally TEST the agent they just built. Geography lens (today's segment): the home market exercises installs HARDEST, extending the ledger's EC>>peers retention concentration onto the template surface. Ecuador is 51% of all installers (54/105) AND over-indexes on exercise -- 78% run the agent (42/54) vs 70% overall and 55% test it (29/53) vs 43% overall. US installers run at 81% (13/16) but barely test (22%, 2/9). Small-N peers are noisy (CO 65%/50%, MX 43%/57%, PE 50%/25%, CL 83% run but 0/5 test). Size the leak (today's twist), in absolute companies over the 180d window: ~30% x 105 ~= 32 installers (~5/month) never send a single agent message after installing (true shelfware), and ~57% x 104 ~= 59 installers install a template but never start a tester session -- 59 companies that pulled a template onto the canvas and never once formally tested the agent. Marks not drives; distinct_id not company-deduped; agent_message_sent is a wide net (could include builder-copilot), tester_session_started is the cleaner 'exercised the built agent' signal.

- **Metric:** install->tester_session_started 30d (formally-tested rate) = **43**
- **Theme/angle:** Templates: intent vs. action — Time-from-install-to-first-use -- shelfware check: run-it (agent_message) vs test-it (tester_session) vs build-more (node_used) after install, geography lens + absolute leak sizing
- **Segment:** by geography (mp_country_code); install-exercise nets  ·  **Sources:** mixpanel
- **Confidence:** medium (base N=105 installers solid for overall run/test rates; per-country small-N -- Ecuador N=54 the only robust cell, others 3-17 directional)
- **Caveat:** Base = 105 unique template_installed users (104 in the tester/node funnels), prod, last 180d (template_installed/template_preview_opened carry only ~180d history). Funnels cohort on install then count the outcome within 30d on any device, unique users. Recent installers (<30d) have partial windows so the 43%/44%/70% rates are mild UNDER-counts of the fully-mature rate. Unit is distinct_id, NOT company_id-deduped. agent_message_sent ('AI Assistant Message Sent') is a WIDE net that may include builder-copilot messages, so the 70% run-rate overstates 'used the installed template specifically'; tester_session_started is the cleaner 'exercised the built agent' proxy (43%) and node_used the 'kept building' proxy (44%). time-from-install: mean ~19-27h to first agent message, ~4.1 days (350k s) to first tester session, ~3.1 days (267k s) to next node -- means are tail-dragged (converters only). Per-country cells are small (EC 54, CO 16-17, US 9-16, PE 8, MX 7, CL 5-6, AR/PA 3): only Ecuador is robust; US test-rate 22% (2/9) and Chile 0/5 are directional. mp_country_code is geo-IP at event time, not billing country. Absolute leak sizing (~32 never-converse, ~59 never-test over 180d) applies the overall rates to the 104-105 base. Reproduces & extends the Jul-1 neon finding ('installs aren't shelfware; 21% never return') in Mixpanel-native terms and adds the test-depth leak + geography lens; also directionally answers the backlog Q on whether the EC>>peers gap holds on builder/template cohorts (it does). Deployment/publish of the installed template and reconciled pay-through still need ClickHouse/Stripe (deferred). Marks not drives; reverse causation (committed users install AND exercise more) is at least as likely.

---

### 2026-07-30 — 🆕 NEW — Media signups are NOT the dead-on-arrival cohort -- that's a desktop-only-metric artifact; on the widest net media activates 70% vs organic 63%

Today's assigned angle -- size the dead-on-arrival cohort (signed up, fired ZERO activation) and name its channel -- has a reframe answer once you stop scoring activation by the desktop-only builder. On a clean pre-collapse cohort (prod signups May 18-Jun 30 2026, N=3,697; agent_message_sent instrumented ~May 18 so the window is clean of both the rollout burst and the Jul-3 signup collapse), the WIDEST activation net is agent_message_sent: 65% (2,399) send an agent message within 30d, vs only 13% (483) who ever add a node and 3% (127) who start a tester session -- and build/test are almost entirely nested inside messagers, so the truly-dead-on-ALL-surfaces cohort is ~one-third of signups (~33-35%; 35% never-message is the widest-net upper bound). The NEW part is the CHANNEL split, which INVERTS depending on which net you use. On the BUILD net media looks half-dead: media (initial_utm_source set, N=982) build at 7% (73) vs organic (N=2,715) 15% (410) -- reproducing the Jul-6 'paid ~6% vs organic 15%' story. But on the WIDEST net media activates MORE than organic: media 70% (686/982) message vs organic 63% (1,713/2,715), so media's dead-on-arrival rate is 30% vs organic's 37%. Media/paid signups are therefore NOT the dead-on-arrival cohort -- they are mobile-heavy (Jul-6: paid 77% mobile) users who structurally can't drag nodes but converse at high rates; the 'paid buys dead signups' read is an artifact of measuring activation by a desktop-only feature (mechanism matches the Jul-17 mobile-converses-at-60% finding). Twist (recent vs older, both pre-collapse): the media edge is RECENT and widening -- older half May 18-Jun 8 organic led 70% (1,330/1,899) vs media 59% (201/341), but recent half Jun 9-30 media led 76% (485/641) vs organic 47% (383/816). The recent organic drop to 47% is directional (candidate causes: free-limit cut ~Jun 11, or attribution/window timing) and needs confirmation; the pooled media>=organic inversion is the robust read. Marks, does not drive; distinct_id not company-deduped.

- **Metric:** media 30d agent-message activation (widest net) vs organic = **70**
- **Theme/angle:** Activation & time-to-milestone — Dead-on-arrival cohort -- how big & which channel, measured on the WIDEST activation net (agent_message) vs the desktop-only build net; recent-vs-older twist
- **Segment:** by acquisition channel (media vs organic)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (clean cohort N=3,697; media N=982 / organic N=2,715 solid for the pooled inversion; recent/older halves smaller and the organic-recent dip directional)
- **Caveat:** Cohort = prod signups May 18-Jun 30 2026 (agent_message_sent first fired ~May 18, so the window is clean of the rollout burst and the Jul-3 signup_completed collapse); the funnel cohorts on signup then counts the outcome within 30d on ANY device (as of Jul 30 signups have 30-73d elapsed, so all 30d windows are mature). 'media' = initial_utm_source is-set on the $user profile (~27% of signups, 982/3,697); 'organic' = is-not-set (direct/untagged, treated as organic). Unit is distinct_id, NOT company_id-deduped. The 'truly-dead ~33-35%' figure anchors on agent_message_sent as the widest net (65%) and treats build (13%)/test (3%) as ~fully nested in messagers; the exact union is not measurable without JQL groupByUser (unavailable in this MCP), so 35% never-messaged is a near-upper-bound and the all-surface-dead rate is marginally lower. Recent-vs-older halves are smaller-N (media 341/641) and the organic recent 47% is unconfirmed (window-boundary vs free-limit-cut). Reconciled by-channel revenue/pay-through still needs Stripe (deferred). 'Marks' the activation gap; does not by itself 'drive' retention/pay.

---

### 2026-07-29 — 🆕 NEW — Within the email/password path, the PASSWORD step is the single biggest leak — 60% never submit a password

Scoping the assigned 'which step sheds most' question to the minority email/password path where those step events actually fire: the answer is unambiguously the password step, not profiling or the final submit. On an ordered email-path funnel (June 2026, prod, unique, 1-day window) step_email_submitted -> step_password_submitted -> signup_completed runs 409 -> 162 (40%) -> 153 (94%). So 60% of users who submit an email never submit a password (the decisive drop), and essentially everyone who clears the password step completes (94%). Crucially this is GENUINE abandonment, not users hopping to Google SSO: only 30 of the 409 email-submitters (7%) subsequently fire start_signup_sso within a day, so path-switching explains at most ~7pts of the 60-point drop. The email/password credential step — specifically committing a password after typing an email — is where the self-serve email signup path bleeds out.

- **Metric:** email->password step conversion (email-path funnel, %) = **40**
- **Theme/angle:** Acquisition & signup funnel — Step-level signup leakage — which step sheds most users (email-path funnel)
- **Segment:** by signup step  ·  **Sources:** mixpanel
- **Confidence:** medium-high (N=409 email-submitters, June prod, ordered 1-day funnel; path-switch check N=30)
- **Caveat:** Applies only to the ~11% email/password path (companion finding); the majority SSO path has a different, higher-converting shape (72%). distinct_id, not company-deduped. 1-day conversion window; a longer window would recover a few late password submits (would soften the 60% slightly). 'Marks' the leak step; Mixpanel can't say WHY the password step is abandoned (friction, second thoughts, bot-filtering). company_profiling_step_completed excluded from this funnel (newborn ~Jul 1, post-dates the clean June window).

---

### 2026-07-29 — 🆕 NEW — The assigned email/password step funnel is a minority path — signup is overwhelmingly Google SSO

Today's angle (which signup step — email/password/profiling — sheds the most users) is largely mis-scoped in Mixpanel: the email/password step events describe only a small minority of signups, because the dominant path is Google SSO. On the last clean pre-collapse month (June 2026, prod, unique), of 3,814 onboarding_started only 409 (11%) ever fire step_email_submitted, whereas 1,377 (36%) fire start_signup_sso — SSO is ~3.4x the email path. And SSO converts far better: onboarding_started->SSO-started->signup_completed runs 3,814 -> 1,359 (36%) -> 984 (72% of SSO-starters), i.e. 984 SSO completions vs only ~153 clean email-path completions in the same 1-day-window funnel (~87% of measured path-attributable completions are SSO). So the 'email/password step leakage' the rotation asks about covers ~1 in 9 onboarding-starters; the real signup funnel is a Google-SSO click, and its main leak is the 64% of starters who never start SSO at all (onboarding_started->SSO 36%), not any within-email micro-step. Two structural caveats compound the mis-scope: company_profiling_step_completed (the 'profiling' step) was only instrumented ~Jul 1 2026 (0 before), so the profiling leg has no clean pre-collapse history; and the 26-day signup-funnel collapse (below) has floored every one of these events since Jul 3, so recent-vs-older and template lenses are non-viable at these Ns.

- **Metric:** email/password step-funnel coverage of onboarding-starters (%) = **11**
- **Theme/angle:** Acquisition & signup funnel — Step-level signup leakage (email/password/profiling) — feasibility & path composition
- **Segment:** by signup path (SSO vs email/password)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (June prod uniques: onboarding_started 3,814; start_signup_sso 1,377; step_email_submitted 409; signup_completed 1,832; path funnels 1-day window)
- **Caveat:** June 2026 is the last clean pre-collapse month. Counts are distinct_id uniques, prod, not company-deduped. start_signup_sso = 'Signup · Google SSO Started' (SSO intent click, not guaranteed completion; 72% complete). onboarding_started 3,814 vs identifiable paths (409 email + 1,377 SSO = 1,786) leaves ~2,000 starters who fire neither in-window — some complete later/returning, some abandon before choosing a path; the SSO-vs-email SHARE among path-committed users is the robust read, the absolute 11% is a lower bound on email-path share of *starters*. step_email/password are real (clean 94% password->complete downstream) not broken, just minority. Profiling step (company_profiling_step_completed) newborn ~Jul 1. Reconciled server-side signup counts still deferred (needed to close the collapse question).

---

### 2026-07-28 — 🆕 NEW — The assigned 'plan' lens can't segment the base -- self_service_cohort tags only 1.2% of agent users, so Ecuador's edge is NOT a self-serve/managed mix

The rotation's segment lens was 'by plan (SELF_SERVICE vs the rest)', and the backlog explicitly asks whether Ecuador's ~2.3x retention edge is a self-serve-vs-managed MIX by market. It cannot be, and the lens itself is barely populated: of 3,506 agent-active users in 90d (prod), only 42 (1.2%) carry self_service_cohort='yes' and the alternative cohort_tag='SELF_SERVICE' flag is 0% populated on this base. A user property that covers ~1 in 80 active users cannot move a market-level retention average, so the self-serve/managed-mix explanation for the geography gap is ruled out at this flag's coverage -- the gap is intrinsic to the markets, not a plan-composition artifact. Directionally (and against the common intuition that no-touch self-serve users are the churny ones), the tiny tagged self-serve cohort does NOT retain worse -- weekly wk1 self-retention ~37% vs the 24% base, i.e. if anything stickier -- but N=42 over 90d is far too small to bank and is noted only to flag that 'self-serve = leaky' is unsupported here. Net: the plan lens is an instrumentation gap (like the Jul-23 upgrade_cta_clicked gap), and a real self-serve-vs-managed retention split needs a populated plan/tier field from Neon/Stripe (deferred).

- **Metric:** self_service_cohort='yes' coverage of agent-active users (90d, %) = **1.2**
- **Theme/angle:** Retention & churn cohorts — Plan lens feasibility (self_service_cohort / cohort_tag) -- can 'self-serve vs managed' explain the geography retention gap?
- **Segment:** by plan (self_service_cohort)  ·  **Sources:** mixpanel
- **Confidence:** high (coverage counts are exact: 42 of 3,506; cohort_tag 0/3,506)
- **Caveat:** Coverage is exact and robust; the 'self-serve retains better' direction is N=42 and NOT reliable (reported only to counter the assumption that self-serve is the churny segment). self_service_cohort/cohort_tag are $user-profile flags; 'undefined' is the overwhelming majority (96%+) and may mean either genuinely-not-self-serve OR simply untagged -- Mixpanel can't distinguish, which is exactly why the lens is unusable. Rules OUT plan-mix as the driver of the EC>>CO/MX>>PE gap at this coverage; does not identify what DOES drive it (language/localization, sales-touch, account size -- open backlog). True plan/tier segmentation deferred to Neon/Stripe.

---

### 2026-07-28 — 🆕 NEW — Retention concentrates agent usage MORE than acquisition -- Ecuador is 43% of ACQUIRED agent users but ~70% of WEEK-1-RETAINED; Peru 12% -> 1.4%

Today's angle was to break a prior insight; I tried to break the 'Ecuador retention edge is a home-market artifact' story two ways and it not only survived -- it got sharper. Re-running weekly agent_message_sent self-retention on an independent clean window (prod, births May 25-Jun 29 2026) re-confirms the Jul-15 geography rates almost exactly: wk1 return Ecuador 39%, Colombia 16%, Mexico 17%, Peru 3% (overall 24%), with Ecuador durable (wk2 32%, wk3 29%, wk4 26%) and Peru flat ~0% after week 1. The NEW finding is what happens when you multiply 90d acquired agent users (unique, prod) by each market's wk1 return rate to size RETAINED users: Ecuador 1,502 acquired x 39% ~= 586 retained; Colombia 473 x 16% ~= 76; Mexico 295 x 17% ~= 50; Peru 414 x 3% ~= 12; total wk1-retained pool ~= 841 (0.24 x 3,506). So retention roughly DOUBLES Ecuador's dominance: it is 42.8% of acquired agent users (1,502/3,506) but ~70% of week-1-retained ones (586/841) -- higher than the 50.5% share-of-activity in the Jul-7 concentration finding, i.e. counting activity UNDERSTATES how concentrated the retained base is. Peru inverts: 11.8% of acquired users collapses to ~1.4% of retained (12/841). Sizing Peru's leak in absolute users (today's twist): of ~414 Peruvian agent users acquired per quarter, ~400 are one-week-and-done; if Peru merely retained at Ecuador's 39% it would keep ~161 instead of ~12, a shortfall of ~149 week-1-retained users lost purely to the retention gap (holding acquisition constant). Marks, does not drive; distinct_id not company-deduped.

- **Metric:** Ecuador share of week-1-retained agent users (vs 42.8% of acquired) = **70**
- **Theme/angle:** Retention & churn cohorts — Try-to-break the geography-retention story -- retained-USER concentration (acquired volume x wk1 return) and absolute sizing of the Peru leak
- **Segment:** by geography (mp_country_code), retained-user share  ·  **Sources:** mixpanel
- **Confidence:** medium-high
- **Caveat:** Retained-user counts are a back-of-envelope: 90d unique agent users per country (prod; Ecuador 1,502, Colombia 473, Peru 414, Mexico 295, total 3,506) multiplied by each market's weekly wk1 self-retention rate from the retention curve (EC 0.39/CO 0.16/MX 0.17/PE 0.03/overall 0.24). Mixing a 90d snapshot count with a per-weekly-cohort rate is approximate (order-of-magnitude sizing, not an exact headcount), and the retained-pool denominator (~841) uses the overall 24% so country shares sum to ~roughly 100% only across measured markets. Rates re-confirmed on births May 25-Jun 29 2026 (mature >=4wk); agent_message_sent instrumented ~May 18 so window is clean of the rollout burst. Unit is distinct_id, NOT company_id-deduped -- Peru's near-zero could still be a few churned accounts (open backlog Q) and Ecuador's share could be swung by large accounts. mp_country_code is geo-IP at event time. Extends (does not overturn) Jul-7 (EC 50.5% of activity) and Jul-15 (EC 38% wk1); the contradiction attempt FAILED to break either and instead tightened the concentration read. Reconciled revenue by market still needs Stripe (deferred).

---

### 2026-07-27 — 🆕 NEW — Skills stall 2x harder than nodes at the same step -- 59% of skill creators never make a 2nd, and it takes them ~6 days

Companion to the node depth-cliff: the skills surface has the IDENTICAL cliff-then-ramp shape but roughly twice as steep at the decisive 2nd step. On a skill_created depth funnel (prod, 90d, unique, N=736 creators), only 41% make a 2nd skill -- so 59% are one-and-done (vs 30% for nodes) -- then step-conversion ramps the same way: 57% (2->3), 77% (3->4), 82%, 86%. Cumulatively 41% reach 2 skills, 24% reach 3, 18% reach 4, 15% reach 5, 13% reach 6. And it's slower: the 1st->2nd skill gap averages ~5.8 days (500,270s) vs ~2.6 days for the 1st->2nd node -- skills stall both harder and later. This corroborates and reframes the Jul-16 'skills are created but not deployed / 57% made exactly one skill' finding inside the same universal depth-cliff structure: on BOTH build surfaces the whole depth battle is the 2nd action, and skills are the weaker of the two.

- **Metric:** skill 1->2 drop-off (one-and-done creators), % who never make a 2nd skill = **59**
- **Theme/angle:** Agent & workflow usage depth — Depth cliff: distribution of skills per user -- skill vs node stall comparison (repeated-event depth funnel)
- **Segment:** by build-depth step (overall baseline)  ·  **Sources:** mixpanel
- **Confidence:** medium-high
- **Caveat:** Repeated-event depth funnel on skill_created ('Skill Created'), prod, last 90d, countType=unique, 90d window; step N: 736 -> 305 (0.41) -> 175 (0.57) -> 135 (0.77) -> 111 (0.82) -> 96 (0.86). avg_time 1st->2nd = 500,270s ~= 5.8 days (converters only). Same distinct_id (not company-deduped) caveat as the node finding -- per-company cliff likely gentler. skill_created is ~92% desktop (prior ledger). Consistent with the Jul-16 create-vs-deploy finding (57% exactly one skill); here re-derived as an ordered depth funnel and framed against the node cliff. Marks the stall step; deployment/publish of the created skills needs ClickHouse (deferred).

---

### 2026-07-27 — 🆕 NEW — The depth cliff is the SECOND action -- 30% of builders never add a 2nd node, then commitment ramps

Today's angle -- where do users stall in build depth? -- has a sharp, self-similar answer on a repeated-event depth funnel (node_used, prod, 90d, unique users, 90d conversion window, N=1,699 builders). Almost all depth attrition is concentrated at ONE step: getting from the 1st node to the 2nd. Step-conversion is 70% at node 1->2 (i.e. 30% of everyone who ever adds a node never adds a second -- the single biggest drop), then RISES monotonically every step after: 77% (2->3), 79% (3->4), 84%, 86%, 89%, 91% by node 7->8. Cumulatively 70% reach 2 nodes, 54% reach 3, 43% reach 4, 36% reach 5, 31% reach 6, and 25% reach 8. So there is no gradual depth decay to chase -- the hazard is front-loaded and DECLINING with depth: once a builder is ~4-5 nodes in they almost never stop (survivorship/commitment ramp). The time dimension (today's twist) points the same way: the 1st->2nd node gap is not just the biggest drop but the SLOWEST step, averaging ~2.6 days (225,368s) among those who cross it, vs a fully-built 8-node graph taking ~11.6 days from the first node. This is the DEPTH-dimension twin of the Jul-24 week-1 retention cliff and the Jul-10 first-hour activation finding: a cliff-then-ramp shape where the whole battle is the 2nd action. The skills surface shows the identical shape but ~2x steeper (companion finding). Actionable: the build onboarding job-to-be-done is getting the 2nd node placed in the first session -- not teaching depth, which takes care of itself once the 2nd node lands.

- **Metric:** node 1->2 drop-off (one-and-done builders), % who never add a 2nd node = **30**
- **Theme/angle:** Agent & workflow usage depth — Depth cliff: distribution of nodes per user -- where do builders stall (repeated-event depth funnel + time-to-next-step twist)
- **Segment:** by build-depth step (overall baseline)  ·  **Sources:** mixpanel
- **Confidence:** medium-high
- **Caveat:** Repeated-event depth funnel on node_used ('Node Added to Canvas'), prod, last 90d, countType=unique, 90d conversion window; step_conv_ratio N: 1699 -> 1188 (0.70) -> 920 (0.77) -> 725 (0.79) -> 609 (0.84) -> 522 (0.86) -> 463 (0.89) -> 421 (0.91). A 'unique' repeated-event funnel measures users who fired node_used at least N times in temporal order within the window, i.e. the 'reached depth >=N' distribution -- a valid depth read. Unit is distinct_id, NOT company_id-deduped: at company grain the 1st->2nd cliff is likely GENTLER (a company's nodes can spread across users/sessions), so 30% one-and-done is an upper bound on the per-company cliff -- the open backlog question. The rising step-conversion could be mildly flattered by the fixed 90d window truncating recent builders' time to reach deep steps, but that truncation biases LATER steps DOWN, so the true commitment ramp is if anything steeper, not an artifact -- the cliff-at-node-2 conclusion is robust. avg_time is over converters only (survivor times). node_used is the desktop-only drag-drop builder, so this is the desktop build surface (mobile ~0 by construction, prior ledger). Marks the stall point; does not by itself say WHY the 2nd node is hard (UX friction vs intent). Extends the Jul-7 node power-law (65% <5 nodes) with the step-by-step SHAPE and pinpoints node #2 as the stall.

---

### 2026-07-24 — 🆕 NEW — Churn is a week-1 cliff, not a 2-week decay -- 75% of agent-activated users never return the next week; the 25% who do are durable (flat wk2-6)

Today's assigned angle -- the activity-decay pattern in the ~2 weeks before a company goes silent -- has a clean, slightly counterintuitive answer in Mixpanel: there is NO gradual 2-week ramp-down to catch. Agent-usage churn is a WEEK-1 CLIFF, not a slope. On a weekly self-retention curve for agent_message_sent (prod, births May 25-Jul 20 2026, avg cohort n~89/day), only 25% (22.6/89.4) of users who send an agent message in a given week return the FOLLOWING week -- i.e. ~75% are one-week-and-done. But the 25% who survive week 1 are durable: their weekly active count is essentially FLAT from wk2 onward (19.7 -> 19.0 -> 16.7 -> 16.7 -> 17.9 across wk2-wk6), ~79% still active by wk6 relative to wk1, with NO further net decay -- a plateau. So virtually all attrition is the single wk0->wk1 drop; there is no observable gentle decline in the fortnight before silence because most churners simply never produce a second week to decay across. The daily 14-day curve confirms the shape: 69% same-week, then a sharp single drop to ~14% by day 1 and a flat 5-14% band thereafter (weekly-rhythm bumps at d7/d14) -- the largest hazard by far is the very first missed week. The pattern generalizes across surfaces: the builder is the same cliff-then-plateau, just shallower (Jul-21 ledger: 43% return wk1 = a 57% cliff, plateau ~32% by wk6), consistent with builder being ~2x stickier than agent. Leading-indicator takeaway: the ONE predictive churn signal is failing to return in week 1 -- an activity-tier of 'one-and-done' that is set almost entirely in the first week. There is no slow-fade cohort to build a decay-based early-warning on; the intervention window is week 1 itself, echoing the Jul-10/Jul-17 finding that activation is a first-HOUR event.

- **Metric:** week-1 churn cliff (agent-activated users not returning the next week), self-retention = **75%**
- **Theme/angle:** Retention & churn cohorts — Churn leading indicators: activity-decay pattern before going silent -- cliff vs gradual ramp-down (churn hazard curve)
- **Segment:** by tenure week (churn hazard curve)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (weekly self-retention on agent_message_sent, prod, births May 25-Jul 20 2026, avg cohort n~89/day; shape stable across daily cohorts; 14d daily curve confirms the day-1 cliff; builder corroboration from the Jul-21 ledger)
- **Caveat:** Mixpanel unbounded weekly retention on agent_message_sent (canonical usage), SELF-retention (same event as birth and return), prod, births May 25-Jul 20 2026; wk7-8 truncated/immature and not used. 'Unbounded' return counts users who skip a week then come back, which is why wk5-6 active counts tick slightly ABOVE wk4 (~16.7 -> 17.9) -- that is re-entry, NOT growth, and it reinforces the plateau (no net decay), not a recovery. Unit is distinct_id, NOT company_id-deduped: 'goes silent' here = a distinct_id stops firing agent messages; a company could still be active via another user or on the builder surface, so this is user-level agent-usage silence, not confirmed company churn (true company churn/revenue needs Neon/Stripe -- deferred, and they were today's assigned primary sources). agent_message_sent was instrumented ~May 18 2026 so births >=May 25 are clean of the rollout burst. Builder comparison figures (43%/32%) are quoted from the Jul-21 ledger entry, not re-run this session. This describes the SHAPE of the hazard (front-loaded, cliff-then-plateau); it MARKS that week-1 no-return is the observable leading indicator but cannot say WHY users don't return, and at the weekly grain it cannot detect intra-week micro-decay. Correlational, marks not drives.

---

### 2026-07-23 — 🆕 NEW — The pay-intent funnel the team just wired up can't be measured -- upgrade_cta_clicked is brand-new (0 before Jul 2026, 7 firings) and subscription_changed is still newborn

Why today's assigned angle (upgrade_cta_clicked -> subscription_changed by source) is unanswerable, and it's a live instrumentation gap worth flagging. upgrade_cta_clicked fired ZERO times in the 12 months before July 2026 and only 7 times (6 unique users) so far this month -- it was just instrumented. subscription_changed remains newborn too (20 unique users / 31 events in 90d, live since ~Jun 24 per prior ledger). So the designated intent->conversion funnel has N<10 at the top and N<25 at the bottom: it cannot be measured in Mixpanel yet. Any dashboard wired to upgrade_cta_clicked as the upgrade-intent KPI is effectively blind -- the real, high-volume intent signal is page_visited_settings_billing (1,187 users). Directly answers the backlog question 'realized conversion from upgrade_cta_clicked to a paid charge, by source': not possible yet.

- **Metric:** upgrade_cta_clicked unique users, 90d (0 before Jul 2026) = **6**
- **Theme/angle:** Monetization & pay-drivers — upgrade_cta_clicked -> subscription_changed feasibility (assigned angle) -- instrumentation maturity
- **Segment:** overall  ·  **Sources:** mixpanel
- **Confidence:** high (event first-fire dates + 90d uniques, prod; the near-zero volume is the whole point)
- **Caveat:** upgrade_cta_clicked: 0 firings Jul 2025-Jun 2026, 7 firings / 6 users in Jul 2026 -- treat as a just-shipped event, not a real behavioral signal. subscription_changed newborn (~Jun 24). Revisit both once they mature (a few more weeks of volume). Reconciled subscription conversion/MRR remains Stripe-only (deferred).

---

### 2026-07-23 — 🆕 NEW — Monetization intent is organic at the INTENT stage too -- 90% of billing-page viewers are organic and conversion is flat media vs organic

Extends the Jul-14 'credit-buying is not a media story' finding upstream from the ACTION stage to the INTENT stage. Of 1,177 billing-page viewers (prod 90d), 90% (1,060) are organic/direct (no initial_utm_source) -- even more organic than the ~79% credit-buyer base and ~79% signup base. Paid channels barely reach the billing page at all (~10% of viewers: Google Ads 48, fb 23, adwords 17, ig 11) AND convert at the same rate: organic 5.8% (61/1,060) vs Google Ads 8.3% (4/48, small-N) vs fb 4% (1/23), ~6% either way. So media buys neither the upgrade intent nor a better intent->pay conversion -- monetization intent is an engaged-organic-user behavior end to end.

- **Metric:** organic share of billing-page (upgrade-intent) viewers = **90**
- **Theme/angle:** Monetization & pay-drivers — Upgrade-intent by media source -- does channel drive billing intent or its conversion
- **Segment:** by acquisition channel (initial_utm_source)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (N=1,177 viewers; organic N=1,060 solid; per-media buckets small-N 11-48, directional)
- **Caveat:** initial_utm_source on the $user profile; undefined treated as organic/direct (~90% here). Per-channel conversion buckets are small-N (Google Ads 48, fb 23, ig 11) so the media-vs-organic rate parity is directional, but the 90% organic SHARE is robust. Same credit_topup pre-settlement/credits-only caveat as the companion finding. distinct_id, not company-deduped.

---

### 2026-07-23 — 🆕 NEW — Only ~6% of billing-page visitors ever top up -- a 94% upgrade-intent->pay leak, and the billing page (1,187 users) IS the intent signal since upgrade_cta_clicked is dead

Today's assigned pay-intent funnel (upgrade_cta_clicked -> subscription_changed) is unmeasurable, so I pivoted to the intent signal that actually fires: page_visited_settings_billing. It is the dominant, usable upgrade-intent event -- 1,187 unique users in 90d (prod) vs just 6 for upgrade_cta_clicked (~200x). Of those billing-page viewers, only ~6% (72/1,177) go on to fire a credit_topup within 30d, avg ~5 days later -- i.e. ~94% of people who open the billing/settings page never top up. This is the first time the intent->payment CONVERSION has been sized (prior ledger characterized only the ~120 buyers themselves). The leak is broadly flat across geography (big markets 4-8%: Ecuador 6.6% N=455, Mexico 7.1% N=154, Colombia 3.9% N=180, Peru 8.3% N=60) with no meaningful geo differentiation -- Ecuador dominates billing-intent VOLUME (39% of viewers) exactly as it dominates usage, but not the conversion RATE. Note this is credit-topup intent (pre-settlement, credits only); subscription conversion stays a Stripe question.

- **Metric:** billing-page -> credit_topup 30d conversion = **6**
- **Theme/angle:** Monetization & pay-drivers — Upgrade-intent -> payment conversion (billing-settings page as the real intent signal)
- **Segment:** overall (geography lens: flat)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (funnel unique, prod 90d, 30d conversion window; N=1,177 viewers / 72 conversions; geo big-markets solid, small markets anecdotal)
- **Caveat:** credit_topup fires pre-checkout so it's intent-to-pay (credits only), not reconciled revenue; subscription conversion is Stripe-only (deferred). Funnel is ordered page_visited_settings_billing -> credit_topup, unique users, 30d window; recent viewers (<30d) have partial windows so 6% is a mild UNDER-count of the fully-mature rate. Unit is distinct_id, NOT company_id-deduped. mp_country_code is geo-IP at event time. Conversion shows NO reliable time trend -- a naive split at May 20 looked like a doubling (4.0% -> 9.6%) but a clean pre/post free-limit-cut split (Jun 11) is flat (5.5% -> 6.3%) and the daily trend is noise, so the apparent shift is a window-boundary artifact, NOT a June-11 pricing effect. 'marks' intent, does not by itself 'drive' payment.

---

### 2026-07-22 — 🆕 NEW — Templates mark DEPTH, not just pay -- but only the 2nd+ install; a single install barely beats non-installers

Todays angle -- do template installers use agents more DEEPLY once activated (not just pay)? -- has a sharp, dose-response answer among agent-messagers (prod, 90d). Non-installers (N=3,365) have a median of 3 agent messages/user (mean 7.3). Installing ONE template barely moves it: N=56, median 4, mean 11.0 -- statistically a rounding error above non-installers. The depth signal is entirely in the SECOND-and-beyond install: 2-3 installs (N=21) run median ~14-15 (mean ~45), and the 2+ group overall (N=40) averages ~62 agent messages/user = ~8.4x non-installers (mean) / ~5x on the tail-robust median. It climbs monotonically further for the handful who install many (5 installs N=4 median 61; 10 installs N=1 median 211; 31 installs N=1 median 321). The same dose-response holds on the OTHER surface, building: node_used median 3 (0 installs) -> 4 (1) -> 12+ (2+), so multi-install marks GENERAL engagement depth, not agent-chat specifically. Channel lens (todays segment): installers are 89% organic/direct (85/95), even more organic than the ~79% base -- template-installing is an engaged-organic-user behavior, not media-driven, echoing the credit-buyer channel mix. Read carefully: this MARKS serious users, it does not DRIVE depth. Reverse causation is the likely mechanism (deep/committed users explore more templates), matching the prior Jun 24 finding that template pay-lift is a fragile marker not a driver -- this extends that verdict from PAY to USAGE DEPTH, and pinpoints the marker as the 2nd install, not the 1st.

- **Metric:** 2+ template installers agent-msg depth vs non-installers (mean multiple) = **8.4**
- **Theme/angle:** Templates: intent vs. action — Template installers vs non-installers: agent-usage depth once activated (not just pay) -- dose-response by install count
- **Segment:** by template-install count (dose-response)  ·  **Sources:** mixpanel
- **Confidence:** medium (agent-messagers prod 90d; non-installer base N=3,365 solid; installer base N=95/96 with only ~40 at 2+ installs and 1-4 users in each high bucket -- individual high buckets anecdotal, but the 0/1/2+ contrast is robust and mirrored on node_used)
- **Caveat:** Correlational -- MARKS not DRIVES; reverse causation (engaged users install more templates) is at least as plausible as templates deepening usage, and heavy users simply do everything more. Base = users who sent >=1 agent_message_sent (activated), split by their template_installed count in the same 90d window -- NOT a signup cohort (so it sidesteps the ongoing Jul-3 signup-collapse unreliability), but also not time-ordered (install could precede or follow the messages). Unit is distinct_id, not company_id-deduped. High-install buckets are N=1-4 (anecdotal); the defensible contrast is 0 (N=3,365) vs 1 (N=56) vs 2+ (N=40). template_installed carries only ~180d history and installs sprawl across ~40 custom/renamed templates (per Jul 13). Internal/test accounts not separately excludable by id and could inflate the tiny high-install tail. Means are tail-dominated (a few 200-320-message users); medians (3 -> 4 -> ~14) are the robust read. Credit/subscription pay linkage not re-measured here (deferred per prior ledger).

---

### 2026-07-21 — 🆕 NEW — Builder is ~2x stickier than agent chat -- conversation activates wide but shallow, building activates narrow but deep

Once a user first builds (node_used), 43% return the next week and it plateaus ~32%% through wk6; once they first message an agent, only 24%% return wk1, decaying to ~16%% by wk6 -- a sustained ~1.8-2x stickiness gap that complicates the Jul 17 read that agent conversation is the right activation yardstick.

- **Metric:** builder wk1 self-retention 43%% vs agent 24%% (ratio 1.8x; ~2x by wk6) = **43**
- **Theme/angle:** Activation & time-to-milestone — Which activation surface retains -- builder (node_used) vs agent (agent_message_sent) week-over-week self-retention
- **Segment:** by activation surface (builder vs agent)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (weekly retention curves, prod, born May 25-Jul 1; builder $avg cohort n~61/day, agent n~97/day; gap stable across daily cohorts wk1-wk6)
- **Caveat:** Event-age confound: node_used has long pre-window history so born-in-window builder cohorts may include seasoned users re-engaging (inflating builder stickiness), whereas agent_message_sent launched ~May 18 so its births are near-true-first -- the gap DIRECTION is robust (large and stable across daily cohorts) but the MAGNITUDE may be overstated; a true first-ever-builder cohort needs DB confirmation. Self-retention (same event as birth and return); wk7-8 truncated/immature and excluded. distinct_id, NOT company-deduped. Reach differs from stickiness: per the Jul 17 cohort 65%% of signups ever message vs 13%% ever build, so in ABSOLUTE terms agent still yields ~3x more wk1-retained users (0.65*0.24=15.6%% of signups vs 0.13*0.43=5.6%%) -- building is the deeper per-user hook, conversation the wider net. Template-installer->build stickiness (today segment lens) was small-N (~130 births) and inconclusive. Marks not drives (self-selection: users who build may already be more committed).

---

### 2026-07-20 — 🆕 NEW — Signup collapse is 17 days deep and NOT signup-only -- onboarding_started also fell ~67%

The Jul 3 signup break (prior ledger: '-91% WoW, isolated to signup_completed, 6 days sustained') is now 17 days deep with NO recovery -- and it is NOT signup-only. onboarding_started, the TOP of the same funnel, also collapsed on Jul 3: prod last-7d (Jul 13-19) = 420 vs a pre-collapse 7d (Jun 26-Jul 2) of 1,264 = -67%, while signup_completed = 80 vs 542 = -85%. So there are two compounding hits: (1) ~67% fewer users ENTER onboarding, AND (2) the onboarding_started->signup_completed same-day ratio itself roughly halved, 43% (542/1,264) -> 19% (80/420). The break is broad across landing context, not one variant: home_a -72% (1,187->328), home_b -69% (1,085->340), and the untagged 'undefined' home_variant -91% (867->79). Crucially the installed base is untouched over the IDENTICAL window -- node_used ran 187-271/day (Jul 13-17), agent_message_sent 166-250/day, tester_session_started 133-193/day, all normal weekday levels -- so this is NOT a project-wide Mixpanel outage, and all-environment totals match production so it is NOT env-tag drift. It is specific to the NEW-USER acquisition/onboarding funnel. Because onboarding_started fell too (not just the final event), the earlier 'just a broken signup_completed tag' read is incomplete: this is either a real top-of-funnel acquisition outage (marketing entry / campaigns) OR a shared onboarding-flow instrumentation regression that hits both events and the final step hardest. Either way, every signup-cohort acquisition metric stays unreliable 17 days on, and today's assigned angle (does home_variant/has_template change conversion?) is unanswerable until the funnel is restored. In absolute terms the leak is ~66 signups/day below the ~77/day June baseline -- roughly 460 lost signups/week, ~1,150+ over the 17-day outage.

- **Metric:** onboarding_started last-7d vs pre-collapse baseline (prod) = **-67**
- **Theme/angle:** Acquisition & signup funnel — New-user onboarding funnel collapse -- scope & duration: onboarding_started co-collapsed (not signup-only), 17 days sustained
- **Segment:** overall  ·  **Sources:** mixpanel
- **Confidence:** high (production daily event counts, 45d; all-environment cross-check rules out env-tag drift; downstream events cross-checked healthy over the identical window; the onboarding->signup conversion ratio is a same-day aggregate, directional)
- **Caveat:** onboarding_started->signup_completed 'conversion' is a same-day daily-total ratio, NOT a true per-user funnel (a per-user funnel is itself unreliable while signup_completed under-fires), so the 43%->19% halving is directional and cannot separate a real completion drop from signup_completed being under-instrumented. Mixpanel alone cannot distinguish a real acquisition/top-of-funnel outage from a shared onboarding-flow tracking regression -- server-side signup counts / DB user-created rows are needed to close it out. 7d windows are Jul 13-19 vs Jun 26-Jul 2; Jul 20 is a partial day and is excluded. Counts are event totals, not company-deduped. home_variant 'undefined' = no variant assigned at onboarding_started. Supersedes/extends the Jul 8-9 anomaly entries which read the break as isolated to signup_completed.

---

### 2026-07-17 — 🆕 NEW — Time-to-first-conversation is a first-hour event -- 56% of ALL signups message an agent within 1h

Time-to-first-conversation is even more front-loaded than time-to-first-build. Of ALL 3,697 signups (not just activators), 56% (2,085) send their first agent message within 1 HOUR of signup, 60% within 1 day, 65% within 7 days -- and the 30d rate is also 65%, i.e. after day 7 you gain essentially nothing. Conditional on ever messaging, 87% (2,085/2,398) do it in hour one. The signup->first-conversation window is the same session; onboarding that isn't in-product/first-hour misses it entirely. (Compare the Jul 10 build finding: 66% of build-ACTIVATORS build within 1h -- here it's 56% of ALL signups messaging within 1h.) Cohort-month lens is stable: May 69%, June 61% (June marginally truncated). A thin monetization tail follows: 51 of the cohort (~1.4% of signups, ~2.1% of messagers) topped up credits within 30d, median ~2.8d after signup -- small-N, pre-settlement intent only.

- **Metric:** first-hour share of ALL signups sending an agent message = **56**
- **Theme/angle:** Cross-source anomaly & wildcard — Activation & time-to-milestone -- signup->first agent_message_sent timing distribution; does speed predict outcome
- **Segment:** by time-to-milestone (cumulative CDF)  ·  **Sources:** mixpanel
- **Confidence:** high (cohort N=3,697; cumulative funnel windows 1h/1d/7d/30d; monetization tail small-N)
- **Caveat:** Same clean cohort as companion finding (prod signups May 18-Jun 30). CDF built from cumulative funnel conversion windows (1h 56%, 1d 60%, 7d 65%, 30d 65%), not a ttc histogram. June cohort (61%) marginally truncated (signups after ~Jun 17 have <30d to today), but since ~92% of eventual messagers fire by day 1 the understatement is minor. Monetization outcome (credit_topup) is N=51, pre-checkout intent only (credits, not reconciled revenue; subscriptions/MRR are Stripe-only, deferred) -- too small to claim speed 'predicts' paying; reported as directional. distinct_id not company-deduped.

---

### 2026-07-17 — 🆕 NEW — Mobile isn't dead-on-arrival -- it activates via conversation (60%), not building (2.9%)

The team's activation KPI (node_used, the desktop drag-drop builder) tautologically writes off the mobile half of signups -- but on the RIGHT yardstick, agent conversation, mobile is alive. On a clean post-instrumentation cohort (3,697 prod signups May 18-Jun 30; agent_message_sent went live May 19, so no rollout contamination), 65% (2,398) send an agent message within 30d vs only 13% (482) who ever add a node -- a 5x gap on the IDENTICAL cohort. And messaging shows near device-parity: mobile signups activate at 60% (Android 63% 909/1,454, iOS 51% 181/353 = 1,090/1,807) vs desktop 69% (Windows 71% 1,005/1,406, Mac 63% 266/419 = 1,308/1,890) -- a ~9pt gap, NOT the ~9x gap building shows (mobile 2.9% vs desktop 27%, prior ledger). So the device barrier is specific to the builder canvas, not the product: mobile signups are 'dead-on-arrival' only if you insist on measuring them by a desktop-only feature. They converse at roughly the same rate as desktop; they just can't drag nodes.

- **Metric:** mobile signup->agent-message 30d activation = **60**
- **Theme/angle:** Cross-source anomaly & wildcard — Activation & time-to-milestone -- agent-message activation vs build activation, and the mobile device barrier
- **Segment:** by device ($os at signup)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (cohort N=3,697 signups; mobile N=1,807, desktop N=1,890; clean post-instrumentation window; funnel sequential signup->message)
- **Caveat:** Cohort = prod signups May 18-Jun 30 2026 (agent_message_sent first fired May 19, so window is clean of rollout artifacts; funnel cohorts on signup in-window then counts message within 30d on any device). Unit is distinct_id, NOT company_id-deduped. 'agent_message_sent' = 'AI Assistant Message Sent' (canonical usage event used across the ledger); it could include builder-copilot/assistant messages as well as end-user agent chat, but it is user-driven not automated (varies 51-71% by device and 35% of signups never fire it -- automation would be ~flat/~100%). node_used comparison (2.9%/27%) is from the prior ledger (cohort-by-signup-device, any-device). 'marks' the activation surface, does not by itself 'drive' retention/revenue -- retention/monetization linkage is thin here (see companion finding).

---

### 2026-07-16 — 🆕 NEW — Skills are created but not deployed -- only ~1 in 4 creators ever puts a skill on the canvas

Skills are created prolifically but almost never deployed to a workflow. In the last 90d (prod), 761 unique users across 542 companies fired skill_created, generating 2,894 skills (~3.8 per creating user) -- yet only ~1 in 4 skill-creating companies ever adds a skill to the canvas (skill_used = 'Skill Added to Canvas'): 153/542 companies = 28%, 178/761 users = 23% (unordered, 90d), and just 89/754 = 12% on a strict ordered 30-day created->deployed funnel. Creation itself is shallow and one-and-done: 57% of creators (437/761) made exactly one skill, 19% made two, and only 24% made >=3. Critically, this deployment leak is NOT the mobile-can't-build story: skill_created is already 92% desktop (Windows 437, Mac 227, Linux 81 vs only 60 mobile) and skill_used is 100% desktop, so even among desktop creators only ~25% (178/701) ever deploy. Skills look like an exploration/toy surface -- users spin them up (often AI-assisted, many at once) and abandon them before wiring one into a live agent. The create->canvas step is the real activation milestone for the skills feature, and it's leaking ~72-88%.

- **Metric:** skill create->deploy rate (company-level, added to canvas) = **28**
- **Theme/angle:** Agent & workflow usage depth — Skill lifecycle: create vs deploy (does creating a skill translate into putting one on the canvas?)
- **Segment:** by activity tier (one-and-done vs power creators)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (N=761 creating users / 542 companies, 2,894 skill_created events, prod 90d; deploy funnel N=754; device split conclusive)
- **Caveat:** 'skill_used' is the 'Skill Added to Canvas' event = deploying a skill onto a workflow, the closest available proxy for skill activation; it is not proof the deployed workflow was then published/run (that needs ClickHouse, deferred). Deploy rate spans 12% (strict ordered per-user 30d funnel) to 28% (company-level, unordered 90d) depending on unit/window/order -- all point the same way. company_id is on skill events (used for the 542/153 company counts); agent_message_sent carries NO company_id (distinct=1) so cross-linking skill deploy to agent-message depth needs the $user profile and was not done this run. skill_creation_started (256 users) badly under-fires vs skill_created (761), so the started->created step is unreliable and excluded. 'Marks' an exploration/abandonment pattern; does not by itself 'drive' churn -- retention linkage (do deployers retain better than create-only users?) is the open follow-up.

---

### 2026-07-15 — 🆕 NEW — Agent-usage retention is a home-market story — Ecuador returns 38% wk1 vs CO/MX ~16-17% and Peru ~3%

Agent-usage return (resurrection) is starkly uneven by geography, and it inverts the naive 'Ecuador is just high-volume' read. On clean post-instrumentation cohorts (agent_message_sent was newly instrumented ~May 18 — 0 unique users before, 1,123 the week of — so the May 18–24 burst is existing users getting their FIRST TRACKED message, not real onboarding; excluded), weekly unbounded return curves diverge ~13x across markets. Ecuador (home market, ~1,495 first-time agent users) returns wk1 38%, and stays durable: wk2 34%, wk3 31%, wk4 27%, wk6 24%. The expansion markets retain roughly HALF as well: Colombia (N~576) wk1 16% / wk3 15%, Mexico (N~395) wk1 17% / wk3 14%. And Peru — the #4 market by agent volume (N~463) — is a near-total retention dead zone: wk1 ~3%, and flat ~3-4% thereafter, i.e. users fire the agent once and essentially never come back. (US wk1 22% but N~155/small, noisy.) So Ecuador is not merely 50% of volume (Jul 7 finding) — per user it is also ~2.3x stickier than the next markets, while Peru converts real volume into ~zero retention. The 'invert' lens lands on Peru: the market that most conspicuously does NOT come back.

- **Metric:** wk1 agent-usage return rate, home market Ecuador (clean cohort) = **38**
- **Theme/angle:** Retention & churn cohorts — Resurrection/return by geography — who comes back and who never does (agent usage)
- **Segment:** by geography (mp_country_code)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (return curves on clean mature cohorts; N solid for EC/CO/MX/PE; distinct_id not company-deduped; US small-N)
- **Caveat:** Mixpanel unbounded weekly retention on agent_message_sent (canonical usage), prod, cohort window May 25–Jul 1 2026 (mature, ≥2 wk). Cohort unit is distinct_id (a user/company proxy), NOT company_id-deduped — country-level rates could be swung by a few large accounts (esp. Peru's near-zero, which may be one/few churned cos, and Ecuador's high rate if a big active co dominates). agent_message_sent only instrumented ~May 18 so pre-May-25 cohorts are rollout artifacts (the contaminated full-range Ecuador avg reads a misleading 8% because a May 20 spike of 650 first-tracked users returned at 4%); clean-window figures used throughout. mp_country_code is geo-IP at event time, not billing country. 'Resurrection' here = unbounded weekly RETURN (includes users who skip weeks then come back); the specific trigger EVENT of a comeback (backlog Q) is not yet isolated — Mixpanel MCP exposes no JQL groupByUser, only report types. US small-N. 'marks' not 'drives'.

---

### 2026-07-14 — 🆕 NEW — Credit top-ups are small, organic-led, and don't stick — 79% organic, $10 median, agent-use decays 46%->14%->6%

Characterizing the one monetization path with real history (credit_topup, 120 unique users May 13–Jul 14, prod). Amounts are small: median $10, mean $15.2, p90 $20, ~$3,360 total intent-to-pay over 2.5 months (pre-checkout, credits only — not reconciled revenue). By acquisition channel, credit-buying is NOT a media story: 79% of buyers (95/120) are organic/direct (no initial_utm_source), ~21% media (Google Ads 13, Meta fb/ig 5, other 7) — i.e. it mirrors the ~21% media share of the signup base, so paid channels buy proportionally, not disproportionately. And top-ups don't mark stickiness: on a weekly born->return curve (credit_topup -> agent_message_sent), 46% send an agent message the same week, but only 14% the next week and 6% two weeks out. Buying credits marks a moment of intent, it doesn't mark a retained user.

- **Metric:** credit-topper wk1 agent-activity retention = **14%**
- **Theme/angle:** Monetization & pay-drivers — Credit top-up size, channel mix, and post-topup engagement retention
- **Segment:** by acquisition channel (initial_utm_source)  ·  **Sources:** mixpanel
- **Confidence:** medium-high (N=120 buyers for amount/channel; retention $average across cohorts, mature May cohorts anchor the wk0-2 decay; small-N per channel)
- **Caveat:** credit_topup fires pre-checkout so amount is intent-to-pay, not settled revenue, and credits only (subscriptions excluded). Retention proxied by agent_message_sent (canonical usage event) — if credits are spent on non-agent surfaces this understates stickiness. Channel split uses initial_utm_source on the $user profile (undefined=organic/direct). wk0/1/2 are cohort-weighted averages; recent (Jul) cohorts have immature windows. 'marks' not 'drives'.

---

### 2026-07-14 — 🆕 NEW — "Which path retains better" is unanswerable in Mixpanel yet — subscription_changed only went live ~Jun 24

Today's angle (credit_topup vs subscription_changed: which retains better) can't be answered from Mixpanel yet, and the reason is a rigor trap. A naive lifetime pull looks like credit top-ups crush subscriptions ~9:1 (120 vs 14 unique users, prod), but subscription_changed fired ZERO before the week of Jun 22 and only started in earnest ~Jun 24 2026 (weekly: 0…0,8,6,1,1) — it's a brand-new event. Credit_topup has ~9 weeks of history (since ~May 13); subscription_changed has ~3. On a fair, co-existing window (Jun 24–Jul 14) it's 24 credit-toppers vs 14 subscribers = ~1.7:1, not 9:1. Because all 14 subscription_changed users are <3 weeks old, their retention curves are immature (wk0 35%, wk1 18%, then no mature data), so a credit-vs-subscription retention comparison is not yet possible here. Reconciled subscription retention/MRR stays a Stripe question (deferred).

- **Metric:** credit_topup:subscription_changed user ratio (fair window Jun24-Jul14) = **1.7x (24 vs 14)**
- **Theme/angle:** Monetization & pay-drivers — Credit purchase vs subscription conversion: which path retains better (event-availability)
- **Segment:** overall  ·  **Sources:** mixpanel
- **Confidence:** high (event first-fire dates + fair-window uniques, prod); the ratio itself is small-N
- **Caveat:** subscription_changed went live ~Jun 22-24 2026 (0 firings before), so any lifetime credit-vs-sub comparison is an instrumentation artifact — use the Jun24+ window only. Both are low-volume (24 and 14 users over 3 weeks); ratios are directional, not stable. Subscription retention is unmeasurable in Mixpanel until cohorts mature; true subscription conversion/MRR is Stripe-only (deferred). Uniques are distinct_id, a company proxy, not company_id-deduped.

---

### 2026-07-13 — 🆕 NEW — Template gallery leaks 82% at preview->install; two scheduling templates convert 0%

The template gallery has a real intent-vs-action leak: of 147 unique users who opened a template preview (prod, last 180d, 30d conversion window), only 27 went on to install any template = 18% overall. That is 120 companies who signalled template intent and installed nothing. At the per-template level, preview->install conversion ranges from 0% to 36%: Identity Verification 36% (5/14), Jelou Shop in-chat payment 26% (7/27), Shopify native checkout 24% (9/37) and Bitrix Lead Capture 20% (1/5) convert best, while WooCommerce 11% (2/18) and Schedule w/ Google Calendar 12% (4/32) lag. Two gallery templates are outright dead ends: "Appointment scheduling" (0/13) and "Schedule with Microsoft Outlook Calendar" (0/6) drew 19 previewers between them and converted ZERO. Crucially "Schedule with Google Calendar" DOES convert (12%), so scheduling is not dead as a category -- the Outlook and generic-appointment templates specifically are. The install side also reveals a gallery/catalog mismatch: previews fire on ~8 curated English-named templates, but installs sprawl across ~40 mostly custom/Spanish names (Agente Shopify 39, Tienda Jelou Shop 14), i.e. most installs come from outside the previewable gallery.

- **Metric:** template preview->install conversion (unique users, 180d) = **18**
- **Theme/angle:** Templates: intent vs. action — Template gallery preview->install conversion, per template
- **Segment:** by template previewed  ·  **Sources:** mixpanel
- **Confidence:** medium (per-user funnel, prod, 180d; overall N=147 previewers solid; per-template small-N directional)
- **Caveat:** Counts are unique users (distinct_id), a close proxy for companies but not company_id-deduped; sizing in true companies would refine the 120. Small-N per template (previewers 5-37): the two dead-ends are 13 and 6 previewers -- individually marginal, but combined 0/19 vs an 18% base rate is unlikely by chance (~2%). Step 2 is template_installed (ANY template) within 30d, so a 0% cell means those previewers installed nothing at all, not that they installed a renamed equivalent. template_installed/template_preview_opened only carry ~180d of history (163 installs total). Downstream node_used activation per template is too thin to split. This is preview->install (intent->action), not preview->build; "marks" not "drives".

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


# Daily insights routine — CLOUD playbook (Mixpanel-only)

You are the daily insights agent for the Jelou Brain Studio retention
investigation, running as a **scheduled cloud session**. You have this git repo
checked out and the **Mixpanel MCP connector**. You do NOT have `.env`, database
credentials, or access to ClickHouse / Neon / Stripe. **All data comes from
Mixpanel via the MCP tools.** Revenue and conversation-level angles are deferred
until DB secrets are wired — say so when a theme needs them.

Your job each run: surface one or a few **genuinely new** Mixpanel findings about
acquisition, activation, in-app usage, or template/engagement behavior — then log
them to the ledger, commit, and write the digest.

## Steps

1. **Get today's assignment** (no secrets needed):
   ```
   python -m insights.rotation
   ```
   Then read `insights/INSIGHTS_LOG.md` — the "already known" list. Do **not**
   re-report a known number unless it moved materially.

2. **Map the assignment to what Mixpanel can answer.** Prefer the day's angle; if
   it needs a backend you can't reach, pivot to the Mixpanel-answerable facet and
   note what's deferred.
   - **Strong in Mixpanel:** acquisition funnel, activation timing, usage depth,
     template *events*, device/channel splits, engagement recency.
   - **Weak/deferred (needs DBs):** real revenue (Stripe), assistant conversation
     content & cost (Neon), workflow execution internals (ClickHouse). For a
     monetization day, use *intent* proxies only (`upgrade_cta_clicked`,
     `credit_topup`, `page_visited_settings_billing`) and label them as intent,
     not revenue.

3. **Query Mixpanel via MCP.** First call **Get-Business-Context**, then
   Run-Query / segmentation / JQL as needed. Project: **Jelou Apps `3842718`**.
   Non-negotiable gotchas:
   - Filter **`environment == "production"`** (dev/staging inflate counts).
   - **Uniques are NOT additive** — a union of users across events needs JQL
     `groupByUser`, never summed per-event uniques.
   - Segment via the **`$user` profile**: `company_id`, `self_service_cohort`,
     `initial_utm_source/_medium`, device (`$os`/`$browser`).
   - Prefer **high-query-volume** events (what the team steers by):
     `signup_completed`, `template_installed`, `node_used`, `skill_created`,
     `tester_session_started`, `agent_message_sent`, `campaign_sent`.
   - A second project exists (**Jelou AI Website `3842156`**, marketing) — signup
     funnels can straddle both; don't build a clean sequential funnel across
     projects without reconciling `distinct_id`.
   - Report Ns and base rates; flag small-N; correlation is "marks," not "drives."

4. **Decide what's new** and log survivors:
   ```python
   from insights.ledger import classify, normalize_key, append_insight
   key = normalize_key(theme, metric, segment)
   status, prior = classify(key, value)          # 'new' | 'update' | 'stale'
   if status != "stale":
       append_insight({"title": ..., "one_liner": ..., "theme": ..., "angle": ...,
                       "segment": ..., "metric": ..., "value": ..., "sources": ["mixpanel"],
                       "confidence": "...", "caveat": "..."})
   ```
   **Never write customer PII** (emails, names) into the ledger — aggregates only.
   If nothing survives, log a one-line "explored, dry" note and continue.

5. **Grow the backlog** — append fresh questions to `insights/questions.md`
   (strike answered ones with `- ~~...~~`).

6. **Deliver + persist.** Write the digest file and commit everything back so the
   ledger survives to the next run:
   ```
   python -m insights.digest    # writes data/digests/<date>-insights.md (file mode)
   git add insights/INSIGHTS_LOG.md insights/insights.jsonl insights/questions.md
   git commit -m "insights: <date> — <short headline>"
   git push
   ```
   Then **print the digest in your final message** so it's visible in the session
   (email delivery is deferred until SMTP creds are available cloud-side).

## Quality bar
One verified, surprising finding beats five obvious ones. Numbers with
denominators. Exclude test/internal accounts where identifiable. Be honest when
the angle is dry or when a theme is blocked on deferred backends.

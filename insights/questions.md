# Open question backlog

The daily routine pulls a few of these each run (rotated) and appends new ones as
findings raise fresh questions. Answered questions get struck through (`- ~~...~~`)
so they drop out of rotation but stay as a record.

Format: one question per `- ` bullet. Keep them specific and data-answerable.

## Acquisition
- Which acquisition channel (initial_utm_source) has the best signup→activation→pay full-funnel yield, not just signup volume?
- Is the mobile-vs-desktop activation gap widening or narrowing across recent signup cohorts?
- Do signups that arrive with `has_template=true` at onboarding_started convert better than blank-start signups?
- What share of `onboarding_started` never reach `signup_completed`, and where do they die?

## Activation
- What is the median time from signup_completed to first agent_message_sent, and how does it differ for eventual payers?
- Which single activation milestone most strongly predicts week-2 return?
- How large is the dead-on-arrival cohort (signed up, zero activation events), and which channel produces it most?

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
- What share of all workflow executions come from the top 1% / 10% of companies?
- Do companies with high workflow error_rate_pct churn faster than clean-running ones?
- Does building SKILL-type nodes (vs only tools) mark a stickier user?

## Cross-source / wildcard
- Which company has the highest assistant build cost (Neon) relative to realized executions (ClickHouse)?
- Is there an acquisition channel that is cheap to sign up but never pays (a low-quality source)?

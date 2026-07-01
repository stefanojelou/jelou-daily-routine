# Jelou retention — daily insights routine

Self-contained framework for a scheduled agent that hunts for **new** retention
insights (template usage, agent usage, pay-drivers, time-to-action) and never
re-runs the same analysis twice.

This repo is a **PII-free slice** of a larger local analysis workspace — only the
routine framework lives here. No customer data, no credentials.

## Layout (`insights/`)
- `rotation.py` — the creativity engine: weekday **theme** × weekly **angle** ×
  daily **segment** × random **twist** + a living question backlog. Deterministic
  per date, so every day explores a different cut. `python -m insights.rotation`
- `ledger.py` + `INSIGHTS_LOG.md` + `insights.jsonl` — novelty guard. Classifies
  each candidate as new / update / stale so known numbers aren't repeated unless
  they move >15%.
- `questions.md` — open-question backlog the routine pulls from and grows.
- `digest.py` — delivery (Slack webhook → email → file).
- `connections.py` — read-only connectors for ClickHouse / Neon / Stripe /
  Mixpanel (used by the **local** runner; the cloud runner uses the Mixpanel MCP).
- `CLOUD_ROUTINE.md` — playbook for the scheduled **cloud** agent (Mixpanel-only).
- `DAILY_ROUTINE.md` — playbook for a **local** runner with full DB access.
- `run_daily.py` — assembles the daily brief (assignment + known-insights + check).

## Cloud run (what the routine does)
Reads today's assignment → queries Mixpanel via MCP → keeps only genuinely new
findings → logs them → commits the ledger back here → prints the digest.

Deps: `pip install -r requirements-insights.txt`

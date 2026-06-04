---
name: harbor-add-service
description: Add a background worker or scheduled (cron) job to an existing app via Harbor. Use when the user says "add a worker", "add a background job", "process X in the background", "run this every night", or "add a cron".
---

# Add a service (Harbor)

1. Run `harbor add-service --app=<name> --type=<worker|cron> [--kind=celery|sidekiq|celery-beat] [--schedule="0 6 * * *"]` (no `--approve`) — shows the cost + plan card.
2. Pick the worker flavor from the app's backend (Django → celery, Rails → sidekiq) unless told otherwise.
3. On approval, re-run with `--approve`, then tell the user to run `harbor deploy` to apply it.

Guardrails: mutating — needs an explicit yes before `--approve`.

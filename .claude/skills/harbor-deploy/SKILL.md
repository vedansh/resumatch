---
name: harbor-deploy
description: Deploy or ship an app to staging or production via Harbor. Use when the user says "deploy", "ship it", "push to prod", "deploy to staging", "release", "promote to prod", or "go live".
---

# Deploy (Harbor)

1. Run `harbor deploy --app=<name> --env=<staging|prod>` (no `--approve`) — this prints the plan + approval card (host, branch, rollback). Relay it in plain language.
2. **Default to `staging`** unless the user clearly means prod. Prod is high-risk — confirm explicitly.
3. When the user approves, re-run with `--approve`. It does git pull → `docker compose` build+up → health check → **auto-rollback on failure**.
4. If it fails, tell them it rolled back, and offer `harbor rollback` if needed.

Guardrails: mutating — never add `--approve` without an explicit yes; prod needs extra confirmation.

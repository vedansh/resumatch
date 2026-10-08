---
name: harbor-build-app
description: Scaffold and register a new app on AWS via Harbor — backend (FastAPI/Django/Rails), optional frontend (Next.js / React Native), database, and domain. Use when the user says "build my app", "deploy a new app", "set up a Django backend with a worker and Postgres", "ship my project", or is answering "what are you building?".
---

# Build app (Harbor)

When the user wants to create/deploy a new app:

1. Gather the "what are you building?" essentials if not given: **mobile or web**, **backend** (recommend FastAPI or Django), **database** option (new-on-shared / existing-schema / dedicated), and an optional **domain**.
2. Run `harbor build-app --name=<name> --kind=<web|mobile> --backend=<fastapi|django|rails> --db=<shared-instance|existing-schema|dedicated> [--domain=<domain>]` **without** `--approve`. This prints the **approval card** (cost + risk + undo). Relay it to the user in plain language.
3. When the user approves, re-run the exact same command **with `--approve`**.
4. Tell them what was scaffolded and that `harbor view` shows the new app.

Guardrails:
- build-app is a **mutating** command — always show the card and get an explicit yes before adding `--approve`.
- Recommend the cheapest sensible options (shared host + new-on-shared DB) unless the user needs isolation.

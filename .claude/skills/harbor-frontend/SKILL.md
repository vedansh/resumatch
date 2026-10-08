---
name: harbor-frontend
description: Add an AWS Amplify Hosting frontend to an app (auto-deploy on push to main/develop). Picks framework (Next.js / Astro / Vite / Remix / SvelteKit / Nuxt) and connects to the GitHub repo. Use when the user says "add a frontend", "host my web app on Amplify", "deploy the web", "set up the frontend".
---

# Frontend (Amplify)

When the user wants a web frontend (the backend is handled by `harbor init`):

1. Confirm you're in the app's git repo (origin must be GitHub).
2. Run `harbor frontend --app=<app> --framework=<nextjs|astro|vite-react|remix|sveltekit|nuxt> [--domain=<domain>]` (no `--approve`) → card. Relay it.
3. On approval, re-run with `--approve`. It creates the Amplify app, main + develop branches, optionally a domain association.
4. Tell the user: prod URL = `https://main.<defaultDomain>`, staging URL = `https://develop.<defaultDomain>`; push to either to trigger an auto-build.

Guardrails: needs `gh auth token` with `repo` + `admin:repo_hook` scopes. If missing, tell the user to run `gh auth refresh -s repo,admin:repo_hook`.

---
name: harbor-init
description: Onboard an app onto a Harbor cluster — drops Dockerfile + compose + GitHub Actions workflow + harbor.yaml into the repo, creates DB schema+user, deploys initially, sets GitHub secrets so future pushes auto-deploy. Use when the user says "init this app", "onboard this app", "set up Harbor for this repo", "deploy this to Harbor", or "get this app on Harbor".
---

# Initialize an app on Harbor

When the user wants to onboard the current repo:

1. Confirm you're in a git repo with a GitHub `origin`. The host needs to clone from there.
2. Run `harbor init --name=<app> --backend=<fastapi|django|rails>` (no `--approve`) → prints the card (port, db, host, deploy plan). Relay it.
3. On approval, re-run with `--approve`. Harbor: scaffolds the template into the repo, creates the DB schema+user, SSH-deploys the initial container, sets GitHub secrets (`PROD_HOST`, `DEPLOY_USER`, `DEPLOY_SSH_KEY`).
4. Tell the user to: `git add . && git commit -m 'harbor init' && git push`. Future pushes auto-deploy via the dropped GitHub Actions workflow — Harbor isn't needed after that.

Guardrails: gated. Needs a Harbor cluster (`harbor bootstrap` if none). For private repos, the host needs to be able to clone (public repo works out of the box; private needs a deploy key — guide the user if so).

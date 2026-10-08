---
name: harbor-discover
description: Connect an existing AWS account to Harbor — scan it and infer the apps already running on it. Use when the user says "I already have apps on AWS", "import my existing setup", "what's already deployed?", "connect my existing account", or "find my apps".
---

# Discover existing apps (Harbor)

When the user already runs things on AWS and wants Harbor to understand them:

1. Run `harbor discover` to record their servers (read-only AWS scan).
2. To infer the apps too, Harbor must look *inside* the hosts over SSH. Ask for the key:
   `harbor discover --key=~/.ssh/<their-key>.pem --user=ubuntu`
   (This runs read-only `docker ps` + reads nginx vhosts — it never changes anything.)
3. Relay the proposed servers + apps in plain language. The app topology is a **guess** from container names.
4. When the user confirms it looks right, re-run with `--approve` to record the apps in Harbor.
5. Suggest `harbor doctor <app>` on each to spot gaps (no staging, missing worker, etc.).

Guardrails:
- Read-only: discover never mutates AWS. Only `--approve` writes (to local Harbor state, not AWS).
- Be clear that inferred apps are guesses until confirmed.

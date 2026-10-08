---
name: harbor-bootstrap
description: Provision a fresh Harbor cluster (EC2 + EIP + RDS Postgres + S3 + budget) in the user's AWS account. Idempotent and Harbor-tagged so it's safe alongside existing infra. Use when the user says "bootstrap", "set up a cluster", "provision Harbor", "set up the test infra", or "start a new Harbor environment".
---

# Bootstrap a Harbor cluster

When the user wants a fresh cluster (typically for testing or first-time setup):

1. Run `harbor bootstrap --name=<name> --region=<region>` (no `--approve`) → prints the approval card (cost ~$15–20/mo, what it'll create). Relay it.
2. On approval, re-run with `--approve`. It provisions an EC2 + Elastic IP + RDS Postgres + S3 bucket + budget cap, all tagged `harbor:cluster=<name>` (safe alongside existing infra). RDS takes ~5–10 minutes.
3. Tell the user: SSH key saved at `~/.ssh/harbor-<name>-key.pem`; next step is `cd` into an app repo and run `harbor init`.

Guardrails: real AWS resources cost real money; the card states the estimate. Never run with `--approve` without an explicit yes.

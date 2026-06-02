---
name: harbor-teardown
description: Destroy a Harbor cluster — all its EC2/EIP/RDS/S3/SGs/key pair/SSM/budget. Idempotent. Local SSH key file stays. Use when the user says "tear down", "destroy the cluster", "shut it down", "clean up", or "delete the test cluster".
---

# Teardown (destructive)

When the user wants to destroy a cluster:

1. Run `harbor teardown --cluster=<name>` (no `--approve`) → prints the RED approval card (destructive, RDS deleted without final snapshot, S3 wiped).
2. **Confirm explicitly** with the user — this is irreversible. Read the card back to them; only proceed if they clearly say yes.
3. On approval, re-run with `--approve`. RDS deletion takes ~5 minutes.
4. After: tell them the bill is stopped; their local `~/.ssh/harbor-*-key.pem` is kept in case they want a record.

Guardrails: 🔴 destructive. Only resources tagged `harbor:cluster=<name>` are affected — other AWS resources are untouched.

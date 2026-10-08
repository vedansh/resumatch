---
name: harbor-connect-aws
description: Connect a user's AWS account to Harbor — and help them create an AWS account if they don't have one yet. Use when the user says things like "connect my AWS", "link my AWS account", "set up Harbor", "I don't have AWS yet", or "get started with Harbor".
---

# Connect AWS (Harbor)

When the user wants to connect AWS to Harbor:

1. Run `harbor connect`.
2. If it reports **not connected**, the command prints signup + `aws configure` steps. Relay them in plain language, wait for the user to finish, then run `harbor connect` again.
3. On success, tell them the account ID and suggest **`harbor inventory`** to see what's already running.

Guardrails:
- Never paste the user's AWS keys into chat — they run `aws configure` themselves.
- Creating an AWS account is a manual web step — guide, don't automate.
- Harbor will set a budget cap after connecting (a gated action) — confirm with the user before creating it.

---
name: harbor-inventory
description: Show what is running in the user's AWS account, with managed/unmanaged tags (and cost, once wired). Use when the user says things like "what's in my AWS", "show me everything running", "what am I paying for", or "list my AWS resources".
---

# Inventory (Harbor)

When the user asks what's in their AWS account:

1. Run `harbor inventory` (add `--json` if you need to reason over the data).
2. Summarize in plain language: counts by type, and which are **managed by Harbor** vs **pre-existing/unmanaged**.
3. Reassure them: Harbor never modifies unmanaged resources — it only ever touches what it created.

This is read-only and safe — no approval needed.

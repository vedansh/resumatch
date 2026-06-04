---
name: harbor-install-skills
description: Install Harbor's Claude Code skills into the user's Claude config so natural-language asks auto-trigger them in any repo. Use when the user says "install harbor skills", "set up Claude for Harbor", or after `npm i -g harbor-cli`.
---

# Install skills

Run `harbor install-skills` (default: user-wide at `~/.claude/skills/`) or with `--project` (drops into the current repo's `.claude/skills/`). Idempotent — re-running just overwrites.

After this, Claude Code in any repo recognizes Harbor's verbs from natural language ("bootstrap a cluster", "init this app", "discover my AWS", etc.).

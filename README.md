# Aegis Boundary Skill

> Verify what AI agents are allowed to see, do, and output.

`aegis-boundary` is a free, official Aegis skill for AI coding agents. It
performs an **advisory review** of agent work around Aegis surfaces — code
changes, documents, public claims, and agent task plans — and returns
**READY / REVIEW / STOPPED** with machine-check evidence.

It is a review layer, not an enforcer: it does **not** authorize production
access, enforce policy, or produce receipts. Runtime enforcement belongs to
the [aegis-trust SDK](https://aegisagentcontrol.com) (LITE, in-process
hygiene) and Aegis Core (FULL, gateway enforcement with key separation).

## What it checks

- **Boundary**: does the work keep the SDK / Gateway / Core responsibility
  split intact (cooperative hygiene vs. non-cooperative enforcement)?
- **Claims**: do README / site / sales statements stay within what is
  implemented? LITE/FULL claim separation, never-claims, certification
  wording, and three machine-checked overclaim families.
- **Agent plans**: is what the agent is about to see, do, and output within
  declared purpose and scope — without treating a purpose label as
  authorization?

Output shape:

```
Decision: READY | REVIEW | STOPPED
Machine checks: overclaim_scan PASS|FAIL
Why / Allowed (advisory) / Blocked (advisory) / Required checks / Next
```

## Requirements

The overclaim scan (`scripts/check_overclaims.py`) needs **Python 3.7+**. The
skill instructions themselves are plain markdown and need no runtime.

## Install

**Claude Code** (plugin marketplace):

```
/plugin marketplace add Incierge3789/aegis-boundary
/plugin install aegis-boundary@aegis-skills
```

**Codex** (agent skills):

```bash
mkdir -p ~/.agents/skills
cp -R skills/aegis-boundary ~/.agents/skills/
```

(or `./install.sh codex`)

**Gemini CLI** (extension):

```bash
gemini extensions install https://github.com/Incierge3789/aegis-boundary
```

**Cursor** (plugin): this repository follows the Cursor plugin layout
(`.cursor-plugin/plugin.json` + `skills/`); marketplace listing pending.

## Layout

```
skills/aegis-boundary/
├── SKILL.md                      # the skill (trigger spec + review procedure)
├── references/boundary_canon.md  # vendored boundary canon (parity-tracked)
├── references/pitfalls.md        # defaults a model gets wrong
├── templates/boundary_review.md  # READY/REVIEW/STOPPED output template
└── scripts/check_overclaims.py   # machine check (3 overclaim families)
```

## Honesty contract

This skill applies the same rules to itself that it reviews for: it is
described as advisory everywhere, its bundled canon is parity-tracked against
the internal canonical document (`docs/PARITY.md`), and its own files pass its
own machine checks.

## License

MIT — see `LICENSE`. Copyright (c) 2026 Aegis Project (Incierge).

The MIT license covers the code and text of this repository. It does not
grant rights to the "Aegis" name or logos, or the right to represent forks as
official Aegis distributions. The official distribution of this skill is
`github.com/Incierge3789/aegis-boundary`.

---
name: aegis-boundary
description: |
  Aegis Boundary Skill — review whether AI-agent work stays within Aegis product
  boundaries in what it sees, does, outputs, and claims.
  ADVISORY review only: it does not authorize, enforce, or produce receipts —
  runtime enforcement belongs to the aegis-trust SDK (LITE) and Aegis Core (FULL).
  Reviews whether an agent task, code change, document, or public claim preserves
  Aegis boundaries (SDK/Core responsibility split, LITE/FULL claim separation,
  honesty guardrails, never-claims, naming) and returns READY / REVIEW / STOPPED
  with machine-check evidence.
  Use when: working with aegis-trust or Aegis Core integrations; editing README,
  website, sales, or customer-facing claims about Aegis; changing what an AI agent
  is allowed to see, do, or output through Aegis; before publishing any artifact
  that makes claims about Aegis; or when asked "boundary review", "claim check",
  "境界確認", "claim parity", "can we say this publicly?".
  NOT for: production authorization decisions (SDK/Core runtime territory),
  projects unrelated to Aegis.
allowed-tools:
  - Bash
  - Read
  - Grep
---

# aegis-boundary — Aegis Boundary Skill

> Advisory review: does this work stay within Aegis product boundaries — in
> what it sees, does, outputs, and claims?

## What this skill is NOT (read first, non-negotiable)

This skill does **not** replace the aegis-trust SDK or Aegis Core.

- It does **not** make authorization decisions for production systems.
  Runtime enforcement belongs to the SDK (LITE, cooperative hygiene) and to
  Aegis Core (FULL, non-cooperative enforcement with key separation).
- It does **not** produce receipts, tamper-evident audit, or `decision_id`s.
  Its output is **advisory review**, labeled `source: aegis-boundary-skill` —
  never `source: CORE` (that label is reserved for gateway-constructed
  decisions).
- Product, roadmap, pricing, and publication decisions require human approval.
  This skill can only return REVIEW / STOPPED and route there.

## Review procedure

### Step 1 — classify the surface under review

Pick every class that applies:

- **A. code change** touching an Aegis integration (SDK usage, policy files,
  MCP proxy wiring, gateway clients)
- **B. document / claim change** (README, docs, site, sales, pitch, customer
  answer) that says what Aegis does
- **C. release / publish preparation** of an artifact that makes claims about
  Aegis
- **D. agent task plan** — an agent is about to read data / run tools / emit
  output through Aegis surfaces

### Step 2 — machine checks (decision-capping)

Resolve the script against this skill's own directory (it does not depend on
the current working directory):

```bash
python3 "<skill-dir>/scripts/check_overclaims.py" <changed .md files...>
# In a Claude Code plugin this is "${CLAUDE_PLUGIN_ROOT}/skills/aegis-boundary/scripts/check_overclaims.py";
# when run from the skill directory itself, "scripts/check_overclaims.py" also works.
```

Scans for the three known overclaim families defined in
`references/boundary_canon.md` §5-A (C-1, C-2, C-3). **Exit codes cap this
review's decision: any FAIL means
the final decision can never be READY.** They cap nothing at runtime. Do not
reinterpret, soften, or override a machine FAIL with narrative judgment.

Known limitation: the patterns match English phrasings only. For non-English
claims, apply Step 3 review against the reframes in
`references/boundary_canon.md` — a lint PASS on non-English text is evidence
of nothing.

### Step 3 — boundary review against the bundled canon

Read `references/boundary_canon.md` (vendored, parity-tracked — see
`docs/PARITY.md` in the repository) and check, for the classes from Step 1:

| Class | Check |
|---|---|
| A, B | Names used correctly (aegis-trust = SDK; Aegis Core = gateway + crypto core; the package name `aegis-sdk` is reserved and never used) |
| A, B | Responsibility split — SDK is cooperative hygiene; only Gateway+Core enforce against a non-cooperating agent. Never describe the former as the latter |
| B | LITE/FULL claim separation (inviolable table in the canon) — "Enforced by Aegis Core", "tamper-evident", "policy authorized" are FULL-only vocabulary |
| B | Claim discipline — classify every capability statement as implemented / customer-side / gap+roadmap / never-claim before writing it |
| A, B, C, D | Known pitfalls — `references/pitfalls.md` |
| D | What may the agent see / do / output: a declared purpose is a label, not authorization; fail-closed beats silent degrade |

### Step 4 — decide and emit

Fill `templates/boundary_review.md`. Decision rules:

- **STOPPED** — any machine check FAIL; or the change introduces a never-claim;
  or it attributes FULL-only vocabulary to LITE; or it requires a
  product/roadmap/pricing/publication decision (route to a human).
- **REVIEW** — responsibility boundaries blur but intent seems legitimate; a
  conditional claim lacks its mandatory qualification; naming is off-canon;
  implemented-vs-roadmap status is uncertain; or evidence is missing.
- **READY** — machine checks pass AND no canon conflict found. Say so briefly.

## Output discipline

- Quiet when clean: READY output is a few lines. Spend words only on REVIEW /
  STOPPED (what was caught, why, what is allowed instead, how to proceed).
- Every Blocked item cites its canon section or pitfall number. No uncited
  blocks.
- Never assert time-dependent facts (versions, counts, customers, prices) from
  this skill's text — point at the live source.

## Adaptation

The rules above are fixed; everything else adapts. If the situation is not
covered, do not guess a rule: return REVIEW, state what could not be checked,
and name what the canon would need to cover. If a bundled reference file is
missing, that is a STOPPED finding, not a license to improvise.

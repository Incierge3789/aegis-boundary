# Aegis boundary canon (vendored extract)

Derived from the Aegis Integration Boundary canonical document (internal,
maintained in the Aegis Core repository). This file is a parity-tracked
derivative: on any conflict, the canonical document wins. See `docs/PARITY.md`
in this repository for the source anchor and re-derivation rule.

## 1. What Aegis is (approved 30-second statement)

"Aegis is an enforcement layer that sits between AI agents and their data,
tools, and LLMs. One policy schema and one audit-event schema, enforced at
three strengths — in-process SDK, MCP proxy, and gateway. At every strength it
controls which fields are disclosed for which declared purpose, and records
the evidence."

Aegis does not replace the agent implementation, the LLM provider, or the data
store. It inserts as an enforcement point (PEP) on the path between them:

| Form | Strength | What it is |
|---|---|---|
| aegis-trust SDK (in-process) | LITE | Cooperative field filtering by purpose × scope |
| aegis-mcp-proxy (process boundary) | LITE contract | Minimizes MCP tool/resource results; unknown tools are blocked fail-closed |
| Gateway + crypto core ("Aegis Core") | FULL | Separate trust boundary: authentication, RBAC, mandatory purpose declaration, encrypted capsules with host binding, chain-hashed audit |

## 2. Responsibility split (one line)

**The SDK and MCP proxy correctly constrain a cooperating agent. Gateway +
Core enforce against a non-cooperating one.** Describing the former with the
latter's vocabulary is a claim/implementation mismatch — the inviolable rule
below exists to prevent exactly that.

## 3. LITE / FULL claim separation (inviolable)

This table applies to UI text, speech, slides, proposals, README files, and
any other surface:

| Statement | LITE | FULL |
|---|---|---|
| outcome / allowed / withheld / reason shown | OK | OK |
| "Filtered locally by aegis-trust LITE. No gateway required." | OK (this is the ceiling for LITE) | — |
| "Enforced by Aegis Core" | never | OK |
| "Evidence verified" / "Tamper-evident audit recorded" | never | OK |
| "Policy authorized" / "Cryptographically protected" | never | OK |
| `decision_id` / evidence link shown | never (null) | OK |

It is honest — and encouraged — to explain this separation itself to
customers: LITE is hygiene for cooperating agents and the on-ramp; the same
policy schema carries over when upgrading to FULL.

## 4. Claim discipline (apply before writing any capability statement)

Classify every statement as exactly one of:

1. **implemented** — say "implements", with the live source to verify
2. **customer-side** — the deployer's responsibility (key management policy,
   policy content, lawful-basis decisions, provider selection); say so
3. **gap + roadmap** — say "gap-analyzed, on documented roadmap"; never
   present as current capability
4. **never-claim** — see below; do not say it in any form

Separate substrate from outcome in the same sentence: "the mechanism can X"
is different from "customers have proven X in production".

## 5. Never-claims

**A. Honesty guardrail families (machine-checked by `check_overclaims.py`):**

| ID | Forbidden family | Honest reframe |
|---|---|---|
| C-1 | forbidden: "absolutely will not leak / never leaks" | "Controls where, to whom, for what purpose, and to what scope plaintext reappears — and records the evidence when it does" |
| C-2 | forbidden: "automatically makes all RAG data safe" | "Controls disclosure of documents, chunks, retrieved context, and outputs per user / device / purpose, with an audit trail" |
| C-3 | forbidden: "can delete prompts already sent to the LLM provider" | Decompose "delete" (decryption revocation / reuse stop / retention control / cache deletion / audit evidence), then scope it: "invalidation within what Aegis mediated" |

**B. Certifications:** never write "compliant with", "audited", or "certified"
for SOC 2 / ISO 27001 / CMMC / FedRAMP / FIPS / HIPAA while uncertified. The
implemented thing is evidence endpoints — "designed to produce evidence for
..." with the qualification in the same sentence: "regulatory conformance
itself is an assessment made together with the customer's own operations."

**C. Boundary crossings:** never attribute enforcement / tamper-evidence /
encryption to LITE; never claim hosted or managed FULL is currently offered
(sellable FULL is customer self-host); never present roadmap items as current
capability; no universal claims of the form "secures all agents and all data
automatically".

## 6. Frequent misreadings (correct answers)

| Misreading | Correction |
|---|---|
| "With Aegis, leaks become impossible" | Not claimable. Aegis controls and evidences where plaintext reappears (C-1 reframe) |
| "The SDK alone satisfies audit requirements" | LITE local audit is not tamper-evident. Tamper-evident evidence is FULL-only |
| "LITE is pointless if it can be bypassed" | LITE is hygiene for cooperating agents plus the staged path to FULL with the same policy schema |
| "Data that reached the provider can be erased" | No. Scope honestly: invalidation within what Aegis mediated (C-3) |
| "A declared purpose authorizes the access" | A purpose is a label. Authorization is resolution against policy, scope, and RBAC — and only FULL enforces it against a non-cooperating agent |

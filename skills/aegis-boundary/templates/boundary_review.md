# Boundary review output template

Keep READY short. Spend words only on REVIEW / STOPPED.

```
Aegis Boundary Review
source: aegis-boundary-skill (advisory — not Core enforcement, no receipt)

Decision: READY | REVIEW | STOPPED

Machine checks:
- overclaim_scan: PASS|FAIL (exit N) [files scanned]

Why:
- <each finding, one line, with citation: canon §N / pitfalls #N / scan output>

Allowed (advisory):
- <what may proceed as-is or with stated rewording>

Blocked (advisory):
- <claim or change that must not ship> (citation)

Required checks:
- <what must pass before this becomes READY — e.g. human approval for
  roadmap/pricing/publication, your release process for ship decisions>

Next:
- <smallest concrete step>
```

Rules:
- A machine-check FAIL caps the decision at REVIEW/STOPPED — never READY.
- Every Blocked line carries a citation. No uncited blocks.
- Never emit `source: CORE`, "Enforced by Aegis Core", "tamper-evident", or
  "evidence verified" about this review itself — those are FULL runtime
  vocabulary, and this skill is neither.

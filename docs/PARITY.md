# Vendored-content parity

`skills/aegis-boundary/references/boundary_canon.md` and
`references/pitfalls.md` are **derivatives** of internal canonical sources.
On any conflict, the canonical source wins; fix the vendored copy here, never
argue from it.

## Source anchor (2026-06-12 derivation)

| Item | Value |
|---|---|
| Canonical doc | `aegis-core` repo, `docs/integration/AEGIS_INTEGRATION_BOUNDARY.md` (internal) |
| Canonical sha256 at derivation | `12da58a4ffba04c770f333bfde3a9eb9d0abdd3d58c2c907a4f1b768947bdcb1` |
| Canonical git state at derivation | untracked in aegis-core working tree (follow-up: commit it; record the commit SHA here on next re-derivation) |
| Overclaim patterns ported from | `aegis-core` repo, `tools/check_honesty_lint.py` (canonical implementation remains upstream) |

## Derivation rules

1. Only content the canonical doc classifies as sayable externally is
   vendored (approved claims, the LITE/FULL separation table, never-claims,
   honest reframes, public product names). Internal-only material (internal
   platform names, roadmap details, pricing, incident history) is excluded.
2. English-first: the vendored canon is written in English per the Aegis
   english-first artifact contract.
3. Re-derivation triggers mirror the canonical doc's own update triggers
   (schema review, hosted-FULL availability, guardrail revisions, SDK GA).
   When any fire: re-read the canonical doc, regenerate the vendored files,
   update the anchor table above, and re-run the skill's own machine checks
   plus a self-review (meta claim parity) before tagging a release.

## Verify current vendored hashes

```bash
shasum -a 256 skills/aegis-boundary/references/boundary_canon.md \
              skills/aegis-boundary/references/pitfalls.md
```

Recorded at last derivation (update on every change):

| File | sha256 |
|---|---|
| references/boundary_canon.md | (recorded in CHANGELOG at tag time) |
| references/pitfalls.md | (recorded in CHANGELOG at tag time) |

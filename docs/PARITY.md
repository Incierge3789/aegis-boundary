# Vendored-content parity

`skills/aegis-boundary/references/boundary_canon.md` and
`references/pitfalls.md` are **derivatives** of the Aegis internal canonical
boundary document (private). On any conflict, the canonical source wins; fix
the vendored copy here, never argue from it.

## Source anchor (2026-06-12 derivation)

| Item | Value |
|---|---|
| Canonical source | Aegis internal integration-boundary canonical document (private) |
| Canonical sha256 at derivation | `12da58a4ffba04c770f333bfde3a9eb9d0abdd3d58c2c907a4f1b768947bdcb1` |
| Overclaim patterns ported from | the Aegis internal honesty lint (the canonical implementation remains upstream) |

## Derivation rules

1. Only content the canonical document classifies as sayable externally is
   vendored (approved claims, the LITE/FULL separation table, never-claims,
   honest reframes, public product names). Internal-only material is
   excluded.
2. English-first, per the Aegis english-first artifact contract.
3. Re-derivation triggers mirror the canonical document's own update
   triggers (schema review, hosted-FULL availability, guardrail revisions,
   SDK GA). When any fire: re-read the canonical document, regenerate the
   vendored files, update the anchor table above, and re-run the machine
   checks plus a self-review (meta claim parity) before tagging a release.

## Verify current vendored hashes

```bash
shasum -a 256 skills/aegis-boundary/references/boundary_canon.md \
              skills/aegis-boundary/references/pitfalls.md
```

Recorded at each release tag in `CHANGELOG.md`.

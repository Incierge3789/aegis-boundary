# Changelog

## 0.1.1 — 2026-06-12

Low-severity remediation from the multi-agent failure audit.

- Parity anchor (unchanged this release):
  - `boundary_canon.md` sha256 `99b5af6fb04553d065d163247b0dec7bbd2fb04bcf8b7d4d7f8b7f0998527575`
  - `pitfalls.md` sha256 `451c6c2bb0cf59ceb0e04117de97cfd6b6176770d72a93996c82031ab692de0e`
- Scanner: ASCII-fold (NFKD) before matching so homoglyph/diacritic spellings
  cannot slip the English patterns; C-3 now requires the delete-verb and
  provider-noun to be within proximity (removes false positives on local
  deletion claims); table-row exemption now requires a family-id/keyword so
  marketing text cannot hide in a table; added `--quiet` to suppress matched
  line snippets in log-captured runs.
- Packaging hygiene: `.gitignore` for `__pycache__`/`*.pyc`; `install.sh` now
  installs atomically (stage-then-swap), excludes bytecode, and preflights
  `python3`.
- Manifests: `cursor`/`gemini` now carry `homepage`/`repository`; all four
  manifests pinned to one version.
- Docs: README states the Python 3.7+ requirement; SKILL.md adds an
  outcome-based routing section; `scripts/check_release.sh` enforces
  version + parity-hash consistency before a tag.

## 0.1.0 — 2026-06-12

- Initial release of the aegis-boundary advisory skill, packaged for four
  agent CLIs from one shared `skills/` directory: Claude Code (marketplace +
  plugin), Codex (agent skills), Gemini CLI (extension), Cursor (plugin).
- Standalone overclaim scan (`check_overclaims.py`, three claim families
  ported from the upstream Aegis honesty lint).
- Vendored boundary canon + pitfalls, parity-tracked (`docs/PARITY.md`).
- Parity anchor (vendored-file digests at this tag):
  - `boundary_canon.md` sha256 `99b5af6fb04553d065d163247b0dec7bbd2fb04bcf8b7d4d7f8b7f0998527575`
  - `pitfalls.md` sha256 `451c6c2bb0cf59ceb0e04117de97cfd6b6176770d72a93996c82031ab692de0e`
- Overclaim scan hardened against evasion: encoding-aware reads (UTF-16/UTF-32
  no longer bypass detection), a whole-file pass for line-split phrasings,
  bounded-gap + inverted C-1 matching, and structure-only exemption that prose
  and list bullets cannot self-trigger.
- License: MIT, Copyright (c) 2026 Aegis Project (Incierge).

# Changelog

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

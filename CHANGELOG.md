# Changelog

## 0.1.0 — 2026-06-12 (private prep, unreleased)

- Initial packaging of the aegis-boundary advisory skill for four agent CLIs
  from one shared `skills/` directory: Claude Code (marketplace + plugin),
  Codex (agent skills), Gemini CLI (extension), Cursor (plugin).
- Standalone overclaim scan (`check_overclaims.py`, three families ported
  from the upstream Aegis honesty lint).
- Vendored boundary canon + pitfalls (parity-tracked, see docs/PARITY.md).
- Distribution status and publish gates: docs/DISTRIBUTION.md.
- Repo is private; public flip and marketplace submissions are gated on
  explicit publish GO.

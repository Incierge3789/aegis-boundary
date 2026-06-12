# Distribution targets and status

Status legend: ✅ packaged in this repo / 🔜 action needed / ⛔ gated on human GO.

Repo visibility: **private** (prep stage). Public flip, marketplace
submissions, and any announcement are ⛔ **gated on explicit Giri publish GO**
plus the pre-publish checklist below.

## Targets

### 1. Claude Code plugin marketplace — ✅ packaged

- This repo is both a **marketplace** (`.claude-plugin/marketplace.json`,
  marketplace name `aegis-skills`) and a **plugin** (`.claude-plugin/plugin.json`,
  plugin source `./`). Skills are auto-discovered from `skills/`.
- Install after public flip: `/plugin marketplace add Incierge3789/aegis-boundary`
  then `/plugin install aegis-boundary@aegis-skills`.
- Pre-publish: run `claude plugin validate .` (validates marketplace + plugin
  + skill frontmatter). Marketplace name `aegis-skills` avoids the Anthropic
  reserved-name list. Bump `version` in plugin.json on every release (pinned
  semantics).
- Note: while private, installs work for authenticated users via `gh` /
  `GITHUB_TOKEN` (documented Claude Code behavior for private marketplaces) —
  usable for pre-release dogfood by the team.

### 2. OpenAI Codex skills — ✅ packaged (same skill dir)

- Codex consumes the same `SKILL.md` format; install = copy
  `skills/aegis-boundary` into `~/.agents/skills` (user) or repo
  `.agents/skills` (team). `install.sh codex` does this.
- No central registry to submit to (as of derivation date); distribution is
  repo-based + `$skill-installer`. Public flip is sufficient.

### 3. Gemini CLI extensions — ✅ packaged / 🔜 gallery listing

- `gemini-extension.json` (name/version/contextFileName) + `GEMINI.md` +
  auto-discovered `skills/`. Install after public flip:
  `gemini extensions install https://github.com/Incierge3789/aegis-boundary`.
- Gallery listing at geminicli.com/extensions requires following their
  Extension Releasing Guide (Git repo or GitHub Releases) — submit after
  public flip.

### 4. Cursor marketplace — ✅ packaged / 🔜 submission

- `.cursor-plugin/plugin.json` + auto-discovered `skills/` (and room for
  `rules/`, `mcp.json` later).
- Submission is a form: cursor.com/marketplace/publish — submit after public
  flip. Multi-plugin future: add `.cursor-plugin/marketplace.json`.

### 5. acpservers.org — 🔜 fit decision needed (Giri)

- ACP here = **Agentic Commerce Protocol** registry (agents × payments ×
  commerce infrastructure), with categories including "Collaboration &
  Governance". A skill is not an ACP server; the natural Aegis entry there
  would be an MCP/ACP-shaped governance server (e.g. aegis-mcp-proxy or a
  boundary-review MCP wrapper), not this skill as-is.
- Listing is via their /submit-acp form and needs a public repo.
- Recommendation: treat as a separate decision — either (a) skip, or (b)
  package a small MCP server wrapper around the boundary review and submit
  that. Giri call.

## Pre-publish checklist (run before public flip; all must pass)

1. `python3 skills/aegis-boundary/scripts/check_overclaims.py README.md GEMINI.md docs/*.md skills/aegis-boundary/SKILL.md skills/aegis-boundary/references/*.md skills/aegis-boundary/templates/*.md` → exit 0
2. Internal honesty lint (aegis-core `tools/check_honesty_lint.py --paths` on
   all repo .md) → exit 0
3. Self-review: run the aegis-boundary skill on this repo (meta claim parity)
   → READY
4. `claude plugin validate .` → no errors
5. PARITY.md anchor updated; canonical doc committed upstream and its commit
   SHA recorded
6. Internal-name sweep: no internal platform/codenames, no pricing, no
   roadmap dates, no incident history in any tracked file
7. Published-artifact parity discipline applies to any tag/release (source =
   tag = artifact, clean-install behavior verified)
8. License decided and `LICENSE` file added via the legal panel (MIT
   proposed; LICENSE creation is hook-gated to a legal panel by design —
   panel-fixed-4 + legal officers). Legal entity name confirmed in the same
   panel. Until then the repo intentionally carries no license declaration
9. **Giri publish GO recorded** (beads + chat literal)

## Release flow (after GO)

1. Bump `VERSION` + `.claude-plugin/plugin.json` version + CHANGELOG entry
   (record vendored-file sha256s)
2. Flip repo to public (Giri-authorized action)
3. Tag `v<VERSION>` → GitHub release
4. Submit: Cursor form, Gemini gallery; announce via approved channels only

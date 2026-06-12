#!/usr/bin/env bash
# Install the aegis-boundary skill for a local agent CLI.
# Usage: ./install.sh <codex|claude>
#   codex  -> ~/.agents/skills/aegis-boundary
#   claude -> ~/.claude/skills/aegis-boundary (user-level; or use the plugin
#             marketplace instead: /plugin marketplace add Incierge3789/aegis-boundary)
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
SRC="$HERE/skills/aegis-boundary"
case "${1:-}" in
  codex)  DEST="$HOME/.agents/skills/aegis-boundary" ;;
  claude) DEST="$HOME/.claude/skills/aegis-boundary" ;;
  *) echo "usage: ./install.sh <codex|claude>" >&2; exit 1 ;;
esac

# Preflight: the optional overclaim scanner needs python3.
command -v python3 >/dev/null 2>&1 || \
  echo "warning: python3 not found — the overclaim scanner (scripts/check_overclaims.py) will not run until it is installed (Python 3.7+)." >&2

# Atomic install: stage into a temp dir, then swap, so a partial copy never
# leaves the destination in an unrecoverable half-deleted state.
mkdir -p "$(dirname "$DEST")"
tmp="$DEST.new.$$"
rm -rf "$tmp"
cp -R "$SRC" "$tmp"
# Don't ship version-specific compiled bytecode to users.
find "$tmp" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
find "$tmp" -name '*.pyc' -delete 2>/dev/null || true
rm -rf "$DEST"
mv "$tmp" "$DEST"
echo "installed: $DEST"

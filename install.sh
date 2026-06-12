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
mkdir -p "$(dirname "$DEST")"
rm -rf "$DEST"
cp -R "$SRC" "$DEST"
echo "installed: $DEST"

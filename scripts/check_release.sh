#!/usr/bin/env bash
# Pre-release consistency gate for aegis-boundary.
# Run before tagging a release. Exit 0 = consistent, 1 = drift found.
#
# Checks (closes audit findings on version skew + parity-hash recording):
#   1. All four manifests declare the SAME version string.
#   2. That version appears in CHANGELOG.md.
#   3. The current vendored-file sha256s are recorded in CHANGELOG.md
#      (PARITY.md promises these are recorded at each release tag).
#   4. The overclaim scan passes on the repo's own docs (meta claim parity).
set -u
cd "$(cd "$(dirname "$0")/.." && pwd)"
rc=0
fail() { echo "[DRIFT] $1"; rc=1; }

vers=$(
  python3 - <<'PY'
import json
files = ['.claude-plugin/plugin.json', '.cursor-plugin/plugin.json', 'gemini-extension.json']
vs = set()
for f in files:
    vs.add(json.load(open(f)).get('version'))
# marketplace.json carries the plugin entry version too if present
try:
    mp = json.load(open('.claude-plugin/marketplace.json'))
    for p in mp.get('plugins', []):
        if p.get('version'):
            vs.add(p['version'])
except Exception:
    pass
print('\n'.join(sorted(str(v) for v in vs)))
PY
)
n=$(printf '%s\n' "$vers" | grep -c .)
if [ "$n" -ne 1 ]; then fail "manifest versions disagree: $(echo $vers)"; fi
V=$(printf '%s\n' "$vers" | head -1)
echo "declared version: $V"

grep -q "$V" CHANGELOG.md || fail "version $V not found in CHANGELOG.md"

for f in skills/aegis-boundary/references/boundary_canon.md skills/aegis-boundary/references/pitfalls.md; do
  h=$(shasum -a 256 "$f" | cut -d' ' -f1)
  if ! grep -q "$h" CHANGELOG.md; then fail "sha256 of $f not recorded in CHANGELOG.md ($h)"; fi
done

if ! python3 skills/aegis-boundary/scripts/check_overclaims.py \
    README.md GEMINI.md CHANGELOG.md docs/PARITY.md \
    skills/aegis-boundary/SKILL.md \
    skills/aegis-boundary/references/boundary_canon.md \
    skills/aegis-boundary/references/pitfalls.md \
    skills/aegis-boundary/templates/boundary_review.md >/dev/null 2>&1; then
  fail "overclaim scan failed on the repo's own docs (meta claim parity)"
fi

[ "$rc" -eq 0 ] && echo "[OK] release consistency verified for $V"
exit "$rc"

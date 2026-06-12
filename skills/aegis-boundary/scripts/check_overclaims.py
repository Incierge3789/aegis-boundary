#!/usr/bin/env python3
"""aegis-boundary overclaim scan (standalone distribution port).

Detects three overclaim families that violate Aegis honest-framing rules in
markdown/text files. Ported (patterns and intent) from the Aegis Core honesty
lint so the skill works without an Aegis Core checkout; the upstream lint in
the Aegis Core repository remains the canonical implementation.

Families (see references/boundary_canon.md §5-A for the honest reframes):
  C-1  absolute-leak claim        ("absolutely will not leak", "never leaks")
  C-2  RAG-auto-safe claim        ("RAG ... all/automatically ... safe")
  C-3  provider-side-delete claim ("can erase/delete" + provider context)

Known limitation: English phrasings only. Non-English claims need LLM review
against the canon reframes — a PASS here is evidence of nothing for them.

Usage:  check_overclaims.py <file.md> [more files...]
Exit:   0 = no violations in all readable files
        1 = violations found, or an argument is missing/unreadable
            (a missing file is a FAIL, not a silent skip)
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

PAT_ABSOLUTE_LEAK = re.compile(
    r"(?:absolutely|never)\s+(?:does\s+not\s+leak|will\s+not\s+leak|leaks?\s+nothing|leak-free|"
    r"won't\s+leak)",
    re.IGNORECASE,
)
PAT_RAG_AUTO_SAFE = re.compile(
    r"RAG.{0,40}(?:all|every|every\s+single|automatically|auto).{0,40}"
    r"(?:safe|secure|protect)",
    re.IGNORECASE,
)
PAT_CAN_DELETE = re.compile(
    r"can\s+(?:erase|delete|wipe|remove)|fully\s+(?:erase|delete|wipe)",
    re.IGNORECASE,
)
PROVIDER_CONTEXT = re.compile(
    r"LLM|RAG|provider|prompt|embedding|vector|model|training|external|send",
    re.IGNORECASE,
)
# Lines that quote a forbidden phrase in order to refute or forbid it are not
# violations (mirrors the upstream lint's refutation allowlist, simplified).
REFUTATION_MARKER = re.compile(
    r"forbidden|never-claim|never\s+write|do\s+not\s+say|do\s+not\s+write|reframe|"
    r"overclaim|anti-?pattern|not\s+claimable|violation|incorrect|"
    r"phrases\s+like|family|example\s+of|honest\s+replacement|\bC-[123]\b",
    re.IGNORECASE,
)


def scan_file(path: Path) -> list[tuple[int, str, str]]:
    hits: list[tuple[int, str, str]] = []
    for n, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if REFUTATION_MARKER.search(line):
            continue
        if PAT_ABSOLUTE_LEAK.search(line):
            hits.append((n, "C-1 absolute-leak", line.strip()))
        if PAT_RAG_AUTO_SAFE.search(line):
            hits.append((n, "C-2 RAG-auto-safe", line.strip()))
        if PAT_CAN_DELETE.search(line) and PROVIDER_CONTEXT.search(line):
            hits.append((n, "C-3 provider-side-delete", line.strip()))
    return hits


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: check_overclaims.py <file.md> [more files...]", file=sys.stderr)
        return 1
    rc = 0
    scanned = 0
    for arg in argv:
        path = Path(arg).expanduser()
        if not path.is_file():
            print(f"[FAIL] input not found (missing files are a FAIL, not a skip): {arg}")
            rc = 1
            continue
        scanned += 1
        for n, family, text in scan_file(path):
            print(f"[FAIL] {path}:{n} [{family}]\n    > {text[:200]}")
            rc = 1
    if rc == 0:
        print(f"[OK] {scanned} file(s) scanned, 0 overclaim violations.")
    else:
        print("See references/boundary_canon.md §5-A for honest reframes.")
    return rc


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

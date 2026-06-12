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

This is an honesty gate: a false PASS (a forbidden claim slipping through) is
the worst outcome, so the scan is deliberately evasion-resistant —
encoding-aware reads, a whole-file pass to catch line-split phrasings, and a
structure-only exemption rule that prose cannot self-trigger.

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

# C-1 absolute-leak. Bounded gap (not bare adjacency) so intervening hedge
# words still trip it ("absolutely certain ... will not leak"), and the
# inverted form ("absolutely not leak" / "will absolutely not leak") is caught.
PAT_ABSOLUTE_LEAK = re.compile(
    r"(?:absolutely|never|guarantee[ds]?|100%|completely)\b.{0,40}?"
    r"(?:does\s+not\s+leak|will\s+not\s+leak|not\s+leak|leaks?\s+nothing|"
    r"leak-free|won't\s+leak|\bleaks?\b|\bleaking\b)",
    re.IGNORECASE | re.DOTALL,
)
PAT_RAG_AUTO_SAFE = re.compile(
    r"RAG.{0,40}?(?:all|every|every\s+single|automatically|auto).{0,40}?"
    r"(?:safe|secure|protect)",
    re.IGNORECASE | re.DOTALL,
)
PAT_CAN_DELETE = re.compile(
    r"can\s+(?:erase|delete|wipe|remove)|fully\s+(?:erase|delete|wipe)",
    re.IGNORECASE,
)
PROVIDER_CONTEXT = re.compile(
    r"LLM|RAG|provider|prompt|embedding|vector|model|training|external|send",
    re.IGNORECASE,
)

# Exemption is granted by STRUCTURE ONLY. A line that merely contains a
# refutation word or a family id must NOT be able to exempt itself, or an
# attacker smuggles a real overclaim past the gate. Two legitimate forms:
#   1. a markdown table row  ("| C-1 | forbidden: ... | reframe |")
#   2. a heading / blockquote / comment line that defines the rule and is
#      tagged with a family id OR a definitional keyword
# Bullets and bare prose are excluded — they carry claims, so they are scanned.
FAMILY_ID = re.compile(r"\bC-[123]\b")
DEFINITIONAL = re.compile(
    r"forbidden|never-?claim|reframe|anti-?pattern|overclaim|"
    r"honest\s+(?:replacement|reframe)|family|families|example",
    re.IGNORECASE,
)
# Structural prefixes that denote definition/quote/heading context — NOT list
# bullets ("- " / "* "), which carry prose and must be scanned.
DEFINITION_PREFIX = re.compile(r"^\s*(>|#{1,6}\s|//|#\s)")


def _is_exempt(line: str) -> bool:
    stripped = line.lstrip()
    if stripped.startswith("|"):
        return True  # markdown table row (the canon's never-claim table)
    if DEFINITION_PREFIX.match(line) and (FAMILY_ID.search(line) or DEFINITIONAL.search(line)):
        return True  # heading/quote/comment line clearly defining the rule
    return False


def _decode(path: Path) -> str:
    """Encoding-aware read. A blind utf-8 read lets UTF-16/UTF-32 markdown
    null-interleave keywords past every regex (a pure false-negative leak),
    so sniff BOMs, then strip residual NULs."""
    data = path.read_bytes()
    if data[:4] in (b"\xff\xfe\x00\x00", b"\x00\x00\xfe\xff"):
        text = data.decode("utf-32", errors="replace")
    elif data[:2] in (b"\xff\xfe", b"\xfe\xff"):
        text = data.decode("utf-16", errors="replace")
    else:
        text = data.decode("utf-8", errors="replace")
    return text.replace("\x00", "")


def scan_file(path: Path) -> list[tuple[object, str, str]]:
    hits: list[tuple[object, str, str]] = []
    text = _decode(path)
    lines = text.splitlines()

    # Pass 1: per-line (gives line numbers + applies the structural exemption).
    for n, line in enumerate(lines, 1):
        if _is_exempt(line):
            continue
        if PAT_ABSOLUTE_LEAK.search(line):
            hits.append((n, "C-1 absolute-leak", line.strip()))
        if PAT_RAG_AUTO_SAFE.search(line):
            hits.append((n, "C-2 RAG-auto-safe", line.strip()))
        if PAT_CAN_DELETE.search(line) and PROVIDER_CONTEXT.search(line):
            hits.append((n, "C-3 provider-side-delete", line.strip()))

    # Pass 2: whole-file, over NON-exempt lines only, whitespace-normalized.
    # Catches phrasings split across line breaks that pass 1 cannot see, while
    # preserving the exemption allowlist (exempt lines are dropped first).
    joined = re.sub(r"\s+", " ", " ".join(l for l in lines if not _is_exempt(l)))
    already = {fam for _, fam, _ in hits}
    for pat, fam in (
        (PAT_ABSOLUTE_LEAK, "C-1 absolute-leak"),
        (PAT_RAG_AUTO_SAFE, "C-2 RAG-auto-safe"),
    ):
        if fam not in already and pat.search(joined):
            hits.append(("multi-line", fam, "(phrase split across lines)"))
    if "C-3 provider-side-delete" not in already and (
        PAT_CAN_DELETE.search(joined) and PROVIDER_CONTEXT.search(joined)
    ):
        # require proximity in the joined text to avoid unrelated co-occurrence
        for m in PAT_CAN_DELETE.finditer(joined):
            window = joined[max(0, m.start() - 80): m.end() + 80]
            if PROVIDER_CONTEXT.search(window):
                hits.append(("multi-line", "C-3 provider-side-delete", "(phrase split across lines)"))
                break
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

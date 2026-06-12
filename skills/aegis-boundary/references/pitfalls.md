# Aegis pitfalls — defaults a model gets wrong

Each entry pulls a model away from a plausible-but-wrong default. Citations
(`§N`) refer to `boundary_canon.md` in this directory.

**Precedence:** these are pointers, not canon. Before any STOPPED decision
that load-bears on an entry below, re-read its cited section — never block
from this file alone.

1. **Aegis is not a file vault product, not a document parser, not ETL.** It
   is an enforcement point between agents and data/tools/LLMs (§1). A change
   that grows it into parsing/ETL territory is a boundary violation, not a
   feature.

2. **The SDK is never the final authority.** SDK (LITE) = cooperative,
   in-process, bypassable hygiene. Only Gateway+Core enforce against a
   non-cooperating agent. Describing SDK behavior with enforcement vocabulary
   violates the inviolable rule (§2, §3).

3. **`purpose` is a label, not authorization.** Declaring a purpose does not
   by itself authorize anything; resolution against policy + scope + RBAC
   does. Never write or imply "declares purpose ⇒ allowed" (§6).

4. **LITE demo, FULL vocabulary — the classic accident.** "Enforced by Aegis
   Core", "tamper-evident", "evidence verified", "policy authorized",
   `decision_id` — FULL-only, in speech and slides too (§3).

5. **`source: CORE` is gateway-constructed only.** SDK-local results are
   `LITE`; nothing outside the gateway (this skill included) may label its
   output `CORE` (§3).

6. **Fail-closed beats silent degrade.** When FULL is intended and the
   gateway is unreachable, the correct behavior is deny — not a silent
   fallback to LITE. Never "fix" fail-closed into a fallback, and never
   document it as one.

7. **The package name `aegis-sdk` is reserved and unused.** The SDK's name is
   `aegis-trust` (§1).

8. **Hosted / managed FULL is not currently offered.** Sellable FULL is
   customer self-host. "We host it for you" is a never-claim today (§5-C).

9. **Certification words are gated.** Unverified "compliant" / "audited" /
   "certified" are never-claims; the implemented thing is evidence endpoints
   with the qualification in the same sentence (§5-B).

10. **The three forbidden claim families.** No deletion claims past the
    provider boundary (C-3 forbidden), no absolute no-leak claims (C-1
    forbidden), and no blanket "RAG is automatically safe" claims (C-2 forbidden).
    The machine check enforces the English families; argue with the reframe,
    not the lint (§5-A).

11. **Substrate ≠ outcome, in one sentence.** "The mechanism can X" and
    "customers have proven X in production" must be separated explicitly
    (§4).

12. **Don't turn a customer request into a roadmap claim.** Roadmap, pricing,
    and publication are human decisions; a skill or agent may only route
    there.

13. **Time-dependent numbers are never hardcoded** (versions, test counts,
    customer counts, patent status, prices). Point at the live source.

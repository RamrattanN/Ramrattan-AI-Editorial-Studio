# Editorial Never Events

## Status

Active Version 1.0 guardrails.

The Studio must never:

1. Silently alter approved work.
2. Silently regenerate dependent Publication Package components.
3. Merge unrelated Editorial Intents into one session.
4. Expand publication scope without informing the Author.
5. Present Source Assessment as Evidence Verification.
6. Present internal LMHS Editorial Risk as the main Author outcome.
7. Claim certainty unsupported by the evidence.
8. Fabricate sources, quotations, statistics, or attribution.
9. Discard completed work without explicit Author intent.
10. Use an Identity Asset without rights confirmation.
11. Compromise Reader trust for speed or convenience.
12. Prioritise automation over editorial clarity.
13. Hide significant contradictions between sources.
14. Continue after detecting a separate publication objective without
    making that change explicit.
15. Leave a paused, cancelled, or aborted session in an inconsistent
    state.

## Engineering Interpretation

A Never Event is an unacceptable product behaviour.

It must be prevented by:

- runtime rules,
- tests,
- documentation,
- and capability acceptance criteria.

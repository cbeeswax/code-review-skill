---
name: review-regressions
description: Review a change for regressions in existing behavior, compatibility, state, migrations, and public interfaces. Use for /review-regressions.
license: MIT
---

# review-regressions

## Focus

Establish the before-and-after contract for every changed public interface,
configuration key, persisted value, background job, and integration point.
Trace callers and consumers that retain the old behavior. Check upgrades,
downgrades, partial failures, retries, old data, and mixed-version deployments
when applicable.

Require evidence that existing behavior remains supported or that the breaking
change is intentional, documented, versioned, and reversible.


## Evidence contract

Review the change's stated intent, affected boundary, and non-negotiable
constraints before judging implementation details. Build an evidence ledger:

1. **Intent and constraints:** What behavior is changing? What must remain
   true? What is explicitly out of scope?
2. **Evidence collected:** Commands, tests, simulations, traces, benchmarks,
   screenshots, or repository contracts actually inspected or run.
3. **Result:** What each source of evidence proves, disproves, or does not
   cover.
4. **Evidence gaps:** Important behavior that cannot be verified from the
   available code, tests, tooling, or stated intent.
5. **Residual risk and rollback:** What may still fail, how it will be
   detected, and how the change can be safely reversed.

Rank evidence in this order:

1. Reproducible test, simulation, benchmark, screenshot, command output, or
   observed failing behavior.
2. A traced code path tied to a documented contract, invariant, or established
   repository behavior.
3. Inference from a diff, name, or pattern alone.

Only the first two levels support a defect finding. Treat level-three concerns
as evidence gaps or questions, never as asserted bugs.

## Finding rules

Report only issues introduced or made reachable by the reviewed change. Mark
pre-existing issues separately. Do not report style preferences, speculative
problems, or cleanup unless they create a concrete correctness, security,
privacy, reliability, or performance impact.

Each finding must include:

- Severity and confidence.
- Changed file and line evidence.
- The affected behavior, user, system, or data.
- A concrete failure scenario or reproducer.
- A specific remediation or verification step.
- Introduced versus pre-existing classification.
- Test or validation evidence.

Start the final report with the count of verified findings. If there are none,
say `0 verified findings` plainly. Include evidence gaps separately.

## Pull-request behavior

Produce a local report by default. Post GitHub comments only when the user
explicitly asks and the available integration supports it. Post only
high-confidence, evidence-backed, actionable findings and one concise summary.
Never post hypotheses, approve a pull request, merge, or modify code unless
the user explicitly requests that separate action.

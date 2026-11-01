---
name: review-risk
description: Review code changes for operational risk, blast radius, rollout, rollback, observability, and failure handling. Use for /review-risk.
license: MIT
---

# review-risk

## Focus

Identify who and what can be affected if the change fails. Review flags,
defaults, migrations, retries, rate limits, queues, background work, external
dependencies, dashboards, logs, alerts, and rollback paths that are touched by
the diff.

For each material risk, ask how it is detected, contained, and reversed. A
missing rollback or observable failure signal is an evidence gap unless a
concrete unsafe behavior is demonstrated.


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
- Business context first: the affected customer, operational outcome, revenue,
  compliance, trust, or delivery risk.
- A concrete failure scenario in plain language.
- Changed file and line evidence, then the technical cause in only the detail
  needed to make the remediation clear.
- A specific remediation or verification step.
- Introduced versus pre-existing classification.
- Test or validation evidence.

Start the final report with the count of verified findings. If there are none,
say `0 verified findings` plainly. Include evidence gaps separately.

## Inline comment style

Write inline comments for a business reader before a technical reader. Lead
with what could go wrong, for whom, and under what condition. Follow with the
minimum code-level evidence needed to make the concern credible and actionable.
Avoid unexplained framework names, implementation trivia, or jargon in the
first sentence.

Use this shape:

```text
[Severity] Business consequence

When <business scenario>, <customer, operational, financial, compliance, or
trust consequence> can occur. This change <plain-language explanation of why>.

Evidence: <file:line and concise technical cause>
Suggested next step: <specific fix or verification>
```

For example, write `A customer could be charged twice after a payment timeout`
instead of `Missing idempotency guard in retry path`. Keep the technical cause
in the evidence line. Do not post a comment if the business consequence cannot
be explained from the available evidence.

## Pull-request behavior

Produce a local report by default. Post GitHub comments only when the user
explicitly asks and the available integration supports it. Post only
high-confidence, evidence-backed, actionable findings inline and one concise
business-impact summary. Keep broad process notes, evidence gaps, and
low-confidence concerns in the local report rather than posting them inline.
Never post hypotheses, approve a pull request, merge, or modify code unless
the user explicitly requests that separate action.

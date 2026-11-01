---
name: code-review
description: Run an evidence-driven code review that selects correctness, regression, architecture, risk, security, privacy, testing, and performance lenses by change risk. Use for /code-review and general pull-request review requests.
license: MIT
---

# code-review

## Workflow

1. Read the PR description, issue, commit messages, repository instructions,
   and changed files. State the intended behavior in one sentence. If intent
   is missing, record it as an evidence gap.
2. Establish the merge-base diff and identify affected data, users, external
   interfaces, operational dependencies, and rollback mechanism.
3. Classify risk by the **change**, not its author:
   - **Low:** docs, copy, isolated internal changes, or additive code behind a
     flag. Run correctness, regressions, and testing.
   - **Medium:** ordinary product behavior, state handling, caching, external
     interfaces, or configuration. Add architecture and risk.
   - **High:** authentication, authorization, billing, secrets, personal data,
     CI/release workflows, migrations, destructive operations, or broad blast
     radius. Run every applicable lens, including security, privacy, and
     performance.
   Missing evidence raises the tier; it never silently lowers it.
4. Ask or run the narrowest available verification: static tracing, targeted
   tests, build/type checks, simulations, fuzz/property tests, benchmarks, or
   screenshots for UI changes.
5. Run selected lenses independently. Deduplicate their findings, preserve the
   strongest evidence, and separate verified findings from evidence gaps.
6. Deliver: risk tier; verified finding count; findings sorted by severity;
   evidence ledger; tests run and results; evidence gaps; rollback and
   residual-risk summary.

Do not substitute a generic diff summary for verification. A change that lacks
the evidence required for its risk tier is not ready for a confident review.


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

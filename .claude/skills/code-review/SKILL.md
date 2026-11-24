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
4. Name the load-bearing assumptions before reading the implementation's
   explanation of itself, and decide what evidence would show each one wrong.
5. Load and follow the selected sibling skill instructions before applying its
   lens: `review-correctness`, `review-regressions`, `review-testing`,
   `review-architecture`, `review-risk`, `review-security`, `review-privacy`,
   and `review-performance`. Run selected lenses independently, but do not
   treat their agreement as independent evidence: they read the same
   requirements, code, and tests.
6. Ask or run the narrowest available verification: static tracing, targeted
   tests, build/type checks, simulations, fuzz/property tests, benchmarks, or
   screenshots for UI changes. Prefer evidence that can contradict the
   implementation over evidence that restates it.
7. Deduplicate lens findings, preserve the strongest evidence, and separate
   verified findings from evidence gaps.
8. Deliver: risk tier; verified finding count and what it covers; findings
   sorted by impact, each with confidence and verification status; load-bearing
   assumptions with their basis; decisions for the owner; evidence ledger;
   tests run and results; evidence gaps; rollback and residual-risk summary.

## Let risk decide the evidence required

- **Low risk** with clear intent, passing required checks, and no material
  uncertainty: say that the change appears eligible for automatic approval
  *under the team's agreed policy*. Do not approve it yourself.
- **Medium and high risk:** the report is for a human owner, who reviews the
  documented intent, constraints, evidence, and unresolved questions rather
  than every line. Make it answerable: does the evidence address the failure
  that matters? Twenty checks that never test the harmful assumption do not.
- **An unresolved, high-impact concern** is not cleared by another approval,
  another reviewer, or more tests of the same assumption. State the evidence
  that would resolve it and mark the change not ready until it exists.

Do not substitute a generic diff summary for verification. A change that lacks
the evidence required for its risk tier is not ready for a confident review.


## Evidence contract

Review the change's stated intent, affected boundary, and non-negotiable
constraints before judging implementation details. Build an evidence ledger:

1. **Intent and constraints:** What behavior is changing? What must remain
   true? What is explicitly out of scope? What promise does the change make to
   the user or the business?
2. **Load-bearing assumptions:** The beliefs the change depends on to be safe,
   and the basis for each (see below).
3. **Evidence collected:** Commands, tests, simulations, traces, benchmarks,
   screenshots, or repository contracts actually inspected or run.
4. **Result:** What each source of evidence proves, disproves, or does not
   cover.
5. **Evidence gaps:** Important behavior that cannot be verified from the
   available code, tests, tooling, or stated intent.
6. **Residual risk and rollback:** What may still fail, how it will be
   detected, and how the change can be safely reversed.

Rank evidence in this order:

1. Reproducible test, simulation, benchmark, screenshot, command output, or
   observed failing behavior.
2. A traced code path tied to a documented contract, invariant, or established
   repository behavior.
3. Inference from a diff, name, or pattern alone.

Only the first two levels support a defect finding. Treat level-three concerns
as evidence gaps or questions, never as asserted bugs. A test or mock counts
as evidence about the outside world only when its behavior comes from a source
other than the implementation under review.

## Challenge the shared assumption

The implementation, its tests, and a reviewer can all agree and still rest on
the same wrong assumption. Three green lights can be one assumption repeated
three times. Before concluding, name the assumptions the change depends on —
for example, "a missing response means the action failed" — and for each ask:

> **What would show that this reasoning is wrong?**

Then look for evidence that does not inherit the implementation's view:

- An agreed business constraint or a separately specified expected outcome.
- An external service contract, documentation, or integration test against the
  real behavior.
- An observation, log, or trace that contradicts the current explanation.

Record each assumption's basis as **independent** (contract, documentation,
observed behavior, owner decision) or **inherited** (the implementation, a mock
written to make it pass, or the same incomplete requirements). An inherited
basis is an evidence gap, however convincing the explanation sounds.

Agreement is not independence. Passing tests, a second review lens, another
model, or another person add confidence only when they rely on different
evidence. Several reviewers reading the same requirements, mocks, and code can
reproduce the same mistake; do not count their agreement as corroboration.

## Impact, confidence, and verification

Report these as three separate properties of every finding and gap; never
blend them into one reassuring score:

- **Impact:** what happens, and to whom, if the concern is real.
- **Confidence:** how strongly the evidence supports the concern or its
  absence.
- **Verification:** `verified`, `partially verified`, or `unverified`, and by
  which evidence.

A high-impact concern stays in the report while it is unverified; low
confidence lowers how it is labelled, not whether the owner hears about it. A
confident explanation resting on a weak or inherited test is still unverified.

## Finding rules

Report only issues introduced or made reachable by the reviewed change. Mark
pre-existing issues separately. Do not report style preferences, speculative
problems, or cleanup unless they create a concrete correctness, security,
privacy, reliability, or performance impact.

Each finding must include:

- Severity (impact), confidence, and verification status, stated separately.
- Business context first: the affected customer, operational outcome, revenue,
  compliance, trust, or delivery risk.
- A concrete failure scenario in plain language.
- Changed file and line evidence, then the technical cause in only the detail
  needed to make the remediation clear.
- A specific remediation or verification step.
- Introduced versus pre-existing classification.
- Test or validation evidence, and whether its basis is independent or
  inherited.

Behavior can work exactly as written and still break the promise. When the
change quietly decides something an owner should decide — availability over
verified access, a destructive step before its replacement is confirmed,
retrying an action whose outcome is unknown — report it as a **decision for
the owner**, with the promise at stake, even if no line of code is wrong.

Start the final report with the count of verified findings. If there are none,
say `0 verified findings` plainly — and say what that covers. "No issues found"
is not proof that no important issue exists: state what was checked, what
supports the conclusion, and where confidence stops. Include evidence gaps,
unverified high-impact concerns, and decisions for the owner separately.

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

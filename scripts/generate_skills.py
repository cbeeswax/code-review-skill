#!/usr/bin/env python3
"""Generate identical public skill folders for supported agent ecosystems."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
LOCATIONS = (".github/skills", ".claude/skills", ".agents/skills")

COMMON = """\
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
"""

SKILLS = {
    "code-review": {
        "description": (
            "Run an evidence-driven code review that selects correctness, "
            "regression, architecture, risk, security, privacy, testing, and "
            "performance lenses by change risk. Use for /code-review and "
            "general pull-request review requests."
        ),
        "body": """\
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
""",
    },
    "review-correctness": {
        "description": (
            "Review changed code for functional defects, root-cause mismatch, "
            "and broken behavior. Use for /review-correctness and normal code "
            "review requests."
        ),
        "body": """\
## Focus

Trace the changed behavior from input through state, side effects, and output.
Compare it with the requested intent and existing contracts. Verify error
paths, empty and boundary inputs, ordering, retries, idempotency, and
concurrency only where the change makes them relevant.

Prefer a targeted test or a concrete execution trace over a suspicious-looking
line. For bug fixes, verify that the change addresses the root cause rather
than hiding one symptom.

Check that the behavior preserves the promise, not only that it executes. For
multi-step changes, ask what state the user is left in when a later step
fails: replacing an appointment by cancelling it first loses the booking if
the new one cannot be created. For retries, ask whether a missing response is
being treated as proof of a failed action, and what the operation reference
is across attempts.
""",
    },
    "review-regressions": {
        "description": (
            "Review a change for regressions in existing behavior, compatibility, "
            "state, migrations, and public interfaces. Use for /review-regressions."
        ),
        "body": """\
## Focus

Establish the before-and-after contract for every changed public interface,
configuration key, persisted value, background job, and integration point.
Trace callers and consumers that retain the old behavior. Check upgrades,
downgrades, partial failures, retries, old data, and mixed-version deployments
when applicable.

Require evidence that existing behavior remains supported or that the breaking
change is intentional, documented, versioned, and reversible.

Watch for guarantees that disappear through ordering or error handling rather
than through a changed signature: a step that used to happen only after
confirmation, or an error that used to stop the flow and now lets it continue.
""",
    },
    "review-architecture": {
        "description": (
            "Review code changes for architecture, system boundaries, invariants, "
            "dependencies, and reusable patterns. Use for /review-architecture."
        ),
        "body": """\
## Focus

Map the changed component's responsibility, dependencies, and ownership
boundary. Check whether it bypasses an existing abstraction, duplicates a
service contract, reverses dependency direction, leaks infrastructure concerns,
or establishes a pattern that future changes will copy.

Validate claimed invariants against callers and downstream consumers. Flag an
architecture issue only when a traced dependency or documented system rule
shows a concrete consequence.
""",
    },
    "review-risk": {
        "description": (
            "Review code changes for operational risk, blast radius, rollout, "
            "rollback, observability, and failure handling. Use for /review-risk."
        ),
        "body": """\
## Focus

Identify who and what can be affected if the change fails. Review flags,
defaults, migrations, retries, rate limits, queues, background work, external
dependencies, dashboards, logs, alerts, and rollback paths that are touched by
the diff.

For each material risk, ask how it is detected, contained, and reversed. A
missing rollback or observable failure signal is an evidence gap unless a
concrete unsafe behavior is demonstrated.

Pay particular attention to outcomes the system cannot know: a call to an
external service that timed out may still have succeeded. Ask what the change
does when the outcome of the original request remains unknown, and whether
that path has been verified at all.
""",
    },
    "review-security": {
        "description": (
            "Review code changes for exploitable security vulnerabilities, trust "
            "boundary violations, authentication, authorization, secrets, and "
            "unsafe input handling. Use for /review-security."
        ),
        "body": """\
## Focus

Treat security as an independent review. Trace untrusted input to sensitive
sinks and verify authentication, authorization, tenancy, cryptography, secret
handling, deserialization, command execution, file access, and network
boundaries affected by the change.

Every security finding needs an attack path, affected asset or boundary, and
reproducible evidence or a traced exploit chain. Do not dilute security
findings with style feedback. Escalate missing trust-boundary evidence as an
explicit review gap.

Error handling on a security check is a security decision. If a verification
error lets the request continue (fail-open), that is an authorization choice
of availability over verified access, not a resilience improvement — even when
a test confirms it works as written. Report it as a decision for the owner
unless an agreed requirement already settles it.
""",
    },
    "review-privacy": {
        "description": (
            "Review code changes for privacy and data-handling risks, including "
            "collection, disclosure, retention, access, and deletion. Use for "
            "/review-privacy."
        ),
        "body": """\
## Focus

Trace personal, sensitive, and identifier-like data through collection,
classification, storage, access control, logs, analytics, third parties,
retention, export, and deletion flows. Check that the change preserves data
minimization, purpose limitation, access boundaries, and deletion behavior
already required by the system.

Every privacy finding needs a data-flow path and an affected data category.
Label policy uncertainty as an evidence gap; do not invent legal requirements.
""",
    },
    "review-testing": {
        "description": (
            "Review test strategy and verification evidence for changed behavior. "
            "Use for /review-testing and requests to find test gaps."
        ),
        "body": """\
## Focus

Start with the behavior the change claims to establish, then identify the
smallest reliable verification for it. Inspect the tests actually affected and
their assertions, fixtures, mocks, isolation, and negative cases. Prefer
targeted tests, builds, type checks, simulations, property tests, fuzzing, and
end-to-end flows when the repository supports them.

Do not demand tests mechanically. Explain the failure mode a missing test
would expose and why existing evidence does not cover it.

More tests are not automatically better evidence. For each important test, ask
which assumption it challenges. Tests of more timeouts, more exception types,
or more branches of the same mechanism can all repeat the implementation's
explanation instead of challenging it. A useful test separates the events that
matter — for example, *the payment succeeds, then its response is lost* — and
checks the next step against the real behavior of the system involved.

Inspect what each mock or fake asserts about the outside world. If its
behavior was written to make the implementation pass rather than taken from a
documented contract or observed behavior, it is inherited evidence: report the
gap and name the contract or integration test that would settle it.
""",
    },
    "review-performance": {
        "description": (
            "Review code changes for performance, resource use, scale assumptions, "
            "benchmarks, and latency or throughput regressions. Use for "
            "/review-performance."
        ),
        "body": """\
## Focus

Trace changed hot paths, query patterns, allocations, network calls, cache
behavior, fan-out, batching, retries, and algorithmic complexity. Identify the
input size, concurrency, or traffic assumption under which the change matters.

Use existing benchmarks, profiling, production measurements, or controlled
comparisons when available. Do not claim a performance regression from
complexity intuition alone; report missing measurements as an evidence gap.
""",
    },
}


def render(name: str, spec: dict[str, str]) -> str:
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {spec['description']}\n"
        "license: MIT\n"
        "---\n\n"
        f"# {name}\n\n"
        f"{spec['body']}\n\n"
        f"{COMMON}"
    )


def generated_files() -> dict[Path, str]:
    return {
        ROOT / location / name / "SKILL.md": render(name, spec)
        for location in LOCATIONS
        for name, spec in SKILLS.items()
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="fail if generated skills drift")
    args = parser.parse_args()

    drift = []
    for path, content in generated_files().items():
        if not path.exists() or path.read_text(encoding="utf-8") != content:
            drift.append(path.relative_to(ROOT))
            if not args.check:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")

    if args.check and drift:
        print("Generated skills are out of date:", file=sys.stderr)
        for path in drift:
            print(f"  {path}", file=sys.stderr)
        return 1
    if not args.check:
        print(f"Generated {len(generated_files())} skill files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

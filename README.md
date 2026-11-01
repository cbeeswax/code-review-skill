# Evidence-driven code review skills

A public, multi-agent code-review skill pack for GitHub Copilot, Claude Code,
and Agent Skills-compatible tools.

The pack reviews **intent and evidence**, not a diff in isolation. It chooses
review depth from the change's risk, asks for verification the repository can
actually run, and separates verified findings from evidence gaps.

## What is included

| Skill | Purpose |
| --- | --- |
| `/code-review` | Dispatcher: scopes the change, sets risk, selects lenses, and assembles the report. |
| `/review-correctness` | Functional behavior, root cause, and implementation defects. |
| `/review-regressions` | Before/after behavior, compatibility, state, and migration regressions. |
| `/review-architecture` | Boundaries, invariants, dependencies, and reusable patterns. |
| `/review-risk` | Blast radius, rollout, rollback, observability, and operational failures. |
| `/review-security` | Security boundaries, trust assumptions, and exploitable vulnerabilities. |
| `/review-privacy` | Data collection, disclosure, retention, access, and deletion risks. |
| `/review-testing` | Test strategy, executable verification, and missing failure cases. |
| `/review-performance` | Resource use, scale assumptions, benchmarks, and performance regressions. |

## Evidence policy

Every review produces an evidence ledger containing the requested behavior,
constraints, verification performed, results, unresolved gaps, rollback plan,
and residual risk.

Findings require a file/line reference, concrete impact, a reproducer or
behavior trace, and a remediation or verification step. A missing test,
contract, or trace is an **evidence gap**, not a defect claim. Only
high-confidence, evidence-backed findings may be posted to a pull request, and
only when the user explicitly asks for posting.

## Install

Clone this repository and use the location your agent discovers:

```text
.github/skills/   GitHub Copilot project skills
.claude/skills/   Claude Code project skills
.agents/skills/   Agent Skills-compatible project skills
```

For GitHub Copilot CLI, start `copilot` from a cloned checkout and use
`/skills reload`. For Claude Code, copy or link `.claude/skills` into the
target project if the repository is not already present.

## Usage

Use the dispatcher for most requests:

```text
/code-review Review the current pull request. Run the required checks and
report high-confidence findings plus evidence gaps.
```

Call a focused lens when needed:

```text
/review-architecture Review this change for boundary and invariant violations.
/review-regressions Check the migration for backward-compatibility regressions.
```

To post to a GitHub pull request, explicitly request it and provide the PR.
The skill posts only verified, high-confidence actionable findings plus one
summary, using the available GitHub integration. It does not post, approve,
merge, or change code by default.

## Development

The canonical skill source is `scripts/generate_skills.py`. It generates and
checks in identical skill folders for all three ecosystems:

```bash
python scripts/generate_skills.py
python scripts/generate_skills.py --check
python -m unittest discover -s tests -v
```

## Inspiration

The evidence-first approach is informed by Anthropic's discussion of
[code review at agent scale](https://claude.dev/blog/solving-code-review-at-anthropic/)
and [agent-scale source control](https://www.anthropic.com/research/redesigning-source-control).
This project is independent and does not reproduce Anthropic's internal
systems or trained reviewers.

## License

MIT.

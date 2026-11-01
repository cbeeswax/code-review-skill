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

Inline PR comments lead with the business consequence: who is affected, what
can go wrong, and when. The supporting file/line evidence and technical cause
come after that plain-language context. A comment without a clear, evidence-
backed business consequence stays in the local report.

## Install in another repository

Clone this repository once:

```powershell
git clone https://github.com/cbeeswax/code-review-skill.git
```

Then copy the skills into the repository you want to review.

### GitHub Copilot

**Project-only install** (commit the skills with the reviewed repository if
the whole team should use them):

```powershell
New-Item -ItemType Directory -Force C:\path\to\your-project\.github\skills | Out-Null
Copy-Item -Recurse code-review-skill\.github\skills\* C:\path\to\your-project\.github\skills\
cd C:\path\to\your-project
copilot
```

Run `/skills reload`, then invoke `/code-review` or a focused review skill.

**Personal install** (available from every repository):

```powershell
New-Item -ItemType Directory -Force $HOME\.copilot\skills | Out-Null
Copy-Item -Recurse code-review-skill\.github\skills\* $HOME\.copilot\skills\
```

Restart Copilot CLI or run `/skills reload`.

### Claude Code

**Project-only install:**

```powershell
New-Item -ItemType Directory -Force C:\path\to\your-project\.claude\skills | Out-Null
Copy-Item -Recurse code-review-skill\.claude\skills\* C:\path\to\your-project\.claude\skills\
```

**Personal install:**

```powershell
New-Item -ItemType Directory -Force $HOME\.claude\skills | Out-Null
Copy-Item -Recurse code-review-skill\.claude\skills\* $HOME\.claude\skills\
```

### Agent Skills-compatible tools

Copy the standard Agent Skills directory into the target project:

```powershell
New-Item -ItemType Directory -Force C:\path\to\your-project\.agents\skills | Out-Null
Copy-Item -Recurse code-review-skill\.agents\skills\* C:\path\to\your-project\.agents\skills\
```

Tools that support personal Agent Skills can use:

```powershell
New-Item -ItemType Directory -Force $HOME\.agents\skills | Out-Null
Copy-Item -Recurse code-review-skill\.agents\skills\* $HOME\.agents\skills\
```

All three directories contain the same generated skill content. Choose the
directory your agent discovers; do not install all three into the same target
repository unless that repository intentionally supports multiple agents.

## Usage

Use the dispatcher for most requests:

```text
/code-review Review the current pull request. Run the required checks and
report high-confidence findings plus evidence gaps.
```

The dispatcher chooses the review lenses from the change's risk and loads their
instructions automatically. You only need to call a focused skill when you
want that single perspective or want it emphasized.

Call a focused lens when needed:

```text
/review-architecture Review this change for boundary and invariant violations.
/review-regressions Check the migration for backward-compatibility regressions.
```

To post to a GitHub pull request, explicitly request it and provide the PR.
The skill posts only verified, high-confidence actionable findings inline,
written in business context first, plus one business-impact summary. It does
not post, approve, merge, or change code by default.

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

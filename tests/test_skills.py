from pathlib import Path
import subprocess
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
LOCATIONS = (".github/skills", ".claude/skills", ".agents/skills")
NAMES = {
    "code-review",
    "review-correctness",
    "review-regressions",
    "review-architecture",
    "review-risk",
    "review-security",
    "review-privacy",
    "review-testing",
    "review-performance",
}


class GeneratedSkillTests(unittest.TestCase):
    def test_generated_skills_are_current(self):
        result = subprocess.run(
            [sys.executable, "scripts/generate_skills.py", "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_skill_locations_are_identical(self):
        reference = ROOT / LOCATIONS[0]
        for name in NAMES:
            expected = (reference / name / "SKILL.md").read_text(encoding="utf-8")
            for location in LOCATIONS[1:]:
                actual = (ROOT / location / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertEqual(actual, expected, f"{location}/{name} drifted")

    def test_every_skill_has_required_frontmatter(self):
        for location in LOCATIONS:
            found = {path.parent.name for path in (ROOT / location).glob("*/SKILL.md")}
            self.assertEqual(found, NAMES)
            for name in NAMES:
                content = (ROOT / location / name / "SKILL.md").read_text(encoding="utf-8")
                self.assertTrue(content.startswith(f"---\nname: {name}\n"))
                self.assertIn("description: ", content)

    def test_skills_require_business_context_for_inline_comments(self):
        content = (ROOT / ".github/skills/code-review/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("## Inline comment style", content)
        self.assertIn("Business context first", content)
        self.assertIn("A customer could be charged twice after a payment timeout", content)

    def test_every_skill_challenges_shared_assumptions(self):
        for name in NAMES:
            content = (ROOT / ".github/skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Challenge the shared assumption", content, name)
            self.assertIn("What would show that this reasoning is wrong?", content, name)
            self.assertIn("**independent**", content, name)
            self.assertIn("**inherited**", content, name)
            self.assertIn("Agreement is not independence.", content, name)

    def test_impact_confidence_and_verification_stay_separate(self):
        for name in NAMES:
            content = (ROOT / ".github/skills" / name / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn("## Impact, confidence, and verification", content, name)
            self.assertIn("never\nblend them into one reassuring score", content, name)
            self.assertIn("decision for\nthe owner", content, name)
            self.assertIn("where confidence stops", content, name)

    def test_dispatcher_lets_risk_decide_the_evidence(self):
        content = (ROOT / ".github/skills/code-review/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("## Let risk decide the evidence required", content)
        self.assertIn("Do not approve it yourself.", content)
        self.assertIn("not cleared by another approval", content)
        self.assertIn("do not\n   treat their agreement as independent evidence", content)

    def test_lenses_cover_the_part_three_failure_modes(self):
        def lens(name):
            return (ROOT / ".github/skills" / name / "SKILL.md").read_text(encoding="utf-8")

        self.assertIn("the payment succeeds, then its response is lost", lens("review-testing"))
        self.assertIn("inherited evidence", lens("review-testing"))
        self.assertIn("fail-open", lens("review-security"))
        self.assertIn("preserves the promise", lens("review-correctness"))
        self.assertIn("remains unknown", lens("review-risk"))

    def test_dispatcher_loads_selected_review_lenses(self):
        content = (ROOT / ".github/skills/code-review/SKILL.md").read_text(
            encoding="utf-8"
        )
        self.assertIn("Load and follow the selected sibling skill instructions", content)
        self.assertIn("review-security", content)
        self.assertIn("review-performance", content)


if __name__ == "__main__":
    unittest.main()

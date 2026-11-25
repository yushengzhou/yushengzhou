import unittest

from profile_checks import DECISION_NEEDLES, check_docs, materialize

REPO = __import__("pathlib").Path(__file__).resolve().parents[1]


class InputDocs(unittest.TestCase):
    def test_docs_happy_inputs_and_decision(self):
        self.assertEqual(check_docs(REPO), [])

    def test_docs_failure_when_spec_missing(self):
        with materialize({}) as root:
            errors = check_docs(root)
        self.assertIn("missing docs/spec.md", errors)
        self.assertIn("missing docs/decisions.md", errors)

    def test_decision_edge_wrong_date(self):
        text = "\n".join(needle if needle != "2026-11-25" else "2026-11-24" for needle in DECISION_NEEDLES)
        with materialize({"docs/decisions.md": text + "\n"}) as root:
            errors = check_docs(root)
        self.assertTrue(any("2026-11-25" in error for error in errors))

    def test_decision_failure_when_pin_missing(self):
        kept = [needle for needle in DECISION_NEEDLES if not needle.startswith("d8f67150")]
        with materialize({"docs/decisions.md": "\n".join(kept) + "\n"}) as root:
            errors = check_docs(root)
        self.assertTrue(any("d8f6715049803e982ee5ff501b6b9b7d5deeb09b" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

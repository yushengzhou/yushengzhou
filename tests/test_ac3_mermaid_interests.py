import unittest

from profile_checks import INTEREST_LABELS, check_ac3, materialize, valid_files

REPO = __import__("pathlib").Path(__file__).resolve().parents[1]


class MermaidInterests(unittest.TestCase):
    def test_ac3_happy_interest_flowchart(self):
        self.assertEqual(check_ac3(REPO), [])

    def test_ac3_edge_minimal_valid_fixture(self):
        with materialize(valid_files()) as root:
            self.assertEqual(check_ac3(root), [])

    def test_ac3_failure_when_mermaid_missing(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace("```mermaid", "```text")
        with materialize(files) as root:
            errors = check_ac3(root)
        self.assertTrue(any("expected one mermaid diagram, found 0" in error for error in errors))

    def test_ac3_failure_when_direction_is_lr(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace("flowchart TD", "flowchart LR", 1)
        with materialize(files) as root:
            errors = check_ac3(root)
        self.assertTrue(any("disallowed direction" in error or "flowchart TD" in error for error in errors))

    def test_ac3_edge_click_directive(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(
            "  registers --> methods\n```",
            '  registers --> methods\n  click exposures "https://example.com"\n```',
            1,
        )
        with materialize(files) as root:
            errors = check_ac3(root)
        self.assertIn("mermaid diagram contains a click directive", errors)

    def test_ac3_edge_init_directive(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(
            "flowchart TD\n",
            "%%{init: {'theme': 'neutral'}}%%\nflowchart TD\n",
            1,
        )
        with materialize(files) as root:
            errors = check_ac3(root)
        self.assertIn("mermaid diagram contains an init directive", errors)

    def test_ac3_edge_missing_one_interest(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(
            f"  registers[{INTEREST_LABELS[4]}]\n",
            "",
        )
        with materialize(files) as root:
            errors = check_ac3(root)
        self.assertIn("mermaid diagram is missing an interest label", errors)

    def test_ac3_edge_invented_sixth_node(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(
            "flowchart TD\n",
            "flowchart TD\n  extra[An invented topic]\n",
            1,
        )
        with materialize(files) as root:
            errors = check_ac3(root)
        self.assertIn("mermaid diagram has an unexpected node label", errors)

    def test_ac3_edge_label_too_long(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(
            INTEREST_LABELS[0],
            "Extreme heat " + ("and greenspace " * 12),
            1,
        )
        with materialize(files) as root:
            errors = check_ac3(root)
        self.assertIn("mermaid label is too long for the content column", errors)


if __name__ == "__main__":
    unittest.main()

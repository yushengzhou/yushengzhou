import unittest

from profile_checks import check_ac1, materialize, valid_files

REPO = __import__("pathlib").Path(__file__).resolve().parents[1]


class ProfileVisible(unittest.TestCase):
    def test_ac1_happy_profile_readme(self):
        self.assertEqual(check_ac1(REPO), [])

    def test_ac1_edge_minimal_valid_fixture(self):
        with materialize(valid_files()) as root:
            self.assertEqual(check_ac1(root), [])

    def test_ac1_failure_when_readme_missing(self):
        with materialize({}) as root:
            errors = check_ac1(root)
        self.assertIn("missing README.md", errors)

    def test_ac1_failure_when_readme_empty(self):
        with materialize({"README.md": ""}) as root:
            errors = check_ac1(root)
        self.assertIn("README.md is empty", errors)

    def test_ac1_edge_whitespace_only(self):
        with materialize({"README.md": " \n\t\n"}) as root:
            errors = check_ac1(root)
        self.assertIn("README.md is empty", errors)

    def test_ac1_edge_html_comment_only(self):
        with materialize({"README.md": "<!-- hidden -->\n"}) as root:
            errors = check_ac1(root)
        self.assertIn("README.md has no visible content", errors)

    def test_ac1_edge_default_github_stub(self):
        files = valid_files()
        files["README.md"] = "Here are some ideas to get you started\n"
        with materialize(files) as root:
            errors = check_ac1(root)
        self.assertIn("README.md is still the default GitHub profile stub", errors)


if __name__ == "__main__":
    unittest.main()

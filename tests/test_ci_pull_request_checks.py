import unittest

from profile_checks import CHECKOUT, check_ci, materialize, valid_files

REPO = __import__("pathlib").Path(__file__).resolve().parents[1]


class PullRequestChecks(unittest.TestCase):
    def test_ci_happy_pull_request_checks(self):
        self.assertEqual(check_ci(REPO), [])

    def test_ci_edge_minimal_valid_fixture(self):
        with materialize(valid_files()) as root:
            self.assertEqual(check_ci(root), [])

    def test_ci_failure_when_workflow_missing(self):
        files = valid_files()
        del files[".github/workflows/checks.yml"]
        with materialize(files) as root:
            errors = check_ci(root)
        self.assertIn("missing .github/workflows/checks.yml", errors)

    def test_ci_failure_contents_write(self):
        files = valid_files()
        files[".github/workflows/checks.yml"] = files[".github/workflows/checks.yml"].replace(
            "contents: read",
            "contents: write",
        )
        with materialize(files) as root:
            errors = check_ci(root)
        self.assertTrue(any("permissions are" in error for error in errors))

    def test_ci_edge_unpinned_action(self):
        files = valid_files()
        files[".github/workflows/checks.yml"] = files[".github/workflows/checks.yml"].replace(
            CHECKOUT,
            "actions/checkout@v7",
        )
        with materialize(files) as root:
            errors = check_ci(root)
        self.assertTrue(any("not pinned" in error or "must only use" in error for error in errors))

    def test_ci_edge_missing_unittest_command(self):
        files = valid_files()
        files[".github/workflows/checks.yml"] = files[".github/workflows/checks.yml"].replace(
            "python3 -m unittest discover -s tests -v",
            "python3 -m unittest discover -s other -v",
        )
        with materialize(files) as root:
            errors = check_ci(root)
        self.assertIn("checks workflow does not run the acceptance checks", errors)


if __name__ == "__main__":
    unittest.main()

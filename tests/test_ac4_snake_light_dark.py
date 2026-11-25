import unittest

from profile_checks import SNAKE_DARK, check_ac4, materialize, valid_files

REPO = __import__("pathlib").Path(__file__).resolve().parents[1]


class SnakeLightDark(unittest.TestCase):
    def test_ac4_happy_snake_workflow_and_readme(self):
        self.assertEqual(check_ac4(REPO), [])

    def test_ac4_edge_minimal_valid_fixture(self):
        with materialize(valid_files()) as root:
            self.assertEqual(check_ac4(root), [])

    def test_ac4_failure_when_action_not_pinned(self):
        files = valid_files()
        files[".github/workflows/snake.yml"] = files[".github/workflows/snake.yml"].replace(
            "Platane/snk/svg-only@d8f6715049803e982ee5ff501b6b9b7d5deeb09b",
            "Platane/snk/svg-only@v3.5.0",
        )
        with materialize(files) as root:
            errors = check_ac4(root)
        self.assertTrue(any("not pinned" in error or "not checkout then" in error for error in errors))

    def test_ac4_failure_when_contents_not_write(self):
        files = valid_files()
        text = files[".github/workflows/snake.yml"]
        text = text.replace("contents: write", "contents: read", 1)
        files[".github/workflows/snake.yml"] = text
        with materialize(files) as root:
            errors = check_ac4(root)
        self.assertTrue(any("permissions are" in error for error in errors))

    def test_ac4_edge_missing_dark_svg_url(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(SNAKE_DARK, SNAKE_DARK.replace("-dark", ""))
        with materialize(files) as root:
            errors = check_ac4(root)
        self.assertTrue(any("no light/dark picture" in error for error in errors))

    def test_ac4_edge_extra_permission(self):
        files = valid_files()
        files[".github/workflows/snake.yml"] = files[".github/workflows/snake.yml"].replace(
            "  contents: write\n",
            "  contents: write\n  pull-requests: write\n",
            1,
        )
        with materialize(files) as root:
            errors = check_ac4(root)
        self.assertTrue(any("permissions are" in error for error in errors))

    def test_ac4_edge_cron_not_0500_utc(self):
        files = valid_files()
        files[".github/workflows/snake.yml"] = files[".github/workflows/snake.yml"].replace(
            'cron: "0 5 * * *"',
            'cron: "0 6 * * *"',
        )
        with materialize(files) as root:
            errors = check_ac4(root)
        self.assertTrue(any("snake cron" in error for error in errors))

    def test_ac4_failure_third_party_deploy_action(self):
        files = valid_files()
        files[".github/workflows/snake.yml"] += "\n# JamesIves/github-pages-deploy-action\n"
        with materialize(files) as root:
            errors = check_ac4(root)
        self.assertTrue(any("third-party deploy" in error for error in errors))

    def test_ac4_edge_pat_secret(self):
        files = valid_files()
        files[".github/workflows/snake.yml"] = files[".github/workflows/snake.yml"].replace(
            "secrets.GITHUB_TOKEN",
            "secrets.GH_PAT",
        )
        with materialize(files) as root:
            errors = check_ac4(root)
        self.assertTrue(any("personal access token" in error or "secrets are" in error for error in errors))

    def test_ac4_edge_push_targets_main(self):
        files = valid_files()
        files[".github/workflows/snake.yml"] = files[".github/workflows/snake.yml"].replace(
            "HEAD:refs/heads/output",
            "HEAD:refs/heads/main",
        )
        with materialize(files) as root:
            errors = check_ac4(root)
        self.assertTrue(any("force-push only" in error or "pushes main" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

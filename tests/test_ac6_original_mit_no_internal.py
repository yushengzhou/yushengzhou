import unittest

from profile_checks import COPYRIGHT, check_ac6, materialize, valid_files

REPO = __import__("pathlib").Path(__file__).resolve().parents[1]


def _marker(kind: str) -> str:
    if kind == "path":
        return "/" + "workspace"
    if kind == "alias":
        return "Rooty" + "29"
    if kind == "note":
        return "connec" + "tor"
    raise AssertionError(kind)


class OriginalMit(unittest.TestCase):
    def test_ac6_happy_mit_license_and_clean_tree(self):
        self.assertEqual(check_ac6(REPO), [])

    def test_ac6_edge_minimal_valid_fixture(self):
        with materialize(valid_files()) as root:
            self.assertEqual(check_ac6(root), [])

    def test_ac6_failure_missing_license(self):
        files = valid_files()
        del files["LICENSE"]
        with materialize(files) as root:
            errors = check_ac6(root)
        self.assertIn("missing LICENSE", errors)

    def test_ac6_failure_internal_path(self):
        files = valid_files()
        files["README.md"] += "\n" + _marker("path") + "\n"
        with materialize(files) as root:
            errors = check_ac6(root)
        self.assertTrue(any("forbidden internal marker (path)" in error for error in errors))

    def test_ac6_failure_private_account_alias(self):
        files = valid_files()
        files["docs-note.txt"] = _marker("alias")
        with materialize(files) as root:
            errors = check_ac6(root)
        self.assertTrue(any("forbidden internal marker (alias)" in error for error in errors))

    def test_ac6_failure_internal_note(self):
        files = valid_files()
        files[".github/workflows/snake.yml"] += "\n# " + _marker("note") + "\n"
        with materialize(files) as root:
            errors = check_ac6(root)
        self.assertTrue(any("forbidden internal marker (note)" in error for error in errors))

    def test_ac6_edge_borrowed_branding_in_readme(self):
        files = valid_files()
        files["README.md"] += "\n" + "BE" + "Pb" + "\n"
        with materialize(files) as root:
            errors = check_ac6(root)
        self.assertTrue(any("disallowed branding" in error for error in errors))

    def test_ac6_edge_wrong_copyright_year(self):
        files = valid_files()
        files["LICENSE"] = files["LICENSE"].replace(COPYRIGHT, "Copyright (c) 2025 Yusheng Zhou")
        with materialize(files) as root:
            errors = check_ac6(root)
        self.assertTrue(any("copyright line" in error for error in errors))

    def test_ac6_edge_phone_link(self):
        files = valid_files()
        files["README.md"] += "\n[Phone](tel:+4500000000)\n"
        with materialize(files) as root:
            errors = check_ac6(root)
        self.assertTrue(any("phone link" in error for error in errors))

    def test_ac6_edge_branding_allowed_in_source_docs(self):
        files = valid_files()
        files["docs/spec.md"] = "Acceptance criteria\nSee " + "BE" + "Pb" + " for ideas only.\n"
        with materialize(files) as root:
            errors = check_ac6(root)
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()

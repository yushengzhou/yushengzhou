import unittest

from profile_checks import EMAIL, ORCID, SITE, check_ac5, materialize, valid_files

REPO = __import__("pathlib").Path(__file__).resolve().parents[1]


class ContactLinks(unittest.TestCase):
    def test_ac5_happy_three_contact_links(self):
        self.assertEqual(check_ac5(REPO), [])

    def test_ac5_edge_minimal_valid_fixture(self):
        with materialize(valid_files()) as root:
            self.assertEqual(check_ac5(root), [])

    def test_ac5_failure_wrong_email(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(EMAIL, "mailto:someone@example.com")
        with materialize(files) as root:
            errors = check_ac5(root)
        self.assertIn("contact links are not exactly the site, ORCID, and email", errors)

    def test_ac5_edge_site_not_https(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(SITE, "http://yushengzhou.github.io")
        with materialize(files) as root:
            errors = check_ac5(root)
        self.assertIn("site link is not https", errors)

    def test_ac5_edge_orcid_typo(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(ORCID, ORCID[:-1] + "0")
        with materialize(files) as root:
            errors = check_ac5(root)
        self.assertIn("contact links are not exactly the site, ORCID, and email", errors)

    def test_ac5_failure_extra_mailto(self):
        files = valid_files()
        files["README.md"] += "\n- [Other](mailto:other@example.com)\n"
        with materialize(files) as root:
            errors = check_ac5(root)
        self.assertIn("contact links are not exactly the site, ORCID, and email", errors)

    def test_ac5_edge_trailing_slash_on_site(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(f"]({SITE})", f"]({SITE}/)", 1)
        with materialize(files) as root:
            errors = check_ac5(root)
        self.assertIn("contact links are not exactly the site, ORCID, and email", errors)


if __name__ == "__main__":
    unittest.main()

import unittest

from profile_checks import (
    NAME,
    TAGLINES,
    TYPING_DARK,
    TYPING_LIGHT,
    check_ac2,
    materialize,
    typing_svg,
    valid_files,
)

REPO = __import__("pathlib").Path(__file__).resolve().parents[1]


class TypingNameRole(unittest.TestCase):
    def test_ac2_happy_typing_name_and_role(self):
        self.assertEqual(check_ac2(REPO), [])

    def test_ac2_edge_minimal_valid_fixture(self):
        with materialize(valid_files()) as root:
            self.assertEqual(check_ac2(root), [])

    def test_ac2_failure_when_svg_contains_script(self):
        files = valid_files()
        files[TYPING_LIGHT] += "\n<script>bad()</script>\n"
        with materialize(files) as root:
            errors = check_ac2(root)
        self.assertTrue(any("contains a script" in error for error in errors))

    def test_ac2_failure_when_name_missing_from_svg(self):
        files = valid_files()
        files[TYPING_LIGHT] = typing_svg("#ffffff").replace(NAME, "Someone Else")
        with materialize(files) as root:
            errors = check_ac2(root)
        self.assertTrue(any(f"does not include {NAME}" in error for error in errors))

    def test_ac2_edge_name_only_in_comment(self):
        files = valid_files()
        files[TYPING_LIGHT] = (
            '<svg xmlns="http://www.w3.org/2000/svg">'
            f"<!-- {NAME} {TAGLINES[0]} -->"
            "<text>Hello</text>"
            '<animate attributeName="opacity" dur="1s" repeatCount="indefinite" values="1;0"/>'
            "</svg>"
        )
        with materialize(files) as root:
            errors = check_ac2(root)
        self.assertTrue(any(f"{TYPING_LIGHT} text does not include {NAME}" in error for error in errors))

    def test_ac2_edge_animation_does_not_loop(self):
        files = valid_files()
        files[TYPING_DARK] = typing_svg("#0d1117").replace('repeatCount="indefinite"', 'repeatCount="1"')
        with materialize(files) as root:
            errors = check_ac2(root)
        self.assertTrue(any("does not loop" in error for error in errors))

    def test_ac2_failure_when_postdoc_title_returns(self):
        files = valid_files()
        files[TYPING_LIGHT] = typing_svg("#ffffff").replace(TAGLINES[0], "Postdoctoral Researcher")
        with materialize(files) as root:
            errors = check_ac2(root)
        self.assertTrue(any(f"does not include {TAGLINES[0]}" in error for error in errors))

    def test_ac2_edge_light_and_dark_identical(self):
        files = valid_files()
        files[TYPING_DARK] = files[TYPING_LIGHT]
        with materialize(files) as root:
            errors = check_ac2(root)
        self.assertIn("light and dark typing SVGs are identical", errors)

    def test_ac2_edge_dark_scheme_points_at_light_svg(self):
        files = valid_files()
        files["README.md"] = files["README.md"].replace(
            f'(prefers-color-scheme: dark)" srcset="{TYPING_DARK}"',
            f'(prefers-color-scheme: dark)" srcset="{TYPING_LIGHT}"',
            1,
        )
        with materialize(files) as root:
            errors = check_ac2(root)
        self.assertTrue(any("no light/dark picture" in error for error in errors))

    def test_ac2_failure_third_party_typing_endpoint(self):
        files = valid_files()
        files["README.md"] += "\nhttps://" + "readme-typing-" + "svg." + "demo" + "lab.com/demo\n"
        with materialize(files) as root:
            errors = check_ac2(root)
        self.assertIn("typing intro uses a third-party endpoint", errors)


if __name__ == "__main__":
    unittest.main()

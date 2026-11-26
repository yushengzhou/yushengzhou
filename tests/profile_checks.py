"""Acceptance checks for the yushengzhou profile README.

The functions take a repository root and return a list of problems.
An empty list means the check passed. The standard-library unittest
modules under tests/ are the runner; this module is not a test file.
"""

from __future__ import annotations

import html
import os
import re
import tempfile
from contextlib import contextmanager
from pathlib import Path

CHECKOUT = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"
CHECKOUT_VERSION = "v7.0.1"
SNAKE_ACTION = "Platane/snk/svg-only@d8f6715049803e982ee5ff501b6b9b7d5deeb09b"
SNAKE_VERSION = "v3.5.0"

SNAKE_LIGHT = "https://raw.githubusercontent.com/yushengzhou/yushengzhou/output/github-snake.svg"
SNAKE_DARK = "https://raw.githubusercontent.com/yushengzhou/yushengzhou/output/github-snake-dark.svg"
TYPING_LIGHT = "assets/typing-light.svg"
TYPING_DARK = "assets/typing-dark.svg"

SITE = "https://yushengzhou.github.io"
ORCID = "https://orcid.org/0009-0003-6736-6496"
EMAIL = "mailto:yushengzhou29@hotmail.com"
CONTACT_LINKS = [SITE, ORCID, EMAIL]

NAME = "Yusheng Zhou"
# Lines typed in turn under the name. Fields, not job titles, so they do not
# change with the position (ADR-0007).
TAGLINES = [
    "Environmental Epidemiologist",
    "Climate, Environment & Cardiovascular Health",
    "R · Python · Data Science",
]
COPYRIGHT = "Copyright (c) 2026 Yusheng Zhou"

INTEREST_LABELS = [
    "Extreme heat, greenspace, and other environmental exposures",
    "Cardiovascular morbidity and mortality",
    "DLNM, multilevel and geospatial modelling, and machine-learning pipelines",
    "Sex, gender, and socioeconomic determinants",
    "Register-based epidemiology",
]

BRANDING_ALLOWLIST = {
    "docs/spec.md",
    "docs/references.md",
    "docs/requirements.md",
}

DECISION_NEEDLES = [
    "2026-11-25",
    "d8f6715049803e982ee5ff501b6b9b7d5deeb09b",
    "v3.5.0",
    "Platane/snk/svg-only",
    "with no code copied or vendored",
    "generate-snake-animation@3.5.0",
    "all-rights-reserved",
    "dahan8473/snake-and-commits",
    "Decided by Root via github chief.",
]

INPUT_DOCS = {
    "docs/spec.md": "Acceptance criteria",
    "docs/references.md": "Borrowing record",
    "docs/requirements.md": "Demand card",
}


def rel(root: Path, path: Path) -> str:
    return path.relative_to(root).as_posix()


def iter_files(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {".git", "__pycache__", ".pytest_cache"}]
        for name in filenames:
            if name.endswith((".pyc", ".pyo")):
                continue
            yield Path(dirpath) / name


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def code_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]


def internal_markers() -> list[tuple[str, str]]:
    return [
        ("/" + "workspace", "path"),
        ("Rooty" + "29", "alias"),
        ("connec" + "tor", "note"),
    ]


def branding_needles() -> list[str]:
    return [
        "BE" + "Pb",
        "And" + "rej",
        "Marin" + "chenko",
        "demo" + "lab.com",
        "heroku" + "app",
        "readme-typing-" + "svg",
        "laobi" + ".icu",
        "shields" + ".io",
        "github-readme-" + "stats",
        "github-profile-" + "trophy",
        "star-" + "history",
        "visitor-" + "badge",
        "neural " + "networks",
        "header_" + ".png",
        "Bottom_up" + ".svg",
    ]


def typing_endpoint_needles() -> list[str]:
    return [
        "demo" + "lab.com",
        "heroku" + "app",
        "readme-typing-" + "svg",
    ]


def parse_attrs(raw: str) -> dict[str, str]:
    attrs = {}
    for match in re.finditer(
        r"""([A-Za-z_:][-A-Za-z0-9_:.]*)\s*=\s*(?:"([^"]*)"|'([^']*)')""",
        raw,
    ):
        value = match.group(2) if match.group(2) is not None else match.group(3)
        attrs[match.group(1).lower()] = value
    return attrs


def pictures(markdown: str) -> list[dict[str, object]]:
    found = []
    for body in re.findall(r"<picture\b[^>]*>(.*?)</picture>", markdown, flags=re.I | re.S):
        sources = []
        for raw in re.findall(r"<source\b([^>]*)>", body, flags=re.I | re.S):
            attrs = parse_attrs(raw)
            sources.append((attrs.get("media", ""), attrs.get("srcset", "").strip()))
        img_src = ""
        alt = ""
        images = re.findall(r"<img\b([^>]*)>", body, flags=re.I | re.S)
        if images:
            attrs = parse_attrs(images[0])
            img_src = attrs.get("src", "").strip()
            alt = attrs.get("alt", "")
        found.append({"sources": sources, "img_src": img_src, "alt": alt})
    return found


def scheme_map(picture: dict[str, object]) -> dict[str, str]:
    mapping: dict[str, str] = {}
    for media, srcset in picture["sources"]:  # type: ignore[misc]
        key = media.lower().replace(" ", "")
        if "prefers-color-scheme:dark" in key:
            mapping["dark"] = srcset
        elif "prefers-color-scheme:light" in key:
            mapping["light"] = srcset
    return mapping


def mermaid_blocks(markdown: str) -> list[str]:
    blocks = []
    collecting = False
    buf: list[str] = []
    for line in markdown.splitlines():
        stripped = line.strip()
        if not collecting:
            if re.match(r"^```mermaid\s*$", stripped):
                collecting = True
                buf = []
            continue
        if stripped.startswith("```"):
            blocks.append("\n".join(buf))
            collecting = False
            buf = []
            continue
        buf.append(line)
    return blocks


def markdown_hrefs(markdown: str) -> list[str]:
    return re.findall(r"(?<!!)\[(?:[^\]]*)\]\((\S+?)\)", markdown)


def permission_blocks(text: str) -> list[dict[str, str]]:
    lines = text.splitlines()
    blocks = []
    for index, line in enumerate(lines):
        if line.strip().startswith("#") or line.strip() != "permissions:":
            continue
        block: dict[str, str] = {}
        for nxt in lines[index + 1 :]:
            if nxt.strip() == "" or nxt.strip().startswith("#"):
                continue
            if nxt[0] not in " \t":
                break
            match = re.match(r"^\s+([A-Za-z0-9_-]+):\s*(\S+)\s*$", nxt)
            if not match:
                block["__invalid__"] = "yes"
                break
            block[match.group(1)] = match.group(2)
        blocks.append(block)
    return blocks


def action_uses(text: str) -> list[tuple[str, str]]:
    found = []
    for line in code_lines(text):
        code, _, comment = line.partition("#")
        match = re.search(r"uses:\s*(\S+)", code)
        if match:
            found.append((match.group(1), comment.strip()))
    return found


def svg_text_content(svg: str) -> str:
    cleaned = re.sub(r"<!--.*?-->", "", svg, flags=re.S)
    cleaned = re.sub(r"<script\b[^>]*>.*?</script>", "", cleaned, flags=re.I | re.S)
    chunks = re.findall(r"<text\b[^>]*>(.*?)</text>", cleaned, flags=re.I | re.S)
    text = " ".join(re.sub(r"<[^>]+>", " ", chunk) for chunk in chunks)
    return html.unescape(re.sub(r"\s+", " ", text).strip())


def check_svg_file(root: Path, relative: str) -> list[str]:
    path = root / relative
    if not path.is_file():
        return [f"missing {relative}"]
    svg = read_text(path)
    errors = []
    if re.search(r"<\s*script\b", svg, flags=re.I):
        errors.append(f"{relative} contains a script")
    if re.search(r"<\s*(foreignObject|iframe|embed|object)\b", svg, flags=re.I):
        errors.append(f"{relative} contains an embedded document")
    if re.search(r"\bon[a-z]+\s*=", svg, flags=re.I):
        errors.append(f"{relative} contains an event handler")
    without_namespace = svg.replace("http://www.w3.org/2000/svg", "")
    if re.search(r"https?://", without_namespace, flags=re.I):
        errors.append(f"{relative} references an external URL")
    if not re.search(r"<animate\b", svg, flags=re.I):
        errors.append(f"{relative} has no SMIL animate element")
    if not re.search(r"""repeatCount\s*=\s*["']indefinite["']""", svg):
        errors.append(f"{relative} animation does not loop")
    visible = svg_text_content(svg)
    for required in (NAME, *TAGLINES):
        if required not in visible:
            errors.append(f"{relative} text does not include {required}")
    return errors


def expect_permissions(text: str, expected: dict[str, str]) -> list[str]:
    blocks = permission_blocks(text)
    if not blocks:
        return ["workflow is missing a permissions block"]
    errors = []
    for block in blocks:
        if block != expected:
            errors.append(f"permissions are {block}, expected {expected}")
    return errors


def check_ac1(root: Path) -> list[str]:
    path = root / "README.md"
    if not path.is_file():
        return ["missing README.md"]
    text = read_text(path)
    errors = []
    if not text.strip():
        errors.append("README.md is empty")
        return errors
    visible = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    if not visible.strip():
        errors.append("README.md has no visible content")
    if "Here are some ideas to get you started" in text:
        errors.append("README.md is still the default GitHub profile stub")
    if TYPING_LIGHT not in text or TYPING_DARK not in text:
        errors.append("README.md does not reference both typing SVGs")
    if "```mermaid" not in text:
        errors.append("README.md has no mermaid diagram")
    if SNAKE_LIGHT not in text or SNAKE_DARK not in text:
        errors.append("README.md does not reference both snake SVGs")
    for link in CONTACT_LINKS:
        if link not in text:
            errors.append(f"README.md is missing {link}")
    for fence in ("```bash", "```sh", "```shell"):
        if fence in text:
            errors.append("README.md contains setup instructions")
            break
    if "gh workflow run" in text:
        errors.append("README.md contains setup instructions")
    return errors


def typing_picture_errors(markdown: str) -> list[str]:
    errors = []
    matched = False
    for picture in pictures(markdown):
        mapping = scheme_map(picture)
        if mapping.get("dark") == TYPING_DARK and mapping.get("light") == TYPING_LIGHT:
            matched = True
            if picture["img_src"] != TYPING_LIGHT:
                errors.append("typing picture fallback is not the light SVG")
            alt = html.unescape(str(picture["alt"]))
            if any(part not in alt for part in (NAME, *TAGLINES)):
                errors.append("typing picture alt text does not include the name and every tagline")
    if not matched:
        errors.append("README.md has no light/dark picture for the typing SVGs")
    return errors


def check_ac2(root: Path) -> list[str]:
    readme_path = root / "README.md"
    errors = []
    readme = ""
    if not readme_path.is_file():
        errors.append("missing README.md")
    else:
        readme = read_text(readme_path)
        errors.extend(typing_picture_errors(readme))
    errors.extend(check_svg_file(root, TYPING_LIGHT))
    errors.extend(check_svg_file(root, TYPING_DARK))
    light = root / TYPING_LIGHT
    dark = root / TYPING_DARK
    if light.is_file() and dark.is_file() and light.read_bytes() == dark.read_bytes():
        errors.append("light and dark typing SVGs are identical")
    blob = readme
    for relative in (TYPING_LIGHT, TYPING_DARK):
        path = root / relative
        if path.is_file():
            blob += "\n" + read_text(path)
    for needle in typing_endpoint_needles():
        if needle.lower() in blob.lower():
            errors.append("typing intro uses a third-party endpoint")
            break
    return errors


def check_ac3(root: Path) -> list[str]:
    path = root / "README.md"
    if not path.is_file():
        return ["missing README.md"]
    blocks = mermaid_blocks(read_text(path))
    if len(blocks) != 1:
        return [f"expected one mermaid diagram, found {len(blocks)}"]
    block = blocks[0]
    errors = []
    if not re.search(r"(?m)^flowchart\s+TD\b", block):
        errors.append("mermaid diagram must use flowchart TD")
    if re.search(r"(?mi)\bflowchart\s+(LR|RL|BT)\b", block) or re.search(
        r"(?mi)\bgraph\s+(LR|RL|TD|BT)\b", block
    ):
        errors.append("mermaid diagram uses a disallowed direction")
    if re.search(r"(?mi)^\s*click\b", block):
        errors.append("mermaid diagram contains a click directive")
    if "%%{" in block:
        errors.append("mermaid diagram contains an init directive")
    if "-->" not in block:
        errors.append("mermaid diagram has no edges")
    labels = re.findall(r"\[([^\]\n]+)\]", block)
    expected = set(INTEREST_LABELS)
    found = set(labels)
    if len(labels) != len(found):
        errors.append("mermaid diagram repeats a node label")
    missing = expected - found
    extra = found - expected
    if missing:
        errors.append("mermaid diagram is missing an interest label")
    if extra:
        errors.append("mermaid diagram has an unexpected node label")
    if any(len(label) > 90 for label in labels):
        errors.append("mermaid label is too long for the content column")
    return errors


def check_snake_workflow(text: str) -> list[str]:
    errors = expect_permissions(text, {"contents": "write"})
    lines = code_lines(text)
    if not any(line.strip() == "workflow_dispatch:" for line in lines):
        errors.append("snake workflow is missing workflow_dispatch")
    if not any(line.strip() == "push:" for line in lines):
        errors.append("snake workflow does not run on push")
    if not any(re.match(r"-\s*main\s*$", line.strip()) for line in lines):
        errors.append("snake workflow push trigger does not include main")
    crons = []
    for line in lines:
        match = re.search(r"""cron:\s*["']([^"']+)["']""", line)
        if match:
            crons.append(match.group(1))
    if crons != ["0 5 * * *"]:
        errors.append(f"snake cron is {crons}, expected 05:00 UTC daily")
    uses = action_uses(text)
    refs = [ref for ref, _comment in uses]
    if refs != [CHECKOUT, SNAKE_ACTION]:
        errors.append("snake workflow actions are not checkout then the pinned svg-only action")
    expected_versions = {CHECKOUT: CHECKOUT_VERSION, SNAKE_ACTION: SNAKE_VERSION}
    for ref, comment in uses:
        if not re.fullmatch(r"\S+@[0-9a-f]{40}", ref):
            errors.append(f"action is not pinned to a full commit SHA: {ref}")
        version = expected_versions.get(ref)
        if version and version not in comment:
            errors.append(f"action {ref} is missing the {version} comment")
        if not re.search(r"v\d+\.\d+\.\d+", comment):
            errors.append(f"action {ref} is missing a version comment")
    if not any(line.strip() == "github_user_name: yushengzhou" for line in lines):
        errors.append("snake workflow must set github_user_name to yushengzhou")
    if "dist/github-snake.svg" not in text:
        errors.append("snake workflow does not write github-snake.svg")
    if "dist/github-snake-dark.svg?palette=github-dark" not in text:
        errors.append("snake workflow does not write the dark palette SVG")
    secrets = set(re.findall(r"secrets\.([A-Za-z0-9_]+)", text))
    if secrets != {"GITHUB_TOKEN"}:
        errors.append(f"snake workflow secrets are {sorted(secrets)}, expected only GITHUB_TOKEN")
    for banned in ("GH_PAT", "PERSONAL_ACCESS_TOKEN", "github_pat_"):
        if banned in text:
            errors.append("snake workflow refers to a personal access token")
    for banned in (
        "JamesIves",
        "crazy-max/ghaction-github-pages",
        "peaceiris/actions-gh-pages",
        "github-pages-deploy-action",
    ):
        if banned in text:
            errors.append("snake workflow uses a third-party deploy action")
    if "--all" in text or "--mirror" in text:
        errors.append("snake workflow must not push every ref")
    push_lines = [line for line in text.splitlines() if "git push" in line and not line.strip().startswith("#")]
    if len(push_lines) != 1:
        errors.append("snake workflow must publish with one git push")
    elif "--force" not in push_lines[0] or "HEAD:refs/heads/output" not in push_lines[0]:
        errors.append("snake workflow must force-push only refs/heads/output")
    elif re.search(r"\bmain\b", push_lines[0]):
        errors.append("snake workflow pushes main")
    return errors


def snake_picture_errors(markdown: str) -> list[str]:
    for picture in pictures(markdown):
        mapping = scheme_map(picture)
        if mapping.get("dark") == SNAKE_DARK and mapping.get("light") == SNAKE_LIGHT:
            if picture["img_src"] != SNAKE_LIGHT:
                return ["snake picture fallback is not the light SVG"]
            if not str(picture["alt"]).strip():
                return ["snake picture is missing alt text"]
            return []
    return ["README.md has no light/dark picture for the snake SVGs"]


def check_ac4(root: Path) -> list[str]:
    errors = []
    workflow = root / ".github" / "workflows" / "snake.yml"
    if not workflow.is_file():
        errors.append("missing .github/workflows/snake.yml")
    else:
        errors.extend(check_snake_workflow(read_text(workflow)))
    readme = root / "README.md"
    if not readme.is_file():
        errors.append("missing README.md")
    else:
        errors.extend(snake_picture_errors(read_text(readme)))
    return errors


def check_ac5(root: Path) -> list[str]:
    path = root / "README.md"
    if not path.is_file():
        return ["missing README.md"]
    text = read_text(path)
    errors = []
    hrefs = markdown_hrefs(text)
    if sorted(hrefs) != sorted(CONTACT_LINKS):
        errors.append("contact links are not exactly the site, ORCID, and email")
    if "http://yushengzhou.github.io" in text:
        errors.append("site link is not https")
    if "tel:" in text.lower():
        errors.append("README.md contains a phone link")
    return errors


def license_errors(text: str) -> list[str]:
    errors = []
    if not text.lstrip().startswith("MIT License"):
        errors.append("LICENSE must start with MIT License")
    copyrights = [line.strip() for line in text.splitlines() if line.strip().lower().startswith("copyright")]
    if copyrights != [COPYRIGHT]:
        errors.append("LICENSE copyright line is not Copyright (c) 2026 Yusheng Zhou")
    for phrase in (
        "Permission is hereby granted, free of charge",
        "The above copyright notice and this permission notice shall be included in all",
        'THE SOFTWARE IS PROVIDED "AS IS"',
        "NONINFRINGEMENT",
    ):
        if phrase not in text:
            errors.append("LICENSE is missing the MIT terms")
            break
    return errors


def check_ac6(root: Path) -> list[str]:
    license_path = root / "LICENSE"
    errors = []
    if not license_path.is_file():
        errors.append("missing LICENSE")
    else:
        errors.extend(license_errors(read_text(license_path)))
    for path in iter_files(root):
        relative = rel(root, path)
        try:
            text = read_text(path)
        except UnicodeDecodeError:
            errors.append(f"{relative} is not UTF-8 text")
            continue
        lowered = text.lower()
        for marker, code in internal_markers():
            if marker.lower() in lowered:
                errors.append(f"{relative} contains a forbidden internal marker ({code})")
        if relative not in BRANDING_ALLOWLIST:
            for needle in branding_needles():
                if needle.lower() in lowered:
                    errors.append(f"{relative} contains disallowed branding")
                    break
        if relative == "README.md" or relative == "LICENSE" or relative.startswith(("assets/", ".github/")):
            if re.search(r"\bphone\b", text, flags=re.I) or re.search(r"\breferees?\b", text, flags=re.I):
                errors.append(f"{relative} contains personal contact beyond the public profile")
            if "tel:" in lowered:
                errors.append(f"{relative} contains a phone link")
            if "placeholder" in lowered:
                errors.append(f"{relative} contains a placeholder")
    return errors


def check_ci(root: Path) -> list[str]:
    path = root / ".github" / "workflows" / "checks.yml"
    if not path.is_file():
        return ["missing .github/workflows/checks.yml"]
    text = read_text(path)
    errors = expect_permissions(text, {"contents": "read"})
    lines = code_lines(text)
    if not any(line.strip() == "pull_request:" or line.strip().startswith("pull_request:") for line in lines):
        errors.append("checks workflow does not run on pull requests")
    if any("cron:" in line or line.strip() == "schedule:" for line in lines):
        errors.append("checks workflow must not run on a schedule")
    if "python3 -m unittest discover -s tests -v" not in text:
        errors.append("checks workflow does not run the acceptance checks")
    if re.search(r"secrets\.", text):
        errors.append("checks workflow must not use secrets")
    uses = action_uses(text)
    refs = [ref for ref, _comment in uses]
    if refs != [CHECKOUT]:
        errors.append("checks workflow must only use the pinned checkout action")
    for ref, comment in uses:
        if not re.fullmatch(r"\S+@[0-9a-f]{40}", ref):
            errors.append(f"action is not pinned to a full commit SHA: {ref}")
        if ref == CHECKOUT and CHECKOUT_VERSION not in comment:
            errors.append("checkout action is missing the v7.0.1 comment")
        if not re.search(r"v\d+\.\d+\.\d+", comment):
            errors.append(f"action {ref} is missing a version comment")
    return errors


def check_docs(root: Path) -> list[str]:
    errors = []
    for relative, needle in INPUT_DOCS.items():
        path = root / relative
        if not path.is_file():
            errors.append(f"missing {relative}")
            continue
        if needle not in read_text(path):
            errors.append(f"{relative} is missing its expected heading")
    decision = root / "docs" / "decisions.md"
    if not decision.is_file():
        errors.append("missing docs/decisions.md")
        return errors
    text = read_text(decision)
    for needle in DECISION_NEEDLES:
        if needle not in text:
            errors.append(f"docs/decisions.md is missing required decision text ({needle})")
    return errors


def snake_workflow_text() -> str:
    return f"""name: Contribution snake

on:
  schedule:
    - cron: "0 5 * * *"
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  contents: write

jobs:
  generate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: {CHECKOUT} # {CHECKOUT_VERSION}

      - name: Draw the contribution snake
        uses: {SNAKE_ACTION} # {SNAKE_VERSION}
        with:
          github_user_name: yushengzhou
          github_token: ${{{{ secrets.GITHUB_TOKEN }}}}
          outputs: |
            dist/github-snake.svg
            dist/github-snake-dark.svg?palette=github-dark

      - name: Publish SVGs to the output branch
        env:
          PUSH_TOKEN: ${{{{ secrets.GITHUB_TOKEN }}}}
        run: git push --force "https://x-access-token:${{PUSH_TOKEN}}@github.com/${{GITHUB_REPOSITORY}}.git" HEAD:refs/heads/output
"""


def checks_workflow_text() -> str:
    return f"""name: Checks

on:
  pull_request:

permissions:
  contents: read

jobs:
  acceptance:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: {CHECKOUT} # {CHECKOUT_VERSION}

      - name: Run acceptance checks
        run: python3 -m unittest discover -s tests -v
"""


def typing_svg(fill: str) -> str:
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">
  <text>{NAME}</text>
  <text>{html.escape(TAGLINES[0])}</text>
  <text>{html.escape(TAGLINES[1])}</text>
  <text>{html.escape(TAGLINES[2])}</text>
  <rect width="1" height="1" fill="{fill}">
    <animate attributeName="opacity" dur="1s" repeatCount="indefinite" values="1;0;1"/>
  </rect>
</svg>
"""


def readme_text() -> str:
    labels = "\n".join(
        f"  {anchor}[{label}]"
        for anchor, label in (
            ("exposures", INTEREST_LABELS[0]),
            ("cardiovascular", INTEREST_LABELS[1]),
            ("methods", INTEREST_LABELS[2]),
            ("determinants", INTEREST_LABELS[3]),
            ("registers", INTEREST_LABELS[4]),
        )
    )
    return f"""<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{TYPING_DARK}">
  <source media="(prefers-color-scheme: light)" srcset="{TYPING_LIGHT}">
  <img alt="{html.escape(NAME + ". " + "; ".join(TAGLINES))}" src="{TYPING_LIGHT}">
</picture>

## Research interests

```mermaid
flowchart TD
{labels}
  exposures --> cardiovascular
  determinants --> cardiovascular
  methods --> cardiovascular
  registers --> methods
```

## Contributions

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="{SNAKE_DARK}">
  <source media="(prefers-color-scheme: light)" srcset="{SNAKE_LIGHT}">
  <img alt="Contribution snake" src="{SNAKE_LIGHT}">
</picture>

## Contact

- [Personal site]({SITE})
- [ORCID]({ORCID})
- [Email]({EMAIL})
"""


def license_text() -> str:
    return f"""MIT License

{COPYRIGHT}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


@contextmanager
def materialize(files: dict[str, str]):
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        yield root


def valid_files() -> dict[str, str]:
    return {
        "README.md": readme_text(),
        "LICENSE": license_text(),
        TYPING_LIGHT: typing_svg("#ffffff"),
        TYPING_DARK: typing_svg("#0d1117"),
        ".github/workflows/snake.yml": snake_workflow_text(),
        ".github/workflows/checks.yml": checks_workflow_text(),
    }

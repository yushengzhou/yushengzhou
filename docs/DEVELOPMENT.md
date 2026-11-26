# Development

How to edit this public GitHub profile and run its checks.

## Install

Python 3 is the local tool the checks need. They use the standard library only (`unittest`). No extra Python packages are installed for them.

```bash
python3 --version
```

The command should print a Python 3 version. No lint tool and no Mermaid CLI are part of this repository. The diagram is checked by the test suite below, and GitHub renders it.

## Usage

The profile page is `README.md` on `main`. This guide is where setup stays.

### Typing introduction

The introduction is two original SVGs, switched with `<picture>` and `prefers-color-scheme` (ADR-0002, ADR-0007):

- Light: `assets/typing-light.svg` (background `#ffffff`, name `#24292f`, other text `#57606a`)
- Dark: `assets/typing-dark.svg` (background `#0d1117`, name `#e6edf3`, other text `#8d96a0`)

`README.md` points the dark source at `assets/typing-dark.svg`, the light source at `assets/typing-light.svg`, and the `<img>` fallback at the light file. The image `alt` is the name followed by the three taglines.

Line 1 is static: `Yusheng Zhou` in bold with `, MPH, PhD` in a regular-weight `<tspan>`. Line 2 types three taglines in turn on a 15-second loop, 5 seconds each (type 1.6 s, hold, erase 0.5 s):

1. `Environmental Epidemiologist`
2. `Climate, Environment & Cardiovascular Health` (written `&amp;` in the SVG)
3. `R · Python · Data Science`

Each tagline is a monospace 18 px `<text>` with `textLength` set to 10.8 px per character and `lengthAdjust="spacing"`, so its width is fixed whatever monospace font the viewer has. Its `clipPath` width and caret `x` animate to that same width (caret ends at 24 plus the width). Each tagline sits in a `<g>` whose opacity is 1 only during its slot. All `<animate>` elements use `repeatCount="indefinite"`. There is no script.

The taglines are fields, not job titles, so they need no change when the position changes. To change one, edit both SVGs (the `<text>`, its `textLength`, the matching clip and caret values, and the `<title>`), the README `alt` text, and `TAGLINES` in `tests/profile_checks.py`.

### Research interests

The README has one Mermaid block. It is `flowchart TD` and its node labels are exactly these five:

1. Extreme heat, greenspace, and other environmental exposures (`exposures`)
2. Cardiovascular morbidity and mortality (`cardiovascular`)
3. DLNM, multilevel and geospatial modelling, and machine-learning pipelines (`methods`)
4. Sex, gender, and socioeconomic determinants (`determinants`)
5. Register-based epidemiology (`registers`)

The edges are `exposures --> cardiovascular`, `determinants --> cardiovascular`, `methods --> cardiovascular`, and `registers --> methods`. Keep the block on `flowchart TD`, with these labels only. It has no `%%{init}%%` directive and no `click` directive. GitHub draws the diagram and switches light and dark on its own.

### Contact

The contact section is these three links:

- Personal site: https://yushengzhou.github.io
- ORCID: https://orcid.org/0009-0003-6736-6496
- Email: mailto:yushengzhou29@hotmail.com

The site href stays on that URL. The site itself can answer 404 until https://yushengzhou.github.io is published.

### Contribution snake

`.github/workflows/snake.yml` draws the snake and publishes it.

- Schedule: cron `0 5 * * *` (05:00 UTC every day).
- `workflow_dispatch`.
- `push` to `main`.
- Permission: `contents: write` only. The only secret is `GITHUB_TOKEN`.
- `actions/checkout` is pinned to `3d3c42e5aac5ba805825da76410c181273ba90b1` (v7.0.1).
- `Platane/snk/svg-only` is pinned to `d8f6715049803e982ee5ff501b6b9b7d5deeb09b` (v3.5.0). The Action’s `github_user_name` is `yushengzhou`.
- The Action writes `dist/github-snake.svg` and `dist/github-snake-dark.svg?palette=github-dark`. The `palette` query is an input. The published files are `github-snake.svg` and `github-snake-dark.svg`.
- The publish step copies those two files, commits them as `github-actions[bot]`, and force-pushes `HEAD` to `refs/heads/output`. The `output` branch holds those two SVGs. A run does not cancel one that is already in progress.

The README loads them with `<picture>`:

- Light: `https://raw.githubusercontent.com/yushengzhou/yushengzhou/output/github-snake.svg`
- Dark: `https://raw.githubusercontent.com/yushengzhou/yushengzhou/output/github-snake-dark.svg`

Those raw URLs stay broken until the first successful run creates the `output` branch. GitHub will not `workflow_dispatch` this workflow before the file is on the default branch `main` (a dispatch before that returns workflow not found). Merging to `main` is a push, so that push starts a run. Right after the merge, start it yourself with `workflow_dispatch` if that push has not already produced the SVGs: open the Actions tab, or run `gh workflow run snake.yml --repo yushengzhou/yushengzhou`.

A later run overwrites the same raw URLs. GitHub’s camo proxy can keep serving the previous image for a while after that overwrite.

## Development

Pull requests run `.github/workflows/checks.yml` (`contents: read`). From the repository root, the check step is:

```bash
python3 -m unittest discover -s tests -v
```

No lint or format command is configured.

## License

This repository is under the MIT License. `LICENSE` is Copyright (c) 2026 Yusheng Zhou.

The snake Action `Platane/snk` is an unlicensed third-party dependency. The workflow uses it only as the pinned Action `Platane/snk/svg-only` at `d8f6715049803e982ee5ff501b6b9b7d5deeb09b` (v3.5.0). No snake source is copied into this repository. See [ADR-0001](decisions/ADR-0001-pin-platane-snk-action.md).

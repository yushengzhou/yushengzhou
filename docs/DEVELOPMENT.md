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

The introduction is two original SVGs, switched with `<picture>` and `prefers-color-scheme`:

- Light: `assets/typing-light.svg` (background `#ffffff`, text `#24292f`)
- Dark: `assets/typing-dark.svg` (background `#0d1117`, text `#e6edf3`)

`README.md` points the dark source at `assets/typing-dark.svg`, the light source at `assets/typing-light.svg`, and the `<img>` fallback at the light file. The image `alt` is `Yusheng Zhou, Postdoctoral Researcher`.

The name and the role are the character data of the `<text>` elements, and the same words are in the SVG `<title>`. In both files:

- `Yusheng Zhou` is the `<text>` clipped by `#clip-name`, with `textLength="234"`.
- `Postdoctoral Researcher` is the `<text>` clipped by `#clip-role`, with `textLength="432"`.

`textLength` with `lengthAdjust="spacingAndGlyphs"` locks each line to that width. The SMIL clip widens to the same width, and the caret’s `x` animation ends at 24 plus that width (258 for the name, 456 for the role). The `<animate>` elements use `repeatCount="indefinite"`. There is no script.

To change the name or the role, edit both SVGs so the `<text>` lines and the `<title>` stay in step, and edit the README `alt` text to match. Keep the light and dark strings the same. When the line needs a new width, update `textLength` and the matching clip and caret values in that file.

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

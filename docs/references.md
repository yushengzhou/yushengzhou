# Borrowing record — GitHub profile README

Ideas only. No code, markup, images, names, or branding from the sources below may be copied into `yushengzhou/yushengzhou`. This file is a research log, not a template.

Research date: 2026-11-25, Europe/Copenhagen. Content sources for *Root's* text: academic-site PR https://github.com/yushengzhou/yushengzhou.github.io/pull/1 (approved, unmerged) and the academic-site specification.

## Ideas borrowed

| Idea borrowed | Source | How this rewrite differs |
|---|---|---|
| Put a typing-animation intro line at the top of a GitHub profile README | [BEPb profile](https://github.com/BEPb) / [BEPb/BEPb](https://github.com/BEPb/BEPb) (MIT); pattern also popularized by [DenverCoder1/readme-typing-svg](https://github.com/DenverCoder1/readme-typing-svg) (MIT) | BEPb (and most typings) hot-link a third-party generator (`readme-typing-svg` on Heroku historically, now `readme-typing-svg.demolab.com`, still Heroku + Cloudflare — not a Vercel endpoint). This profile commits two original SMIL SVGs in-repo and switches them with `<picture>` + `prefers-color-scheme`. Text is only “Yusheng Zhou” / “Postdoctoral Researcher”. No demolab/heroku URL, no query-string lines, no copy of the generator's SVG markup or demo typography. |
| A research/skills relationship graph in a native Mermaid fence on the profile README | [BEPb profile](https://github.com/BEPb) (MIT repo) | BEPb's graph is a machine-learning skill tree (Data, Algorithms, Statistical Models, etc.). This graph uses only the five research-interest bullets from PR #1 `content/_index.en.md` (environmental exposures, cardiovascular outcomes, DLNM/geospatial/ML methods, sex/gender/socioeconomic determinants, register-based epidemiology). Different nodes, labels, and purpose. No `%%{init}%%` theme copy, no BEPb structure. GitHub-native mermaid only; graph kept small. |
| An animated contribution-graph snake, light and dark, via `<picture>` and `prefers-color-scheme` | [Platane/snk](https://github.com/Platane/snk) README usage (Action; **no license** — see SPEC); the light/dark `<picture>` pattern is also documented by [GitHub](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#specifying-the-theme-an-image-is-shown-to) | Same problem (daily snake SVGs on an `output` branch), different repo, user, and colors limited to snk's built-in `github` / `github-dark` palettes rather than a custom BEPb or ocean theme. README references raw URLs on `yushengzhou/yushengzhou@output`. **Do not vendor or copy snk source.** Action use is approved in [ADR-0001](decisions/ADR-0001-pin-platane-snk-action.md); the project is unlicensed, so the workflow pins the Action and does not vendor its source. Publish with `git push`, not by copying a third-party workflow file wholesale. |
| Daily regeneration of the snake with GitHub Actions (`schedule` + manual dispatch) and `GITHUB_TOKEN` | [Platane/snk](https://github.com/Platane/snk) Action docs and [example workflow idea](https://github.com/Platane/Platane/blob/master/.github/workflows/main.yml) | Rewrite a minimal workflow in-repo: cron `0 5 * * *`, `workflow_dispatch`, push to `main`; permissions `contents: write` only; pin `Platane/snk/svg-only` and `actions/checkout` by SHA; no PAT; no Pages artifact. Do not copy Platane's or BEPb's workflow files. |
| A short contact block with site / scholarly ID / email | Common profile-README convention; BEPb has a “how to reach me” block | Only three links Root chose: https://yushengzhou.github.io, https://orcid.org/0009-0003-6736-6496, and the site's public email. No social badge row, no chat widgets, no phone, no referees, no BEPb contact channels or icons. |
| Prefer self-hosted or committed SVGs over a public typing service (uptime / privacy) | [readme-typing-svg README](https://github.com/DenverCoder1/readme-typing-svg) (“preferable to host the files on your own server”); reliability notes such as [issue #444](https://github.com/DenverCoder1/readme-typing-svg/issues/444) | We go further than self-hosting their PHP app: the animation is an original static SVG with no runtime service at all. |

## Must not copy — BEPb distinctive elements

BEPb/BEPb is MIT (Copyright 2022 Andrej Marinchenko). MIT would allow reuse *with* attribution, but Root's rule for this project is **ideas only**: no copied text, images, code, names, or branding. Do not use that MIT grant as permission to paste.

Do **not** take any of the following (non-exhaustive):

- The name Andrej Marinchenko, the handle BEPb, the bio line “I make simple things with neural networks,” or any other first-person copy from that profile.
- Header/banner artwork and decorative SVGs (including assets such as `header_.png`, `Bottom_up.svg`, and anything under `src/`).
- The skill/tech badge tables (Language / IDE, Domain Knowledge, CI/CD, Databases, ML frameworks, and the specific badge set).
- Shields.io badge walls, visitor counters (including visitor-badge.laobi.icu), GitHub stats cards, GitHub trophies, Hackerrank trophies, star-history or activity-graph widgets.
- The GeoJSON / map block and any location artwork.
- The machine-learning Mermaid graph (node names, edges, and layout).
- Typing-SVG lines, colors, fonts, or the herokuapp/demolab URL pattern used there.
- Layout, section order beyond the four elements Root picked, emoji clusters, color palette, or overall visual branding.

Root already placed skill badges, stats cards, trophies, visitor counters, star history, auto-follow, phone, and referees **out of scope**.

## Tools checked (not copied)

| Tool | License | Role in this project |
|---|---|---|
| Platane/snk (and npm `generate-snake-animation@3.5.0`) | **No license** (high risk) | Approved pinned Action dependency ([ADR-0001](decisions/ADR-0001-pin-platane-snk-action.md)). Do not vendor source. |
| dahan8473/snake-and-commits | MIT | Inspected as a licensed alternative; rejected as primary (no releases, small/young). |
| jkdevcode/snake_animation, HowardZlh/github-action-shares | MIT (where declared) | Not used; not mature substitutes for snk. |
| DenverCoder1/readme-typing-svg | MIT (Twemoji, if used, is CC-BY 4.0) | Not used at runtime; idea only. Do not copy SVG output or demo HTML. |
| actions/checkout | MIT | Used, pinned by SHA. |
| JamesIves/github-pages-deploy-action, crazy-max/ghaction-github-pages | MIT | Recorded, not chosen (git push instead). |
| rahuldkjain/github-profile-readme-generator | Apache-2.0 | Existing-solution check only; do not generate the README from it. |
| GPRM (GitHub Profile ReadMe Maker) | **GPL-3.0** | Existing-solution check only; **do not use** (copyleft). |
| GitSkins and similar galleries | Various / commercial | Existing-solution check only; do not use templates or branding. |

## Content sources (Root's own material)

| Material | Source | Notes |
|---|---|---|
| Name, role, public email, ORCID | PR #1 `data/profile.yaml` | Real, not marked placeholder. Email `yushengzhou29@hotmail.com`. Role “Postdoctoral Researcher”. |
| Research interest bullets | PR #1 `content/_index.en.md` | Real, not marked placeholder. PR body: only the portrait is still a placeholder. Portrait is out of scope here. |
| Site URL | Project handoff | https://yushengzhou.github.io — expected 404 until the academic PR is merged. |

Do not invent interests or a different email. Do not ship machine-local paths or other internal notes in the profile repo.

# GitHub profile README — buildable spec

**For:** Yusheng Zhou (Root). **Repo (to be created):** `yushengzhou/yushengzhou` (PUBLIC special profile repo). **Live URL:** https://github.com/yushengzhou. **LICENSE:** MIT. **GitHub account:** `yushengzhou` only. **Kickoff approved:** 2026-11-25 23:20 Europe/Copenhagen.

Checked 2026-11-25 23:24 Europe/Copenhagen: unauthenticated API for `yushengzhou/yushengzhou` returns **404**. Engineer creates the public profile repo under `yushengzhou` before the first push.

**Existing-solution check:** Mature README *generators* exist (rahuldkjain/github-profile-readme-generator, Apache-2.0, ~24.5k stars; GPRM / GitHub Profile ReadMe Maker, **GPL-3.0**; GitSkins and similar template galleries). They emit generic badge/stats/trophy pages and do not ship Root's four chosen elements as an original academic profile. **Building is still right.** Do not start from those generators, and do not use GPRM (GPL-3.0).

**License flag (needs github chief go-ahead before implementation):** `Platane/snk` — the mature contribution-snake Action — has **no LICENSE file**, no `license` in `package.json`, GitHub `license: null`, and npm `generate-snake-animation@3.5.0` also has no license. That is **high risk** (default copyright / all rights reserved). Using it as an Action is still a dependency. See Stack and Risks.

## Goal

A short, original GitHub profile README for Yusheng Zhou that shows a typing intro (name + role), a small Mermaid graph of his research interests, a daily light/dark contribution snake, and three public contact links, all maintained in `yushengzhou/yushengzhou`.

## Features

1. **Typing-animation intro (top of README).** What it does: a looping typewriter line showing **Yusheng Zhou** and **Postdoctoral Researcher**. Inputs: those two strings from academic-site PR #1 `data/profile.yaml` (name, `role.en`). Outputs: two original static SVGs committed on `main` (`assets/typing-light.svg`, `assets/typing-dark.svg`), referenced with `<picture>` + `prefers-color-scheme`. Animation must be declarative **SMIL** (CSS `@keyframes` also usually survive in GitHub `<img>`, but SMIL is the more consistently reported path). **No** `readme-typing-svg` public endpoint, **no** scripts (GitHub's camo/`<img>` path is secure animated mode: scripts, external fetches, and interactivity do not run; SMIL/CSS declarative animation does).

2. **Research-interests Mermaid graph.** What it does: a small GitHub-native `mermaid` fenced flowchart of the five interest bullets from PR #1 `content/_index.en.md`. Inputs: those bullets only (do not invent nodes). Outputs: a rendered diagram on https://github.com/yushengzhou. Use stable `flowchart TD`, short labels, no `%%{init}%%` theme, no `click` directives, no wide `LR` layout. GitHub adapts light/dark automatically.

3. **Contribution snake, daily, light + dark.** What it does: animated SVGs of a snake on the user's contribution grid, regenerated every day. Inputs: public contribution calendar for `yushengzhou` via the GitHub API and `GITHUB_TOKEN`. Outputs: `github-snake.svg` and `github-snake-dark.svg?palette=github-dark` on branch `output`, referenced from README with `<picture>` + `prefers-color-scheme`. Workflow: `schedule` cron `0 5 * * *` (05:00 UTC = 06:00 Europe/Copenhagen in winter), plus `workflow_dispatch` and `push` to `main`. Permissions: `contents: write` only. Token: `secrets.GITHUB_TOKEN` only (required by snk v3+). Pin Actions by commit SHA. Publish with `actions/checkout` + `git push` to `output` (no third-party deploy Action, no Pages artifact). **Blocked on chief go-ahead** to use unlicensed `Platane/snk/svg-only`.

4. **Contact links.** What it does: three working links — personal site https://yushengzhou.github.io, ORCID https://orcid.org/0009-0003-6736-6496, email `mailto:yushengzhou29@hotmail.com`. Inputs: site URL from the handoff; ORCID and email from PR #1 `data/profile.yaml` (the same public email the academic site uses). Outputs: those three links in the README. No other personal contact.

**Content status (not placeholders):** Academic-site PR https://github.com/yushengzhou/yushengzhou.github.io/pull/1 is open, approved, unmerged (`feat/site-v1`, head `9f89d73`). The PR body says **only the portrait is still a placeholder**. `content/_index.en.md` research interests and `data/profile.yaml` email/role are **real, unmarked**. This spec uses them as-is and does not invent replacements. (The earlier academic-site SPEC had required placeholders; the later approved PR filled them from the CV / ORCID.)

## Out of scope

Skill badges, stats cards, trophies, visitor counters, star history, auto-follow, phone, referees, portrait, publications list, grants, Chinese toggle, custom domain, copying BEPb (or any) assets/text/layout/branding, vendoring snake or typing-SVG source, and any third-party typing endpoint.

## Stack

Checked 2026-11-25. Prefer no dependency where possible.

| Purpose | Choice | Reason | License | Last release | Maintainers | Activity | Vulns / security issues | Stars : open issues |
|---|---|---|---|---|---|---|---|---|
| Typing intro | **Original SMIL SVGs in-repo** | Name + role are static; avoids a third-party host, rate limits, and query-string privacy. GitHub camo serves `image/svg+xml` and does not strip SVG internals; `<img>` plays SMIL/CSS, not scripts. | Original work, repo MIT | n/a | n/a | n/a | n/a | n/a |
| Typing (rejected runtime) | DenverCoder1/readme-typing-svg at `readme-typing-svg.demolab.com` | Mature MIT tool, but the public service is **Heroku + Cloudflare** (not Vercel). No published SLA, rate limit, or privacy policy. Project itself prefers self-hosting. Past XSS in query `lines` (issue #7, 2021, closed). Occasional broken-image reports (e.g. #444). | MIT | v0.11.0, 2026-11-19 | 135 contributors | Push 2026-11-24; 9.5k stars | Closed XSS #7 (2021); no open security issues found; no OSV hit used | 9546 : 26 ≈ 367 : 1 |
| Diagram | **GitHub-native Mermaid** | No image, no service, auto light/dark. Confirmed for Markdown files (docs) and used on profile READMEs (e.g. BEPb). Keep the graph small. | n/a (platform) | n/a | n/a | n/a | Interactive `click` disabled in GitHub's sandbox | n/a |
| Snake (proposed, **license go-ahead required**) | **Platane/snk/svg-only** pinned to `d8f6715049803e982ee5ff501b6b9b7d5deeb09b` (`v3.5.0`) | De-facto standard; SVG-only is faster than the GIF-capable Action; recent enough (release < 18 months); 5 open issues. **Do not copy source** — Action use only. Single maintainer; PRs not accepted. OpenSSF Scorecard (2026-08-24): License 0/10, Maintained 0/10 (a later push was 2026-11-17). | **None (high risk)** | v3.5.0, 2026-04-25 | 5 contributors, almost all one maintainer | Release 7 months ago; push 2026-11-17 | No matching issues or OSV vulns found for this repo/package | 6203 : 5 ≈ 1241 : 1 |
| Snake (rejected as primary) | dahan8473/snake-and-commits | MIT, but **no releases**, 31 stars, 1 maintainer, created 2026-07-20. Fails the “release within 18 months unless no alternative” rule as a first choice. | MIT | none | 1 | Push 2026-11-25 | None found | 31 : 0 (no ratio) |
| Checkout / publish | **actions/checkout** `3d3c42e5aac5ba805825da76410c181273ba90b1` (`v7.0.1`) + `git push` to `output` | Official Action, MIT, active. Pushing with `GITHUB_TOKEN` avoids a third-party deploy Action and avoids Pages artifacts (wrong tool here). | MIT | v7.0.1, 2026-07-20 | 54 contributors (org: GitHub) | Push 2026-10-17 | No package-specific advisory found in this review | 9048 : 702 ≈ 13 : 1 (issue volume is normal for this Action) |
| Deploy Action (not chosen) | JamesIves/github-pages-deploy-action or crazy-max/ghaction-github-pages | Both MIT and maintained; unnecessary if git push is used. Recorded only as fallbacks. | MIT / MIT | v4.9.0 2026-08-08 / v5.0.0 2026-03-02 | 39 / 11 | Pushes 2026-11-24 / 2026-11-25 | None found in this review | 4612 : 7 ≈ 659 : 1 / 535 : 11 ≈ 49 : 1 |

**Rejected:** GPRM (GPL-3.0). Unlicensed or trademark-only assets. Any snake Action with no release and no mature alternative except as a last resort after chief declines snk.

## Data / APIs needed

- Public profile identity: name `Yusheng Zhou`, role `Postdoctoral Researcher` (PR #1 `data/profile.yaml`).
- Research interest bullets (PR #1 `content/_index.en.md`): extreme heat, greenspace, and other environmental exposures; cardiovascular morbidity and mortality; DLNM, multilevel and geospatial modelling, and machine-learning pipelines; sex, gender, and socioeconomic determinants; register-based epidemiology.
- Public email: `yushengzhou29@hotmail.com`. ORCID: `0009-0003-6736-6496`. Site: `https://yushengzhou.github.io`.
- GitHub API contribution calendar for `yushengzhou`, authenticated with `GITHUB_TOKEN` only.
- No other personal data, no internal paths, no unpublished facts.

**Open inputs:** none for interests or email (both are real in the approved PR). Chief go-ahead is required for `Platane/snk` (no license).

## File / branch layout

```
main:
  README.md
  LICENSE                          # MIT, copyright Yusheng Zhou, 2026
  assets/typing-light.svg
  assets/typing-dark.svg
  .github/workflows/snake.yml      # pin Actions by SHA; GITHUB_TOKEN only

output:                            # generated; do not edit by hand
  github-snake.svg
  github-snake-dark.svg
```

README image URLs: `https://raw.githubusercontent.com/yushengzhou/yushengzhou/output/github-snake.svg` and the `-dark` sibling. Typing images: repo-relative `assets/typing-*.svg`.

## Acceptance criteria

**AC1 — Profile visible.** Given the public repo `yushengzhou/yushengzhou` exists on branch `main` with `README.md`, when a visitor opens https://github.com/yushengzhou, then the profile README renders above the pinned/repo list.

**AC2 — Typing shows name + role.** Given the README references the committed light/dark typing SVGs via `<picture>`, when the profile is viewed in light and in dark GitHub appearance, then an animated intro is visible and the text includes “Yusheng Zhou” and “Postdoctoral Researcher”.

**AC3 — Mermaid renders.** Given the README contains a `mermaid` fenced flowchart of the five research-interest bullets, when the profile is viewed, then GitHub renders a diagram (not a raw code block) in both light and dark appearance, and the diagram stays within the content column without a huge horizontal scroll.

**AC4 — Snake generated, light + dark.** Given the workflow has been run (`workflow_dispatch` or the daily cron) with `contents: write` and `GITHUB_TOKEN`, when a visitor views the profile in light and in dark appearance, then the matching snake SVG from the `output` branch appears and animates (or, immediately after the first run, both raw URLs return HTTP 200 `image/svg+xml`).

**AC5 — Contact links work.** Given the contact section, when a visitor opens the site, ORCID, and email links, then they target https://yushengzhou.github.io, https://orcid.org/0009-0003-6736-6496, and `mailto:yushengzhou29@hotmail.com` respectively. (The site URL may 404 until academic PR #1 is merged — that is a known risk, not an AC5 failure if the href is correct.)

**AC6 — Original, MIT, no extra personal or internal data.** Given the repo tree, when it is reviewed, then `LICENSE` is MIT; README, SVGs, and workflow are original (ideas may follow references.md; no BEPb text, images, code, names, or branding); there is no phone, referee, or personal info beyond the public email and the already-public name/role/ORCID/interests; and no machine-local paths, private-account aliases, or other internal data appear in shipped files.

## Install / test / start

Repo does not exist yet; engineer creates it, then:

```bash
# after first push to main
gh workflow run snake.yml --repo yushengzhou/yushengzhou
gh run watch --repo yushengzhou/yushengzhou

# link check (site may 404 until the academic PR is merged)
curl -sSI https://github.com/yushengzhou
curl -sSI https://yushengzhou.github.io
curl -sSI https://orcid.org/0009-0003-6736-6496
curl -sSI https://raw.githubusercontent.com/yushengzhou/yushengzhou/output/github-snake.svg
curl -sSI https://raw.githubusercontent.com/yushengzhou/yushengzhou/output/github-snake-dark.svg

# shipped-tree sanity
rg -n "yushengzhou29@hotmail.com|orcid.org/0009-0003-6736-6496|yushengzhou.github.io" README.md
rg -n "PLACEHOLDER" README.md LICENSE assets .github || true
# README, LICENSE, assets, and .github must not contain machine-local paths or a private account alias
test -f LICENSE
```

Local Markdown preview cannot fully substitute for GitHub (Mermaid, camo, `<picture>` theme switching). Final checks are on https://github.com/yushengzhou in both appearance modes.

## Risks

- **`Platane/snk` has no license.** High risk. Engineer must not implement the snake Action until github chief approves this dependency. If declined, there is no equally mature licensed alternative; do not quietly switch to an unreleased MIT Action.
- **Site link 404** until academic PR #1 is merged and Pages is serving.
- **First snake 404** until the first successful workflow run creates `output`.
- **Camo / raw.githubusercontent.com cache** may show a stale snake after a daily overwrite of the same URL.
- **External typing service downtime** is avoided by the in-repo SVG choice; do not regress to demolab.com.
- **Snake Action breakage** if GitHub changes the contribution-calendar API or if the unlicensed Action is abandoned (single maintainer, PRs not accepted).
- **Mermaid** can fail if the graph is too large or uses a non-stable diagram type; keep it small and `flowchart`-only.
- Default `GITHUB_TOKEN` permissions must include `contents: write` or the push to `output` will fail. No PAT.

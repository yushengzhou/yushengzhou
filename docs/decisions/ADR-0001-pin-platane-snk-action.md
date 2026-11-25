# ADR-0001: Pin Platane/snk/svg-only as the snake Action

- Date: 2026-11-25
- Status: accepted

## Context

The profile includes a daily contribution snake. On 2026-11-25 23:28 CET the owner chose among three options:

- A. Use `Platane/snk/svg-only` as a pinned Action, with no copied code.
- B. Use `dahan8473/snake-and-commits`, an immature MIT alternative: no releases, 31 stars, 1 maintainer.
- C. Drop the snake.

`Platane/snk` has no LICENSE file. GitHub reports `license: null`. The npm package `generate-snake-animation@3.5.0` has no license either, so the work is all-rights-reserved by default. Calling it from Actions is still a dependency.

## Decision

Option A. The workflow uses `Platane/snk/svg-only` pinned to `d8f6715049803e982ee5ff501b6b9b7d5deeb09b` (v3.5.0), with no code copied or vendored. Decided by Root via github chief.

## Rationale

Option A was the mature snake Action, and the owner accepted the license risk that comes with it. Option B had no release to pin. Option C would remove the snake from the profile. The SVG-only Action is the one this profile needs, because the README shows SVG images.

## Consequences

- Legal risk: the dependency has no license and is all-rights-reserved by default, including `generate-snake-animation@3.5.0`.
- Maintenance risk: a single maintainer. The upstream project does not take pull requests as its way of working.
- The Action is pinned to a full commit SHA. A newer release is used only when this repository changes the pin.
- No snake source is copied into this repository, so the profile tree does not redistribute that code.

# ADR-0004: Publish the snake with checkout and git push

- Date: 2026-11-25
- Status: accepted

## Context

The snake SVGs are regenerated on a schedule and stored where the README can point at stable raw URLs. A third-party deploy Action, or a GitHub Pages artifact, could publish generated files. Pages is a site host. A deploy Action is a further dependency.

## Decision

`.github/workflows/snake.yml` publishes the snake with `actions/checkout` and `git push` to the `output` branch. `actions/checkout` is pinned to `3d3c42e5aac5ba805825da76410c181273ba90b1` (v7.0.1). `Platane/snk/svg-only` is pinned to `d8f6715049803e982ee5ff501b6b9b7d5deeb09b` (v3.5.0). The workflow permission is `contents: write` only. The only secret is `GITHUB_TOKEN`. The publish step force-pushes `HEAD` to `refs/heads/output` and does not push `main`.

## Rationale

`GITHUB_TOKEN` with contents write is enough to update one branch in this repository. That keeps publishing inside GitHub’s own checkout Action and git. A deploy Action or a Pages site would be a second publishing system for two SVG files.

## Consequences

- The `output` branch contains `github-snake.svg` and `github-snake-dark.svg`. Each successful run replaces that branch.
- The README raw URLs stay the same. They serve the SVGs after the first successful run creates the branch. Until then, the URLs are broken.
- The workflow does not use a personal access token. If the token lacks `contents: write`, the push to `output` fails.
- Publishing does not go through a third-party deploy Action or through GitHub Pages.

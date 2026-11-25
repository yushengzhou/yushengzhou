# ADR-0002: Draw the typing intro with original SMIL SVGs

- Date: 2026-11-25
- Status: accepted

## Context

The top of the profile shows the name Yusheng Zhou and the role Postdoctoral Researcher, looping, in light and dark. DenverCoder1’s public typing-SVG service can generate that kind of animation. `docs/spec.md` and `docs/references.md` name that service. It is a third-party host with no published SLA and no published privacy policy, and it had a cross-site scripting bug in its query text (closed in 2021). GitHub shows a README image through its image proxy. In that mode, script elements do not run. SMIL animation does run.

## Decision

The introduction is two original SVGs committed in this repository, `assets/typing-light.svg` and `assets/typing-dark.svg`, switched with `<picture>` and `prefers-color-scheme`. The animation is declarative SMIL. The profile does not call DenverCoder1’s public typing-SVG service (named in `docs/spec.md` and `docs/references.md`), and the SVGs contain no scripts.

## Rationale

The name and the role are fixed strings, so the artwork can live next to the README. That removes a hosted service from the path that every profile view would otherwise depend on. SMIL is the animation GitHub’s image path actually plays.

## Consequences

- Wording changes are edits to the `<text>` elements, the `<title>`, the `textLength` values, and the README alt text, in both the light and the dark file.
- The profile has no runtime dependency on the typing service, and it does not send the name and role out as a query string.
- Script-based animation is unavailable in these images. The effect stays SMIL.

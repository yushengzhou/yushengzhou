# ADR-0007: Fixed name, rotating taglines

- Date: 2026-11-26
- Status: accepted
- Amends: [ADR-0002](ADR-0002-original-smil-typing-svgs.md) (still original SMIL SVGs in the repository)

## Context

The first intro typed the name, erased it, then typed "Postdoctoral Researcher" in its place. The owner found the flashing role odd, and a job title goes stale when the position changes.

## Decision

The name stays on line 1 with the credentials: **Yusheng Zhou**, MPH, PhD. Line 2 types three field-based taglines in turn: Environmental Epidemiologist; Climate, Environment & Cardiovascular Health; R · Python · Data Science.

## Rationale

Owner's choice on 2026-11-26: keep the animation, drop the job title, rotate several lines. Keeping the name fixed removes the flash. The taglines describe the field and skills, which do not change with the role, and match the site's About text.

## Consequences

The checks require the name and all three taglines in each SVG's text and in the image alt text, and still require a looping SMIL animation and no script.

# ADR-0005: Build the profile from scratch

- Date: 2026-11-25
- Status: accepted

## Context

README generators already exist. `rahuldkjain/github-profile-readme-generator` (Apache-2.0) and similar galleries emit generic badge and stats pages. GPRM (GitHub Profile ReadMe Maker) is GPL-3.0. The reference profile in `docs/references.md` is ideas only: a typing line, a Mermaid graph, and a contribution snake are patterns a profile can use. That borrowing record lists the ideas and the boundary around them.

## Decision

The profile is built from scratch in this repository, around the four chosen elements: the typing introduction, the research-interests graph, the contribution snake, and the three contact links. README generators are not the source of the page. Nothing is copied from the reference profile named in `docs/references.md`: no text, images, code, names, or branding. Ideas may follow that borrowing record.

## Rationale

The generators produce a different kind of page from this academic profile. GPRM is GPL-3.0, and this repository is MIT, so that generator is not a source. The reference profile in `docs/references.md` is useful as a map of ideas and is the wrong source for assets or wording. The name, role, interests, and contact links are this profile’s own content.

## Consequences

- `README.md`, the typing SVGs, and the workflow are maintained here as original work.
- GPL-3.0 generator output stays out of the tree.
- A later edit that pastes text, images, code, names, or branding from the reference profile in `docs/references.md` would break this decision. The borrowing record remains the list of what was looked at.

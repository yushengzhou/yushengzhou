# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- The intro keeps the name fixed as Yusheng Zhou, MPH, PhD and types three taglines in turn underneath: Environmental Epidemiologist; Climate, Environment & Cardiovascular Health; R · Python · Data Science. The job title is gone (ADR-0007).

### Added

- The profile README: a light and dark typing introduction, a research-interests diagram, a light and dark contribution snake, and links to the personal site, ORCID, and public email.
- Original light and dark typing SVGs for the name and the role.
- A workflow that draws the contribution snake and publishes the SVGs on the `output` branch. It runs every day at 05:00 UTC, on a manual dispatch, and on a push to `main`.
- The MIT license, Copyright (c) 2026 Yusheng Zhou.
- Acceptance checks for the profile page, and a pull-request workflow that runs them.
- The profile spec, the borrowing record, and the demand card.
- The decision to draw the snake with the pinned Platane/snk Action, now kept with the other architecture decision records.
- This development guide and this changelog.

### Changed

- `docs/decisions.md` is an index of the architecture decision records.

### Fixed

- The opening of the spec said the profile repository was still to be created. It now says `yushengzhou/yushengzhou` exists.
- The spec’s contribution-snake feature and the borrowing record’s snake row said the snake Action was blocked. They now cite the accepted decision to pin it.
- The spec’s license flag, stack-table snake row, open inputs, install lead-in, and license risk, and the borrowing record’s tools row, now say the repository exists and that the snake Action is the approved pinned dependency. The no-license risk text stays.

[Unreleased]: https://github.com/yushengzhou/yushengzhou/compare/main...feat/profile-readme

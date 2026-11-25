# Decisions

Index of accepted architecture decision records for this profile. Dated 2026-11-25.

- [ADR-0001: Pin Platane/snk/svg-only](decisions/ADR-0001-pin-platane-snk-action.md). Use Platane/snk/svg-only pinned to d8f6715049803e982ee5ff501b6b9b7d5deeb09b (v3.5.0), with no code copied or vendored. The npm package generate-snake-animation@3.5.0 has no license, so the dependency is all-rights-reserved by default. The alternative dahan8473/snake-and-commits was declined. Decided by Root via github chief.
- [ADR-0002: Original SMIL typing SVGs](decisions/ADR-0002-original-smil-typing-svgs.md). The typing introduction is original SMIL artwork committed in the repository.
- [ADR-0003: GitHub-native Mermaid](decisions/ADR-0003-github-native-mermaid.md). The research-interests graph is a Mermaid block in the README.
- [ADR-0004: Publish the snake to `output`](decisions/ADR-0004-publish-snake-to-output-branch.md). `actions/checkout` and `git push` publish the SVGs with `GITHUB_TOKEN`.
- [ADR-0005: Build the profile from scratch](decisions/ADR-0005-build-the-profile-from-scratch.md). The page is original work. Comparisons with generators and with the reference profile stay in the borrowing record.
- [ADR-0006: Widgets left out of the profile](decisions/ADR-0006-leave-profile-widgets-out-of-scope.md). Badges, stats, trophies, counters, star history, auto-follow, phone, and referees stay out.

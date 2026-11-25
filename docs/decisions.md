# Decisions

## 2026-11-25 — Contribution snake Action

**Decision:** Use Platane/snk/svg-only as an Actions dependency, pinned to SHA d8f6715049803e982ee5ff501b6b9b7d5deeb09b (v3.5.0), with no code copied or vendored.

**Risk:** The Platane/snk repo has no LICENSE (GitHub license null, and the npm generate-snake-animation@3.5.0 package has no license either), so it is all-rights-reserved by default.

**Alternatives considered:** dahan8473/snake-and-commits (MIT, no releases), or dropping the snake.

Decided by Root via github chief.

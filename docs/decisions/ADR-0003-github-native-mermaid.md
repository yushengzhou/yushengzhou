# ADR-0003: Draw research interests with GitHub-native Mermaid

- Date: 2026-11-25
- Status: accepted

## Context

The profile needs a small graph of the five research interests. An exported image would be a second asset to keep in sync, with a separate light and dark file. An external diagram service would be another host on the profile page.

## Decision

The graph is one GitHub-native Mermaid block in `README.md`. The diagram type is `flowchart TD`. The node labels are exactly the five research interests. The block has no `%%{init}%%` theme and no `click` directive. GitHub renders the diagram and adapts it to light and dark. There is no image and no diagram service.

## Rationale

Mermaid is part of GitHub Markdown, including on a profile README. The graph is small enough to stay in the content column. The repository then has one source for the labels, which is the README itself.

## Consequences

- The five labels and their edges are edited in the Mermaid block. Adding or renaming a node is a content change to that block.
- How the diagram looks depends on GitHub’s renderer. A local Markdown preview is not a full substitute.
- A wide layout, an init theme, or a click directive would be a different decision. This record keeps the block on `flowchart TD`.

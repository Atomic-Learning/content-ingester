---
description: End-to-end content ingestion workflow for Atomic Learning pages.
applyTo: "**"
---

# Content Ingestion Policy

## Scope

- Default to top-level `inputs/`, `outputs/`, and `templates/`. Within `inputs/`, website export files go in `live-website-export/` and new content to ingest goes in `content-to-ingest/`.
- Allow overriding ingestion inputs/outputs via `.env`:
  - `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
  - `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Non-negotiable Rules

- Keep work in dependency order.
- Pause for user approval at each checkpoint and after each generated page.
- Keep generated ingestion artifacts in the active output directory for the run.
- Reuse existing support docs as references when needed:
  - `.github/instructions/atomisation-guidelines.md`
  - `.github/instructions/updating-proposed-structure.md`
  - `.github/instructions/content_file_details.md`

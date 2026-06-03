---
description: End-to-end content ingestion workflow for Atomic Learning pages.
applyTo: "**"
---

# Content Ingestion Policy

Use this instruction file for normal ingestion work only.

The assigned agent is responsible for timeline orchestration and skill ordering.

## Scope

- Default to top-level `inputs/`, `outputs/`, and `templates/`.
- Ignore `workflow-validation/` unless the user explicitly asks for validation work.
- If the user asks for validation tests/regression validation, switch to `.github/instructions/validation-workflow.instructions.md`.

## Non-negotiable Rules

- Keep work in dependency order.
- Pause for user approval at each checkpoint and after each generated page.
- Keep generated ingestion artifacts in top-level `outputs/`.
- Reuse existing support docs as references when needed:
  - `.github/atomisation-guidelines.md`
  - `.github/proposed-structure-format.md`
  - `.github/content_file_details.md`

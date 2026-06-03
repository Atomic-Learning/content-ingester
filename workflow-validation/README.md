# Workflow Validation

This folder contains regression validation cases for workflow and agent changes.

## How To Use

1. Prompt the agent to run the validation workflow.
2. Read `workflow-validation/validation-report.md`.
3. Decide whether divergences from expected outputs are acceptable for the change, or indicate regression risk.
4. The validation report is committed to the repository, so there is a clear trail of current divergence from ideal behaviour.

## Case Layout

Each validation case lives in `workflow-validation/<case>/` with:

- `inputs/`
- `human-inputs/` (optional)
- `expected-outputs/`
- `generated-outputs/` (created by the agent during validation)

## What To Check In validation-report.md

Review the per-case sections in the single report file and decide whether the reported differences are acceptable in context of your change, with attention to:

- single learning objective per page
- prerequisite/related-content quality
- page splitting/combining choices
- tag consistency
- content and metadata clarity

## Adding A New Validation Example

When adding a new case, create `workflow-validation/<new-case>/` with:

- `inputs/`
- `human-inputs/` These are supplementary details that were provided during ingestion to generated expected outputs.
- `expected-outputs/` baseline

Then ask the agent to run validation and review the per-case sections in `workflow-validation/validation-report.md`.

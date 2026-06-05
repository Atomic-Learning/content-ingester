# Repository Router

Use this file as the top-level routing policy for this workspace.

## Primary Routing Rule

- For normal Atomic Learning ingestion work using configured ingestion folders (defaults: `inputs/` and `outputs/`), use the `Content Ingestion Assistant`.
- For regression validation work, validation reports, or any request that explicitly mentions `workflow-validation/`, use the `validate-workflow` skill.

## Route To Content Ingestion Assistant

Use `Content Ingestion Assistant` when the user asks to:

- read or understand source content from the configured ingestion inputs directory
- review existing Atomic Learning content and tags
- propose or revise `<output-dir>/proposed_structure.json`
- generate or regenerate the prerequisite dependency graph for normal ingestion outputs
- create, edit, review, or delete page folders under the configured ingestion output directory
- check output consistency for normal generated pages
- recommend related content for existing pages
- upload generated pages to GitHub repositories
- continue the normal ingestion workflow from any checkpoint

## Route To validate-workflow Skill

Use `validate-workflow` when the user asks to:

- run validation tests or regression validation
- work inside `workflow-validation/`
- compare validation outputs against expected outputs
- update or review `workflow-validation/validation-report.md`
- verify that ingestion workflow changes did not alter normal outputs

## Conflict Resolution

- If the task is ambiguous, ask the user for clarification before proceeding.
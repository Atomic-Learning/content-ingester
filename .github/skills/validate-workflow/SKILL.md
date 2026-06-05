---
name: validate-workflow
description: Run isolated validation cases end-to-end by invoking Content Ingestion Assistant with per-case input/output folders and appending comparison results.
---

# validate-workflow

Use this skill from the active chat agent.

This skill owns validation orchestration. The actual ingestion generation is delegated to `Content Ingestion Assistant` and must run only against the case-local validation folders.

## Per-case orchestration steps
1. Clean case generated outputs before generation:

```bash
python .github/skills/validate-workflow/validation_clean_case_outputs.py --case <case-name>
```

2. Invoke `Content Ingestion Assistant` for case-local generation.

The `Content Ingestion Assistant` must treat:
- `workflow-validation/<case-name>/inputs/` as source inputs
- `workflow-validation/<case-name>/generated-outputs/` as output target

The handoff prompt must explicitly state validation mode and provide these exact folders.

3. Compare generated outputs to expected outputs and append the report:

```bash
python .github/skills/validate-workflow/validation_compare_case.py --case <case-name> --report workflow-validation/validation-report.md --append
```

## Rules
- Never read `expected-outputs/` before generation.
- Do not write validation artifacts into top-level `outputs/`.
- Do not upload validation artifacts.

## Execution Contract
- The orchestrating agent running this skill is responsible for iterating all validation cases.
- For each case, perform clean -> content-ingester handoff -> compare in that order.
- If subagent invocation is unavailable in the runtime, stop and report that validation cannot be completed as designed in that session.

## Optional follow-up

If the user explicitly asks to rerun comparison or report generation, use:

```bash
python .github/skills/validate-workflow/validation_compare_case.py --case <case-name> --report workflow-validation/validation-report.md --append
```

Keep any assessment qualitative only.

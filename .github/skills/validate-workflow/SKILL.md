---
name: validate-workflow
description: Run isolated regression validation cases and produce qualitative report.
---

# validate-workflow

Use this skill with the workflow validation agent.

## Per-case deterministic steps
1. Stage case files:

```bash
python .github/skills/validate-workflow/validation_stage_case.py --case <case-name> --clean
```

2. Generate outputs in staged workspace only.
3. Sync staged outputs to `generated-outputs/`:

```bash
python .github/skills/validate-workflow/validation_sync_case_outputs.py --case <case-name> --clean-target
```

4. Compare and append report section:

```bash
python .github/skills/validate-workflow/validation_compare_case.py --case <case-name> --report workflow-validation/validation-report.md --append
```

## Rules
- Never read `expected-outputs/` before generation.
- Keep report qualitative only.
- Do not upload validation artifacts.

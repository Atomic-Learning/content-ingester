---
name: validate-workflow
description: Run isolated validation cases end-to-end by invoking Content Ingestion Assistant with per-case input/output folders and writing a fresh comparison report.
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

3. Compare generated outputs to expected outputs and overwrite the report section for the run:

```bash
python .github/skills/validate-workflow/validation_compare_case.py --case <case-name> --report workflow-validation/validation-report.md
```

Capture the script's stdout — it contains unified diffs for every changed text file.

4. Read the diffs from stdout, then write concise qualitative sections into the report.

The script leaves two empty sections in the report for you to fill in. Do not copy or paste raw diff content into the report — write a brief human-readable summary only.

- **Qualitative difference assessment** — 2–5 bullet points on what actually changed and whether it matters: were learning objectives preserved, did content quality improve or regress, were structural choices (page splits, combining) appropriate, is metadata accurate, are tags consistent? Only include points where there is something meaningful to say.
- **Notable divergences** — bullet points calling out specific differences a reviewer should pay attention to, referencing the file and the nature of the change. Omit this section if there are no meaningful divergences.

Write these sections by editing the report file directly after the script runs.

## Rules
- Never read `expected-outputs/` before generation.
- Do not write validation artifacts into top-level `outputs/`.
- Do not upload validation artifacts.
- Do not write generic automated text in qualitative sections — every observation must come from reading the actual diffs.

## Execution Contract
- The orchestrating agent running this skill is responsible for iterating all validation cases.
- For each case, perform clean -> content-ingester handoff -> compare -> write qualitative assessment in that order.
- If subagent invocation is unavailable in the runtime, stop and report that validation cannot be completed as designed in that session.

## Optional follow-up

If the user explicitly asks to rerun comparison or report generation, use:

```bash
python .github/skills/validate-workflow/validation_compare_case.py --case <case-name> --report workflow-validation/validation-report.md
```

Then read the diff output from stdout and rewrite the qualitative sections in the report.

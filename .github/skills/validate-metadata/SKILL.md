---
name: validate-metadata
description: Validate one or all metadata.json files against the metadata schema.
---

# validate-metadata

Use this skill to validate `metadata.json` file(s) against `.github/instructions/metadata.schema.json`.

Run after page generation (see `page-generation-and-review-and-edit`) or as part of the
`check-output-consistency` workflow.

Resolve paths from `.env` before running:
- `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Validate a single file

```bash
python .github/skills/validate-metadata/validate_metadata.py --metadata-file <output-dir>/<slug>/metadata.json
```

## Validate all metadata.json files in the output directory

```bash
python .github/skills/validate-metadata/validate_metadata.py --metadata-root <output-dir>
```

## Exit codes

| Code | Meaning |
|------|---------|
| `0`  | All validated files are valid. |
| `1`  | One or more files failed schema validation (errors are printed per file). |
| `2`  | A file or the schema could not be read. |

## Guardrails

- Fix any reported errors before proceeding to `upload-and-check`.
- Slug in `metadata.json` must match the page directory name; the schema enforces the slug format but not the directory match — verify that separately via `check-output-consistency`.

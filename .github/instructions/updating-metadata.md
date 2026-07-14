# Updating Metadata

Use this guide when creating or editing a `metadata.json` file for any content page.

## Source of truth

- Field definitions and constraints are in `.github/instructions/metadata.schema.json`.
- A concrete reference example is available in `workflow-validation/what-is-numpy-scipy/expected-outputs/python-numpy-introduction/metadata.json`.

## Required workflow after creating or editing

1. Validate the file against the schema:

```bash
python .github/skills/validate-metadata/validate_metadata.py --metadata-file <output-dir>/<slug>/metadata.json
```

2. Verify that the `slug` value matches the name of the page's output directory exactly.

## Notes

- Resolve `<output-dir>` from `.env` when present:
  - `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)
- Keep valid JSON only (double quotes, no trailing commas, no markdown fencing).
- `slug` must be lowercase and hyphen-separated (`^[a-z0-9]+(-[a-z0-9]+)*$`). It must also match the page's directory name.
- `description` has a maximum of 500 characters.
- `duration` is a positive integer (minutes); do not use ranges (e.g. use `10`, not `5–15`).
- `authors` and `tags` must each contain at least one entry and no duplicates.
- `prerequisites` and `related` contain slugs only; both default to an empty array when none apply.
- A slug must not appear in both `prerequisites` and `related` for the same page.
- A page must not list its own slug as a prerequisite.
- Prerequisite slugs should refer to pages that already exist on the platform or are being introduced in the same ingestion batch.

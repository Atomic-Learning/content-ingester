# Updating Proposed Structure

Use this guide when creating or editing `outputs/proposed_structure.json`.

## Source of truth

- Structure and required fields are defined in `.github/instructions/proposed-structure.schema.json`.
- A concrete reference payload is available in `workflow-validation/what-is-numpy-scipy/expected-outputs/proposed_structure.json`.

## Required workflow after any update

1. Validate JSON structure and reject circular prerequisite dependencies:

```bash
python .github/skills/input-to-proposed-structure/validate_proposed_structure.py --proposed-file <output-dir>/proposed_structure.json
```

/Users/sraja/projects/content-ingester/workflow-validation/what-is-numpy-scipy/expected-outputs/proposed_structure.json

1. Regenerate dependency graph from proposed structure:

```bash
python .github/skills/input-to-proposed-structure/generate_prerequisite_graph.py --source proposed_structure --inputs-dir <input-dir> --proposed-file <output-dir>/proposed_structure.json --output-dir <output-dir>
```

## Notes

- Resolve `<input-dir>` and `<output-dir>` from `.env` when present:
  - `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
  - `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)
- Keep valid JSON only (double quotes, no trailing commas, no markdown fencing).
- Keep `pages[*].status` as either `new` or `missing`.

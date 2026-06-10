# Proposed Structure Format

This file defines the expected format of `outputs/proposed_structure.json`.

## Goals

1. Keep the Step 2 proposal fully detailed.
2. Make the proposal directly machine-readable without duplicating the same information in markdown and JSON.
3. Allow tools such as the dependency graph generator to consume the proposal reliably.

## Schema

The machine-readable schema is `proposed-structure.schema.json` in this directory — the source of truth the validation script checks against (see Validation below).

## Validation

Structural validity is checked by a script. It validates the file against the schema in `proposed-structure.schema.json`:

```bash
python .github/skills/input-to-proposed-structure/validate_proposed_structure.py --proposed-file <output-dir>/proposed_structure.json
```

The script reports every invalid field with its JSON path and exits non-zero if the structure does not conform. The schema it checks against is fixed and cannot be overridden.

## Notes For Tooling

- The dependency graph tool reads `pages[*].slug`, `pages[*].prerequisites`, and `pages[*].status`.
- All other fields are preserved so the JSON file can be used directly for review and later content generation steps.
- Keep slugs and tags as plain strings.
- Use valid JSON only: double quotes, no trailing commas, no markdown fencing.
- Structural validation is enforced by `validate_proposed_structure.py` (see Validation above), not by manual review.

## Backward Compatibility

No backward compatibility constraints apply for this workspace. Use the status-based schema above.

---
name: set-authors
description: Set author names in metadata.json files from authors.md.
---

# set-authors

Use this skill to populate `authors` fields in metadata.json files from a central `authors.md` file.

Resolve paths from `.env` before running:
- `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
- `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Inputs

- `<input-dir>/authors.md` file listing author identifiers (one per line)
- `<output-dir>/<slug>/metadata.json` file(s) to update

## Produce

- Updated `metadata.json` files with `authors` field set from `authors.md`
- Validation report showing which files were modified and which failed validation

## Configuration

The user should have edited `<input-dir>/authors.md` (default: `inputs/authors.md`) to specify the author identifiers to use in the metadata files, one author per line. For example:

```
jane-doe
joe-bloggs
```

Author identifiers must be lowercase, hyphen-separated (e.g. `john-doe`), matching the pattern `^[a-z0-9]+(-[a-z0-9]+)*$`.

## Usage

Update all metadata.json files under an output directory:

```bash
python .github/skills/set-authors/set_authors.py --output-dir <output-dir>
```

Update a single metadata.json file:

```bash
python .github/skills/set-authors/set_authors.py --metadata-file <output-dir>/<slug>/metadata.json
```

## Guardrails

- `<input-dir>/authors.md` must exist and contain at least one valid author identifier. The script exits with code 2 if missing or empty.
- Authors in the file must be one per line, lowercase and hyphen-separated. Invalid identifiers cause exit code 2.
- **Example authors warning**: If `authors.md` contains example author names (`jane-doe` or `joe-bloggs`), the script will print a warning to remind you to replace them with real authors. The script will still proceed and apply the example authors to metadata files.
- Updated metadata.json files are validated against the metadata schema. Validation failures cause exit code 1.
- Output directory must exist and contain metadata.json files. Missing directory or no files found causes exit code 2.
- This skill is intended to be run after page generation when you want to standardise author names across a batch.
- All generated pages require at least one author (per the metadata schema), so this skill enforces author configuration.

## Configuration Required

This skill requires `<input-dir>/authors.md` to exist and contain author identifiers. If it is not present, the script will exit with code 2:

```
Reading authors from inputs/authors.md...
✗ Error: inputs/authors.md not found or is empty.
  Authors are required for generated pages.
  Please create authors.md with one author per line:
    jane-doe
    jim-bloggs
```

**To run this skill:**

1. Create `<input-dir>/authors.md` (default: `inputs/authors.md`) with one author identifier per line:
   ```
   jane-doe
   jim-bloggs
   ```
2. Save the file
3. Run the skill — it will apply the authors to all metadata.json files and validate them against the schema

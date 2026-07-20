---
name: set-authors-from-env
description: Set author names in metadata.json files from .env configuration.
---

# set-authors-from-env

Use this skill to populate `authors` fields in metadata.json files from a central `.env` configuration.

Resolve paths from `.env` before running:
- `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
- `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Inputs

- `.env` file with `CONTENT_INGESTER_AUTHORS` configuration
- `<output-dir>/<slug>/metadata.json` file(s) to update

## Produce

- Updated `metadata.json` files with `authors` field set from `.env`
- Validation report showing which files were modified and which failed validation

## Configuration

Add to `.env`:

```
CONTENT_INGESTER_AUTHORS=author-one,author-two,author-three
```

Author identifiers must be lowercase, hyphen-separated (e.g. `john-doe`), matching the pattern `^[a-z0-9]+(-[a-z0-9]+)*$`.

## Usage

Update all metadata.json files under an output directory:

```bash
python .github/skills/set-authors-from-env/set_authors.py --output-dir <output-dir>
```

Update a single metadata.json file:

```bash
python .github/skills/set-authors-from-env/set_authors.py --metadata-file <output-dir>/<slug>/metadata.json
```

## Guardrails

- `CONTENT_INGESTER_AUTHORS` must be configured in `.env` before running this skill. The script exits with code 2 if missing.
- Authors from `.env` must be a comma-separated list of valid author identifiers (lowercase, hyphen-separated). Invalid identifiers cause exit code 2.
- Updated metadata.json files are validated against the metadata schema. Validation failures cause exit code 1.
- Output directory must exist and contain metadata.json files. Missing directory or no files found causes exit code 2.
- This skill is intended to be run after page generation when you want to standardise author names across a batch.
- All generated pages require at least one author (per the metadata schema), so this skill enforces author configuration.

## Configuration Required

This skill requires `CONTENT_INGESTER_AUTHORS` to be configured in `.env`. If it is not configured, the script will exit with code 2:

```
Reading authors from .env...
✗ Error: CONTENT_INGESTER_AUTHORS not configured in .env.
  Authors are required for generated pages.
  Please add: CONTENT_INGESTER_AUTHORS=author-one,author-two
```

**To run this skill:**

1. Edit `.env` to add a line with your author identifiers (lowercase, hyphen-separated):
   ```
   CONTENT_INGESTER_AUTHORS=author-name,another-author
   ```
2. Save the file
3. Run the skill — it will apply the authors to all metadata.json files and validate them against the schema

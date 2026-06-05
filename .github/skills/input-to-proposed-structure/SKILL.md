---
name: input-to-proposed-structure
description: Read ingestion inputs, propose atomic page structure, and generate dependency graph.
---

# input-to-proposed-structure

Use this skill to produce `<output-dir>/proposed_structure.json` from the configured input directory.

Resolve paths from `.env` before running:
- `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
- `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Read
- `<input-dir>/current_content.md`
- `<input-dir>/tags_current.md`
- New content files in `<input-dir>/`
- `.github/instructions/atomisation-guidelines.md`
- `.github/instructions/proposed-structure-format.md`

## Produce
- `<output-dir>/proposed_structure.json`
- `<output-dir>/dependency_graph.md` by running:

```bash
python .github/skills/input-to-proposed-structure/generate_prerequisite_graph.py --source proposed_structure --inputs-dir <input-dir> --proposed-file <output-dir>/proposed_structure.json --output-dir <output-dir>
```

## Guardrails
- Preserve existing platform content boundaries.
- Mark proposed prerequisite gaps as `status: "missing"`.
- Keep each page focused on one learning objective.

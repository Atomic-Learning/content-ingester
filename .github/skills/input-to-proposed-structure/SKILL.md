---
name: input-to-proposed-structure
description: Read ingestion inputs, propose atomic page structure, and generate dependency graph.
---

# input-to-proposed-structure

Use this skill to produce `outputs/proposed_structure.json` from top-level `inputs/`.

## Read
- `inputs/current_content.md` (or nearest variant)
- `inputs/tags_current.md` (or nearest variant)
- New source files in `inputs/`
- `.github/atomisation-guidelines.md`
- `.github/proposed-structure-format.md`

## Produce
- `outputs/proposed_structure.json`
- `outputs/dependency_graph.md` by running:

```bash
python .github/skills/input-to-proposed-structure/generate_prerequisite_graph.py --source proposed_structure
```

## Guardrails
- Preserve existing platform content boundaries.
- Mark proposed prerequisite gaps as `status: "missing"`.
- Keep each page focused on one learning objective.

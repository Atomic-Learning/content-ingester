---
name: proposed-structure-review-and-edit
description: Review and revise proposed_structure.json with dependency-aware edits.
---

# proposed-structure-review-and-edit

Use this skill after initial structure generation to refine `outputs/proposed_structure.json`.

## Tasks
- Validate required fields for each page.
- Refine prerequisite ordering and avoid cycles.
- Improve split decisions to keep one learning objective per page.
- Reconcile tags against `inputs/tags_current.md`.

## Regenerate graph after edits

```bash
python .github/skills/input-to-proposed-structure/generate_prerequisite_graph.py --source proposed_structure
```

## Output
- Updated `outputs/proposed_structure.json`
- Updated `outputs/dependency_graph.md`

---
name: check-output-consistency
description: Validate consistency of generated pages, links, tags, and dependency graph.
---

# check-output-consistency

Use this skill after page generation to run consistency checks across `outputs/`.

## Tasks
- Verify `metadata.json` slug matches page directory.
- Validate prerequisite and related-content references.
- Check tag consistency against `inputs/tags_current.md`.
- Ensure each page has `license.md` and `resources/.gitkeep`.

## Generate final dependency graph from metadata

```bash
python .github/skills/input-to-proposed-structure/generate_prerequisite_graph.py --source metadata
```

## Produce
- Updated `outputs/dependency_graph.md`
- `outputs/related_content_recommendations.md`

---
name: check-output-consistency
description: Validate consistency of generated pages, links, tags, and dependency graph.
---

# check-output-consistency

Use this skill after page generation to run consistency checks across `<output-dir>/`.

Resolve paths from `.env` before running:
- `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
- `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Tasks
- Verify `metadata.json` slug matches page directory.
- Validate prerequisite and related-content references.
- Check tag consistency against `<input-dir>/live-website-export/tags_current.md`.
- Ensure each page has `license.md` and `resources/.gitkeep`.

## Generate final dependency graph from metadata

```bash
python .github/skills/input-to-proposed-structure/generate_prerequisite_graph.py --source metadata --metadata-root <output-dir> --inputs-dir <input-dir> --output-dir <output-dir>
```

## Produce
- Updated `<output-dir>/dependency_graph.md`
- `<output-dir>/related_content_recommendations.md`

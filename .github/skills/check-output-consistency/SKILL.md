---
name: check-output-consistency
description: Validate consistency of generated pages, links, tags, and dependency graph.
---

# check-output-consistency

Use this skill after page generation to run consistency checks across `<output-dir>/`.

## Preferred one-command workflow

Run the reusable checker script:

```bash
python .github/skills/check-output-consistency/run_consistency_checks.py
```

Optional flags:

```bash
python .github/skills/check-output-consistency/run_consistency_checks.py --strict-tags
python .github/skills/check-output-consistency/run_consistency_checks.py --skip-graph
python .github/skills/check-output-consistency/run_consistency_checks.py --skip-recommendations
python .github/skills/check-output-consistency/run_consistency_checks.py --inputs-dir <input-dir> --outputs-dir <output-dir>
```

This command validates metadata, checks required files and cross-page references,
verifies tags, regenerates `dependency_graph.md` from metadata, and refreshes
`related_content_recommendations.md`.

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

The command above is still valid for graph-only regeneration, but for regular
checkpoint usage prefer `python .github/skills/check-output-consistency/run_consistency_checks.py`.

## Produce

- Updated `<output-dir>/dependency_graph.md`
- `<output-dir>/related_content_recommendations.md`

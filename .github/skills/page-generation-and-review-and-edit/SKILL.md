---
name: page-generation-and-review-and-edit
description: Generate one page at a time in dependency order and iterate with user review.
---

# page-generation-and-review-and-edit

Use this skill for checkpoint 2 page generation from approved structure.

Resolve paths from `.env` before running:
- `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
- `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Inputs
- `<output-dir>/proposed_structure.json`
- `<input-dir>/current_content.md`
- `.github/instructions/content_file_details.md`

## Required per-page output structure
- `<output-dir>/<slug>/metadata.json`
- `<output-dir>/<slug>/content.md`
- `<output-dir>/<slug>/license.md`
- `<output-dir>/<slug>/resources/`
- `<output-dir>/<slug>/resources/.gitkeep`

## Rules
- Generate pages strictly in dependency order.
- Work one page at a time.
- Pause for user review before proceeding to the next page.

---
name: page-generation-and-review-and-edit
description: Generate one page at a time in dependency order and iterate with user review.
---

# page-generation-and-review-and-edit

Use this skill for checkpoint 2 page generation from approved structure.

## Inputs
- `outputs/proposed_structure.json`
- `inputs/current_content.md`
- `.github/content_file_details.md`

## Required per-page output structure
- `outputs/<slug>/metadata.json`
- `outputs/<slug>/content.html`
- `outputs/<slug>/license.md`
- `outputs/<slug>/resources/`
- `outputs/<slug>/resources/.gitkeep`

## Rules
- Generate pages strictly in dependency order.
- Work one page at a time.
- Pause for user review before proceeding to the next page.

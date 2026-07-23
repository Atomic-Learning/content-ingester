---
description: End-to-end content ingestion workflow for Atomic Learning pages.
applyTo: "**"
---

# Content Ingestion Policy

## Scope

- Default to top-level `inputs/`, `outputs/`, and `templates/`. Within `inputs/`, website export files go in `live-website-export/` and new content to ingest goes in `content-to-ingest/`.
- If a `human-inputs/` directory exists alongside the active input directory, read and use its contents (e.g. images, supplementary notes) when generating pages. It is optional — if it is absent, continue normally without complaint.
- Allow overriding ingestion inputs/outputs via `.env`:
  - `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
  - `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Non-negotiable Rules

- Keep work in dependency order.
- **Always activate the `.venv` virtual environment before running any Python command.** Use `. .venv/bin/activate` on Linux/macOS or `.venv\Scripts\activate` on Windows in the terminal before executing Python scripts or tools.
- Before proposing structure or generating pages, download the content template repository (`https://github.com/Atomic-Learning/content-template`) into `templates/` by following `.github/skills/download-template/SKILL.md`. Do not continue until the template files are present in `templates/`.
- Pause for user approval at each checkpoint and after each generated page.
- Keep generated ingestion artifacts in the active output directory for the run.
- Treat PDFs and PPTX files in `<input-dir>/content-to-ingest/` as supported source material.
- Before using PDF source material for structure or page generation, run `python tools/extract_pdf_assets.py` and follow `.github/instructions/pdf-data-extraction.md`.
- Before using PPTX source material for structure or page generation, run `python tools/extract_pptx_assets.py` and follow `.github/instructions/pptx-data-extraction.md`.
- Reuse existing support docs as references when needed:
  - `.github/instructions/atomisation-guidelines.md`
  - `.github/instructions/updating-proposed-structure.md`
  - `.github/instructions/updating-metadata.md`
  - `.github/instructions/content_file_details.md`
  - `.github/instructions/pdf-data-extraction.md`
  - `.github/instructions/pptx-data-extraction.md`

## Skill Routing

- For template setup, load `.github/skills/download-template/SKILL.md` before proceeding.
- For initial structure generation or regeneration of `proposed_structure.json`, load `.github/skills/input-to-proposed-structure/SKILL.md`.
- For reviewing or editing `proposed_structure.json`, load `.github/skills/proposed-structure-review-and-edit/SKILL.md`.
- For page creation from approved structure, load `.github/skills/page-generation-and-review-and-edit/SKILL.md`.
- For copying `license.md` into generated outputs, load `.github/skills/license-file-copying/SKILL.md`.
- For populating metadata authors from `authors.md`, load `.github/skills/set-authors/SKILL.md`.
- For schema validation of generated metadata, load `.github/skills/validate-metadata/SKILL.md`.
- For post-generation verification of links, tags, and graph consistency, load `.github/skills/check-output-consistency/SKILL.md`.
- For uploading approved pages to GitHub, load `.github/skills/upload-and-check/SKILL.md`.
- For regression testing under `workflow-validation/`, load `.github/skills/validate-workflow/SKILL.md`.

## Input File Hints

- In `<input-dir>/live-website-export/`, content exports may be named `current_content.md`, `selected-content-*.md`, or `content-export*.md`.
- In `<input-dir>/live-website-export/`, tag exports may be named `tags_current.md` or `selected-tags-*.md`.
- When a skill refers to live website exports, prefer the files that actually exist in the active input directory rather than assuming a single canonical filename.

---
name: upload-and-check
description: Upload generated pages to GitHub one page at a time with dry-run and review checkpoints.
---

# upload-and-check

Use this skill for checkpoint 4 publication workflow.

Resolve output path from `.env` before running:
- `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Per-page process
1. Dry run:

```bash
python .github/skills/upload-and-check/github_uploader.py Atomic-Learning -d <output-dir>/<slug> --dry-run
```

2. Upload after confirmation:

```bash
python .github/skills/upload-and-check/github_uploader.py Atomic-Learning -d <output-dir>/<slug> --force
```

3. If the user's GitHub account does not have permission to create new repositories in the organisation, the upload will fail. In that case, the user should contact the Atomic Learning team to request access, or send them the generated pages for them to upload on their behalf.
4. Update `<output-dir>/upload_summary.txt` with cumulative status (created, skipped, failed).
5. Pause for user live-site review before next page.

## Guardrails
- Keep upload order aligned with prerequisites.
- Never batch-upload all pages without explicit user instruction.

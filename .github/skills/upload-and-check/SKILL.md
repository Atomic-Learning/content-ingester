---
name: upload-and-check
description: Upload generated pages to GitHub one page at a time with dry-run and review checkpoints.
---

# upload-and-check

Use this skill for checkpoint 4 publication workflow.

## Per-page process
1. Dry run:

```bash
python .github/skills/upload-and-check/github_uploader.py Atomic-Learning -d outputs/<slug> --dry-run
```

2. Upload after confirmation:

```bash
python .github/skills/upload-and-check/github_uploader.py Atomic-Learning -d outputs/<slug> --force
```

3. Update `outputs/upload_summary.txt` with cumulative status (created, skipped, failed).
4. Pause for user live-site review before next page.

## Guardrails
- Keep upload order aligned with prerequisites.
- Never batch-upload all pages without explicit user instruction.

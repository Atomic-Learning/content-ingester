---
name: download-template
description: Download the Atomic Learning content template repository into the local templates directory.
---

# download-template

Clone the shared content template repository into `templates/` so that any step which
consumes template assets (for example `license-file-copying`, which copies `license.md`)
has them available from a known local location.

Run this before any step that reads from `templates/`.

Resolve paths from `.env` before running:
- `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
- `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

The downloader authenticates with a GitHub Personal Access Token stored in `.env`:
- `GITHUB_PAT=your_token_here`

## Produce

- A populated `templates/` directory containing the template repository contents
  (a family of template files, including `license.md`).

```bash
python .github/skills/download-template/github_downloader.py https://github.com/Atomic-Learning/content-template -d templates
```

## Guardrails

- The gate for progressing the workflow is that the template files are present in
  `templates/` (i.e. the repository has been cloned), not the exit status of the
  download command.
- If `templates/` is already populated, the script exits with an error because it will
  not overwrite existing files. This is an expected and acceptable outcome: the template
  changes infrequently, so an existing local copy is sufficient. Treat this failure as a
  no-op and continue, provided the template files are already present in `templates/`.
- Only treat the step as blocking if `templates/` is still empty after running it
  (for example due to a missing `GITHUB_PAT` or an authentication failure on a fresh clone).

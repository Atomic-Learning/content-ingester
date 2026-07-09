---
name: license-file-copying
description: Copy license file from template repo to output directories
---

# License File Copying

Use this skill to copy the template license file to a destination location.

## Read

- `.github/instructions/content_file_details.md`

## Produce

- In the output directory for each new piece of content, explicitly copy the license file from the template repository.

```bash
python .github/skills/license-file-copying/copy-license.py <output-dir>
```

- `<output-dir>` is required and may be a directory (the file is copied as `license.md`) or a full file path.
- Use the optional `--source-file <path>` argument to override the source, which defaults to `templates/license.md`.

## Guardrails

- If the license file is missing, the skill should fail and report an error.
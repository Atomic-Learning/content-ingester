# Content Ingester

This repository supports the Atomic Learning content-ingestion workflow:

1. Start from source teaching material in inputs.
2. Propose atomic pages and their prerequisite structure.
3. Build page folders with metadata and HTML content.
4. Validate structure and consistency.
5. Publish pages as one GitHub repository per page.

The process is designed so a human editor can run it end-to-end with clear checkpoints.

## Set up environment

It is recommended to open this repository in Visual Studio Code with GitHub Copilot agent or GitHub Codespaces.

Windows (PowerShell):

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Linux/macOS (bash):

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Create .env from .env.example and set your token:

```dotenv
GITHUB_PAT=your_github_pat_here
```

## Workflow

The agent instructions provided in this repository contains the full process of content ingestion and should be able to produce a sensible output from input content without human intervention. Nevertheless, it is recommended to guide the agent following the checkpoints described below to ensure high-quality output.

### Before you start

Place files in:

- inputs/
  - current_content.md (or similarly named existing content export)
    - Should list existing page slugs with brief descriptions and prerequisite/related links where available.
    - Used by the agent to avoid duplicating already-published content and to validate prerequisite references.
  - tags_current.md (or similar tags export)
    - Should list the current platform tag names (one per line or simple grouped lists).
    - Used by the agent to reuse existing tags and only propose new tags when necessary.
  - new source material in .md or .ipynb format

Outputs will be created in outputs/. Template assets may be downloaded to templates/.

### Checkpoint 1: Structure proposal

Prompt the agent to create the proposed structure from the input files, for example:

"Read everything in inputs/ and produce outputs/proposed_structure.json using .github/proposed-structure-format.md and .github/atomisation-guidelines.md. Then generate outputs/dependency_graph.md from proposed_structure and summarise key risks."

Review before approval:

1. outputs/proposed_structure.json has required keys and complete page entries.
2. Page slugs and prerequisites make sense for your curriculum.
3. status is used correctly (new vs missing prerequisites).
4. outputs/dependency_graph.md has no obvious circular dependencies.
5. Proposed tags align with current tags, with any new tags clearly justified.

### Checkpoint 2: Page generation

Prompt the agent to generate page folders and content, for example:

"Using the approved outputs/proposed_structure.json, generate all page folders in outputs/<slug>/ with metadata.json, content.html, license.md, resources/, and resources/.gitkeep. Follow .github/content_file_details.md."

Review before approval:

1. Each page folder contains all required files.
2. metadata.json slug matches folder name.
3. content.html follows house rules (no h1, UK English, clean HTML).
4. Prerequisites and related content are plausible and consistent.
5. Spot-check 3 to 5 pages for quality and scope (single learning objective).

### Checkpoint 3: Consistency and recommendations

Prompt the agent to run a consistency pass and generate recommendations, for example:

"Run a full consistency pass across outputs/, fix metadata/linking issues, regenerate outputs/dependency_graph.md from metadata, and create outputs/related_content_recommendations.md for existing platform pages."

Review before approval:

1. Final graph still has no circular dependencies.
2. No broken or unknown prerequisite slugs remain.
3. related_content_recommendations.md is specific and actionable.

### Checkpoint 4: Publish

Prompt the agent to run the publish workflow, for example:

"Run a dry-run upload with tools/github_uploader.py and show the summary. If approved, run the real upload and report created, skipped, and failed repos plus outputs/upload_summary.txt."

Review before approval:

1. Dry-run list matches the pages you expect to publish.
2. Real upload summary has acceptable failures/skips.
3. Repository URLs in outputs/upload_summary.txt are correct.

## Minimal Checklist

1. Approve proposed_structure.json and dependency_graph.md.
2. Approve generated page files and metadata quality.
3. Approve final consistency pass and recommendations.
4. Approve dry-run, then approve real publish.

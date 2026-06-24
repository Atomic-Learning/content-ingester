# Content Ingester

This repository supports the Atomic Learning content-ingestion workflow:

1. Start from source teaching material in inputs.
2. Propose atomic pages and their prerequisite structure.
3. Review the structure of all proposed pages as a whole and finalise.
4. Create and review page content one page at a time, in dependency order.
5. Publish each page to GitHub and sync to the learning site, one at a time.

The process is designed so a human editor can run it end-to-end with clear checkpoints.

## Set up environment

It is recommended to open this repository in Visual Studio Code [locally](#local-setup) on your machine with GitHub Copilot agent or [remotely](#github-codespaces-setup) in GitHub Codespaces.

### GitHub Codespaces setup

This repository includes a dev container configuration in `.devcontainer/` for Codespaces.

1. Open the repository on GitHub.
2. Select **Code** -> **Codespaces** -> **Create codespace on main** (or your working branch).
3. Wait for container build and `postCreateCommand` to finish.

### Local setup

Python 3.10 or higher is required. Create and activate a virtual environment, then install dependencies. The agent will attempt
to perform the local setup automatically if a venv is not detected.

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

### GitHub API access

A GitHub Personal Access Token (PAT) with repo permissions is required to publish content.
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
  - new source material in .md, .ipynb, or .pdf format

PDF files are supported. For PDFs, the agent should use `tools/extract_pdf_assets.py` (documented in `.github/pdf-data-extraction.md`) to extract text and image assets before proposing structure or generating page content. The default run is cross-platform and collision-safe (new suffixed output folders are created unless overwrite is explicitly requested).

If the agent hits blockers while processing PDFs, it should ask the user concise clarifying questions before continuing:

1. Background preference for extracted images: `transparent`, `white`, or `opaque`?
2. Should vector-only figures be captured with full-page rendering (`--render-vector-pages`)?
3. If output folders already exist, should extraction overwrite them (`--overwrite`) or create new suffixed folders?
4. If text extraction quality is low (for scanned PDFs), should the workflow continue with manual review notes, or pause for OCR guidance?

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

### Checkpoint 2: Per-page content creation

Pages are created one at a time, in dependency order (prerequisites first). For each page, prompt the agent to generate it and review it before moving on, for example:

"Generate the next page from outputs/proposed_structure.json that hasn't been created yet. Create the page folder in outputs/<slug>/ with metadata.json, content.html, license.md, resources/, and resources/.gitkeep. Follow .github/content_file_details.md."

Repeat this for each page. The agent will determine the next page based on which pages in proposed_structure.json do not yet have a folder in outputs/. You can delete a page folder and revisit it, or ask the agent to skip a page and return to it later.

Review before approving each page:

1. Page folder contains all required files.
2. metadata.json slug matches folder name.
3. content.html follows house rules (no h1, UK English, clean HTML).
4. Prerequisites and related content are plausible and consistent.
5. Page has a single, focused learning objective.

### Checkpoint 3: Consistency and recommendations

Once all pages have been created and individually reviewed, prompt the agent to run a consistency pass and generate recommendations, for example:

"Run a full consistency pass across outputs/, fix metadata/linking issues, regenerate outputs/dependency_graph.md from metadata, and create outputs/related_content_recommendations.md for existing platform pages."

Review before approval:

1. Final graph still has no circular dependencies.
2. No broken or unknown prerequisite slugs remain.
3. related_content_recommendations.md is specific and actionable.

### Checkpoint 4: Per-page publish

Pages are published one at a time, in the same dependency order used during content creation. For each page, prompt the agent to upload it, register it with the site, and review it before moving on, for example:

"Upload outputs/<slug>/ to GitHub using tools/github_uploader.py, register the new repository with the Atomic Learning site, trigger a sync, and share the live URL for review."

Review before approving each page:

1. The correct repository was created on GitHub.
2. outputs/upload_summary.txt has been updated to reflect all uploads so far.
3. The page appears correctly on the live site.
4. Prerequisites and related content resolve to valid pages on the site.

Once all pages have been published, prompt the agent to generate the final upload summary:

"Report all created, skipped, and failed repositories and write outputs/upload_summary.txt."

## Minimal Checklist

1. Approve proposed_structure.json and dependency_graph.md.
2. Approve each page's content individually as it is generated (in dependency order).
3. Approve final consistency pass and recommendations.
4. Approve each page's upload and site appearance individually (in dependency order).

## Developers

Focused guidance for developers of the content ingester

### Workflow Validation

Developers should run this validation process whenever they change workflow or agent behaviour (for example changes to instructions, atomisation guidance, or generation/comparison logic). See [Workflow Validation](workflow-validation/README.md) for details.

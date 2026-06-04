# Tools

This directory contains utility scripts for the content ingester project.

## generate_inputs.py

A Python script to download content and tags from HTTP export endpoints and save them to the `inputs/` folder.

### Setup

1. **Create a `.env` file** in the project root:

   ```
   API_BASE_URL=https://your-api-url
   ```

   See `.env.example` for a template.

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

Download content export:

```bash
python tools/generate_inputs.py content
```

Download tags export:

```bash
python tools/generate_inputs.py tags
```

### What it does

- Fetches `{API_BASE_URL}/content/export` or `{API_BASE_URL}/tags/export` depending on the command
- Saves the downloaded payload as-is to the `inputs/` directory
- Creates the `inputs/` directory if it doesn't exist

## generate_prerequisite_graph.py

A Python script to generate dependency graphs as Mermaid flowcharts.

This script supports two source modes:

- Step 2 mode: parse `outputs/proposed_structure.json` and generate a planning graph.
- Step 5 mode: parse `metadata.json` files in page folders and generate a final graph.

The script always writes the same output file:

- `outputs/dependency_graph.md`

### Usage

Generate from Step 2 proposed structure:

```bash
python tools/generate_prerequisite_graph.py
```

Generate from Step 5 metadata files:

```bash
python tools/generate_prerequisite_graph.py --source metadata
```

Use explicit source selection for proposed structure:

```bash
python tools/generate_prerequisite_graph.py --source proposed_structure
```

Write `dependency_graph.md` to a different output directory:

```bash
python tools/generate_prerequisite_graph.py --source metadata --output-dir outputs/dummy-tests
```

Notes:

- Existing content slugs are auto-detected from `inputs/current_content.md` when present, otherwise from `inputs/content-export*.md`.
- Output file name is always `dependency_graph.md`.
- In `--source proposed_structure` mode, the canonical input is `proposed_structure.json`.
- In proposed structure mode, pages with `status: "missing"` are rendered as missing prerequisites in the graph.

## github_downloader.py

A Python script to download GitHub repositories using a Personal Access Token (PAT).

### Setup

1. **Create a `.env` file** in the project root:

   ```
   GITHUB_PAT=your_github_token_here
   ```

   - Create a GitHub PAT at: https://github.com/settings/tokens
   - Recommended scopes: `repo` (full control of private repositories)
   - See `.env.example` for a template

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

### Usage

#### Basic usage (repo name as directory):

```bash
python tools/github_downloader.py https://github.com/owner/repo
```

#### Specify custom target directory:

```bash
python tools/github_downloader.py https://github.com/owner/repo -d /path/to/target
```

#### Supported URL formats:

- `https://github.com/owner/repo`
- `https://github.com/owner/repo.git`
- `git@github.com:owner/repo.git`

### Examples

```bash
# Download with default directory name
python tools/github_downloader.py https://github.com/torvalds/linux

# Download to specific directory
python tools/github_downloader.py https://github.com/torvalds/linux -d ./my-linux-clone

# Using SSH URL
python tools/github_downloader.py git@github.com:torvalds/linux.git -d ./linux-repo
```

### Notes

- The `.env` file containing your GitHub PAT is not tracked by git (see `.gitignore`)
- The script will fail if the target directory already exists
- Your GitHub PAT should never be committed to version control

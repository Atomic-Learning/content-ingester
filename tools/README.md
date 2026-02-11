# Tools

This directory contains utility scripts for the content ingester project.

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

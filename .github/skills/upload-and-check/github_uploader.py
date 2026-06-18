"""
GitHub Repository Uploader

Uploads content pages to repositories in a GitHub organization.
Creates new repositories and pushes content from the outputs directory.

Uses a GitHub Personal Access Token (PAT) for authentication.
The token should be stored in a .env file in the project root:
    GITHUB_PAT=your_token_here

Requirements:
    - PyGithub: pip install PyGithub
    - GitPython: pip install GitPython
"""

import os
import sys
import argparse
import json
from pathlib import Path
from git import Repo
from github import Github, GithubException
from dotenv import load_dotenv


def _find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "README.md").exists() and (candidate / ".github").exists():
            return candidate
    raise RuntimeError("Unable to determine repository root from script location.")


def load_github_token():
    """
    Load GitHub PAT from .env file.
    
    Returns:
        str: GitHub Personal Access Token
        
    Raises:
        ValueError: If GITHUB_PAT is not found in .env file
    """
    env_path = _find_repo_root() / ".env"
    load_dotenv(env_path)
    
    token = os.getenv("GITHUB_PAT")
    if not token:
        raise ValueError(
            f"GITHUB_PAT not found in .env file at {env_path}. "
            "Please create a .env file with: GITHUB_PAT=your_token_here"
        )
    return token


def get_github_client(token: str):
    """
    Create a GitHub API client.
    
    Args:
        token: GitHub Personal Access Token
        
    Returns:
        Github: GitHub API client instance
    """
    return Github(token)


def get_git_credentials_url(token: str, repo_url: str) -> str:
    """
    Build a git URL with embedded PAT for authentication.
    
    Args:
        token: GitHub Personal Access Token
        repo_url: Repository URL (e.g., https://github.com/org/repo)
        
    Returns:
        str: Authenticated git URL
    """
    if repo_url.startswith("https://"):
        return repo_url.replace("https://", f"https://{token}@")
    raise ValueError(f"Invalid repository URL: {repo_url}")


def discover_pages(outputs_dir: Path) -> list:
    """
    Discover all content pages in the outputs directory.
    
    A page is identified by a directory containing metadata.json.
    Excludes the proposed_structure.md file and recommendation files.
    
    Args:
        outputs_dir: Path to the outputs directory
        
    Returns:
        list: List of tuples (page_slug, page_path)
    """
    pages = []
    
    for item in sorted(outputs_dir.iterdir()):
        if not item.is_dir():
            continue
        
        # Skip directories that are clearly not pages
        if item.name.startswith("."):
            continue
        
        metadata_path = item / "metadata.json"
        if metadata_path.exists():
            pages.append((item.name, item))
    
    return pages


def create_repository(org, repo_slug: str, description: str = ""):
    """
    Create a new repository in the organization.
    
    If the repository already exists, returns None to indicate it should be skipped.
    
    Args:
        org: GitHub organization object
        repo_slug: Repository name (slug)
        description: Repository description
        
    Returns:
        dict: Repository information with 'name', 'url', and 'clone_url' keys, or None if repo exists
        
    Raises:
        GithubException: If repository creation fails (for reasons other than existing repo)
    """
    try:
        # Try to get existing repository
        repo = org.get_repo(repo_slug)
        print(f"  ⊘ Repository already exists, skipping: {repo.html_url}")
        return None
    except GithubException as e:
        if e.status == 404:
            # Repository doesn't exist, create it
            try:
                repo = org.create_repo(
                    name=repo_slug,
                    description=description,
                    private=False,
                    auto_init=False,
                    has_issues=True,
                    has_projects=False,
                    has_downloads=False
                )
                print(f"  ✓ Created repository: {repo.html_url}")
                return {
                    "name": repo.name,
                    "url": repo.html_url,
                    "clone_url": repo.clone_url
                }
            except GithubException as create_error:
                raise Exception(f"Failed to create repository {repo_slug}: {create_error.data}")
        else:
            raise


def push_page_to_repository(page_path: Path, repo_info: dict, token: str):
    """
    Initialize or update a git repository in the page directory and push to GitHub.
    
    This converts the page directory into a git repository (if not already one) and 
    pushes its content to the remote repository. The .git directory is left in place
    so the page directory becomes its own git repository.
    
    Args:
        page_path: Path to the local page directory (outputs/repo_slug)
        repo_info: Dictionary with 'clone_url' key from create_repository
        token: GitHub Personal Access Token
        
    Raises:
        Exception: If git operations fail
    """
    try:
        target_branch = "main"
        git_dir = page_path / ".git"
        
        # Initialize git repository in the page directory if not already one
        if not git_dir.exists():
            print("  Initializing git repository...")
            repo = Repo.init(str(page_path), initial_branch=target_branch)
            
            # Set remote
            auth_url = get_git_credentials_url(token, repo_info["clone_url"])
            repo.create_remote("origin", auth_url)
        else:
            print("  Using existing git repository...")
            repo = Repo(str(page_path))
            
            # Update remote URL in case it changed
            auth_url = get_git_credentials_url(token, repo_info["clone_url"])
            try:
                repo.delete_remote("origin")
            except Exception:
                pass
            repo.create_remote("origin", auth_url)

        # Ensure the target branch exists and is checked out
        try:
            repo.git.checkout(target_branch)
        except Exception:
            repo.git.checkout("-B", target_branch)
        
        # Stage all files
        repo.git.add('.')
        
        # Commit if there are changes
        try:
            repo.index.commit("Initial commit")
            print("  [OK] Committed changes")
        except Exception:
            print("  [INFO] No changes to commit")
        
        # Push to remote
        print("  Pushing to remote...")
        origin = repo.remote("origin")
        origin.push(f"{target_branch}:{target_branch}", set_upstream=True)
        print(f"  [OK] Pushed to {repo_info['url']}")
        
    except Exception as e:
        raise Exception(f"Failed to push page content: {str(e)}")


def upload_pages(org_name: str, outputs_dir: str, token: str, dry_run: bool = False):
    """
    Upload all pages from the outputs directory to repositories in an organization.
    
    Args:
        org_name: GitHub organization name
        outputs_dir: Path to the outputs directory
        token: GitHub Personal Access Token
        dry_run: If True, show what would be done without actually doing it
    """
    outputs_path = Path(outputs_dir)
    
    if not outputs_path.exists():
        raise ValueError(f"Outputs directory does not exist: {outputs_dir}")
    
    # Discover pages
    print(f"\nDiscovering pages in {outputs_dir}...")
    pages = discover_pages(outputs_path)
    
    if not pages:
        print("No pages found to upload.")
        return
    
    print(f"Found {len(pages)} pages to upload:")
    for page_slug, _ in pages:
        print(f"  - {page_slug}")
    
    if dry_run:
        print("\n[DRY RUN] Would create the following repositories and push content.")
        print("Use --force to actually perform the upload.")
        return
    
    # Authenticate with GitHub
    print("\nAuthenticating with GitHub...")
    client = get_github_client(token)
    
    try:
        org = client.get_organization(org_name)
        print(f"[OK] Connected to organization: {org.name}")
    except GithubException as e:
        raise ValueError(f"Failed to access organization '{org_name}'. Check that it exists and your token has access. Details: {str(e)}")
    
    # Process each page
    print(f"\nUploading pages to {org_name}...")
    print("=" * 60)
    
    created_repos = []
    skipped_repos = []
    failed_repos = []
    
    for page_slug, page_path in pages:
        try:
            print(f"\nProcessing: {page_slug}")
            
            # Read metadata to get description
            metadata_path = page_path / "metadata.json"
            description = ""
            if metadata_path.exists():
                with open(metadata_path) as f:
                    metadata = json.load(f)
                    description = metadata.get("description", "")
                    # Truncate description to GitHub's limit
                    if len(description) > 300:
                        description = description[:297] + "..."
            
            # Create repository
            repo_info = create_repository(org, page_slug, description)
            
            # If repository already exists, skip
            if repo_info is None:
                skipped_repos.append(page_slug)
                continue
            
            # Push content
            push_page_to_repository(page_path, repo_info, token)
            
            created_repos.append((page_slug, repo_info["url"]))
            
        except Exception as e:
            error_msg = str(e)
            print(f"  [FAILED] {error_msg}")
            failed_repos.append((page_slug, error_msg))
    
    # Summary
    print("\n" + "=" * 60)
    print("\nUpload Summary:")
    print(f"  [OK] Successfully processed: {len(created_repos)} repositories")
    
    if created_repos:
        print("\n  Created/Updated repositories:")
        for repo_slug, repo_url in created_repos:
            print(f"    - {repo_url}")
    
    if skipped_repos:
        print(f"\n  [SKIPPED] Already exist: {len(skipped_repos)} repositories")
        for repo_slug in skipped_repos:
            print(f"    - {repo_slug}")
    
    if failed_repos:
        print(f"\n  [FAILED] {len(failed_repos)} repositories")
        for repo_slug, error in failed_repos:
            print(f"    - {repo_slug}")
            print(f"      Error: {error}")
    else:
        print("\n[OK] All pages processed successfully!")
    
    # Write summary to file
    summary_file = outputs_path / "upload_summary.txt"
    try:
        with open(summary_file, "w", encoding="utf-8") as f:
            f.write("GitHub Upload Summary\n")
            f.write("=" * 80 + "\n\n")
            f.write(f"Organization: {org_name}\n")
            f.write(f"Total pages processed: {len(created_repos) + len(skipped_repos) + len(failed_repos)}\n\n")
            
            # Successfully uploaded
            f.write(f"SUCCESSFULLY UPLOADED ({len(created_repos)}):\n")
            f.write("-" * 80 + "\n")
            if created_repos:
                for repo_slug, repo_url in created_repos:
                    f.write(f"  [OK] {repo_slug}\n")
                    f.write(f"       URL: {repo_url}\n")
            else:
                f.write("  (None)\n")
            f.write("\n")
            
            # Skipped repositories
            f.write(f"SKIPPED - ALREADY EXIST ({len(skipped_repos)}):\n")
            f.write("-" * 80 + "\n")
            if skipped_repos:
                for repo_slug in skipped_repos:
                    f.write(f"  [SKIPPED] {repo_slug}\n")
            else:
                f.write("  (None)\n")
            f.write("\n")
            
            # Failed uploads
            f.write(f"FAILED ({len(failed_repos)}):\n")
            f.write("-" * 80 + "\n")
            if failed_repos:
                for repo_slug, error in failed_repos:
                    f.write(f"  [FAILED] {repo_slug}\n")
                    f.write(f"           Error: {error}\n")
            else:
                f.write("  (None)\n")
        
        print(f"\n[OK] Summary written to {summary_file}")
    except Exception as e:
        print(f"\n[ERROR] Failed to write summary file: {str(e)}")
    
    if failed_repos:
        sys.exit(1)
    else:
        print("\n✓ All pages processed successfully!")


def main():
    """Command-line interface for GitHub repository uploader."""
    parser = argparse.ArgumentParser(
        description="Upload content pages to repositories in a GitHub organization."
    )
    parser.add_argument(
        "organization",
        help="GitHub organization name (e.g., Atomic-Learning)"
    )
    parser.add_argument(
        "-d", "--directory",
        default="outputs",
        help="Output directory containing pages to upload (default: outputs)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without actually doing it"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Actually perform the upload (required if not using --dry-run)"
    )
    
    args = parser.parse_args()
    
    try:
        # Load GitHub token
        token = load_github_token()
        
        # Perform upload
        if args.dry_run:
            upload_pages(args.organization, args.directory, token, dry_run=True)
        elif args.force:
            upload_pages(args.organization, args.directory, token, dry_run=False)
        else:
            print("Error: Use --dry-run to preview or --force to perform the upload")
            sys.exit(1)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

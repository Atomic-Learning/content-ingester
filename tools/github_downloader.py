"""
GitHub Repository Downloader

Downloads the content of a GitHub repository to a specified directory.
Uses a GitHub Personal Access Token (PAT) for authentication.

The token should be stored in a .env file in the project root:
    GITHUB_PAT=your_token_here
"""

import os
import sys
import argparse
from pathlib import Path
from git import Repo
from dotenv import load_dotenv


def load_github_token():
    """
    Load GitHub PAT from .env file.
    
    Returns:
        str: GitHub Personal Access Token
        
    Raises:
        ValueError: If GITHUB_PAT is not found in .env file
    """
    # Load environment variables from .env file in project root
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
    
    token = os.getenv("GITHUB_PAT")
    if not token:
        raise ValueError(
            f"GITHUB_PAT not found in .env file at {env_path}. "
            "Please create a .env file with: GITHUB_PAT=your_token_here"
        )
    return token


def parse_github_url(url: str) -> tuple[str, str]:
    """
    Parse a GitHub URL to extract owner and repo name.
    
    Supports formats:
    - https://github.com/owner/repo
    - https://github.com/owner/repo.git
    - git@github.com:owner/repo.git
    
    Args:
        url: GitHub repository URL
        
    Returns:
        tuple: (owner, repo_name)
    """
    # Remove .git suffix if present
    url = url.rstrip("/")
    if url.endswith(".git"):
        url = url[:-4]
    
    # Extract from HTTPS URL
    if "github.com/" in url:
        parts = url.split("github.com/")[1].split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]
    
    # Extract from SSH URL
    if "github.com:" in url:
        parts = url.split("github.com:")[1].split("/")
        if len(parts) >= 2:
            return parts[0], parts[1]
    
    raise ValueError(f"Invalid GitHub URL format: {url}")


def build_authenticated_url(url: str, token: str) -> str:
    """
    Build an authenticated GitHub URL using a PAT.
    
    Args:
        url: GitHub repository URL
        token: GitHub Personal Access Token
        
    Returns:
        str: Authenticated URL with token embedded
    """
    # Extract owner/repo part from various URL formats
    repo_path = url
    
    # Remove .git suffix if present
    if repo_path.endswith(".git"):
        repo_path = repo_path[:-4]
    
    # Extract from HTTPS URL
    if "github.com/" in repo_path:
        repo_path = repo_path.split("github.com/")[1]
    # Extract from SSH URL
    elif "github.com:" in repo_path:
        repo_path = repo_path.split("github.com:")[1]
    
    return f"https://{token}@github.com/{repo_path}.git"


def download_repository(repo_url: str, target_dir: str, token: str):
    """
    Clone a GitHub repository to the specified directory.
    
    Args:
        repo_url: GitHub repository URL
        target_dir: Target directory for the cloned repository
        token: GitHub Personal Access Token
        
    Raises:
        ValueError: If target directory already exists
        Exception: If git clone fails
    """
    target_path = Path(target_dir)
    
    if target_path.exists():
        raise ValueError(
            f"Target directory already exists: {target_dir}. "
            "Please specify a new directory or remove the existing one."
        )
    
    try:
        auth_url = build_authenticated_url(repo_url, token)
        owner, repo = parse_github_url(repo_url)
        
        print(f"Downloading {owner}/{repo}...")
        print(f"Target directory: {target_path.absolute()}")
        
        Repo.clone_from(auth_url, target_dir)
        
        print(f"✓ Successfully downloaded to {target_dir}")
        
    except Exception as e:
        raise Exception(f"Failed to download repository: {str(e)}")


def main():
    """Command-line interface for GitHub repository downloader."""
    parser = argparse.ArgumentParser(
        description="Download a GitHub repository to a specified directory."
    )
    parser.add_argument(
        "url",
        help="GitHub repository URL (e.g., https://github.com/owner/repo)"
    )
    parser.add_argument(
        "-d", "--directory",
        default=None,
        help="Target directory for the downloaded repository (default: repo name)"
    )
    
    args = parser.parse_args()
    
    try:
        # Load GitHub token
        token = load_github_token()
        
        # Determine target directory
        if args.directory:
            target_dir = args.directory
        else:
            # Use repository name as default
            try:
                _, repo_name = parse_github_url(args.url)
                target_dir = repo_name
            except ValueError:
                print("Error: Could not parse repository URL. Please provide a target directory with -d")
                sys.exit(1)
        
        # Download repository
        download_repository(args.url, target_dir, token)
        
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

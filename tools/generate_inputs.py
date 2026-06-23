"""
Content and Tags Export Downloader

Downloads content and tags from live atomic learning website

The API base URL and API key should be stored in a .env file in the project root:
    API_BASE_URL=https://your-api-url
    API_KEY=your-api-key

Usage:
    python generate_inputs.py "search query"
"""

import os
import sys
import argparse
from pathlib import Path
from urllib.parse import quote

import requests
from dotenv import load_dotenv


def load_api_base_url() -> str:
    """
    Load API base URL from .env file.
    
    Returns:
        str: API base URL
        
    Raises:
        ValueError: If API_BASE_URL is not found in .env file
    """
    env_path = Path(__file__).parent.parent / ".env"
    load_dotenv(env_path)
    
    api_url = os.getenv("API_BASE_URL")
    if not api_url:
        raise ValueError(
            f"API_BASE_URL not found in .env file at {env_path}. "
            "Please create a .env file with: API_BASE_URL=https://your-api-url"
        )
    return api_url


def load_api_key() -> str:
    """
    Load API key from .env file.
    
    Returns:
        str: API key
        
    Raises:
        ValueError: If API_KEY is not found in .env file
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        raise ValueError(
            "API_KEY not found in .env file. "
            "Please add: API_KEY=your-api-key"
        )
    return api_key

def prepare_inputs_directory(inputs_dir: Path) -> Path:
    """
    Ensure inputs directory exists.

    Args:
        inputs_dir: Path to the inputs directory

    Returns:
        Path: Inputs directory path
    """
    inputs_dir.mkdir(parents=True, exist_ok=True)
    return inputs_dir


def download_export(endpoint: str, export_type: str, download_dir: Path, api_key: str) -> None:
    """
    Download content from an export endpoint and save to inputs folder.
    
    Args:
        endpoint: Full URL endpoint to download from
        export_type: Type of export (content or tags)
        download_dir: Path to the inputs directory
        api_key: API key for authentication
        
    Raises:
        requests.RequestException: If HTTP request fails
        IOError: If file operations fail
    """
    inputs_dir = prepare_inputs_directory(download_dir)

    headers = {"X-API-Key": api_key}
    response = requests.get(endpoint, headers=headers, timeout=30)
    response.raise_for_status()

    output_path = inputs_dir / f"current-{export_type}-export.md"
    output_path.write_bytes(response.content)


def parse_arguments() -> argparse.Namespace:
    """
    Parse command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments
    """
    parser = argparse.ArgumentParser(
         description="Download content and tags from query-based endpoints",
        epilog="Examples:\n"
             "  python generate_inputs.py \"numpy\"\n"
             "  python generate_inputs.py \"data science\"",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "query",
        help="Search query used to download both content and tags",
    )
    
    parser.add_argument(
        "-d",
        "--download-dir",
        type=Path,
        default=Path(__file__).parent.parent / "inputs",
        help="Directory to save inputs (default: ./inputs)",
    )
    
    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the CLI.
    """
    try:
        # Parse arguments
        args = parse_arguments()
        
        # Load API base URL and key
        api_base_url = load_api_base_url()
        api_key = load_api_key()
        
        # Ensure URL doesn't have trailing slash for consistency
        api_base_url = api_base_url.rstrip("/")
        normalized_query = " ".join(args.query.split())
        query = quote(normalized_query, safe="")
        
        # Build endpoint URLs and download both exports.
        tags_endpoint = f"{api_base_url}/api/data/tags/{query}/tagsmd"
        content_endpoint = f"{api_base_url}/api/data/content/{query}/contentmd"

        download_export(tags_endpoint, "tags", args.download_dir, api_key)
        download_export(content_endpoint, "content", args.download_dir, api_key)
        
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Network error: Failed to download from endpoint - {e}", file=sys.stderr)
        sys.exit(1)
    except IOError as e:
        print(f"File error: Failed to save file - {e}", file=sys.stderr)
        sys.exit(1)
    except SystemExit:
        # argparse calls sys.exit() for --help and errors
        raise
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

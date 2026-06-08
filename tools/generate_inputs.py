"""
Content and Tags Export Downloader

Downloads content and tags from live atomic learning website

The API base URL should be stored in a .env file in the project root:
    API_BASE_URL=https://your-api-url

Usage:
    python generate_inputs.py content    # Download from {API_BASE_URL}/content/export
    python generate_inputs.py tags       # Download from {API_BASE_URL}/tags/export
"""

import os
import sys
import argparse
from pathlib import Path

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


def download_export(endpoint: str, export_type: str, download_dir: Path) -> None:
    """
    Download content from an export endpoint and save to inputs folder.
    
    Args:
        endpoint: Full URL endpoint to download from
        export_type: Type of export (content or tags)
        download_dir: Path to the inputs directory
        
    Raises:
        requests.RequestException: If HTTP request fails
        IOError: If file operations fail
    """
    inputs_dir = prepare_inputs_directory(download_dir)

    response = requests.get(endpoint, timeout=30)
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
        description="Download content and tags from export endpoints",
        epilog="Examples:\n"
               "  python generate_inputs.py content\n"
               "  python generate_inputs.py tags",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "export_type",
        choices=["content", "tags"],
        help="Type of export to download (content or tags)",
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
        
        # Load API base URL
        api_base_url = load_api_base_url()
        
        # Ensure URL doesn't have trailing slash for consistency
        api_base_url = api_base_url.rstrip("/")
        
        # Build endpoint URL
        endpoint = f"{api_base_url}/{args.export_type}/export"
        
        # Download and save
        download_export(endpoint, args.export_type, args.download_dir)
        
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

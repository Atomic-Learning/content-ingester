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
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv


class OperationCancelledError(Exception):
    """Raised when the user cancels an interactive operation."""


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


def prepare_inputs_directory(export_type: str) -> Path:
    """
    Ensure inputs directory is ready for a new export.

    If matching export files already exist in inputs, ask the user whether to
    delete only those matching files before continuing.

    Returns:
        Path: Inputs directory path

    Raises:
        OperationCancelledError: If user chooses not to delete matching files
        OSError: If matching files cannot be removed
    """
    inputs_dir = Path(__file__).parent.parent / "inputs"
    inputs_dir.mkdir(parents=True, exist_ok=True)

    existing_entries = [
        path
        for path in inputs_dir.glob(f"{export_type}-export-*.md")
        if path.is_file() or path.is_symlink()
    ]
    if not existing_entries:
        return inputs_dir

    print(f"Detected existing {export_type} export files in {inputs_dir}.")
    response = input(
        f"Delete existing {export_type} export files before downloading new export? [y/N]: "
    ).strip().lower()
    if response != "y":
        raise OperationCancelledError("Operation cancelled by user.")

    for entry in existing_entries:
        entry.unlink()

    return inputs_dir


def download_export(endpoint: str, export_type: str) -> None:
    """
    Download content from an export endpoint and save to inputs folder.
    
    Args:
        endpoint: Full URL endpoint to download from
        export_type: Type of export (content or tags)
        
    Raises:
        requests.RequestException: If HTTP request fails
        IOError: If file operations fail
    """
    inputs_dir = prepare_inputs_directory(export_type)

    response = requests.get(endpoint, timeout=30)
    response.raise_for_status()

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_path = inputs_dir / f"{export_type}-export-{timestamp}.md"
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
        download_export(endpoint, args.export_type)
        
    except ValueError as e:
        print(f"Configuration error: {e}", file=sys.stderr)
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Network error: Failed to download from endpoint - {e}", file=sys.stderr)
        sys.exit(1)
    except OperationCancelledError as e:
        print(str(e), file=sys.stderr)
        sys.exit(0)
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

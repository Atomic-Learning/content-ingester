"""Set author names in metadata.json files from authors.md.

This script reads author names from <input-dir>/authors.md and applies them to
metadata.json files. It validates the updated files against the metadata schema.

Usage:
    Update all metadata.json files under an output directory::

        python .github/skills/set-authors/set_authors.py --output-dir outputs

    Update a single metadata.json file::

        python .github/skills/set-authors/set_authors.py --metadata-file outputs/my-page/metadata.json
"""

import argparse
import json
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
import os


def _find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "README.md").exists() and (candidate / ".github").exists():
            return candidate
    raise RuntimeError("Unable to determine repository root from script location.")


ROOT_DIR = _find_repo_root()
load_dotenv(ROOT_DIR / ".env")

# Resolve input directory from .env (default: inputs/)
INPUT_DIR = Path(os.getenv("CONTENT_INGESTER_INPUTS_DIR", "inputs"))
if not INPUT_DIR.is_absolute():
    INPUT_DIR = ROOT_DIR / INPUT_DIR

# Schema for validation
DEFAULT_SCHEMA_FILE = ROOT_DIR / ".github" / "instructions" / "metadata.schema.json"


def _validate_author_id(author_id: str) -> bool:
    """Check if an author ID matches the required pattern: ^[a-z0-9]+(-[a-z0-9]+)*$"""
    return bool(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", author_id))


def _warn_if_example_authors(authors: list[str]) -> None:
    """Warn if authors list contains example/placeholder names.
    
    Example authors are: jane-doe, joe-bloggs
    """
    example_authors = {"jane-doe", "joe-bloggs"}
    found_examples = [a for a in authors if a in example_authors]
    
    if found_examples:
        print(
            f"\n⚠ Warning: Found example author(s): {', '.join(found_examples)}",
            file=sys.stderr,
        )
        print(
            "  Please replace these with real author identifiers in inputs/authors.md",
            file=sys.stderr,
        )
        print()


def _parse_authors_from_file(authors_path: Path) -> list[str] | None:
    """Read and parse authors from authors.md file.
    
    Expected format: one author slug per line, e.g.
    jane-doe
    jim-bloggs
    chris-cooling
    
    Returns:
        List of author slugs (stripped and validated), or None if file not found.
        
    Raises:
        ValueError: If file contains invalid author slugs or is malformed.
    """
    if not authors_path.exists():
        return None
    
    try:
        with authors_path.open("r", encoding="utf-8") as f:
            lines = [line.strip() for line in f if line.strip()]
    except OSError as e:
        raise ValueError(f"Failed to read {authors_path}: {e}")
    
    if not lines:
        return None
    
    # Validate each author ID
    invalid_authors = [a for a in lines if not _validate_author_id(a)]
    if invalid_authors:
        raise ValueError(
            f"Invalid author identifier(s) in {authors_path}: {', '.join(invalid_authors)}. "
            "Author identifiers must be lowercase, hyphen-separated (e.g. john-doe)."
        )
    
    return lines


def _validate_metadata_file(metadata_path: Path) -> bool:
    """Validate a metadata.json file against the schema.
    
    Returns:
        True if valid, False otherwise. Prints validation errors to stderr.
    """
    # Import the shared validation utility
    sys.path.insert(0, str(ROOT_DIR / ".github" / "skills"))
    from _shared.validate_json import validate_file
    
    exit_code = validate_file(metadata_path, DEFAULT_SCHEMA_FILE)
    return exit_code == 0


def _update_metadata_authors(metadata_path: Path, authors: list[str]) -> bool:
    """Update authors field in a metadata.json file.
    
    Args:
        metadata_path: Path to the metadata.json file.
        authors: List of author slugs to set.
        
    Returns:
        True if successful, False otherwise.
    """
    try:
        with metadata_path.open("r", encoding="utf-8") as f:
            metadata = json.load(f)
        
        # Update authors field
        metadata["authors"] = authors
        
        # Write back with consistent formatting
        with metadata_path.open("w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4, ensure_ascii=False)
            f.write("\n")  # Trailing newline for consistency
        
        return True
    except (json.JSONDecodeError, OSError, KeyError) as e:
        print(f"✗ Error updating {metadata_path}: {e}", file=sys.stderr)
        return False


def _process_metadata_file(metadata_path: Path, authors: list[str]) -> bool:
    """Process a single metadata.json file: update authors and validate.
    
    Returns:
        True if successful, False if validation failed.
    """
    # Normalize to absolute path
    abs_path = metadata_path.resolve()
    
    if not abs_path.exists():
        print(f"✗ File not found: {abs_path}", file=sys.stderr)
        return False
    
    # Update the file
    if not _update_metadata_authors(abs_path, authors):
        return False
    
    # Validate - use display path that's relative if possible, else absolute
    try:
        display_path = abs_path.relative_to(ROOT_DIR)
    except ValueError:
        display_path = abs_path
    
    print(f"  Validating {display_path}...")
    if not _validate_metadata_file(abs_path):
        print(f"✗ Validation failed for {abs_path}", file=sys.stderr)
        return False
    
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Set author names in metadata.json files from authors.md.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--metadata-file",
        type=Path,
        help="Path to a single metadata.json file to update.",
    )
    group.add_argument(
        "--output-dir",
        type=Path,
        help="Output directory to recursively find and update all metadata.json files.",
    )
    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()
        
        # Parse authors from authors.md
        authors_file = INPUT_DIR / "authors.md"
        print(f"Reading authors from {authors_file}...")
        authors = _parse_authors_from_file(authors_file)
        
        # Authors are required for this skill
        if not authors:
            print(
                f"✗ Error: {authors_file} not found or is empty.",
                file=sys.stderr,
            )
            print(
                "  Authors are required for generated pages.",
                file=sys.stderr,
            )
            print(
                "  Please create authors.md with one author per line:",
                file=sys.stderr,
            )
            print(
                "    jane-doe",
                file=sys.stderr,
            )
            print(
                "    jim-bloggs",
                file=sys.stderr,
            )
            return 2
        
        print(f"  Authors: {', '.join(authors)}")
        
        # Warn if using example authors
        _warn_if_example_authors(authors)
        
        # Collect metadata files to process
        if args.metadata_file:
            # Normalize relative paths to absolute
            metadata_file = args.metadata_file.resolve()
            metadata_files = [metadata_file]
        else:
            # Normalize relative paths to absolute
            output_dir = args.output_dir.resolve()
            if not output_dir.is_dir():
                print(f"✗ Directory not found: {output_dir}", file=sys.stderr)
                return 2
            
            metadata_files = sorted(output_dir.rglob("metadata.json"))
            if not metadata_files:
                print(
                    f"✗ No metadata.json files found under {output_dir}",
                    file=sys.stderr,
                )
                return 2
        
        # Process all files
        print(f"\nUpdating {len(metadata_files)} file(s)...")
        results = [_process_metadata_file(f, authors) for f in metadata_files]
        
        # Report summary
        total = len(results)
        successful = sum(1 for r in results if r)
        failed = total - successful
        
        print()
        if failed == 0:
            print(f"✓ Successfully updated all {total} metadata.json file(s).")
            return 0
        else:
            print(
                f"✗ {failed}/{total} metadata.json file(s) failed "
                "(see errors above)."
            )
            return 1
            
    except ValueError as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return 2
    except Exception as e:
        print(f"✗ Unexpected error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

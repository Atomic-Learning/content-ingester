import argparse
import sys
from pathlib import Path

# Make the shared skills utilities importable without package installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _shared.validate_json import validate_file  # noqa: E402

# Schema lives at .github/instructions/ — two directories up from this skill folder.
DEFAULT_SCHEMA_FILE = (
    Path(__file__).resolve().parents[2] / "instructions" / "metadata.schema.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate metadata.json file(s) against metadata.schema.json.",
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "--metadata-file",
        type=Path,
        help="Path to a single metadata.json file to validate.",
    )
    group.add_argument(
        "--metadata-root",
        type=Path,
        help="Root directory to recursively find and validate all metadata.json files.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.metadata_file:
        return validate_file(args.metadata_file, DEFAULT_SCHEMA_FILE)

    # Directory mode: validate every metadata.json found under the root.
    if not args.metadata_root.is_dir():
        print(f"Directory not found: {args.metadata_root}", file=sys.stderr)
        return 2

    metadata_files = sorted(args.metadata_root.rglob("metadata.json"))
    if not metadata_files:
        print(
            f"No metadata.json files found under {args.metadata_root}", file=sys.stderr
        )
        return 2

    results = [validate_file(f, DEFAULT_SCHEMA_FILE) for f in metadata_files]
    total = len(results)
    invalid = sum(1 for r in results if r != 0)
    exit_code = max(results)

    if exit_code == 0:
        print(f"\n✓ All {total} metadata.json file(s) valid.")
    else:
        print(f"\n✗ {invalid}/{total} metadata.json file(s) failed validation.")

    return exit_code


if __name__ == "__main__":
    sys.exit(main())

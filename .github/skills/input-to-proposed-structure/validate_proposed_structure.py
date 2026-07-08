import argparse
import sys
from pathlib import Path

# Make the shared skills utilities importable without package installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _shared.validate_json import validate_file  # noqa: E402

# Schema lives at .github/instructions/ — two directories up from this skill folder.
DEFAULT_SCHEMA_FILE = (
    Path(__file__).resolve().parents[2]
    / "instructions"
    / "proposed-structure.schema.json"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate proposed_structure.json against proposed-structure.schema.json.",
    )
    parser.add_argument(
        "--proposed-file",
        type=Path,
        required=True,
        help="Path to the proposed_structure JSON file to validate.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    return validate_file(args.proposed_file, DEFAULT_SCHEMA_FILE)


if __name__ == "__main__":
    sys.exit(main())

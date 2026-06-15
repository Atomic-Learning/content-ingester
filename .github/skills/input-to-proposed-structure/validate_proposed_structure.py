import argparse
import json
import sys
from pathlib import Path
from jsonschema import Draft202012Validator

# Schema lives at .github/instructions/ — two directories up from this skill folder.
DEFAULT_SCHEMA_FILE = (
    Path(__file__).resolve().parents[2] / "instructions" / "proposed-structure.schema.json"
)


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)



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

    if not DEFAULT_SCHEMA_FILE.exists():
        print(f"Schema file not found: {DEFAULT_SCHEMA_FILE}", file=sys.stderr)
        return 2
    if not args.proposed_file.exists():
        print(f"Proposed structure file not found: {args.proposed_file}", file=sys.stderr)
        return 2

    try:
        schema = load_json(DEFAULT_SCHEMA_FILE)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Unable to load schema {DEFAULT_SCHEMA_FILE}: {exc}", file=sys.stderr)
        return 2

    try:
        instance = load_json(args.proposed_file)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {args.proposed_file}: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Unable to read {args.proposed_file}: {exc}", file=sys.stderr)
        return 2

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(instance), key=lambda e: list(e.absolute_path))

    if not errors:
        print(f"✓ {args.proposed_file} is valid against {DEFAULT_SCHEMA_FILE.name}")
        return 0

    print(f"✗ {len(errors)} schema error(s) in {args.proposed_file}:")
    for error in errors:
        print(f"  - {'/'.join(str(p) for p in error.absolute_path) or '<root>'}: {error.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main())

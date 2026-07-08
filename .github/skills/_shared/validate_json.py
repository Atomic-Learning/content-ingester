"""Shared JSON schema validation helper used by validate_proposed_structure.py and
validate_metadata.py.  Import this module by inserting the parent skills directory
onto sys.path first:

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from _shared.validate_json import validate_file
"""

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


def load_json(path: Path) -> object:
    with path.open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def validate_file(instance_path: Path, schema_path: Path) -> int:
    """Validate *instance_path* against *schema_path*.

    Returns:
        0  – file is valid.
        1  – file contains schema errors.
        2  – a file could not be read or the schema is missing.
    """
    if not schema_path.exists():
        print(f"Schema file not found: {schema_path}", file=sys.stderr)
        return 2
    if not instance_path.exists():
        print(f"File not found: {instance_path}", file=sys.stderr)
        return 2

    try:
        schema = load_json(schema_path)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Unable to load schema {schema_path}: {exc}", file=sys.stderr)
        return 2

    try:
        instance = load_json(instance_path)
    except json.JSONDecodeError as exc:
        print(f"Invalid JSON in {instance_path}: {exc}", file=sys.stderr)
        return 2
    except OSError as exc:
        print(f"Unable to read {instance_path}: {exc}", file=sys.stderr)
        return 2

    validator = Draft202012Validator(schema)
    errors = sorted(
        validator.iter_errors(instance), key=lambda e: list(e.absolute_path)
    )

    if not errors:
        print(f"✓ {instance_path} is valid against {schema_path.name}")
        return 0

    print(f"✗ {len(errors)} schema error(s) in {instance_path}:")
    for error in errors:
        path_str = "/".join(str(p) for p in error.absolute_path) or "<root>"
        print(f"  - {path_str}: {error.message}")
    return 1

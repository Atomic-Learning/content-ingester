import argparse
import sys
from pathlib import Path
from typing import Dict, List, Optional

# Make the shared skills utilities importable without package installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _shared.validate_json import load_json, validate_file  # noqa: E402

# Schema lives at .github/instructions/ — two directories up from this skill folder.
DEFAULT_SCHEMA_FILE = (
    Path(__file__).resolve().parents[2]
    / "instructions"
    / "proposed-structure.schema.json"
)


def find_prerequisite_cycle(payload: object) -> Optional[List[str]]:
    """Return a detected prerequisite cycle as an ordered slug path, if any.

    Args:
        payload: Parsed JSON payload expected to contain a pages list.

    Returns:
        Ordered cycle path ending at the repeated slug, or None when acyclic.
    """
    if not isinstance(payload, dict) or not isinstance(payload.get("pages"), list):
        return None

    dependencies: Dict[str, List[str]] = {}
    for page in payload["pages"]:
        if not isinstance(page, dict):
            continue
        slug = page.get("slug")
        prerequisites = page.get("prerequisites")
        if not isinstance(slug, str) or not isinstance(prerequisites, list):
            continue
        dependencies.setdefault(slug, []).extend(
            prerequisite
            for prerequisite in prerequisites
            if isinstance(prerequisite, str)
        )

    states: Dict[str, int] = {}
    path: List[str] = []
    path_indexes: Dict[str, int] = {}

    def visit(slug: str) -> Optional[List[str]]:
        states[slug] = 1
        path_indexes[slug] = len(path)
        path.append(slug)

        for prerequisite in dependencies[slug]:
            if prerequisite not in dependencies:
                continue
            if states.get(prerequisite, 0) == 0:
                cycle = visit(prerequisite)
                if cycle is not None:
                    return cycle
            elif states[prerequisite] == 1:
                return path[path_indexes[prerequisite] :] + [prerequisite]

        path.pop()
        path_indexes.pop(slug)
        states[slug] = 2
        return None

    for slug in dependencies:
        if states.get(slug, 0) == 0:
            cycle = visit(slug)
            if cycle is not None:
                return cycle

    return None


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments for proposed structure validation.

    Returns:
        Parsed CLI arguments namespace.
    """
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


def validate_proposed_structure(proposed_file: Path) -> int:
    """Validate schema and prerequisite graph.

    Args:
        proposed_file: Path to the proposed_structure JSON file.

    Returns:
        Process exit code: 0 on success, 1 on validation failure.
    """
    result = validate_file(proposed_file, DEFAULT_SCHEMA_FILE)
    if result != 0:
        return result

    cycle = find_prerequisite_cycle(load_json(proposed_file))
    if cycle is None:
        return 0

    print(f"✗ circular prerequisite dependency in {proposed_file}:")
    print(f"  - {' -> '.join(cycle)}")
    return 1


def main() -> int:
    """Run the CLI entrypoint.

    Returns:
        Process exit code.
    """
    args = parse_args()
    return validate_proposed_structure(args.proposed_file)


if __name__ == "__main__":
    sys.exit(main())

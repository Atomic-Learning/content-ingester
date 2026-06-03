import argparse
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple


def _find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "README.md").exists() and (candidate / ".github").exists():
            return candidate
    raise RuntimeError("Unable to determine repository root from script location.")


ROOT_DIR = _find_repo_root()
DEFAULT_INPUTS_DIR = ROOT_DIR / "inputs"
DEFAULT_OUTPUTS_DIR = ROOT_DIR / "outputs"
DEFAULT_GRAPH_MARKDOWN = DEFAULT_OUTPUTS_DIR / "dependency_graph.md"


def detect_existing_content_file(inputs_dir: Path) -> Optional[Path]:
    candidates: List[Path] = []
    patterns = [
        "current_content.md",
        "*current_content*.md",
        "content-export*.md",
        "*content*export*.md",
    ]

    for pattern in patterns:
        candidates.extend(inputs_dir.glob(pattern))

    unique_files = sorted(set(candidates), key=lambda p: p.name.lower())
    if not unique_files:
        return None

    # Prefer exact current_content naming when present.
    exact = [p for p in unique_files if p.name.lower() == "current_content.md"]
    if exact:
        return exact[0]

    return unique_files[0]


def parse_existing_slugs(content_file: Optional[Path]) -> Set[str]:
    slugs: Set[str] = set()
    if content_file is None or not content_file.exists():
        return slugs

    slug_line_pattern = re.compile(r"^\s*-\s*slug:\s*([^\s]+)\s*$")
    heading_pattern = re.compile(r"^##\s+([^\s]+)\s*$")

    with content_file.open("r", encoding="utf-8") as handle:
        for line in handle:
            slug_match = slug_line_pattern.match(line)
            if slug_match:
                slugs.add(slug_match.group(1).strip())
                continue

            heading_match = heading_pattern.match(line)
            if heading_match:
                slugs.add(heading_match.group(1).strip())

    return slugs


def parse_proposed_structure_json(proposed_file: Path) -> Tuple[Dict[str, List[str]], Set[str]]:
    with proposed_file.open("r", encoding="utf-8-sig") as handle:
        payload = json.load(handle)

    return _parse_structured_graph_payload(payload)


def _parse_structured_graph_payload(payload: dict) -> Tuple[Dict[str, List[str]], Set[str]]:
    pages: Dict[str, List[str]] = {}
    proposed_missing: Set[str] = set()

    raw_pages = payload.get("pages", [])
    if isinstance(raw_pages, list):
        for entry in raw_pages:
            if not isinstance(entry, dict):
                continue
            slug = entry.get("slug")
            if not isinstance(slug, str) or not slug.strip():
                continue
            prerequisites = entry.get("prerequisites", [])
            if not isinstance(prerequisites, list):
                prerequisites = []
            normalized_prereqs = [str(item).strip() for item in prerequisites if str(item).strip()]
            clean_slug = slug.strip()
            pages[clean_slug] = normalized_prereqs

            status = entry.get("status")
            if isinstance(status, str) and status.strip().lower() == "missing":
                proposed_missing.add(clean_slug)

    return pages, proposed_missing


def parse_proposed_structure(proposed_file: Path) -> Tuple[Dict[str, List[str]], Set[str]]:
    if proposed_file.suffix.lower() != ".json":
        raise ValueError("proposed_structure input must be JSON with pages[].status set to new/missing.")

    return parse_proposed_structure_json(proposed_file)


def parse_metadata_pages(metadata_root: Path) -> Dict[str, List[str]]:
    pages: Dict[str, List[str]] = {}

    for metadata_file in sorted(metadata_root.rglob("metadata.json")):
        try:
            with metadata_file.open("r", encoding="utf-8-sig") as handle:
                payload = json.load(handle)
        except (json.JSONDecodeError, OSError):
            continue

        slug = payload.get("slug")
        prerequisites = payload.get("prerequisites", [])

        if not isinstance(slug, str) or not slug.strip():
            continue
        if not isinstance(prerequisites, list):
            prerequisites = []

        normalized = [str(item).strip() for item in prerequisites if str(item).strip()]
        pages[slug.strip()] = normalized

    return pages


def _safe_id(raw_slug: str, used_ids: Set[str]) -> str:
    candidate = re.sub(r"[^a-zA-Z0-9_]", "_", raw_slug)
    candidate = re.sub(r"_+", "_", candidate).strip("_")
    if not candidate:
        candidate = "node"
    if candidate[0].isdigit():
        candidate = f"n_{candidate}"

    unique = candidate
    index = 2
    while unique in used_ids:
        unique = f"{candidate}_{index}"
        index += 1

    used_ids.add(unique)
    return unique


def _classify_nodes(
    pages: Dict[str, List[str]],
    existing_slugs: Set[str],
    proposed_missing: Set[str],
) -> Tuple[Dict[str, str], List[Tuple[str, str]]]:
    node_types: Dict[str, str] = {}
    edges: List[Tuple[str, str]] = []

    for slug in pages:
        if slug in proposed_missing:
            node_types[slug] = "missing"
        else:
            node_types[slug] = "new"

    for slug, prereqs in pages.items():
        for prereq in prereqs:
            if prereq not in node_types:
                if prereq in proposed_missing:
                    node_types[prereq] = "missing"
                else:
                    node_types[prereq] = "existing" if prereq in existing_slugs else "unknown"
            edges.append((prereq, slug))

    for missing_slug in proposed_missing:
        node_types.setdefault(missing_slug, "missing")

    return node_types, edges


def build_mermaid(
    pages: Dict[str, List[str]],
    existing_slugs: Set[str],
    proposed_missing: Set[str],
    direction: str,
) -> str:
    node_types, edges = _classify_nodes(pages, existing_slugs, proposed_missing)
    used_ids: Set[str] = set()
    slug_to_id: Dict[str, str] = {}

    for slug in sorted(node_types):
        slug_to_id[slug] = _safe_id(slug, used_ids)

    lines: List[str] = [f"flowchart {direction}"]

    for slug in sorted(node_types):
        node_id = slug_to_id[slug]
        label = slug.replace('"', "'")
        lines.append(f'    {node_id}["{label}"]')

    for source, target in sorted(set(edges)):
        source_id = slug_to_id[source]
        target_id = slug_to_id[target]
        lines.append(f"    {source_id} --> {target_id}")

    lines.append("")
    lines.append("    classDef new fill:#b6e7a7,stroke:#2d6a4f,color:#111,stroke-width:1px;")
    lines.append("    classDef existing fill:#d9d9d9,stroke:#666,color:#111,stroke-width:1px;")
    lines.append("    classDef missing fill:#ffe8a3,stroke:#946200,color:#111,stroke-width:1px;")
    lines.append("    classDef unknown fill:#ffd6d6,stroke:#a33,color:#111,stroke-width:1px;")

    grouped: Dict[str, List[str]] = {"new": [], "existing": [], "missing": [], "unknown": []}
    for slug, kind in node_types.items():
        grouped[kind].append(slug_to_id[slug])

    for kind in ["new", "existing", "missing", "unknown"]:
        if grouped[kind]:
            id_list = ",".join(sorted(grouped[kind]))
            lines.append(f"    class {id_list} {kind};")

    return "\n".join(lines) + "\n"


def write_markdown_wrapper(markdown_file: Path, mermaid_content: str, mode: str) -> None:
    markdown = (
        "# Dependency Graph\n\n"
        f"Generated from mode: {mode}.\n\n"
        "## Legend\n\n"
        "- Green: new page in this proposal or content batch\n"
        "- Grey: existing page already present in platform content\n"
        "- Yellow: proposed missing prerequisite not yet in platform\n"
        "- Red: referenced slug not identified as existing or proposed missing\n\n"
        "```mermaid\n"
        f"{mermaid_content}"
        "```\n"
    )
    markdown_file.write_text(markdown, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate dependency graph markdown as Mermaid from proposed structure or metadata.",
    )
    parser.add_argument(
        "--source",
        choices=["proposed_structure", "metadata"],
        default="proposed_structure",
        help="Graph source: Step 2 proposed_structure.json or Step 5 metadata files.",
    )
    parser.add_argument(
        "--proposed-file",
        type=Path,
        default=DEFAULT_OUTPUTS_DIR / "proposed_structure.json",
        help="Path to proposed_structure JSON file.",
    )
    parser.add_argument(
        "--metadata-root",
        type=Path,
        default=DEFAULT_OUTPUTS_DIR,
        help="Root directory containing page folders with metadata.json files.",
    )
    parser.add_argument(
        "--existing-content-file",
        type=Path,
        default=None,
        help="Optional explicit path to current/existing content export markdown.",
    )
    parser.add_argument(
        "--inputs-dir",
        type=Path,
        default=DEFAULT_INPUTS_DIR,
        help="Inputs directory used to auto-detect existing content file.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUTS_DIR,
        help="Directory where dependency_graph.md will be written.",
    )
    parser.add_argument(
        "--direction",
        choices=["TB", "TD", "LR", "RL", "BT"],
        default="TD",
        help="Mermaid flow direction.",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.source == "proposed_structure":
        if not args.proposed_file.exists():
            raise FileNotFoundError(f"Proposed structure file not found: {args.proposed_file}")
        pages, proposed_missing = parse_proposed_structure(args.proposed_file)
        selected_mode = "proposed"
    else:
        pages = parse_metadata_pages(args.metadata_root)
        proposed_missing = set()
        selected_mode = "metadata"

    if not pages and not proposed_missing:
        raise RuntimeError("No pages found to graph. Check input files and mode.")

    existing_content_file = args.existing_content_file
    if existing_content_file is None:
        existing_content_file = detect_existing_content_file(args.inputs_dir)

    existing_slugs = parse_existing_slugs(existing_content_file)

    mermaid = build_mermaid(
        pages=pages,
        existing_slugs=existing_slugs,
        proposed_missing=proposed_missing,
        direction=args.direction,
    )

    output_markdown_file = args.output_dir / DEFAULT_GRAPH_MARKDOWN.name
    output_markdown_file.parent.mkdir(parents=True, exist_ok=True)
    write_markdown_wrapper(output_markdown_file, mermaid, selected_mode)

    print(f"Generated dependency graph markdown: {output_markdown_file}")
    print(f"Mode: {selected_mode}")
    print(f"Page count: {len(pages)}")
    print(f"Existing content file: {existing_content_file if existing_content_file else 'none found'}")


if __name__ == "__main__":
    main()

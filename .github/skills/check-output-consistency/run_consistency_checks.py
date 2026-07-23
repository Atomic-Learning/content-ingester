#!/usr/bin/env python3
"""Run end-to-end consistency checks for generated ingestion outputs.

This script is intended to be run repeatedly during checkpoint 3.
It validates metadata files, verifies cross-page references, checks tags,
regenerates dependency_graph.md from metadata, and writes
related_content_recommendations.md.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Sequence, Set, Tuple

from dotenv import load_dotenv
from jsonschema import Draft7Validator  # type: ignore[import-untyped]


@dataclass
class CheckResult:
    errors: List[str]
    warnings: List[str]


def find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "README.md").exists() and (candidate / ".github").exists():
            return candidate
    raise RuntimeError("Unable to determine repository root.")


def resolve_dir(root: Path, env_name: str, fallback: str) -> Path:
    raw = os.getenv(env_name, fallback).strip()
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    return path


def detect_existing_content_file(inputs_dir: Path) -> Optional[Path]:
    patterns = [
        "current_content.md",
        "*current_content*.md",
        "selected-content*.md",
        "content-export*.md",
        "*content*export*.md",
    ]
    search_dir = inputs_dir / "live-website-export"
    if not search_dir.is_dir():
        search_dir = inputs_dir

    candidates: List[Path] = []
    for pattern in patterns:
        candidates.extend(search_dir.glob(pattern))

    unique = sorted(set(candidates), key=lambda p: p.name.lower())
    if not unique:
        return None

    exact = [p for p in unique if p.name.lower() == "current_content.md"]
    if exact:
        return exact[0]
    return unique[0]


def detect_tags_file(inputs_dir: Path) -> Optional[Path]:
    patterns = [
        "tags_current.md",
        "*tags_current*.md",
        "selected-tags*.md",
        "tags*.md",
    ]
    search_dir = inputs_dir / "live-website-export"
    if not search_dir.is_dir():
        search_dir = inputs_dir

    candidates: List[Path] = []
    for pattern in patterns:
        candidates.extend(search_dir.glob(pattern))

    unique = sorted(set(candidates), key=lambda p: p.name.lower())
    if not unique:
        return None

    exact = [p for p in unique if p.name.lower() == "tags_current.md"]
    if exact:
        return exact[0]
    return unique[0]


def parse_existing_slugs(content_file: Optional[Path]) -> Set[str]:
    slugs: Set[str] = set()
    if content_file is None or not content_file.exists():
        return slugs

    slug_line_pattern = re.compile(r"^\s*-\s*slug:\s*([^\s]+)\s*$")
    heading_pattern = re.compile(r"^##\s+([^\s]+)\s*$")

    for line in content_file.read_text(encoding="utf-8").splitlines():
        match = slug_line_pattern.match(line)
        if match:
            slugs.add(match.group(1).strip())
            continue

        match = heading_pattern.match(line)
        if match:
            slugs.add(match.group(1).strip())

    return slugs


def parse_existing_tags(tags_file: Optional[Path]) -> Set[str]:
    tags: Set[str] = set()
    if tags_file is None or not tags_file.exists():
        return tags

    for line in tags_file.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#"):
            continue
        if stripped.lower().startswith("generated:"):
            continue
        tags.add(stripped)

    return tags


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def discover_pages(outputs_dir: Path) -> List[Path]:
    return sorted(
        [p for p in outputs_dir.iterdir() if p.is_dir() and (
            p / "metadata.json").exists()],
        key=lambda p: p.name,
    )


def validate_metadata_schema(metadata_files: Sequence[Path], schema_file: Path) -> List[str]:
    errors: List[str] = []
    schema = load_json(schema_file)
    validator = Draft7Validator(schema)

    for metadata_file in metadata_files:
        try:
            data = load_json(metadata_file)
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{metadata_file}: invalid JSON ({exc})")
            continue

        file_errors = sorted(validator.iter_errors(data),
                             key=lambda e: list(e.path))
        for err in file_errors:
            path_str = ".".join(str(part) for part in err.path) or "<root>"
            errors.append(
                f"{metadata_file}: schema error at {path_str}: {err.message}")

    return errors


def run_consistency_checks(
    repo_root: Path,
    outputs_dir: Path,
    inputs_dir: Path,
    strict_tags: bool,
) -> CheckResult:
    errors: List[str] = []
    warnings: List[str] = []

    if not outputs_dir.exists():
        return CheckResult(errors=[f"Outputs directory not found: {outputs_dir}"], warnings=[])

    pages = discover_pages(outputs_dir)
    if not pages:
        return CheckResult(
            errors=[
                f"No page directories with metadata.json found in: {outputs_dir}"],
            warnings=[],
        )

    schema_file = repo_root / ".github" / "instructions" / "metadata.schema.json"
    metadata_files = [p / "metadata.json" for p in pages]
    errors.extend(validate_metadata_schema(metadata_files, schema_file))

    # Build slug map and verify required files.
    slug_to_page: Dict[str, Path] = {}
    for page_dir in pages:
        metadata_file = page_dir / "metadata.json"
        data = load_json(metadata_file)
        slug = data.get("slug")

        if not isinstance(slug, str) or not slug.strip():
            errors.append(f"{metadata_file}: missing or invalid slug")
            continue

        clean_slug = slug.strip()
        if clean_slug != page_dir.name:
            errors.append(
                f"Slug mismatch: directory '{page_dir.name}' vs metadata slug '{clean_slug}' in {metadata_file}"
            )

        if clean_slug in slug_to_page:
            errors.append(
                f"Duplicate slug '{clean_slug}' in {metadata_file} and {slug_to_page[clean_slug] / 'metadata.json'}"
            )
        else:
            slug_to_page[clean_slug] = page_dir

        for rel in ("content.md", "license.md", "resources/.gitkeep"):
            required = page_dir / rel
            if not required.exists():
                errors.append(f"Missing required file: {required}")

    local_slugs = set(slug_to_page)
    existing_content_file = detect_existing_content_file(inputs_dir)
    existing_slugs = parse_existing_slugs(existing_content_file)
    known_slugs = local_slugs.union(existing_slugs)

    tags_file = detect_tags_file(inputs_dir)
    existing_tags = parse_existing_tags(tags_file)

    # Reference and tag checks.
    for slug, page_dir in sorted(slug_to_page.items()):
        metadata_file = page_dir / "metadata.json"
        data = load_json(metadata_file)

        prerequisites = data.get("prerequisites", [])
        related = data.get("related", [])

        if not isinstance(prerequisites, list):
            errors.append(f"{metadata_file}: prerequisites must be a list")
            prerequisites = []
        if not isinstance(related, list):
            errors.append(f"{metadata_file}: related must be a list")
            related = []

        overlap = set(prerequisites).intersection(related)
        if overlap:
            errors.append(
                f"{metadata_file}: slugs cannot appear in both prerequisites and related: {sorted(overlap)}"
            )

        if slug in prerequisites:
            errors.append(
                f"{metadata_file}: page cannot list itself as prerequisite")
        if slug in related:
            errors.append(
                f"{metadata_file}: page cannot list itself as related")

        for ref in prerequisites:
            if ref not in known_slugs:
                errors.append(
                    f"{metadata_file}: unknown prerequisite slug '{ref}'")
        for ref in related:
            if ref not in known_slugs:
                errors.append(f"{metadata_file}: unknown related slug '{ref}'")

        tags = data.get("tags", [])
        if isinstance(tags, list) and existing_tags:
            for tag in tags:
                if tag not in existing_tags:
                    message = (
                        f"{metadata_file}: tag '{tag}' not found in {tags_file}"
                        if tags_file
                        else f"{metadata_file}: tag '{tag}' not found in detected tag export"
                    )
                    if strict_tags:
                        errors.append(message)
                    else:
                        warnings.append(message)

    if existing_content_file is None:
        warnings.append(
            "No existing content export detected; external prerequisite checks are limited.")
    if tags_file is None:
        warnings.append(
            "No tags export detected; tag consistency checks were skipped.")

    return CheckResult(errors=errors, warnings=warnings)


def regenerate_dependency_graph(repo_root: Path, outputs_dir: Path, inputs_dir: Path) -> None:
    script = repo_root / ".github" / "skills" / \
        "input-to-proposed-structure" / "generate_prerequisite_graph.py"
    cmd = [
        sys.executable,
        str(script),
        "--source",
        "metadata",
        "--metadata-root",
        str(outputs_dir),
        "--inputs-dir",
        str(inputs_dir),
        "--output-dir",
        str(outputs_dir),
    ]
    subprocess.run(cmd, check=True)


def build_related_recommendations(outputs_dir: Path) -> str:
    pages = discover_pages(outputs_dir)
    metadata_by_slug: Dict[str, dict] = {}
    for page_dir in pages:
        data = load_json(page_dir / "metadata.json")
        metadata_by_slug[data["slug"]] = data

    recommendations: List[Tuple[str, str]] = []

    for slug, data in sorted(metadata_by_slug.items()):
        prerequisites = set(data.get("prerequisites", []))
        related = set(data.get("related", []))

        # Suggest foundational back-link if page has prerequisites but no related links.
        if prerequisites and not related:
            parent = sorted(prerequisites)[0]
            recommendations.append(
                (
                    slug,
                    f"Consider adding '{parent}' to related for revision context.",
                )
            )

        # Suggest sibling discovery links for pages sharing prerequisites.
        siblings = []
        for other_slug, other_data in metadata_by_slug.items():
            if other_slug == slug:
                continue
            other_prereq = set(other_data.get("prerequisites", []))
            if prerequisites and prerequisites.intersection(other_prereq):
                siblings.append(other_slug)
        siblings = sorted(set(siblings) - related)
        if siblings:
            sample = ", ".join(siblings[:2])
            recommendations.append(
                (
                    slug,
                    f"Optional discoverability link(s): {sample}.",
                )
            )

    lines: List[str] = []
    lines.append("# Related Content Recommendations")
    lines.append("")
    lines.append("Generated from metadata relationships in outputs/.")
    lines.append("")

    if not recommendations:
        lines.append(
            "No additional related-content recommendations were identified.")
        lines.append("")
        return "\n".join(lines)

    lines.append("## Recommendations")
    lines.append("")
    for idx, (slug, message) in enumerate(recommendations, start=1):
        lines.append(f"{idx}. `{slug}`: {message}")

    lines.append("")
    return "\n".join(lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run repeatable consistency checks for generated output pages.",
    )
    parser.add_argument(
        "--inputs-dir",
        type=Path,
        default=None,
        help="Override inputs directory (default from CONTENT_INGESTER_INPUTS_DIR or inputs/).",
    )
    parser.add_argument(
        "--outputs-dir",
        type=Path,
        default=None,
        help="Override outputs directory (default from CONTENT_INGESTER_OUTPUTS_DIR or outputs/).",
    )
    parser.add_argument(
        "--strict-tags",
        action="store_true",
        help="Fail when a metadata tag is missing from current tags export.",
    )
    parser.add_argument(
        "--skip-graph",
        action="store_true",
        help="Skip dependency_graph.md regeneration.",
    )
    parser.add_argument(
        "--skip-recommendations",
        action="store_true",
        help="Skip related_content_recommendations.md generation.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = find_repo_root()
    load_dotenv(repo_root / ".env")

    inputs_dir = args.inputs_dir or resolve_dir(
        repo_root, "CONTENT_INGESTER_INPUTS_DIR", "inputs")
    outputs_dir = args.outputs_dir or resolve_dir(
        repo_root, "CONTENT_INGESTER_OUTPUTS_DIR", "outputs")

    if not inputs_dir.is_absolute():
        inputs_dir = repo_root / inputs_dir
    if not outputs_dir.is_absolute():
        outputs_dir = repo_root / outputs_dir

    result = run_consistency_checks(
        repo_root=repo_root,
        outputs_dir=outputs_dir,
        inputs_dir=inputs_dir,
        strict_tags=args.strict_tags,
    )

    print("Consistency Check Report")
    print("=" * 80)
    print(f"Inputs directory : {inputs_dir}")
    print(f"Outputs directory: {outputs_dir}")
    print(f"Errors           : {len(result.errors)}")
    print(f"Warnings         : {len(result.warnings)}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"- {warning}")

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"- {error}")
        return 1

    if not args.skip_graph:
        regenerate_dependency_graph(
            repo_root=repo_root, outputs_dir=outputs_dir, inputs_dir=inputs_dir)
        print("\nRegenerated outputs/dependency_graph.md from metadata.")

    if not args.skip_recommendations:
        recommendations = build_related_recommendations(outputs_dir)
        recommendations_file = outputs_dir / "related_content_recommendations.md"
        recommendations_file.write_text(recommendations, encoding="utf-8")
        print("Generated outputs/related_content_recommendations.md.")

    print("\nAll consistency checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

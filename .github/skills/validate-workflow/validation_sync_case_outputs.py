import argparse
import shutil
from pathlib import Path


def _find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "README.md").exists() and (candidate / ".github").exists():
            return candidate
    raise RuntimeError("Unable to determine repository root from script location.")


ROOT_DIR = _find_repo_root()
WORKFLOW_VALIDATION_DIR = ROOT_DIR / "workflow-validation"
DEFAULT_STAGING_ROOT = ROOT_DIR / ".validation-staging"


def _copy_tree(src: Path, dst: Path) -> None:
    if not src.exists():
        return
    shutil.copytree(src, dst, dirs_exist_ok=True)


def sync_outputs(case_name: str, staging_root: Path, clean_target: bool) -> Path:
    case_dir = WORKFLOW_VALIDATION_DIR / case_name
    if not case_dir.exists() or not case_dir.is_dir():
        raise ValueError(f"Validation case not found: {case_dir}")

    staged_outputs = staging_root / case_name / "outputs"
    if not staged_outputs.exists() or not staged_outputs.is_dir():
        raise ValueError(f"Staged outputs not found: {staged_outputs}")

    target = case_dir / "generated-outputs"
    if clean_target and target.exists():
        shutil.rmtree(target)

    target.mkdir(parents=True, exist_ok=True)
    _copy_tree(staged_outputs, target)
    return target


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy staged validation outputs back into workflow-validation/<case>/generated-outputs.",
    )
    parser.add_argument("--case", required=True, help="Validation case folder name.")
    parser.add_argument(
        "--staging-root",
        type=Path,
        default=DEFAULT_STAGING_ROOT,
        help="Root folder containing staged validation workspaces.",
    )
    parser.add_argument(
        "--clean-target",
        action="store_true",
        help="Delete generated-outputs before copying staged outputs.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    target = sync_outputs(args.case, args.staging_root, args.clean_target)
    print(f"Synced staged outputs to: {target}")


if __name__ == "__main__":
    main()

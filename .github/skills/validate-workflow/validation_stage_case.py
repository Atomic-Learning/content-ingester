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


def stage_case(case_name: str, staging_root: Path, clean: bool) -> Path:
    case_dir = WORKFLOW_VALIDATION_DIR / case_name
    if not case_dir.exists() or not case_dir.is_dir():
        raise ValueError(f"Validation case not found: {case_dir}")

    inputs_dir = case_dir / "inputs"
    if not inputs_dir.exists():
        raise ValueError(f"Missing required inputs directory: {inputs_dir}")

    staged_case = staging_root / case_name
    if clean and staged_case.exists():
        shutil.rmtree(staged_case)

    (staged_case / "inputs").mkdir(parents=True, exist_ok=True)
    (staged_case / "outputs").mkdir(parents=True, exist_ok=True)

    _copy_tree(inputs_dir, staged_case / "inputs")

    human_inputs = case_dir / "human-inputs"
    if human_inputs.exists() and human_inputs.is_dir():
        (staged_case / "human-inputs").mkdir(parents=True, exist_ok=True)
        _copy_tree(human_inputs, staged_case / "human-inputs")

    return staged_case


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Stage a workflow-validation case into an isolated workspace.",
    )
    parser.add_argument("--case", required=True, help="Validation case folder name.")
    parser.add_argument(
        "--staging-root",
        type=Path,
        default=DEFAULT_STAGING_ROOT,
        help="Root folder for staged validation workspaces.",
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Delete existing staged case folder before staging.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    staged_case = stage_case(args.case, args.staging_root, args.clean)
    print(f"Staged case: {staged_case}")
    print(f"Inputs: {staged_case / 'inputs'}")
    print(f"Outputs: {staged_case / 'outputs'}")
    if (staged_case / "human-inputs").exists():
        print(f"Human inputs: {staged_case / 'human-inputs'}")


if __name__ == "__main__":
    main()

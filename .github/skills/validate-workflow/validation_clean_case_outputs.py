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


def clean_case_outputs(case_name: str) -> Path:
    case_dir = WORKFLOW_VALIDATION_DIR / case_name
    if not case_dir.exists() or not case_dir.is_dir():
        raise ValueError(f"Validation case not found: {case_dir}")

    generated_outputs = case_dir / "generated-outputs"

    if generated_outputs.exists() and generated_outputs.is_dir():
        for child in generated_outputs.iterdir():
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    else:
        generated_outputs.mkdir(parents=True, exist_ok=True)

    return generated_outputs


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Clean workflow-validation/<case>/generated-outputs while preserving the directory."
        ),
    )
    parser.add_argument("--case", required=True, help="Validation case folder name.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cleaned_dir = clean_case_outputs(args.case)
    print(f"Cleaned generated outputs: {cleaned_dir}")


if __name__ == "__main__":
    main()
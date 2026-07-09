import argparse
import shutil
from pathlib import Path

from dotenv import load_dotenv


def _find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "README.md").exists() and (candidate / ".github").exists():
            return candidate
    raise RuntimeError("Unable to determine repository root from script location.")


ROOT_DIR = _find_repo_root()
load_dotenv(ROOT_DIR / ".env")

DEFAULT_SOURCE_FILE = ROOT_DIR / "templates" / "license.md"


def copy_license(source_file: Path, destination: Path) -> Path:
    if not source_file.exists():
        raise FileNotFoundError(f"Source license file not found: {source_file}")

    if destination.is_dir() or destination.suffix == "":
        target_file = destination / source_file.name
    else:
        target_file = destination

    target_file.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_file, target_file)

    return target_file


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Copy the template license file to a destination location.",
    )
    parser.add_argument(
        "destination",
        type=Path,
        help="Destination file path or directory to copy the license file into.",
    )
    parser.add_argument(
        "--source-file",
        type=Path,
        default=DEFAULT_SOURCE_FILE,
        help=(
            "Path to the source license file. Defaults to "
            "templates/license.md relative to the repository root."
        ),
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()
    # Treat relative CLI paths as repository-relative for consistency with defaults.
    if not args.source_file.is_absolute():
        args.source_file = ROOT_DIR / args.source_file
    if not args.destination.is_absolute():
        args.destination = ROOT_DIR / args.destination

    target_file = copy_license(args.source_file, args.destination)

    print(f"Copied license file: {args.source_file}")
    print(f"Destination: {target_file}")


if __name__ == "__main__":
    main()

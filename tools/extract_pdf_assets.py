#!/usr/bin/env python3
"""Extract text and images from PDFs in a cross-platform way.

Overview:
    - Extract text with ``PyMuPDF`` (``pymupdf``).
    - Extract raster images with ``PyMuPDF`` (``pymupdf``).
    - Avoid OS-specific tools such as ``pdftotext`` and ``pdfimages``.

Usage:
    Basic run over all PDFs in ``inputs/content-to-ingest/``::

        python tools/extract_pdf_assets.py

    Specify image background mode and output location::

        python tools/extract_pdf_assets.py \
            --background transparent \
            --output-dir outputs/pdf-processing

    Render full pages when no embedded raster images are found
    (useful for vector graphics)::

        python tools/extract_pdf_assets.py --render-vector-pages --render-dpi 200

    Intentionally overwrite existing matching output directories::

        python tools/extract_pdf_assets.py --overwrite

Output layout:
    For each ``inputs/content-to-ingest/<name>.pdf``, this script creates:

    - ``outputs/pdf-processing/<name>/text.md``
    - ``outputs/pdf-processing/<name>/resources/*.png``

    By default, name collisions create suffixed directories (for example,
    ``summary-2``) to avoid overwriting previous outputs.

Requirements:
    Install dependencies from ``requirements.txt`` or directly::

    python -m pip install pymupdf
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

import pymupdf
from dotenv import load_dotenv


def _find_repo_root() -> Path:
    for candidate in Path(__file__).resolve().parents:
        if (candidate / "README.md").exists() and (candidate / ".github").exists():
            return candidate
    raise RuntimeError("Unable to determine repository root from script location.")


ROOT_DIR = _find_repo_root()
load_dotenv(ROOT_DIR / ".env")


def _resolve_dir_from_env(var_name: str, fallback: str) -> Path:
    value = os.getenv(var_name, fallback).strip()
    path = Path(value)
    if not path.is_absolute():
        path = ROOT_DIR / path
    return path


DEFAULT_INPUT_DIR = _resolve_dir_from_env("CONTENT_INGESTER_INPUTS_DIR", "inputs") / "content-to-ingest"
DEFAULT_OUTPUT_DIR = _resolve_dir_from_env("CONTENT_INGESTER_OUTPUTS_DIR", "outputs") / "pdf-processing"


@dataclass
class PdfExtractionResult:
    """Result summary for a single processed PDF.

    Attributes:
        pdf_path: Input PDF path.
        output_dir: Output directory for this PDF.
        text_path: Path to extracted text file.
        embedded_images: Number of embedded images exported.
        rendered_pages: Number of full-page fallback renders produced.
    """

    pdf_path: str
    output_dir: str
    text_path: str
    embedded_images: int
    rendered_pages: int


def _save_pixmap(pix: pymupdf.Pixmap, output_path: Path, background: str) -> None:
    """Save a pixmap with the requested background policy.

    Args:
        pix: Source pixmap to write.
        output_path: Destination image path.
        background: Background mode: ``transparent``, ``white``, or ``opaque``.

    Returns:
        None.
    """
    if background == "transparent":
        pix.save(output_path.as_posix())
        return

    if pix.alpha and background in {"white", "opaque"}:
        # Drop alpha for white/opaque output. For strict white flattening,
        # post-process with Pillow if needed.
        flattened = pymupdf.Pixmap(pix, 0)
        flattened.save(output_path.as_posix())
        return

    pix.save(output_path.as_posix())


def _resolve_output_dir(output_root: Path, pdf_path: Path, overwrite: bool) -> Path:
    """Resolve a non-colliding output directory for a PDF.

    Args:
        output_root: Root directory for all extraction outputs.
        pdf_path: Source PDF path.
        overwrite: Whether existing output for the same stem may be reused.

    Returns:
        A directory path that is safe to write to.
    """
    base_dir = output_root / pdf_path.stem
    if overwrite or not base_dir.exists():
        return base_dir

    suffix = 2
    while True:
        candidate = output_root / f"{pdf_path.stem}-{suffix}"
        if not candidate.exists():
            return candidate
        suffix += 1


def _extract_text(doc: pymupdf.Document) -> str:
    """Extract page text from a PDF document using PyMuPDF.

    Args:
        doc: Open PyMuPDF document handle.

    Returns:
        UTF-8 text with page separators suitable for saving to ``text.md``.
    """
    pages: list[str] = []
    for page_index, page in enumerate(doc):
        page_text = page.get_text("text").strip()
        if page_text:
            pages.append(page_text)
        else:
            pages.append(f"[Page {page_index + 1}: no extractable text]")

    return "\n\n---\n\n".join(pages).strip() + "\n"


def extract_pdf(
    pdf_path: Path,
    output_root: Path,
    background: str,
    render_vector_pages: bool,
    render_dpi: int,
    overwrite: bool,
) -> PdfExtractionResult:
    """Extract text and image assets from one PDF.

    Args:
        pdf_path: Source PDF path.
        output_root: Root folder where this PDF's output folder is created.
        background: Image background mode.
        render_vector_pages: Whether to render full pages when no embedded
            images are present.
        render_dpi: DPI used for full-page fallback renders.
        overwrite: Whether existing output directory for the same PDF stem
            should be reused.

    Returns:
        A ``PdfExtractionResult`` describing generated artifacts.
    """
    output_dir = _resolve_output_dir(output_root, pdf_path, overwrite)
    output_dir.mkdir(parents=True, exist_ok=True)

    doc = pymupdf.open(pdf_path.as_posix())

    # 1) Text extraction with PyMuPDF.
    text_path = output_dir / "text.md"
    text_path.write_text(_extract_text(doc), encoding="utf-8")

    # 2) Image extraction with PyMuPDF.
    resources_dir = output_dir / "resources"
    resources_dir.mkdir(parents=True, exist_ok=True)

    embedded_images = 0
    rendered_pages = 0

    for page_index, page in enumerate(doc):
        page_images = page.get_images(full=True)

        if page_images:
            for img_index, img_info in enumerate(page_images):
                # xref is the internal object reference ID for an embedded image
                # inside the PDF file.
                xref = img_info[0]
                # smask is an optional soft-mask object reference. When present,
                # it carries per-pixel alpha/transparency for the image.
                smask = img_info[1]

                if smask > 0:
                    base = pymupdf.Pixmap(doc, xref)
                    mask = pymupdf.Pixmap(doc, smask)

                    # PyMuPDF requires a non-alpha color pixmap when applying
                    # a separate soft mask.
                    if base.alpha:
                        base = pymupdf.Pixmap(base, 0)

                    pix = pymupdf.Pixmap(base, mask)
                else:
                    pix = pymupdf.Pixmap(doc, xref)

                output_name = f"p{page_index + 1:03d}_img{img_index + 1:03d}.png"
                output_path = resources_dir / output_name
                _save_pixmap(pix, output_path, background)
                embedded_images += 1

        elif render_vector_pages:
            # Some PDFs draw charts/diagrams as vector commands rather than
            # embedded raster images. This fallback rasterizes the full page
            # so visual content is still captured.
            pix = page.get_pixmap(
                dpi=render_dpi,
                alpha=(background == "transparent"),
            )
            output_name = f"p{page_index + 1:03d}_page.png"
            output_path = resources_dir / output_name
            _save_pixmap(pix, output_path, background)
            rendered_pages += 1

    return PdfExtractionResult(
        pdf_path=pdf_path.as_posix(),
        output_dir=output_dir.as_posix(),
        text_path=text_path.as_posix(),
        embedded_images=embedded_images,
        rendered_pages=rendered_pages,
    )


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed CLI namespace.
    """

    parser = argparse.ArgumentParser(
        description="Extract text and images from PDFs in a directory.",
    )
    parser.add_argument(
        "--input-dir",
        type=Path,
        default=DEFAULT_INPUT_DIR,
        help="Directory containing PDF files (default: <inputs-dir>/content-to-ingest).",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Directory for extracted assets (default: <outputs-dir>/pdf-processing).",
    )
    parser.add_argument(
        "--background",
        choices=["transparent", "white", "opaque"],
        default="transparent",
        help="Background mode for exported images (default: transparent).",
    )
    parser.add_argument(
        "--render-vector-pages",
        action="store_true",
        help=(
            "Render full page images when a page has no embedded raster images "
            "(helps capture vector charts)."
        ),
    )
    parser.add_argument(
        "--render-dpi",
        type=int,
        default=200,
        help="DPI for full-page rasterization (default: 200).",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help=(
            "Reuse existing output directory names (may overwrite files). "
            "By default, the script creates a unique suffixed directory "
            "when name collisions occur."
        ),
    )
    return parser.parse_args()


def main() -> int:
    """Run the CLI workflow.

    Returns:
        Process exit code. ``0`` means success, ``1`` means a recoverable
        input/configuration error.
    """

    args = parse_args()

    if not args.input_dir.exists():
        print(f"Input directory not found: {args.input_dir}", file=sys.stderr)
        return 1

    pdf_files = sorted(args.input_dir.glob("*.pdf"))
    if not pdf_files:
        print(f"No PDF files found in {args.input_dir}", file=sys.stderr)
        return 1

    args.output_dir.mkdir(parents=True, exist_ok=True)

    all_results: list[PdfExtractionResult] = []
    for pdf_path in pdf_files:
        extraction = extract_pdf(
            pdf_path=pdf_path,
            output_root=args.output_dir,
            background=args.background,
            render_vector_pages=args.render_vector_pages,
            render_dpi=args.render_dpi,
            overwrite=args.overwrite,
        )
        all_results.append(extraction)

    summary = {
        "input_dir": args.input_dir.as_posix(),
        "output_dir": args.output_dir.as_posix(),
        "background": args.background,
        "pdf_count": len(all_results),
        "results": [r.__dict__ for r in all_results],
    }
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

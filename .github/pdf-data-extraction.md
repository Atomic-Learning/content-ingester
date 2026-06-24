# PDF Data Extraction (Current Workflow)

## Purpose

This guide defines the current, cross-platform process for extracting PDF text and images for content-ingester.

Use the script-based workflow only. Do not rely on OS-specific tools.

## Canonical Tool

Run extraction with:

- `tools/extract_pdf_assets.py`

This script handles:

- markdown text extraction via `markitdown`
- image extraction via `PyMuPDF` (`pymupdf`)
- transparency handling using PDF soft masks
- optional vector-graphics fallback (full-page rasterisation)
- output directory collision handling

## Standard Run Procedure

1. Ensure dependencies are installed from `requirements.txt`.
2. Put source PDFs in `inputs/`.
3. Run the extractor script (default settings are preferred unless there is a reason to change them).
4. Confirm artifacts exist under `outputs/pdf-processing/<pdf-name>/`.
5. Use extracted text/image assets to generate or update page content under `outputs/<slug>/`.

## Operational Commands

Basic run:

```bash
python tools/extract_pdf_assets.py
```

Run with explicit background and output path:

```bash
python tools/extract_pdf_assets.py --background transparent --output-dir outputs/pdf-processing
```

Enable vector fallback when diagrams may be vector-drawn:

```bash
python tools/extract_pdf_assets.py --render-vector-pages --render-dpi 200
```

Allow in-place overwrite of existing extraction folders when intentionally re-running:

```bash
python tools/extract_pdf_assets.py --overwrite
```

## Output Contract

For each `inputs/<name>.pdf`, expect:

- `outputs/pdf-processing/<name>/text.md`
- `outputs/pdf-processing/<name>/resources/*.png`

If folder-name collisions occur and `--overwrite` is not set, the script writes to suffixed folders (for example `summary-2`).

## Background Rules

Ask/confirm desired image background when required:

- `transparent`: default for diagrams/logos
- `white`: flattened non-alpha export
- `opaque`: non-alpha export

When the workflow is blocked or ambiguous, ask concise user questions (background mode, vector fallback, overwrite behaviour, OCR decision) before proceeding.

## Consistency Checks After Extraction

1. `text.md` is present and readable.
2. Expected images exist in `resources/`.
3. No unexpected temporary extraction files remain.
4. Referenced resources in generated page `content.html` resolve correctly.

## Known Limitations

- Some PDFs store graphics as vector instructions rather than embedded raster images; use `--render-vector-pages` in those cases.
- Scanned/image-only PDFs may produce weak text extraction and can require OCR-based follow-up.

## Related References

- `tools/extract_pdf_assets.py`
- `tools/README.md`
- `.github/proposed-structure-format.md`
- `.github/atomisation-guidelines.md`

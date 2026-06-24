# PDF Data Extraction (Current Workflow)

## Purpose

This guide defines the current, cross-platform process for extracting PDF text and images for content-ingester.

Use the script-based workflow only. Do not rely on OS-specific tools.

Default paths are resolved from `.env`:

- `CONTENT_INGESTER_INPUTS_DIR` (default: `inputs`)
- `CONTENT_INGESTER_OUTPUTS_DIR` (default: `outputs`)

## Canonical Tool

Run extraction with:

- `tools/extract_pdf_assets.py`

This script handles:

- text extraction via `PyMuPDF` (`pymupdf`)
- image extraction via `PyMuPDF` (`pymupdf`)
- transparency handling using PDF soft masks
- optional vector-graphics fallback (full-page rasterisation)
- output directory collision handling

## Standard Run Procedure

1. Ensure dependencies are installed from `requirements.txt`.
2. Put source PDFs in `<input-dir>/content-to-ingest/` (default `inputs/content-to-ingest/`).
3. Run the extractor script (default settings are preferred unless there is a reason to change them).
4. Confirm artifacts exist under `<output-dir>/pdf-processing/<pdf-name>/` (default `outputs/pdf-processing/<pdf-name>/`).
5. Use extracted text/image assets to generate or update page content under `<output-dir>/<slug>/`.

### Mandatory Image Embedding Rule For Page Generation

When creating `<output-dir>/<slug>/content.html` from PDF inputs, do not stop at extraction output.

You must:

1. Copy each image actually used by the page from `<output-dir>/pdf-processing/<pdf-name>/resources/` into `<output-dir>/<slug>/resources/`.
2. Reference it in `content.html` with a relative path such as `resources/<image-name>.png`.
3. Include `width` and `height` attributes on each `<img>`.
4. Confirm the referenced files exist in `<output-dir>/<slug>/resources/` (not only in `<output-dir>/pdf-processing/...`).

If no images are embedded in `content.html` while source PDF images exist, treat this as an incomplete page build.

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

For each `<input-dir>/content-to-ingest/<name>.pdf`, expect:

- `<output-dir>/pdf-processing/<name>/text.md`
- `<output-dir>/pdf-processing/<name>/resources/*.png`

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
5. If PDF images exist and are relevant, they are copied into `<output-dir>/<slug>/resources/` and embedded in `content.html`.

## Known Limitations

- Some PDFs store graphics as vector instructions rather than embedded raster images; use `--render-vector-pages` in those cases.
- Scanned/image-only PDFs may produce weak text extraction and can require OCR-based follow-up.

## Related References

- `tools/extract_pdf_assets.py`
- `.github/instructions/content-ingestion.instructions.md`
- `.github/instructions/updating-proposed-structure.md`
- `.github/instructions/atomisation-guidelines.md`

from __future__ import annotations

import base64
import hashlib
import os
from pathlib import Path

import fitz  # PyMuPDF

from .app import mcp
from .security import get_allowed_base, get_output_dir, resolve_and_check

MAX_DPI = int(os.getenv("PDF_MAX_DPI", "600"))


@mcp.tool()
def render_pdf_page(
    file_path: str,
    page: int,
    dpi: int = 200,
    fmt: str = "png",
    output_dir: str | None = None,
    return_base64: bool = False,
):
    """Render a single PDF page to an image."""
    if fmt.lower() == "jpg":
        fmt = "jpeg"
    if fmt.lower() not in ("png", "jpeg"):
        raise ValueError("fmt must be 'png' or 'jpeg'")
    if dpi < 72 or dpi > MAX_DPI:
        raise ValueError(f"dpi must be between 72 and {MAX_DPI}")

    base_dir = get_allowed_base()
    pdf_path = resolve_and_check(file_path, base_dir)

    doc = fitz.open(pdf_path)
    if page < 1 or page > doc.page_count:
        raise ValueError(f"page must be in 1..{doc.page_count}")

    p = doc.load_page(page - 1)
    scale = dpi / 72.0
    pix = p.get_pixmap(matrix=fitz.Matrix(scale, scale), alpha=False)

    out_dir = get_output_dir(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = pdf_path.stem
    suffix = "jpg" if fmt == "jpeg" else "png"
    out_file = out_dir / f"{stem}-p{page}-{dpi}dpi.{suffix}"
    pix.save(str(out_file))

    data = out_file.read_bytes()
    sha256 = hashlib.sha256(data).hexdigest()

    result = {
        "path": str(out_file),
        "page": page,
        "dpi": dpi,
        "format": fmt,
        "width": pix.width,
        "height": pix.height,
        "sha256": sha256,
    }
    if return_base64:
        result["data_base64"] = base64.b64encode(data).decode("ascii")
    return result

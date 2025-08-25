from pathlib import Path

import fitz
import pytest

from mcp_pdf_reader.tools_render import render_pdf_page


def make_pdf(tmp_path: Path) -> Path:
    pdf = tmp_path / "sample.pdf"
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Hello PDF")
    doc.save(pdf)
    return pdf


def test_render_png(tmp_path, monkeypatch):
    base = tmp_path / "docs"
    base.mkdir()
    pdf = make_pdf(base)
    monkeypatch.setenv("PDF_BASE_DIR", str(base))
    out = render_pdf_page.fn(str(pdf), page=1, dpi=200, fmt="png", return_base64=False)
    assert out["path"].endswith(".png")
    assert out["width"] > 0 and out["height"] > 0
    assert len(out["sha256"]) == 64


def test_out_of_range(tmp_path, monkeypatch):
    base = tmp_path / "docs"
    base.mkdir()
    pdf = make_pdf(base)
    monkeypatch.setenv("PDF_BASE_DIR", str(base))
    with pytest.raises(ValueError):
        render_pdf_page.fn(str(pdf), page=2)


def test_directory_escape(tmp_path, monkeypatch):
    base = tmp_path / "docs"
    base.mkdir()
    other = tmp_path / "other"
    other.mkdir()
    pdf = make_pdf(other)
    monkeypatch.setenv("PDF_BASE_DIR", str(base))
    with pytest.raises((ValueError, FileNotFoundError)):
        render_pdf_page.fn(str(pdf), page=1)

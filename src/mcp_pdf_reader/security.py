import os
from pathlib import Path


def get_allowed_base() -> Path:
    env = os.getenv("PDF_BASE_DIR")
    if not env:
        raise RuntimeError("PDF_BASE_DIR must be set to an allow-listed directory")
    return Path(env).resolve()


def get_output_dir(overridden: str | None) -> Path:
    env = overridden or os.getenv("PDF_IMAGE_DIR")
    return Path(env).resolve() if env else Path(os.getenv("TMPDIR") or "/tmp")


def resolve_and_check(path: str, base: Path) -> Path:
    p = (base / path).resolve() if not os.path.isabs(path) else Path(path).resolve()
    base_resolved = base.resolve()
    if not str(p).startswith(str(base_resolved) + os.sep) and p != base_resolved:
        raise ValueError("file_path outside allowed base directory")
    if not p.exists():
        raise FileNotFoundError(f"not found: {p}")
    return p

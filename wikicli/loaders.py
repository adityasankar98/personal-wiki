"""Read source files into plain text, locally. One loader per file type.

Markdown and text are read as-is. PDF (pypdf) and DOCX (python-docx) are
converted to Markdown-ish text so the same chunker handles every type; both run
offline. Every loader returns a quality report so bad extraction is visible.
"""

from dataclasses import dataclass, field
from pathlib import Path

from . import config


class SourceError(Exception):
    """A source file that cannot or must not be read."""


@dataclass
class Document:
    path: Path
    text: str                      # Markdown-ish text; line numbers refer to this
    kind: str                      # md | txt | pdf | docx
    pages: list = field(default_factory=list)   # [(page_no, first_line, last_line)] for PDFs
    warnings: list = field(default_factory=list)

    def quality(self) -> str:
        words = len(self.text.split())
        parts = [f"{words} words"]
        if self.kind == "pdf":
            parts.append(f"{len(self.pages)} pages")
        if self.warnings:
            parts.append("WARN: " + "; ".join(self.warnings))
        return ", ".join(parts)


def validate_source_path(path) -> Path:
    """Only files inside vault/raw/, real (not symlinks), allowed type, sane size."""
    p = Path(path)
    if p.is_symlink():
        raise SourceError(f"{p} is a symlink; copy the real file into vault/raw/ instead.")
    p = p.resolve()
    if not p.exists():
        raise SourceError(f"{p.name}: file not found.")
    try:
        p.relative_to(config.RAW)
    except ValueError:
        raise SourceError(
            f"{p.name} is outside vault/raw/. Copy originals into vault/raw/ "
            "(or vault/raw/private/ for private documents) so they are preserved unchanged."
        )
    if p.suffix.lower() not in config.ALLOWED_EXTENSIONS:
        raise SourceError(
            f"{p.name}: unsupported type {p.suffix!r}; allowed: "
            + ", ".join(sorted(config.ALLOWED_EXTENSIONS))
        )
    if p.stat().st_size > config.MAX_SOURCE_BYTES:
        raise SourceError(f"{p.name} is larger than {config.MAX_SOURCE_BYTES // 2**20} MB.")
    return p


def load(path: Path) -> Document:
    suffix = path.suffix.lower()
    if suffix in (".md", ".txt"):
        return Document(path, path.read_text(encoding="utf-8"), suffix[1:])
    if suffix == ".pdf":
        return _load_pdf(path)
    if suffix == ".docx":
        return _load_docx(path)
    raise SourceError(f"No loader for {suffix}")


def _load_pdf(path: Path) -> Document:
    try:
        from pypdf import PdfReader
        reader = PdfReader(str(path))
    except Exception as exc:  # corrupt, encrypted, not really a PDF
        raise SourceError(f"{path.name}: could not open PDF ({exc}).")
    lines, pages, warnings = [], [], []
    for n, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if len(text) < 40:
            warnings.append(f"page {n} has almost no text (scanned? would need OCR)")
        first = len(lines) + 1
        lines.append(f"## Page {n}")
        lines.extend(text.splitlines() or [""])
        lines.append("")
        pages.append((n, first, len(lines)))
    doc = Document(path, "\n".join(lines), "pdf", pages, warnings)
    if not doc.text.replace("## Page", "").strip():
        raise SourceError(f"{path.name}: no extractable text (image-only PDF).")
    return doc


def _load_docx(path: Path) -> Document:
    try:
        import docx
        d = docx.Document(str(path))
    except Exception as exc:
        raise SourceError(f"{path.name}: could not open DOCX ({exc}).")
    lines = []
    for para in d.paragraphs:
        text = para.text.strip()
        if not text:
            continue
        style = (para.style.name or "").lower()
        if style.startswith("heading"):
            level = "".join(ch for ch in style if ch.isdigit()) or "2"
            lines += ["", "#" * min(int(level) + 1, 4) + " " + text, ""]
        elif style == "title":
            lines += ["# " + text, ""]
        else:
            lines.append(text)
    for table in d.tables:
        for row in table.rows:
            lines.append(" | ".join(cell.text.strip() for cell in row.cells))
    warnings = [] if lines else ["document contains no text"]
    return Document(path, "\n".join(lines), "docx", [], warnings)

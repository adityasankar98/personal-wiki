"""Split a document into retrieval passages that keep their location.

Passages follow the Markdown heading structure: a passage never spans two
sections, is packed from whole paragraphs up to ~CHUNK_TARGET_WORDS, and records
its source path, heading trail and line range so every citation can be opened
and checked. Fenced code blocks are kept intact (no heading detection inside).
"""

import re
from dataclasses import asdict, dataclass

from . import config

HEADING = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")


@dataclass
class Passage:
    id: str            # "<source-stem>#<n>" -- a machine id, never shown as a note name
    source: str        # repo-relative path, e.g. vault/raw/Pac-Man DQN README.md
    kind: str          # "raw" (original evidence) or "wiki" (generated note)
    section: str       # heading trail, e.g. "What I expected > All five evaluation scores"
    anchor: str        # last heading, usable as an Obsidian [[file#heading]] link
    line_start: int
    line_end: int
    text: str

    def location(self) -> str:
        where = f"{self.source}:{self.line_start}-{self.line_end}"
        return f"{where} § {self.section}" if self.section else where

    def to_dict(self):
        return asdict(self)


def _sections(lines):
    """Yield (trail, anchor, [(line_no, text), ...]) per heading section."""
    trail, body, in_fence = [], [], False
    anchor = ""
    for no, line in enumerate(lines, start=1):
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        m = None if in_fence else HEADING.match(line)
        if m:
            if body:
                yield trail[:], anchor, body
            level, title = len(m.group(1)), m.group(2).strip()
            trail = [t for t in trail if t[0] < level] + [(level, title)]
            anchor = title
            body = []
        else:
            body.append((no, line))
    if body:
        yield trail[:], anchor, body


def _paragraphs(body):
    """Group consecutive non-blank lines (fences kept whole) into paragraphs."""
    para, in_fence = [], False
    for no, line in body:
        if line.lstrip().startswith("```"):
            in_fence = not in_fence
        if not line.strip() and not in_fence:
            if para:
                yield para
                para = []
        else:
            para.append((no, line))
    if para:
        yield para


def _split_long(para):
    """Split one oversized paragraph at line boundaries."""
    piece, words = [], 0
    for no, line in para:
        n = len(line.split())
        if piece and words + n > config.CHUNK_MAX_WORDS:
            yield piece
            piece, words = [], 0
        piece.append((no, line))
        words += n
    if piece:
        yield piece


def chunk(text: str, source: str, kind: str = "raw"):
    lines = text.splitlines()
    stem = source.rsplit("/", 1)[-1].rsplit(".", 1)[0]
    passages = []
    for trail, anchor, body in _sections(lines):
        # The document title (H1) adds little; keep the trail readable.
        names = [t for lvl, t in trail if lvl > 1] or [t for _, t in trail]
        section = " > ".join(names)
        packed, words = [], 0

        def flush():
            nonlocal packed, words
            body_text = "\n".join(l for _, l in packed).strip()
            if len(body_text.split()) >= 3:
                passages.append(Passage(
                    id=f"{stem}#{len(passages) + 1}", source=source, kind=kind,
                    section=section, anchor=anchor,
                    line_start=packed[0][0], line_end=packed[-1][0], text=body_text,
                ))
            packed, words = [], 0

        for para in _paragraphs(body):
            pieces = list(_split_long(para)) if len(" ".join(l for _, l in para).split()) > config.CHUNK_MAX_WORDS else [para]
            for piece in pieces:
                n = len(" ".join(l for _, l in piece).split())
                if packed and words + n > config.CHUNK_TARGET_WORDS:
                    flush()
                packed += piece + [(piece[-1][0], "")]
                words += n
        if packed:
            flush()
    return passages

"""`wiki check`: is the vault usable in Obsidian, traceable, and safe to publish?

  links     every [[target#heading|label]] in the curated vault resolves to exactly
            one file, and the heading (if any) exists in it (Obsidian's rules)
  names     note filename == its H1, 1-6 words, no hashes/ids; no duplicate names
  sources   every raw file still matches the sha256 recorded at ingest
  manifest  every note ingest knows about exists; unknown notes are flagged
  publish   files git would publish contain no secrets, emails, phone numbers or
            local paths (unless allowlisted with a reason), and no private,
            machine or model files are included
"""

import json
import re
import subprocess
from pathlib import Path

from . import config
from .ingest import load_concepts, load_manifest, sha256

LINK = re.compile(r"\[\[([^\]|#]+)(?:#([^\]|]+))?(?:\|[^\]]+)?\]\]")
HEADING = re.compile(r"^#{1,6}\s+(.*?)\s*#*\s*$", re.M)
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "AWS key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "API key": re.compile(r"\b(sk|pk|rk)-[A-Za-z0-9_\-]{20,}\b"),
    "Hugging Face token": re.compile(r"\bhf_[A-Za-z0-9]{30,}\b"),
    "password assignment": re.compile(r"(?i)\b(password|passwd|secret|api_key|token)\w*\s*[:=]\s*['\"][^'\"\s]{6,}['\"]"),
    "connection string": re.compile(r"postgres(ql)?://[^\s:]+:[^\s@]+@"),
    "email address": re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    "phone number": re.compile(r"(?<![\d.])(\+?1[ -]?)?\(?\d{3}\)?[ -]\d{3}-\d{4}\b"),
    "local user path": re.compile(r"/Users/[A-Za-z0-9._-]+|C:\\\\Users\\\\"),
}
FORBIDDEN_PATHS = [
    (re.compile(r"^vault/raw/private/"), "private source"),
    (re.compile(r"^vault/wiki/(Career)/"), "private note"),
    (re.compile(r"^vault/private-index\.md$"), "private index"),
    (re.compile(r"^evidence/private/"), "private evidence"),
    (re.compile(r"^data/"), "machine file (index/manifest)"),
    (re.compile(r"(^|/)\.venv/"), "virtualenv"),
    (re.compile(r"\.(safetensors|gguf|bin|pt|npz)$"), "model weights"),
    (re.compile(r"(^|/)\.env$"), "environment file"),
]


def norm_heading(text: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[#|^:\[\]\\]", " ", text)).strip().lower()


def curated_notes():
    notes = sorted(config.WIKI.rglob("*.md"))
    return notes + [p for p in (config.INDEX_MD, config.SOURCES_MD) if p.exists()]


def check_links(problems):
    by_name = {}
    for p in config.VAULT.rglob("*.md"):
        if ".obsidian" not in p.parts:
            by_name.setdefault(p.stem.lower(), []).append(p)
    count = 0
    for note in curated_notes():
        text = note.read_text(encoding="utf-8")
        for target, heading in LINK.findall(text):
            count += 1
            matches = by_name.get(target.strip().lower(), [])
            where = f"{config.rel(note)} -> [[{target}{'#' + heading if heading else ''}]]"
            if not matches:
                problems.append(("error", "broken link", where))
            elif len(matches) > 1:
                problems.append(("error", "ambiguous link", where))
            elif heading:
                heads = {norm_heading(h) for h in HEADING.findall(matches[0].read_text(encoding="utf-8"))}
                if norm_heading(heading) not in heads:
                    problems.append(("error", "missing heading", where))
    return count


def check_names(problems):
    seen = {}
    for note in sorted(config.WIKI.rglob("*.md")):
        text = note.read_text(encoding="utf-8")
        m = re.search(r"^# (.+)$", text, re.M)
        if not m or m.group(1).strip() != note.stem:
            problems.append(("error", "H1 does not match filename", config.rel(note)))
        words = note.stem.split()
        if not 1 <= len(words) <= 6 or re.search(r"\b[0-9a-f]{8,}\b|readme|chunk", note.stem, re.I):
            problems.append(("error", "machine-style or overlong name", config.rel(note)))
        key = note.stem.lower()
        if key in seen:
            problems.append(("error", "duplicate note name", f"{seen[key]} and {config.rel(note)}"))
        seen[key] = config.rel(note)
    return len(seen)


def check_sources_and_manifest(problems):
    manifest = load_manifest()
    known = set()
    for rel, m in manifest["sources"].items():
        path = config.ROOT / rel
        if not path.exists():
            problems.append(("error", "source missing", rel))
        elif sha256(path) != m["sha256"]:
            problems.append(("warn", "source changed since ingest (re-ingest it)", rel))
        known.add(m["note"])
        if not (config.ROOT / m["note"]).exists():
            problems.append(("error", "note missing", m["note"]))
    for c in load_concepts():
        known.add(f"vault/wiki/{c['folder']}/{c['title']}.md")
    for note in config.WIKI.rglob("*.md"):
        if config.rel(note) not in known:
            problems.append(("warn", "note not produced by ingest (manual or duplicate?)", config.rel(note)))
    raw = [p for p in config.RAW.rglob("*") if p.is_file() and p.suffix.lower() in config.ALLOWED_EXTENSIONS]
    for p in raw:
        if config.rel(p) not in manifest["sources"]:
            problems.append(("warn", "source not ingested yet", config.rel(p)))
    return len(manifest["sources"])


def publishable_files():
    """Files git would publish: tracked + untracked-but-not-ignored."""
    try:
        out = subprocess.run(["git", "ls-files", "--cached", "--others", "--exclude-standard"],
                             cwd=config.ROOT, capture_output=True, text=True, check=True).stdout
        return [l for l in out.splitlines() if l]
    except (OSError, subprocess.CalledProcessError):
        return None


def check_publish(problems):
    files = publishable_files()
    if files is None:
        problems.append(("warn", "not a git repository; publish scan skipped", str(config.ROOT.name)))
        return 0
    allow = json.loads((config.ROOT / "review" / "security-allowlist.json").read_text()).get("allow", []) \
        if (config.ROOT / "review" / "security-allowlist.json").exists() else []
    for f in files:
        for pattern, what in FORBIDDEN_PATHS:
            if pattern.search(f):
                problems.append(("error", f"would publish {what}", f))
        path = config.ROOT / f
        if not path.is_file() or path.stat().st_size > 2_000_000:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for name, pattern in SECRET_PATTERNS.items():
            for m in pattern.finditer(text):
                hit = m.group(0)
                if any(a["file"] == f and a["match"] in hit for a in allow) or \
                        any(a["file"] == "*" and a["match"] in hit for a in allow):
                    continue
                line = text.count("\n", 0, m.start()) + 1
                problems.append(("error", f"possible {name}", f"{f}:{line}: {hit[:60]}"))
    return len(files)


def run():
    problems = []
    n_links = check_links(problems)
    n_notes = check_names(problems)
    n_sources = check_sources_and_manifest(problems)
    n_files = check_publish(problems)
    print(f"checked {n_links} links in {n_notes} wiki notes + index/sources, {n_sources} sources, "
          f"{n_files} publishable files")
    for level, what, where in problems:
        print(f"  {level.upper():5} {what}: {where}")
    errors = sum(1 for p in problems if p[0] == "error")
    print("RESULT:", "FAIL" if errors else "PASS", f"({errors} errors, {len(problems) - errors} warnings)")
    return 1 if errors else 0

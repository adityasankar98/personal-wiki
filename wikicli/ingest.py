"""ingest: original sources -> local Gemma -> linked, human-readable wiki notes.

For each source in vault/raw/:
  1. validate + load + hash (originals are only ever read)
  2. choose the note name once (--title, or a validated Gemma proposal) and
     remember it in data/manifest.json, so re-ingesting updates the same file
  3. per top-level section (<= INGEST_SECTION_WORDS words per call): Gemma writes
     1-3 key-point bullets; then a summary and a one-line description
  4. link to curated concepts (wiki-concepts.json) whose query strongly matches
     a passage of this source; Gemma writes the one-sentence "why" from that passage
  5. apply reviewed corrections (review/corrections.json), write the note,
     keeping any "## Notes (manual)" section
Then concept notes, index.md, sources.md and the search index are rebuilt.

The harness, not the model, writes frontmatter, file names and every link.
"""

import hashlib
import json
import re
import time
from datetime import datetime
from pathlib import Path

from . import config, evidence, llm, prompts, retrieve
from .chunker import chunk
from .loaders import SourceError, load, validate_source_path

CONCEPT_LINK_MIN = 9.0          # BM25 score a source passage needs to link a concept (see README)
MANUAL = "## Notes (manual)"
TITLE_OK = re.compile(r"^[A-Za-z0-9][A-Za-z0-9 &'+(),.-]*$")


# ---------------------------------------------------------------- state files
def _read_json(path: Path, default):
    return json.loads(path.read_text()) if path.exists() else default


def load_manifest():
    return _read_json(config.MANIFEST_FILE, {"sources": {}, "links": {}})


def save_manifest(m):
    config.DATA.mkdir(exist_ok=True)
    config.MANIFEST_FILE.write_text(json.dumps(m, indent=2, ensure_ascii=False) + "\n")


def load_concepts():
    return _read_json(config.CONCEPTS_FILE, {"concepts": []})["concepts"]


def load_corrections():
    return _read_json(config.CORRECTIONS_FILE, {"corrections": []})["corrections"]


# ---------------------------------------------------------------- helpers
def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_title(title: str) -> str:
    title = re.sub(r"\s+", " ", title.strip().strip('"\'*#.').strip())
    words = title.split()
    problems = []
    if not TITLE_OK.match(title or "-"):
        problems.append("use letters, digits, spaces and - & ' ( ) only")
    if not 1 <= len(words) <= 6:
        problems.append("use 1-6 words (2-6 preferred)")
    if re.search(r"\b[0-9a-f]{8,}\b|readme|untitled|chunk|task", title, re.I):
        problems.append("no hashes, ids, 'README', 'chunk' or export-task names")
    if problems:
        raise SourceError(f"note name {title!r} rejected: " + "; ".join(problems))
    return title


def note_path(folder: str, title: str) -> Path:
    if folder not in config.WIKI_FOLDERS:
        raise SourceError(f"folder {folder!r} not allowed; choose one of {sorted(config.WIKI_FOLDERS)}")
    path = (config.WIKI / folder / f"{title}.md").resolve()
    path.relative_to(config.WIKI.resolve())          # refuse to write outside vault/wiki/
    return path


def heading_link(raw_stem: str, heading: str, label: str) -> str:
    """[[file#heading|label]] with the characters Obsidian can't use in heading links removed."""
    if not heading:
        return f"[[{raw_stem}|{label}]]"
    safe = re.sub(r"\s+", " ", re.sub(r"[#|^:\[\]\\]", " ", heading)).strip()
    return f"[[{raw_stem}#{safe}|{label}]]"


def clean(text: str) -> str:
    """Model text is data: strip anything that could become a link, tag or heading."""
    text = re.sub(r"\[\[|\]\]", "", text)
    text = re.sub(r"<([^>]{0,200})>", r"(\1)", text)    # no raw HTML in notes; keep the words
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.M)
    text = text.replace("---", "—")
    return re.sub(r"[ \t]+", " ", text).strip()


def bullets(text: str):
    out = []
    for line in text.splitlines():
        m = re.match(r"^\s*(?:[-*•]|\d+[.)])\s+(.*)", line)
        if m and len(m.group(1).split()) >= 3:
            out.append(clean(m.group(1)))
    return out


class Gemma:
    """Counts calls and time so the ingest log can report cost."""

    def __init__(self):
        self.calls, self.seconds = 0, 0.0

    def __call__(self, task, section_title, section_text):
        text, stats = llm.generate(prompts.ingest_messages(task, section_title, section_text), config.INGEST_SETTINGS)
        self.calls += 1
        self.seconds += stats["seconds"]
        return text


# ---------------------------------------------------------------- sections
def section_groups(doc_text: str, source: str):
    """Group passages by top-level section; split groups above the word budget."""
    groups, order = {}, []
    for p in chunk(doc_text, source):
        top = p.section.split(" > ")[0]
        if top not in groups:
            groups[top] = []
            order.append(top)
        groups[top].append(p)
    for top in order:
        parts, words, current = [], 0, []
        for p in groups[top]:
            n = len(p.text.split())
            if current and words + n > config.INGEST_SECTION_WORDS:
                parts.append(current)
                current, words = [], 0
            current.append(p)
            words += n
        if current:
            parts.append(current)
        for part in parts:
            text = "\n\n".join((f"({p.section})\n" if p.section != top else "") + p.text for p in part)
            if len(text.split()) >= 40 and top.lower() not in ("contents", "table of contents"):
                yield top, part[0].line_start, part[-1].line_end, text


# ---------------------------------------------------------------- one source
def ingest_source(path: Path, manifest, gemma, title=None, folder=None, private=False, origin=None, log=print):
    rel_path = config.rel(path)
    is_private = retrieve.is_private(rel_path)
    if private and not is_private:
        raise SourceError(f"--private sources must live in vault/raw/private/ (got {rel_path}).")
    doc = load(path)
    digest = sha256(path)
    entry = manifest["sources"].get(rel_path, {})
    log(f"\n== {rel_path}  ({doc.quality()}; sha256 {digest[:12]})")

    # -- note name: remembered, given, or proposed by Gemma and validated
    if title:
        title = validate_title(title)
    elif entry.get("title"):
        title = entry["title"]
    else:
        proposal = gemma("Propose a short wiki note name of 2 to 5 words that names the subject of this "
                         "document, like 'GPU Parallel Training'. Output only the name.",
                         "document start", " ".join(doc.text.split()[:400]))
        title = validate_title(clean(proposal).splitlines()[0])
        log(f"   Gemma proposed the note name: {title!r}")
    folder = folder or entry.get("folder") or ("Career" if is_private else "Projects")
    if is_private and folder not in config.PRIVATE_FOLDERS:
        raise SourceError(f"private sources must use a private folder: {sorted(config.PRIVATE_FOLDERS)}")
    target = note_path(folder, title)
    for other_rel, other in manifest["sources"].items():
        if other_rel != rel_path and other.get("title") == title:
            raise SourceError(f"note name {title!r} is already used by {other_rel}; pass a different --title.")

    old = entry.get("note")
    if old and old != config.rel(target):
        rename_note(config.ROOT / old, target, entry["title"], title, log)

    # -- key points per section
    raw_stem = path.stem
    points = []
    for top, a, b, text in section_groups(doc.text, rel_path):
        reply = gemma("Write 1 to 3 bullet points, each starting with '- ', stating the most important facts "
                      "in this section. One sentence each, at most 30 words.", top, text)
        link = heading_link(raw_stem, top if top != _h1(doc.text) else "", f"{raw_stem} § {top}")
        for bullet in bullets(reply)[:3]:
            points.append((top, bullet, f"{link}, lines {a}–{b}"))
        log(f"   section “{top[:60]}”: {len(bullets(reply)[:3])} point(s)")
    point_text = "\n".join(f"- {p[1]}" for p in points)
    summary = clean(gemma("These are key points from one document. Write a 2 to 3 sentence summary of the "
                          "whole document for a wiki note. Plain sentences only.", title, point_text))
    description = clean(gemma("Write a one-line description of this document of at most 15 words. Output only "
                              "the line.", title, point_text)).splitlines()[0].rstrip(".")

    # -- concept links, with a Gemma-written reason taken from the matching passage
    # Scored against the global index (same IDF as `wiki search`), restricted to this source.
    retrieve.rebuild_index()
    index = retrieve.load_index()
    links = {}
    for c in load_concepts():
        if c["title"] == title:
            continue
        hits = [h for h in index.search(c["query"], k=len(index.passages), per_source=0, min_relative=0)
                if h.passage.source == rel_path][:1]
        if hits and hits[0].score >= CONCEPT_LINK_MIN:
            p = hits[0].passage
            why = clean(gemma(f"In one sentence of at most 25 words, state what this passage says about "
                              f"{c['title']} in the project. Output only the sentence.", p.section, p.text))
            links[c["title"]] = {"why": why.splitlines()[0], "section": p.section.split(" > ")[0],
                                 "anchor": p.section.split(" > ")[0], "lines": [p.line_start, p.line_end],
                                 "score": round(hits[0].score, 1)}
    log(f"   linked concepts: {', '.join(links) or 'none'}")

    manifest["sources"][rel_path] = {
        "source_id": entry.get("source_id") or digest[:12],
        "title": title, "folder": folder, "note": config.rel(target), "source_path": rel_path,
        "original_filename": entry.get("original_filename") or path.name,
        "origin": origin or entry.get("origin", ""),
        "sha256": digest, "previous_sha256": entry.get("sha256") if entry.get("sha256") != digest else entry.get("previous_sha256"),
        "type": doc.kind, "visibility": "private" if is_private else "public",
        "description": description, "ingested_at": datetime.now().isoformat(timespec="seconds"),
    }
    manifest["links"][rel_path] = links
    if entry.get("sha256") and entry["sha256"] != digest:
        log("   NOTE: the original changed since the last ingest; the note is regenerated from the new text.")

    body = render_source_note(manifest["sources"][rel_path], raw_stem, summary, points, links)
    return write_note(target, body, log)


def _h1(text: str) -> str:
    m = re.search(r"^#\s+(.+)$", text, re.M)
    return m.group(1).strip() if m else ""


def render_source_note(meta, raw_stem, summary, points, links):
    fm = frontmatter({
        "type": "project" if meta["folder"] == "Projects" else "source-note",
        "description": meta["description"],
        "source_id": meta["source_id"],
        "source_file": f"[[{raw_stem}]]",
        "source_path": meta["source_path"],
        "original_filename": meta["original_filename"],
        "origin": meta["origin"],
        "sha256": meta["sha256"],
        "generated_by": f"{config.MODEL_ID}@{config.MODEL_REVISION[:7]}",
        "generated_at": meta["ingested_at"],
        "reviewed": True,
        "visibility": meta["visibility"],
        "tags": [meta["folder"].lower()],
    })
    lines = [fm, f"# {meta['title']}", "", summary, "", "## Key points", ""]
    current = None
    for top, text, where in points:
        if top != current:
            lines += ([""] if current is not None else []) + [f"### {top}", "", f"Source: {where}", ""]
            current = top
        lines.append(f"- {text}")
    lines += ["", "## Related notes", ""]
    if links:
        for t, l in sorted(links.items()):
            lines.append(f"- [[{t}]] — {l['why']}")
    else:
        lines.append("- _No curated concept matched this source strongly enough to link._")
    lines += ["", "## Sources", "",
              f"- Original: [[{raw_stem}]] (`{meta['source_path']}`, sha256 `{meta['sha256'][:12]}`)",
              "- Catalog entry: [[sources]] · Start page: [[index]]", ""]
    return "\n".join(lines)


def frontmatter(d: dict) -> str:
    out = ["---"]
    for k, v in d.items():
        if isinstance(v, bool):
            out.append(f"{k}: {'true' if v else 'false'}")
        elif isinstance(v, list):
            out.append(f"{k}:")
            out += [f"  - {json.dumps(x, ensure_ascii=False)}" for x in v]
        else:
            out.append(f"{k}: {json.dumps(str(v), ensure_ascii=False)}")
    return "\n".join(out + ["---", ""])


def apply_corrections(title: str, body: str, log):
    for c in load_corrections():
        if c["note"] not in (title, "*"):
            continue
        if c["find"] in body:
            body = body.replace(c["find"], c["replace"])
            log(f"   applied review correction: {c['reason']}")
        elif c["note"] != "*":
            log(f"   WARNING: review correction not applied (text changed): {c['find'][:60]!r}")
    return body


def write_note(target: Path, body: str, log):
    title = target.stem
    body = apply_corrections(title, body, log)
    manual = ""
    if target.exists():
        old = target.read_text(encoding="utf-8")
        if MANUAL in old:
            manual = old[old.index(MANUAL):].rstrip() + "\n"
    body = body.rstrip() + "\n\n" + (manual or f"{MANUAL}\n\n_Anything written below this heading survives re-ingestion._\n")
    target.parent.mkdir(parents=True, exist_ok=True)
    status = "created" if not target.exists() else ("unchanged" if target.read_text(encoding="utf-8") == body else "updated")
    target.write_text(body, encoding="utf-8")
    log(f"   -> {status}: {config.rel(target)}")
    return status, target


def rename_note(old: Path, new: Path, old_title: str, new_title: str, log):
    if old.exists():
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
    for note in config.VAULT.rglob("*.md"):
        if config.RAW in note.parents:
            continue
        text = note.read_text(encoding="utf-8")
        updated = re.sub(r"\[\[" + re.escape(old_title) + r"(?=[\]|#])", "[[" + new_title, text)
        if updated != text:
            note.write_text(updated, encoding="utf-8")
    log(f"   renamed note {old_title!r} -> {new_title!r} and updated incoming links")


# ---------------------------------------------------------------- concepts
def build_concepts(manifest, gemma, only=None, log=print):
    index = retrieve.Index([p for p in retrieve.load_index().passages if p.kind == "raw"])
    by_title = {m["title"]: rel for rel, m in manifest["sources"].items()}
    results = []
    for c in load_concepts():
        appears = [(manifest["sources"][rel]["title"], rel, l[c["title"]])
                   for rel, l in manifest["links"].items()
                   if c["title"] in l and manifest["sources"].get(rel, {}).get("visibility") == "public"]
        if only is not None and not any(rel in only for _, rel, _ in appears) and _concept_path(c).exists():
            continue
        hits = index.search(c["query"], k=4, per_source=2, include_private=False, synonyms=False)
        if not hits:
            log(f"   concept {c['title']}: no public passages, skipped")
            continue
        reply = clean(gemma(
            f"Using only these passages, write 2 to 4 sentences explaining {c['title']} as it appears in "
            "Aditya's projects. After each sentence cite the passage it came from as [S1], [S2] etc.",
            c["title"], prompts.passages_block(hits)))
        body_text = re.sub(r"\s*\[S(\d+)\]", lambda m: _cite_link(hits, int(m.group(1))), reply)
        body_text = re.sub(r"\s+\.", ".", body_text)
        lines = [frontmatter({"type": "concept", "description": c["description"],
                              "sources": list(dict.fromkeys(f"[[{Path(h.passage.source).stem}]]" for h in hits)),
                              "generated_by": f"{config.MODEL_ID}@{config.MODEL_REVISION[:7]}",
                              "reviewed": True, "visibility": "public", "tags": [c["folder"].lower()]}),
                 f"# {c['title']}", "", f"*{c['description']}*", "", body_text, "", "## Where it appears", ""]
        lines += [f"- [[{t}]] — {l['why']}" for t, _, l in sorted(appears)] or ["- _Not linked to a source note yet._"]
        lines += ["", "## Related notes", ""]
        lines += [f"- [[{r['title']}]] — {r['why']}" for r in c.get("related", [])]
        lines += ["", "## Sources", ""]
        lines += [f"- [S{h.rank}] " + heading_link(Path(h.passage.source).stem, h.passage.section.split(" > ")[0],
                                                     f"{Path(h.passage.source).stem} § {h.passage.section.split(' > ')[0]}")
                  + f", lines {h.passage.line_start}–{h.passage.line_end}" for h in hits]
        lines += ["- Catalog: [[sources]] · Start page: [[index]]", ""]
        results.append(write_note(_concept_path(c), "\n".join(lines), log))
    return results


def _concept_path(c):
    return note_path(c["folder"], c["title"])


def _cite_link(hits, i):
    if not 1 <= i <= len(hits):
        return ""
    p = hits[i - 1].passage
    return " (" + heading_link(Path(p.source).stem, p.section.split(" > ")[0], f"S{i}") + ")"


# ---------------------------------------------------------------- index pages
def write_index(manifest):
    concepts = {c["title"]: c for c in load_concepts()}
    groups = {"Projects": [], "Concepts": [], "Tools": [], "People": []}
    private = []
    for rel, m in sorted(manifest["sources"].items(), key=lambda kv: kv[1]["title"]):
        (private if m["visibility"] == "private" else groups.setdefault(m["folder"], [])).append((m["title"], m["description"]))
    for t, c in sorted(concepts.items()):
        if _concept_path(c).exists():
            groups.setdefault(c["folder"], []).append((t, c["description"]))
    intro = {
        "Projects": "One note per original source: what was built, the choices made, and what happened.",
        "Concepts": "Ideas that recur across projects, each linked to where it appears.",
        "Tools": "Platforms, models and hardware the projects ran on.",
        "People": "People who appear in the sources.",
    }
    lines = ["---", 'type: "index"', "---", "# Personal Wiki", "",
             "Aditya's notes on his AgenticAI course projects, generated by a local Gemma model from the original "
             "write-ups in `raw/` and reviewed against them. Start with a project, follow its links to the "
             "concepts it uses, and use each note's **Sources** section to open the original evidence.", ""]
    for folder, items in groups.items():
        if not items:
            continue
        lines += [f"## {folder}", "", f"_{intro.get(folder, '')}_", ""]
        lines += [f"- [[{t}]] — {d}" for t, d in items] + [""]
    lines += ["## Sources", "", "- [[sources]] — catalog of the original documents, their hashes and the notes made from them.", ""]
    config.INDEX_MD.write_text("\n".join(lines), encoding="utf-8")
    if private:
        config.PRIVATE_INDEX_MD.write_text("# Private notes (local only, not committed)\n\n"
                                           + "\n".join(f"- [[{t}]] — {d}" for t, d in private) + "\n")


def write_sources(manifest):
    lines = ["---", 'type: "catalog"', "---", "# Sources", "",
             "Original documents in `raw/`, preserved byte-for-byte. Machine ids and original filenames live here "
             "and in note properties, never in note names.", "",
             "| Original (in raw/) | Note | Source id | SHA-256 | Type | Origin | Last ingested |",
             "|---|---|---|---|---|---|---|"]
    for rel, m in sorted(manifest["sources"].items()):
        if m["visibility"] == "private":
            continue
        lines.append(f"| [[{Path(rel).stem}]] | [[{m['title']}]] | `{m['source_id']}` | `{m['sha256'][:16]}…` | "
                     f"{m['type']} | {m['origin'] or '-'} | {m['ingested_at'][:16].replace('T', ' ')} |")
    lines += ["", "Back to [[index]].", ""]
    config.SOURCES_MD.write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------- entry point
def targets(path_arg: str, private: bool):
    p = Path(path_arg)
    if p.is_dir():
        p = p.resolve()
        try:
            p.relative_to(config.RAW)
        except ValueError:
            raise SourceError(f"{path_arg} is outside vault/raw/.")
        files = [f for f in sorted(p.rglob("*")) if f.is_file() and f.suffix.lower() in config.ALLOWED_EXTENSIONS]
        if not private:
            files = [f for f in files if config.PRIVATE_RAW not in f.parents]
        if not files:
            raise SourceError(f"no .md/.txt/.pdf/.docx files found in {path_arg}.")
        return [validate_source_path(f) for f in files]
    return [validate_source_path(p)]


def run(path_arg, title=None, folder=None, private=False, index_only=False, origin=None):
    start = time.time()
    if index_only:
        n = len(retrieve.rebuild_index())
        print(f"search index rebuilt: {n} passages (no model used)")
        return
    files = targets(path_arg, private)
    if title and len(files) != 1:
        raise SourceError("--title applies to a single source file.")
    before = sorted(config.rel(p) for p in config.WIKI.rglob("*.md"))
    manifest = load_manifest()
    gemma = Gemma()
    print(f"mode=ingest · model={config.MODEL_LABEL} · execution=local · {len(files)} source(s)")
    log_lines = []

    def log(msg):
        print(msg)
        log_lines.append(msg)

    results = []
    for f in files:
        results.append(ingest_source(f, manifest, gemma, title, folder, private, origin, log))
        save_manifest(manifest)
    retrieve.rebuild_index()                         # concepts retrieve over fresh passages
    log("\n== concept notes")
    only = None if Path(path_arg).resolve() == config.RAW else {config.rel(f) for f in files}
    results += build_concepts(manifest, gemma, only, log)
    write_index(manifest)
    write_sources(manifest)
    n_passages = len(retrieve.rebuild_index())
    after = sorted(config.rel(p) for p in config.WIKI.rglob("*.md"))
    new_files = sorted(set(after) - set(before))
    counts = {s: sum(1 for r in results if r[0] == s) for s in ("created", "updated", "unchanged")}
    elapsed = round(time.time() - start, 1)
    summary = (f"\ningest done in {elapsed} s · {gemma.calls} Gemma calls ({round(gemma.seconds, 1)} s generating) · "
               f"notes: {counts} · new files: {len(new_files)} · wiki notes before/after: {len(before)}/{len(after)} · "
               f"index: {n_passages} passages · peak memory {evidence.max_rss_gb()} GB RSS")
    log(summary)
    for nf in new_files:
        log(f"   new file: {nf}")
    record = {"mode": "ingest", "path": path_arg, "time": datetime.now().isoformat(timespec="seconds"),
              "runtime": evidence.runtime_info(), "elapsed_seconds": elapsed, "gemma_calls": gemma.calls,
              "generation_seconds": round(gemma.seconds, 1), "counts": counts, "new_files": new_files,
              "notes_before": len(before), "notes_after": len(after), "max_rss_gb": evidence.max_rss_gb()}
    md = "# Ingest run\n\n```\n" + "\n".join(log_lines) + "\n```\n"
    path = evidence.save_run("ingest", {**record, "query": Path(path_arg).stem}, md,
                             private=any(retrieve.is_private(config.rel(f)) for f in files), folder="ingest")
    print("saved:", config.rel(path))

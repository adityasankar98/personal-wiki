"""The retrieval tool: BM25 keyword search over local passages.

Pure Python, no model and no network. The index is the list of passages in
data/chunks.jsonl (built by `wiki ingest`); BM25 statistics are recomputed on
load because the corpus is small (hundreds of passages, milliseconds).
"""

import json
import math
import re
from collections import Counter
from dataclasses import dataclass

from . import config
from .chunker import Passage, chunk
from .loaders import load

STOPWORDS = set("""
a about above after again against all am an and any are as at be because been before being
below between both but by can could did do does doing down during each few for from further
had has have having he her here hers herself him himself his how i if in into is it its itself
just me more most my myself no nor not now of off on once only or other our ours ourselves out
over own same she should so some such than that the their theirs them themselves then there
these they this those through to too under until up very was we were what when where which
while who whom why will with would you your yours yourself yourselves get got also use used
using one two three tell know
""".split())

TOKEN = re.compile(r"[a-z0-9]+")


def stem(word: str) -> str:
    """A deliberately tiny suffix stripper, applied identically to queries and passages."""
    for suffix, repl, min_len in (("ies", "y", 5), ("sses", "ss", 6), ("ing", "", 6), ("ed", "", 5)):
        if word.endswith(suffix) and len(word) >= min_len:
            return word[: -len(suffix)] + repl
    if word.endswith("s") and len(word) > 3 and not word.endswith(("ss", "us", "is")):
        return word[:-1]
    return word


def tokenize(text: str):
    return [stem(t) for t in TOKEN.findall(text.lower()) if t not in STOPWORDS]


@dataclass
class Hit:
    passage: Passage
    score: float
    coverage: float    # share of distinct query terms present in the passage
    rank: int = 0


def load_synonyms():
    path = config.ROOT / "retrieval-synonyms.json"
    if not path.exists():
        return 0.0, []
    data = json.loads(path.read_text())
    groups = [[tokenize(entry) for entry in group] for group in data["groups"]]
    return float(data.get("weight", 0.5)), [[e for e in g if e] for g in groups]


def expand(terms):
    """Query terms (weight 1) plus synonyms of any matched group (reduced weight)."""
    weight, groups = load_synonyms()
    weights = {t: 1.0 for t in terms}
    present = set(terms)
    for group in groups:
        if any(set(entry) <= present for entry in group):
            for entry in group:
                for t in entry:
                    weights.setdefault(t, weight)
    return weights


class Index:
    def __init__(self, passages):
        self.passages = passages
        # What BM25 sees: file name + heading trail + text, so "Pac-Man" in a
        # question can match a passage whose own text never repeats the title.
        stem_names = [p.source.rsplit("/", 1)[-1].rsplit(".", 1)[0] for p in passages]
        self.docs = [tokenize(f"{n} {p.section} {p.text}") for n, p in zip(stem_names, passages)]
        self.tf = [Counter(d) for d in self.docs]
        self.avgdl = sum(map(len, self.docs)) / max(len(self.docs), 1)
        df = Counter(t for d in self.tf for t in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def search(self, query: str, k: int = config.TOP_K, kinds=("raw",), include_private=True,
               per_source=config.MAX_PER_SOURCE, synonyms=True,
               min_relative=config.MIN_RELATIVE_SCORE):
        terms = list(dict.fromkeys(tokenize(query)))
        if not terms:
            return []
        weights = expand(terms) if synonyms else {t: 1.0 for t in terms}
        k1, b = 1.5, 0.75
        hits = []
        for p, tf, doc in zip(self.passages, self.tf, self.docs):
            if p.kind not in kinds:
                continue
            if not include_private and is_private(p.source):
                continue
            score = 0.0
            for t, w in weights.items():
                f = tf.get(t, 0)
                if f:
                    score += w * self.idf[t] * f * (k1 + 1) / (f + k1 * (1 - b + b * len(doc) / self.avgdl))
            if score > 0:
                cov = sum(1 for t in terms if t in tf) / len(terms)
                hits.append(Hit(p, score, cov))
        hits.sort(key=lambda h: h.score, reverse=True)
        # Relative cut: drop weak filler far below the best match.
        if hits and min_relative:
            hits = [h for h in hits if h.score >= min_relative * hits[0].score]
        # Per-source cap: one long source must not crowd every other source out.
        chosen, per = [], Counter()
        for h in hits:
            if per_source and per[h.passage.source] >= per_source:
                continue
            chosen.append(h)
            per[h.passage.source] += 1
            if len(chosen) == k:
                break
        for i, h in enumerate(chosen, start=1):
            h.rank = i
        return chosen


def is_private(source: str) -> bool:
    return "/raw/private/" in source or any(f"/wiki/{f}/" in source for f in config.PRIVATE_FOLDERS)


class IndexMissing(Exception):
    pass


def load_index() -> Index:
    if not config.CHUNKS_FILE.exists():
        raise IndexMissing("No search index yet. Run `./wiki ingest` first.")
    passages = [Passage(**json.loads(line)) for line in config.CHUNKS_FILE.read_text().splitlines() if line]
    if not passages:
        raise IndexMissing("The search index is empty. Add sources to vault/raw/ and run `./wiki ingest`.")
    return Index(passages)


def rebuild_index():
    """Chunk every raw source and every wiki note into data/chunks.jsonl."""
    passages = []
    for path in sorted(config.RAW.rglob("*")):
        if path.is_file() and path.suffix.lower() in config.ALLOWED_EXTENSIONS and not path.is_symlink():
            doc = load(path)
            passages += chunk(doc.text, config.rel(path), "raw")
    for path in sorted(config.WIKI.rglob("*.md")):
        passages += chunk(path.read_text(encoding="utf-8"), config.rel(path), "wiki")
    config.DATA.mkdir(exist_ok=True)
    config.CHUNKS_FILE.write_text("".join(json.dumps(p.to_dict()) + "\n" for p in passages))
    return passages

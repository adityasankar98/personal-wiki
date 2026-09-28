"""Citation checks on a generated answer.

Automatic checks only catch mechanical problems; a human still opens the cited
passage to confirm it supports the claim (see the evidence cards):
  - every [S#] refers to a passage that was actually shown to the model
  - every factual sentence carries at least one citation
  - every number in a cited sentence appears in one of the passages it cites
"""

import re

from . import config

CITE = re.compile(r"\[(S\d+(?:\s*[,;]\s*S\d+)*)\]")
NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")


def is_insufficient(answer: str) -> bool:
    return answer.strip().lower().lstrip("*# ").startswith(config.INSUFFICIENT.lower())


def cited_ids(text: str):
    ids = []
    for group in CITE.findall(text):
        ids += [int(x.strip()[1:]) for x in re.split(r"[,;]", group)]
    return ids


ABBREVIATIONS = re.compile(r"\b(Ms|Mr|Mrs|Dr|vs|e\.g|i\.e|etc|approx|No)\.\s", re.I)


def _sentences(text: str):
    # Don't split "Ms. Pac-Man": hide the abbreviation's period from the splitter.
    text = ABBREVIATIONS.sub(lambda m: m.group(0).replace(".", "\u2024"), text)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z*\-])|\n+", text)
    return [p.strip() for p in parts if len(p.strip()) > 3]


def _norm_num(n: str) -> str:
    n = n.replace(",", "")
    return n[:-2] if n.endswith(".0") else n


def check(answer: str, hits):
    shown = len(hits)
    report = {"insufficient": is_insufficient(answer), "cited": [], "invalid": [],
              "uncited_sentences": [], "unsupported_numbers": []}
    if report["insufficient"]:
        report["status"] = "PASS (insufficient-evidence reply; no citations needed)"
        return report
    ids = cited_ids(answer)
    report["cited"] = sorted(set(i for i in ids if 1 <= i <= shown))
    report["invalid"] = sorted(set(i for i in ids if not 1 <= i <= shown))
    passages_nums = [{_norm_num(n) for n in NUMBER.findall(h.passage.text)} for h in hits]
    for sentence in _sentences(answer):
        sids = [i for i in cited_ids(sentence) if 1 <= i <= shown]
        if not sids:
            if not sentence.endswith(":"):
                report["uncited_sentences"].append(sentence)
            continue
        allowed = set().union(*(passages_nums[i - 1] for i in sids))
        body = CITE.sub("", sentence)
        for n in NUMBER.findall(body):
            if _norm_num(n) not in allowed:
                report["unsupported_numbers"].append(f"{n} (in: {sentence[:80]})")
    problems = []
    if not report["cited"]:
        problems.append("no valid citations")
    if report["invalid"]:
        problems.append(f"cites passages that were not shown: {report['invalid']}")
    if report["uncited_sentences"]:
        problems.append(f"{len(report['uncited_sentences'])} sentence(s) without a citation")
    if report["unsupported_numbers"]:
        problems.append("numbers not found in the cited passages")
    report["status"] = "PASS" if not problems else "WARN: " + "; ".join(problems)
    return report


def _plain(text: str) -> str:
    text = CITE.sub("", text)
    text = re.sub(r"[*`_|>\"“”]", " ", text)
    return re.sub(r"\s+", " ", text).lower().strip(" .")


def verify_quote(quote: str, hits):
    """True if the quote (minus citation tags and Markdown) occurs verbatim in a cited passage."""
    ids = [i for i in cited_ids(quote) if 1 <= i <= len(hits)]
    body = _plain(quote)
    if len(body.split()) < 4 or not ids:
        return False
    return any(body in _plain(hits[i - 1].passage.text) for i in ids)

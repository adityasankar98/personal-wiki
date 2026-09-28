"""`wiki eval`: the four fixed ask-mode tests, retrieval checked separately from the answer.

For each test: (1) did the expected passage appear in the retrieved set?
(2) the actual ask-mode answer, (3) automatic citation checks, (4) automatic
answer checks against tests/questions.json, and (5) the human assessment from
tests/assessments.json -- shown only if it was written for this exact answer
text, so a changed answer can never inherit an old verdict.
"""

import hashlib
import json
from datetime import datetime

from . import ask, config, evidence, retrieve


def _load(name):
    path = config.TESTS / name
    return json.loads(path.read_text()) if path.exists() else {}


def answer_hash(text: str) -> str:
    return hashlib.sha256(text.strip().encode()).hexdigest()[:12]


def _retrieval_check(test, hits):
    found = []
    for exp in test["expected_sources"]:
        rank = next((h.rank for h in hits if h.passage.source == exp["file"] and exp["must_contain"] in h.passage.text), None)
        found.append({"file": exp["file"], "must_contain": exp["must_contain"], "rank": rank})
    ok = all(f["rank"] for f in found)
    return ok, found


def _answer_check(test, record):
    ans = record["answer"]
    insufficient = record["citation_check"]["insufficient"]
    if test["expect_insufficient"]:
        return insufficient, "expected an insufficient-evidence reply: " + ("got one" if insufficient else "did NOT get one")
    missing = [k for k in test["expected_answer_keywords"] if k.lower() not in ans.lower()]
    ok = not insufficient and not missing and record["citation_check"]["status"] == "PASS"
    detail = []
    if insufficient:
        detail.append("model refused although the evidence was retrieved")
    if missing:
        detail.append(f"missing expected facts: {missing}")
    if record["citation_check"]["status"] != "PASS":
        detail.append("citation check: " + record["citation_check"]["status"])
    return ok, "; ".join(detail) or "expected facts present, citations valid"


def run(retrieval_only: bool = False, label: str = ""):
    tests = _load("questions.json")["tests"]
    assessments = _load("assessments.json")
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    folder = config.EVIDENCE / "ask" / (f"{stamp}-{label}" if label else stamp)
    folder.mkdir(parents=True, exist_ok=True)
    index = retrieve.load_index()
    summary = [f"# Ask-mode eval run {stamp}{' (' + label + ')' if label else ''}", "",
               "| Test | Kind | Retrieval: expected passage found? | Answer check | Human assessment |",
               "|---|---|---|---|---|"]
    for test in tests:
        print(f"\n===== {test['id']} ({test['kind']}) =====")
        if retrieval_only:
            hits = index.search(test["question"])
            r_ok, found = _retrieval_check(test, hits)
            print("retrieval:", "PASS" if r_ok else "FAIL", found)
            summary.append(f"| {test['id']} | {test['kind']} | {_fmt(r_ok, found, test)} | not run | - |")
            continue
        record, hits = ask.answer(test["question"])
        r_ok, found = _retrieval_check(test, hits)
        a_ok, a_detail = _answer_check(test, record)
        h = answer_hash(record["answer"])
        human = assessments.get(test["id"], {})
        human_text = human.get("assessment") if human.get("answer_hash") == h else None
        record.update(test=test, retrieval_check={"pass": r_ok, "expected": found},
                      answer_check={"pass": a_ok, "detail": a_detail}, answer_hash=h,
                      human_assessment=human_text, label=label)
        extra = "\n".join([
            "", "## Expected (from tests/questions.json, written before the run)", "",
            *[f"- `{f['file']}` containing “{f['must_contain']}” → "
              + (f"**found at rank {f['rank']}**" if f["rank"] else "**NOT retrieved**") for f in found],
            *(["- Expected behaviour: an explicit insufficient-evidence statement"] if test["expect_insufficient"] else
              [f"- Expected facts in answer: {', '.join(test['expected_answer_keywords'])}"]),
            "", "## Automatic assessment", "",
            f"- Retrieval: **{'PASS' if r_ok else 'FAIL'}**",
            f"- Answer: **{'PASS' if a_ok else 'FAIL'}** — {a_detail}",
            "", "## Human assessment (I opened each cited passage)", "",
            human_text or f"_Not yet reviewed for this exact answer (answer hash `{h}`)._", "",
        ])
        title = f"{test['id']}: {test['question']}"
        (folder / f"{test['id']}.md").write_text(ask.card_markdown(record, hits, title, extra))
        (folder / f"{test['id']}.json").write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
        summary.append(f"| [{test['id']}]({test['id']}.md) | {test['kind']} | {_fmt(r_ok, found, test)} | "
                       f"{'PASS' if a_ok else 'FAIL'}: {a_detail} | {'reviewed' if human_text else 'pending'} |")
        print(f"\nretrieval {'PASS' if r_ok else 'FAIL'} · answer {'PASS' if a_ok else 'FAIL'} ({a_detail})")
    rt = evidence.runtime_info(model_loaded=not retrieval_only)
    summary += ["", f"Model: `{rt['model']}` @ `{(rt['model_revision'] or '')[:12]}` · {rt['runtime']} · "
                f"{rt['os']} · {rt['chip']} · {rt['unified_memory_gb']} GB · execution: local", ""]
    (folder / "README.md").write_text("\n".join(summary))
    print(f"\nsaved: {config.rel(folder)}/")
    return folder


def _fmt(ok, found, test):
    if not test["expected_sources"]:
        return "n/a (no source should contain the answer)"
    return ("PASS" if ok else "FAIL") + " — ranks " + ", ".join(str(f["rank"] or "missing") for f in found)

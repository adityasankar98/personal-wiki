"""ask mode: the RAG workflow. Stateless: no chat history, no persona.

question -> retrieve passages from the original sources -> gate on evidence
strength -> assemble prompt (research rules + passages + question) -> local
Gemma -> citation check -> display -> optionally save an evidence card.
"""

import sys
from datetime import datetime

from . import citations, config, evidence, llm, prompts, retrieve


def answer(question: str, echo: bool = True):
    """Returns a record dict with everything needed for an evidence card."""
    out = print if echo else (lambda *a, **k: None)
    index = retrieve.load_index()
    hits = index.search(question, k=config.TOP_K, kinds=("raw",))
    out(f"mode=ask · model={config.MODEL_LABEL} · execution=local · history=none · persona=none")
    out(f"[1/4] retrieved {len(hits)} passage(s) from vault/raw/ (BM25)")
    for h in hits:
        out(f"      S{h.rank}  {h.passage.location()}  (score {h.score:.1f})")

    record = {"mode": "ask", "execution": "local", "question": question,
              "time": datetime.now().isoformat(timespec="seconds"),
              "passages": evidence.hits_json(hits)}

    best = hits[0] if hits else None
    if best is None or best.score < config.ASK_MIN_SCORE or best.coverage < config.ASK_MIN_TERM_COVERAGE:
        text = (f"{config.INSUFFICIENT}: no passage in the wiki's sources matches this question "
                "closely enough to answer it.")
        out("[2/4] evidence gate: too weak -> not calling the model")
        record.update(answer=text, gate="blocked (weak retrieval)", model_called=False,
                      citation_check=citations.check(text, hits), stats=None,
                      runtime=evidence.runtime_info(model_loaded=False))
        out("\n" + text)
        return record, hits

    out("[2/4] evidence gate: passed -> building prompt (wiki-instructions.md + passages + question)")
    messages = prompts.ask_messages(question, hits)
    try:
        out("[3/4] generating with local Gemma ...\n")
        text, stats = llm.generate(messages, config.ASK_SETTINGS,
                                   on_text=(lambda t: (sys.stdout.write(t), sys.stdout.flush())) if echo else None)
    except KeyboardInterrupt:
        out("\n[interrupted] generation stopped; nothing saved.")
        raise
    check = citations.check(text, hits)
    rescue_log = None
    if check["insufficient"] and best.score >= config.RESCUE_MIN_SCORE and best.coverage >= config.RESCUE_MIN_COVERAGE:
        out("\n\n[3b] refused despite a strong match -> quote-first double-check ...")
        rescued, rescue_log = rescue(question, hits)
        out(f"     {rescue_log['verdict']}")
        if rescued:
            text = rescued
            out("\n" + text)
            check = citations.check(text, hits)
        second = rescue_log.pop("stats")
        stats = {**second, "seconds": round(stats["seconds"] + second["seconds"], 2),
                 "note": "two model calls (first pass + double-check); seconds is the total"}
    out(f"\n\n[4/4] citation check: {check['status']}")
    if not check["insufficient"]:
        for i in check["cited"]:
            out(f"      [S{i}] -> {hits[i - 1].passage.location()}")
    out(f"      ({stats['seconds']} s, {stats['prompt_tokens']} prompt tokens, "
        f"{stats['generated_tokens']} generated, peak {stats['peak_memory_gb']} GB)")
    record.update(answer=text, gate="passed", model_called=True, citation_check=check,
                  stats=stats, rescue=rescue_log, runtime=evidence.runtime_info())
    return record, hits


def rescue(question: str, hits):
    """Small models sometimes refuse although a passage answers the question in other words.

    Ask again, requiring a verbatim quote before the answer. The harness accepts
    the new answer only if a quote is found word for word in the passage it cites
    and the answer is not itself a refusal; otherwise the refusal stands.
    """
    raw, stats = llm.generate(prompts.ask_quote_first_messages(question, hits), config.ASK_SETTINGS)
    evidence_lines = [l.split(":", 1)[1].strip() for l in raw.splitlines() if l.lower().startswith("evidence:")]
    answer_lines = [l.split(":", 1)[1].strip() for l in raw.splitlines() if l.lower().startswith("answer:")]
    verified = [q for q in evidence_lines if citations.verify_quote(q, hits)]
    answer = answer_lines[0] if answer_lines else ""
    log = {"raw_output": raw, "verified_quotes": verified, "stats": stats}
    if not verified:
        log["verdict"] = "rejected: no quote could be found verbatim in its cited passage; refusal stands"
        return None, log
    if not answer or citations.is_insufficient(answer) or not citations.cited_ids(answer):
        log["verdict"] = "rejected: no cited answer line; refusal stands"
        return None, log
    log["verdict"] = f"accepted: {len(verified)} quote(s) verified verbatim in the cited passage"
    return answer, log


def card_markdown(record: dict, hits, title: str = None, extra: str = "") -> str:
    chk = record["citation_check"]
    rt = record["runtime"]
    stats = record.get("stats") or {}
    lines = [
        f"# {title or 'Ask: ' + record['question']}", "",
        "| | |", "|---|---|",
        f"| Mode | **ask** (standalone: no chat history, no persona) |",
        f"| Execution | **{rt['execution']}** — offline-capable local model |",
        f"| Model | `{rt.get('model') or 'not called'}` @ `{(rt.get('model_revision') or '')[:12]}` ({rt.get('quantization') or '-'}) |",
        f"| Runtime | {rt['runtime']}, Python {rt['python']}, {rt['os']}, {rt['chip']}, {rt['unified_memory_gb']} GB |",
        f"| Time | {record['time']} |",
        f"| Evidence gate | {record['gate']} |",
    ]
    if stats:
        lines.append(f"| Latency / memory | {stats['seconds']} s generation, {stats['prompt_tokens']} prompt tokens, "
                     f"{stats['generated_tokens']} generated tokens, peak MLX memory {stats['peak_memory_gb']} GB |")
    lines += ["", f"**Question:** {record['question']}", "", "## Retrieved passages", "",
              evidence.passages_md(hits), "## Gemma's answer (verbatim)", "",
              "\n".join("> " + l for l in record["answer"].splitlines()), "",
              *(_rescue_md(record["rescue"]) if record.get("rescue") else []),
              "## Citation check (automatic)", "", f"- Status: **{chk['status']}**"]
    if not chk["insufficient"]:
        lines.append("- Cited: " + (", ".join(f"S{i} → `{hits[i-1].passage.location()}`" for i in chk["cited"]) or "none"))
        if chk["invalid"]:
            lines.append(f"- Invalid citation ids: {chk['invalid']}")
        for s in chk["uncited_sentences"]:
            lines.append(f"- Uncited sentence: “{s}”")
        for n in chk["unsupported_numbers"]:
            lines.append(f"- Number not in cited passage: {n}")
    return "\n".join(lines) + "\n" + extra


def _rescue_md(log):
    return ["## Refusal double-check (quote-first second pass)", "",
            "The first pass replied *Insufficient evidence* although retrieval was strong, so the harness asked "
            "again, requiring a verbatim quote. Raw second-pass output:", "",
            "\n".join("> " + l for l in log["raw_output"].splitlines()), "",
            f"- Quotes verified verbatim in the cited passage: {len(log['verified_quotes'])}",
            f"- Verdict: **{log['verdict']}**", ""]


def run(question: str, save: bool, mode: str = "local"):
    record, hits = answer(question)
    if save:
        private = any(retrieve.is_private(h.passage.source) for h in hits)
        path = evidence.save_run("ask", record, card_markdown(record, hits), private)
        print("saved:", config.rel(path))
    return record

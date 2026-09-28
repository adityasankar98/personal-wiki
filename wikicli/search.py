"""search mode: the retrieval tool's raw output. Never imports or calls the model."""

from datetime import datetime

from . import config, evidence, retrieve


def run(query: str, k: int, include_wiki: bool, save: bool):
    index = retrieve.load_index()
    kinds = ("raw", "wiki") if include_wiki else ("raw",)
    hits = index.search(query, k=k, kinds=kinds, per_source=0 if include_wiki else config.MAX_PER_SOURCE)
    print(f"mode=search · retrieval=BM25 (local) · model=not used · scope={'+'.join(kinds)}")
    print(f'query: "{query}"  ->  {len(hits)} passage(s)\n')
    if not hits:
        print("No matching passages. Try other words, or `./wiki search` with --include-wiki.")
    for h in hits:
        p = h.passage
        print(f"[{h.rank}] {p.source}  lines {p.line_start}-{p.line_end}")
        print(f"    § {p.section}   (BM25 {h.score:.2f}, term coverage {h.coverage:.2f})")
        for line in p.text.splitlines():
            print("    | " + line)
        print()
    if save:
        record = {"mode": "search", "query": query, "time": datetime.now().isoformat(timespec="seconds"),
                  "runtime": evidence.runtime_info(model_loaded=False), "scope": list(kinds),
                  "passages": evidence.hits_json(hits)}
        md = (f"# Search: {query}\n\nMode: **search** (no model, no generated answer) · "
              f"retrieval: BM25 · scope: {', '.join(kinds)} · {record['time']}\n\n"
              + evidence.passages_md(hits))
        private = any(retrieve.is_private(h.passage.source) for h in hits)
        print("saved:", config.rel(evidence.save_run("search", record, md, private)))
    return hits

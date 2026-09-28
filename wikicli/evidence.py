"""Saved outputs. Every saved run is a new timestamped file; nothing is overwritten.

Runs that touched private sources go to evidence/private/ (gitignored).
Paths inside records are repo-relative so no local username leaks.
"""

import json
import platform
import re
import resource
import subprocess
from datetime import datetime
from importlib.metadata import PackageNotFoundError, version

from . import config


def runtime_info(model_loaded: bool = True) -> dict:
    def ver(pkg):
        try:
            return version(pkg)
        except PackageNotFoundError:
            return None

    def sysctl(key):
        try:
            return subprocess.run(["sysctl", "-n", key], capture_output=True, text=True).stdout.strip()
        except OSError:
            return None

    mem = sysctl("hw.memsize")
    return {
        "execution": "local",
        "model": config.MODEL_ID if model_loaded else None,
        "model_revision": config.MODEL_REVISION if model_loaded else None,
        "quantization": "4-bit (MLX)" if model_loaded else None,
        "runtime": f"mlx-vlm {ver('mlx-vlm')}, mlx {ver('mlx')}",
        "python": platform.python_version(),
        "os": f"macOS {platform.mac_ver()[0]}",
        "chip": sysctl("machdep.cpu.brand_string"),
        "unified_memory_gb": round(int(mem) / 2**30) if mem and mem.isdigit() else None,
    }


def max_rss_gb() -> float:
    # macOS reports ru_maxrss in bytes.
    return round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1e9, 2)


def slug(text: str, n: int = 40) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")[:n] or "run"


def save_run(mode: str, record: dict, markdown: str, private: bool = False, folder: str = "runs"):
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    base = config.EVIDENCE / ("private" if private else folder)
    base.mkdir(parents=True, exist_ok=True)
    name = f"{stamp}-{mode}-{slug(record.get('question') or record.get('query') or mode)}"
    path = base / f"{name}.json"
    i = 1
    while path.exists():
        path = base / f"{name}-{i}.json"
        i += 1
    path.write_text(json.dumps(record, indent=2, ensure_ascii=False) + "\n")
    path.with_suffix(".md").write_text(markdown)
    return path.with_suffix(".md")


def passages_md(hits) -> str:
    rows = []
    for h in hits:
        p = h.passage
        rows.append(
            f"**[S{h.rank}] `{p.source}` lines {p.line_start}–{p.line_end} § {p.section}** "
            f"(BM25 {h.score:.2f}, term coverage {h.coverage:.2f})\n\n"
            + "\n".join("> " + line for line in p.text.splitlines()) + "\n"
        )
    return "\n".join(rows) if rows else "_No passages retrieved._\n"


def hits_json(hits):
    return [{"id": f"S{h.rank}", "source": h.passage.source, "section": h.passage.section,
             "lines": [h.passage.line_start, h.passage.line_end], "score": round(h.score, 3),
             "coverage": round(h.coverage, 2), "text": h.passage.text} for h in hits]

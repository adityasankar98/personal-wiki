"""The model: local Gemma through mlx-vlm. Loaded once, lazily, from the local cache only.

Gemma only ever sees what the harness passes in `messages`; it does not read
files, remember sessions, or call tools.
"""

import time
import warnings

from . import config


class ModelUnavailable(Exception):
    pass


DOWNLOAD_HINT = (
    "The local model is not in the Hugging Face cache. While online, download it once with:\n"
    "  .venv/bin/python -c \"from huggingface_hub import snapshot_download; "
    f"snapshot_download('{config.MODEL_ID}', revision='{config.MODEL_REVISION}')\"\n"
    "Then run offline as normal."
)

_model = None
REQUIRED_FILES = ("config.json", "model.safetensors", "tokenizer.json", "chat_template.jinja")


def snapshot_path():
    """The pinned snapshot folder in the local HF cache, or None if incomplete.

    Resolved directly rather than via snapshot_download(), which rejects caches
    that lack optional files such as README.md even though the weights are present.
    """
    from huggingface_hub.constants import HF_HUB_CACHE
    from pathlib import Path

    folder = Path(HF_HUB_CACHE) / ("models--" + config.MODEL_ID.replace("/", "--")) / "snapshots" / config.MODEL_REVISION
    if all((folder / name).exists() for name in REQUIRED_FILES):
        return str(folder)
    return None


def _load():
    global _model
    if _model is not None:
        return _model
    warnings.filterwarnings("ignore", message=".*mel filter.*")
    path = snapshot_path()
    if path is None:
        raise ModelUnavailable(DOWNLOAD_HINT)
    try:
        from mlx_vlm import load
    except ImportError:
        raise ModelUnavailable("mlx-vlm is not installed. Run: .venv/bin/pip install -r requirements.txt")
    start = time.time()
    model, processor = load(path)
    _model = (model, processor, time.time() - start)
    return _model


def load_seconds() -> float:
    return _load()[2]


def count_tokens(text: str) -> int:
    _, processor, _ = _load()
    return len(processor.tokenizer.encode(text))


def generate(messages, settings, on_text=None):
    """Run one chat-formatted generation. Returns (text, stats)."""
    from mlx_vlm import stream_generate
    import mlx.core as mx

    model, processor, _ = _load()
    prompt = processor.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    start = time.time()
    text, last = "", None
    for chunk in stream_generate(model, processor, prompt, **settings):
        text += chunk.text
        last = chunk
        if on_text:
            on_text(chunk.text)
    stats = {
        "seconds": round(time.time() - start, 2),
        "prompt_tokens": getattr(last, "prompt_tokens", None),
        "generated_tokens": getattr(last, "generation_tokens", None),
        "tokens_per_second": round(getattr(last, "generation_tps", 0.0), 1),
        "peak_memory_gb": round(mx.get_peak_memory() / 1e9, 2),
    }
    return text.strip(), stats

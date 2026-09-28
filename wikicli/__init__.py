"""Personal wiki CLI: a local-Gemma RAG harness over an Obsidian vault.

Offline is enforced here, before any Hugging Face library can be imported: the
model is loaded only from the local cache and no telemetry is sent.
"""

import os

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

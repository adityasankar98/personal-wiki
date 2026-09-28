"""Every path, model setting and budget in one place."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"
RAW = VAULT / "raw"
PRIVATE_RAW = RAW / "private"
WIKI = VAULT / "wiki"
INDEX_MD = VAULT / "index.md"
SOURCES_MD = VAULT / "sources.md"
PRIVATE_INDEX_MD = VAULT / "private-index.md"

INSTRUCTIONS = ROOT / "instructions"
DATA = ROOT / "data"                       # machine files: kept outside the vault, gitignored
CHUNKS_FILE = DATA / "chunks.jsonl"
MANIFEST_FILE = DATA / "manifest.json"
CONCEPTS_FILE = ROOT / "wiki-concepts.json"   # human-curated concept list (reviewed)
CORRECTIONS_FILE = ROOT / "review" / "corrections.json"
EVIDENCE = ROOT / "evidence"
TESTS = ROOT / "tests"

# --- Model (local, default) -------------------------------------------------
MODEL_ID = "mlx-community/gemma-4-e2b-it-4bit"
MODEL_REVISION = "238767527555cb75a05732a84dff5d6ba0dd6809"   # pinned HF snapshot
MODEL_LABEL = "Gemma 4 E2B-it, 4-bit MLX (local)"

# Greedy decoding for ask and ingest: reproducible, no creative drift.
ASK_SETTINGS = {"max_tokens": 400, "temperature": 0.0}
INGEST_SETTINGS = {"max_tokens": 350, "temperature": 0.0}
CHAT_SETTINGS = {"max_tokens": 600, "temperature": 0.7, "top_p": 0.95}

# --- Passages and retrieval -------------------------------------------------
CHUNK_TARGET_WORDS = 180      # passages are paragraph-aligned, ~180 words
CHUNK_MAX_WORDS = 260         # a single paragraph longer than this is split
TOP_K = 5                     # passages handed to Gemma in ask mode
MAX_PER_SOURCE = 3            # at most 3 of the top 5 from any one source
MIN_RELATIVE_SCORE = 0.3      # drop passages scoring < 30% of the best hit
ASK_MIN_SCORE = 3.0           # below this BM25 score: insufficient evidence, model not called
ASK_MIN_TERM_COVERAGE = 0.34  # ...or when the best passage matches too few question terms
RESCUE_MIN_SCORE = 12.0       # a refusal despite a match this strong gets a verified second look
RESCUE_MIN_COVERAGE = 0.5
CHAT_MIN_SCORE = 6.0          # chat retrieves automatically only on a strong match
CHAT_HISTORY_TOKENS = 3000    # rolling chat history budget
INGEST_SECTION_WORDS = 1400   # max words of source text per Gemma call during ingest (~2k tokens)

# --- Safety limits ----------------------------------------------------------
ALLOWED_EXTENSIONS = {".md", ".txt", ".pdf", ".docx"}
MAX_SOURCE_BYTES = 5 * 1024 * 1024
WIKI_FOLDERS = {"Projects", "Concepts", "Tools", "Career", "People"}
PRIVATE_FOLDERS = {"Career"}   # notes here are never committed (see .gitignore)

INSUFFICIENT = "Insufficient evidence"


def rel(path: Path) -> str:
    """Repo-relative path for display and evidence, so no home-directory path leaks."""
    try:
        return str(Path(path).resolve().relative_to(ROOT))
    except ValueError:
        return Path(path).name

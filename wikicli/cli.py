"""The CLI: parses the command, picks the mode, and routes to the harness.

Each mode module is imported only when used, so `wiki search` and `wiki --help`
never import the model runtime.
"""

import argparse
import sys

from . import config

DESCRIPTION = f"""\
Personal wiki CLI — talk to your own notes with a local Gemma model, offline.

Model (default, local): {config.MODEL_ID} @ {config.MODEL_REVISION[:12]}  (4-bit MLX, via mlx-vlm)
Vault (open in Obsidian): vault/   originals: vault/raw/   generated notes: vault/wiki/
"""

EPILOG = """\
commands:
  ingest [PATH]        read sources in vault/raw/, write/update linked wiki notes, rebuild the index
  search "QUERY"       show original matching passages + paths. No answer, no model.
  ask "QUESTION"       standalone factual answer with citations, or "Insufficient evidence"
  chat                 Scout, a personal assistant with conversation memory; looks up notes when needed
  eval                 run the four fixed ask-mode tests (tests/questions.json) and write evidence cards
  check                verify links, note names, source hashes, and scan for secrets / private files
  help                 this message

examples:
  ./wiki ingest vault/raw
  ./wiki ingest "vault/raw/Pac-Man DQN README.md"
  ./wiki ingest vault/raw/private/resume.pdf --title "Resume" --folder Career --private
  ./wiki search "reward clipping"
  ./wiki ask "Why did the Pac-Man loss go up?" --mode local --save
  ./wiki chat --transcript evidence/chat-demo.md

configuration:
  wikicli/config.py            paths, model id + revision, generation settings, retrieval budgets
  instructions/persona.md      chat personality + capabilities      (chat only)
  instructions/wiki-instructions.md   research rules                 (ask only)
  instructions/ingest-instructions.md note-writing rules             (ingest only)
  wiki-concepts.json           curated concept notes and their keywords
  retrieval-synonyms.json      query expansion groups for BM25

required inputs: source files (.md .txt .pdf .docx) inside vault/raw/; the model in the local
Hugging Face cache (see README "Setup"). Everything runs offline; --mode online is not implemented.
"""


def build_parser():
    p = argparse.ArgumentParser(prog="wiki", description=DESCRIPTION, epilog=EPILOG,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="command", metavar="COMMAND")

    s = sub.add_parser("ingest", help="ingest sources into wiki notes")
    s.add_argument("path", nargs="?", default=str(config.RAW), help="a file or folder inside vault/raw/ (default: all)")
    s.add_argument("--title", help="note name for a NEW source (2-6 words); remembered for re-ingests")
    s.add_argument("--folder", default=None, help=f"topic folder for a new source: {', '.join(sorted(config.WIKI_FOLDERS))}")
    s.add_argument("--private", action="store_true", help="keep this source's note out of git and the public index")
    s.add_argument("--origin", help="where the original came from (e.g. a repository URL); stored in the catalog")
    s.add_argument("--index-only", action="store_true", help="only rebuild the search index (no model)")

    s = sub.add_parser("search", help="show matching original passages (no model)")
    s.add_argument("query")
    s.add_argument("-k", type=int, default=config.TOP_K, help="number of passages (default 5)")
    s.add_argument("--include-wiki", action="store_true", help="also search generated wiki notes")
    s.add_argument("--save", action="store_true", help="save the result under evidence/runs/")

    s = sub.add_parser("ask", help="cited factual answer from your sources")
    s.add_argument("question")
    s.add_argument("--mode", choices=["local", "online"], default="local", help="where the model runs (default local)")
    s.add_argument("--save", action="store_true", help="save an evidence card under evidence/runs/")

    s = sub.add_parser("chat", help="personal assistant with conversation context")
    s.add_argument("--mode", choices=["local", "online"], default="local")
    s.add_argument("--transcript", help="also write the session to this Markdown file")

    s = sub.add_parser("eval", help="run the four ask-mode tests")
    s.add_argument("--retrieval-only", action="store_true", help="check retrieval without calling the model")
    s.add_argument("--label", default="", help="short label for this run, e.g. offline")

    sub.add_parser("check", help="links, names, hashes, secrets")
    sub.add_parser("help", help="show this help")
    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command in (None, "help"):
        parser.print_help()
        return 0
    if getattr(args, "mode", "local") == "online":
        print("error: online mode is not implemented. This project runs Gemma locally; "
              "omit --mode or use --mode local.", file=sys.stderr)
        return 2

    from .llm import ModelUnavailable
    from .loaders import SourceError
    from .retrieve import IndexMissing
    try:
        if args.command == "search":
            from . import search
            search.run(args.query, args.k, args.include_wiki, args.save)
        elif args.command == "ask":
            from . import ask
            ask.run(args.question, args.save)
        elif args.command == "chat":
            from . import chat
            chat.run(args.transcript)
        elif args.command == "ingest":
            from . import ingest
            ingest.run(args.path, args.title, args.folder, args.private, args.index_only, args.origin)
        elif args.command == "eval":
            from . import evals
            evals.run(args.retrieval_only, args.label)
        elif args.command == "check":
            from . import check
            return check.run()
    except (IndexMissing, SourceError, ModelUnavailable) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\ninterrupted.", file=sys.stderr)
        return 130
    return 0

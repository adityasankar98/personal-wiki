"""chat mode: Scout, the personal assistant.

Differs from ask by design:
  - loads instructions/persona.md (voice + real capabilities), not the research rules
  - keeps a rolling conversation history (token-budgeted; oldest turns dropped first)
  - retrieves wiki passages only when a turn needs them (decide_retrieval), and
    only for that turn: passages are never stored in history
  - /save writes a draft to evidence/chat-saves/, never into vault/raw/ or the index
"""

import re
import sys
from datetime import datetime

from . import config, evidence, llm, prompts, retrieve

HELP = """commands:
  /notes <question>  look this up in the wiki for this turn
  /sources           show the passages behind the last reply
  /save [name]       save the last reply as a draft (evidence/chat-saves/, not evidence)
  /clear             forget the conversation
  /help              this list
  /exit              quit"""

# Turns that are about the conversation itself never need the notes.
META = re.compile(r"\b(what can (you|we|i)|help me with|who are you|what are you|how do you work|"
                  r"your (capabilities|commands)|^(hi|hello|hey|thanks|thank you)\b)", re.I)
FOLLOW_UP = re.compile(r"\b(make (that|it|this)|shorter|longer|shorten|rewrite|rephrase|reword|simplify|"
                       r"bullet|more (formal|casual|concise|detail)|less |turn (that|it) into|translate|"
                       r"summari[sz]e (that|it|this)|again|previous|above)\b", re.I)
ASKS_FOR_FACTS = re.compile(r"\?\s*$|^(what|which|when|where|who|why|how|did|do|does|is|are|was|were|can|could|"
                            r"tell|remind|summari[sz]e|explain|describe|list|compare|find|look up)\b", re.I)
DRAFT = re.compile(r"\b(draft|write|outline|plan|brainstorm|compose|come up with)\b", re.I)
DRAFT_HINT = ("\n\n(Harness note: write the draft now. Make reasonable assumptions, state them in one short "
              "line, and do not ask questions before drafting.)")
PERSONAL = re.compile(r"\b(my|mine|i|i'm|i've|did i|have i|our|project|assignment|class|course|notes?|wiki)\b", re.I)


def decide_retrieval(text: str, index, has_history: bool):
    """Return (hits, reason). Rules are deliberately simple so each decision is explainable."""
    if text.startswith("/notes"):
        query = text[len("/notes"):].strip()
        if not query:
            return [], "no: /notes needs a question"
        return index.search(query), "yes: /notes requested a lookup"
    if META.search(text):
        return [], "no: question about the assistant itself"
    if has_history and FOLLOW_UP.search(text):
        return [], "no: follow-up on the conversation"
    if not ASKS_FOR_FACTS.search(text):
        return [], "no: a statement or request for ideas, not a question about facts"
    if not PERSONAL.search(text):
        return [], "no: general request, nothing about Aditya's own work"
    hits = index.search(text)
    if hits and hits[0].score >= config.CHAT_MIN_SCORE and hits[0].coverage >= config.ASK_MIN_TERM_COVERAGE:
        return hits, f"yes: asks about his work and the notes match strongly (BM25 {hits[0].score:.1f})"
    return [], "no: about his work, but no strong match in the notes"


def trim_history(history):
    """Drop the oldest exchanges until the history fits the token budget."""
    while len(history) > 2 and sum(llm.count_tokens(m["content"]) for m in history) > config.CHAT_HISTORY_TOKENS:
        del history[:2]
    return history


def run(transcript_path=None, lines=None):
    interactive = sys.stdin.isatty() and lines is None
    index = retrieve.load_index()
    print(f"mode=chat · assistant=Scout (instructions/persona.md) · model={config.MODEL_LABEL} · execution=local")
    print("loading model ...", flush=True)
    llm.load_seconds()
    print("Scout is ready. Type /help for commands, /exit to quit.\n")
    history, last_hits, last_reply = [], [], ""
    log = [f"# Chat transcript — {datetime.now().isoformat(timespec='seconds')}", "",
           f"Mode: **chat** · assistant: Scout · model: `{config.MODEL_ID}` · execution: local", ""]
    source = iter(lines) if lines is not None else None
    while True:
        try:
            text = next(source) if source else input("you> " if interactive else "")
        except (EOFError, StopIteration):
            break
        except KeyboardInterrupt:
            print()
            break
        text = text.strip()
        if not text:
            continue
        if not interactive:
            print(f"you> {text}")
        log += [f"**you>** {text}", ""]
        if text == "/exit":
            break
        if text == "/help":
            print(HELP + "\n")
            continue
        if text == "/clear":
            history, last_hits = [], []
            print("(conversation cleared)\n")
            log += ["_(conversation cleared)_", ""]
            continue
        if text == "/sources":
            shown = "\n".join(f"  S{h.rank} {h.passage.location()}" for h in last_hits) or "  (the last reply used no notes)"
            print(shown + "\n")
            log += ["```", shown, "```", ""]
            continue
        if text.startswith("/save"):
            if not last_reply:
                print("(nothing to save yet)\n")
                continue
            name = text[len("/save"):].strip() or "draft"
            folder = config.EVIDENCE / "chat-saves"
            folder.mkdir(parents=True, exist_ok=True)
            path = folder / f"{datetime.now():%Y%m%d-%H%M%S}-{evidence.slug(name)}.md"
            path.write_text(f"# Saved chat draft: {name}\n\n_Generated by Scout in chat mode. A draft, not source evidence; "
                            f"never indexed._\n\n{last_reply}\n")
            print(f"(saved draft to {config.rel(path)})\n")
            log += [f"_(saved draft to {config.rel(path)})_", ""]
            continue

        hits, reason = decide_retrieval(text, index, bool(history))
        print(f"[retrieval: {reason}]")
        for h in hits:
            print(f"   S{h.rank} {h.passage.location()}")
        log += [f"`[retrieval: {reason}]`", ""] + [f"- S{h.rank} `{h.passage.location()}`" for h in hits] + ([""] if hits else [])
        user_text = text[len("/notes"):].strip() if text.startswith("/notes") else text
        # A per-turn instruction: the small model otherwise asks clarifying questions instead of drafting.
        turn_text = user_text + (DRAFT_HINT if DRAFT.search(user_text) and not FOLLOW_UP.search(user_text) else "")
        messages = prompts.chat_messages(trim_history(history), turn_text, hits)
        print("scout> ", end="", flush=True)
        try:
            reply, stats = llm.generate(messages, config.CHAT_SETTINGS,
                                        on_text=lambda t: (sys.stdout.write(t), sys.stdout.flush()))
        except KeyboardInterrupt:
            print("\n(interrupted)")
            continue
        print(f"\n   ({stats['seconds']} s, {stats['prompt_tokens']} prompt tokens)\n")
        # History keeps the plain user turn and the reply -- never the passages.
        history += [{"role": "user", "content": user_text}, {"role": "assistant", "content": reply}]
        last_hits, last_reply = hits, reply
        log += ["**scout>** " + reply.replace("\n", "\n\n"), "", f"_({stats['seconds']} s)_", ""]
    print("bye.")
    if transcript_path:
        out = config.ROOT / transcript_path
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text("\n".join(log) + "\n")
        print(f"transcript: {config.rel(out)}")

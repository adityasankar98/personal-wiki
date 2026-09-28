"""Prompt assembly. Each mode loads its own instruction file on every call.

ask   -> instructions/wiki-instructions.md + numbered passages + question (no history, no persona)
chat  -> instructions/persona.md + rolling history (+ numbered passages when retrieval ran)
ingest-> instructions/ingest-instructions.md + one section of a source + a format request
"""

from . import config


def instruction(name: str) -> str:
    return (config.INSTRUCTIONS / name).read_text(encoding="utf-8").strip()


def _escape(text: str) -> str:
    # A source must not be able to close its own <passage> block and pose as instructions.
    return text.replace("<passage", "&lt;passage").replace("</passage", "&lt;/passage")


def passages_block(hits) -> str:
    blocks = []
    for i, h in enumerate(hits, start=1):
        p = h.passage
        blocks.append(
            f'<passage id="S{i}" source="{p.source}" section="{p.section}">\n{_escape(p.text)}\n</passage>'
        )
    return "\n\n".join(blocks)


def ask_messages(question: str, hits):
    user = (
        "Source passages:\n\n" + passages_block(hits)
        + f"\n\nQuestion: {question}\n"
        "Answer from the passages only, citing [S#] after each fact, "
        'or reply "Insufficient evidence: ..." if they do not contain the answer.'
    )
    return [{"role": "system", "content": instruction("wiki-instructions.md")},
            {"role": "user", "content": user}]


QUOTE_FIRST = (
    '\n\nFirst, on a line starting with "Evidence:", copy word for word the one or two sentences from the '
    'passages that answer the question, each followed by its [S#]. If none do, write "Evidence: none".\n'
    'Then, on a line starting with "Answer:", answer in 1-3 sentences with [S#] citations, '
    'or write "Insufficient evidence: ..." if the evidence line is none.'
)


def ask_quote_first_messages(question: str, hits):
    """Second-pass prompt used only to double-check a refusal (see ask.rescue)."""
    messages = ask_messages(question, hits)
    messages[-1]["content"] += QUOTE_FIRST
    return messages


def chat_messages(history, user_text: str, hits=None):
    if hits:
        user_text = (
            "The harness already looked up my notes for this turn; here are the passages:\n\n"
            + passages_block(hits) + f"\n\nMy message: {user_text}\n\n"
            "(Answer my message now from these passages, citing [S#] after each fact from them. "
            "Do not suggest /notes. If they do not contain the answer, say so.)"
        )
    return ([{"role": "system", "content": instruction("persona.md")}]
            + history + [{"role": "user", "content": user_text}])


def ingest_messages(task: str, section_title: str, section_text: str):
    user = (
        f'<passage id="section" section="{section_title}">\n{_escape(section_text)}\n</passage>\n\n{task}'
    )
    return [{"role": "system", "content": instruction("ingest-instructions.md")},
            {"role": "user", "content": user}]

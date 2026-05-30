"""Subtraction — keep only the context your task actually needs.

Extractive, query-aware context compression. Instead of *compressing* (rewriting
text into a denser form), it *subtracts*: it selects the smallest set of original
sentences sufficient to answer the query and drops the rest, including
distractors. Kept sentences are verbatim, so the result stays quotable and
inspectable.

Two backends:
  - "lexical" (default): local TF-IDF relevance. Zero dependencies, no API,
    millisecond latency. A solid baseline.
  - an LLM callable via ``llm_backend(fn)``: the model selects the minimal
    sufficient set and flags distractors. This is the "answer-impact" mode that
    wins on the hard cases where the answer sentence is buried under
    higher-keyword-overlap distractors (see benchmark/).
"""
from __future__ import annotations

import json
import math
import re
from collections import Counter
from dataclasses import dataclass

# --- token counting: tiktoken if available/offline-cached, else a rough estimate
try:
    import tiktoken

    _ENC = tiktoken.get_encoding("cl100k_base")

    def count_tokens(s: str) -> int:
        return len(_ENC.encode(s))
except Exception:  # pragma: no cover - environment dependent

    def count_tokens(s: str) -> int:
        return max(1, round(len(s.split()) * 1.3))


_WORD = re.compile(r"[a-z0-9]+")


def _toks(s):
    return _WORD.findall(s.lower())


def split_sentences(text):
    """Paragraph-aware sentence split; each sentence becomes one chunk."""
    out = []
    for para in text.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        for p in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", para):
            p = p.strip()
            if p:
                out.append(p)
    return out


# --- lexical (TF-IDF) relevance, implemented directly (no numpy/sklearn) -------
def _idf(chunks):
    df = Counter()
    for c in chunks:
        for w in set(_toks(c)):
            df[w] += 1
    n = len(chunks)
    return {w: math.log((n + 1) / (df[w] + 1)) + 1 for w in df}


def _tfidf(text, idf):
    t = _toks(text)
    if not t:
        return {}
    tf = Counter(t)
    n = len(t)
    return {w: (tf[w] / n) * idf.get(w, 0.0) for w in tf}


def _cos(a, b):
    if not a or not b:
        return 0.0
    num = sum(a[w] * b[w] for w in set(a) & set(b))
    na = math.sqrt(sum(x * x for x in a.values()))
    nb = math.sqrt(sum(x * x for x in b.values()))
    return num / (na * nb) if na and nb else 0.0


def lexical_scores(query, chunks):
    """TF-IDF cosine of each chunk against the query."""
    idf = _idf(chunks)
    qv = _tfidf(query, idf)
    return [_cos(_tfidf(c, idf), qv) for c in chunks]


# --- LLM ("answer-impact") backend --------------------------------------------
_SELECT_PROMPT = """You are compressing context for a question-answering system.
Given a QUESTION and a numbered list of SENTENCES, select the SMALLEST set of
sentence numbers that is sufficient to answer the question fully and correctly
— include any exception or condition sentence needed for a complete answer.
Also flag numbers that are topically related but would MISLEAD an answerer
(distractors).

QUESTION: {query}

SENTENCES:
{numbered}

Reply with ONLY compact JSON: {{"keep": [numbers], "distractors": [numbers]}}"""


def _extract_json(text):
    m = re.search(r"\{.*\}", text, re.S)
    if not m:
        return {"keep": [], "distractors": []}
    try:
        return json.loads(m.group(0))
    except Exception:
        return {"keep": [], "distractors": []}


def llm_backend(llm_fn):
    """Wrap any ``llm_fn(prompt: str) -> str`` into a subtraction backend.

    The model picks the minimal sufficient set of sentences and flags
    distractors. Bring your own model (OpenAI, local, anything) — the library
    never imports a provider SDK.
    """

    def backend(query, chunks):
        numbered = "\n".join(f"[{i}] {c}" for i, c in enumerate(chunks))
        obj = _extract_json(llm_fn(_SELECT_PROMPT.format(query=query, numbered=numbered)))
        keep = [i for i in obj.get("keep", []) if isinstance(i, int) and 0 <= i < len(chunks)]
        dist = [i for i in obj.get("distractors", []) if isinstance(i, int) and 0 <= i < len(chunks)]
        if not keep:  # never return an empty context; fall back to best lexical hit
            scores = lexical_scores(query, chunks)
            keep = [max(range(len(chunks)), key=lambda i: scores[i])]
        return [chunks[i] for i in keep], [chunks[i] for i in dist]

    return backend


@dataclass
class SubtractionResult:
    text: str          # the subtracted context, in original order
    kept: list         # kept sentences (verbatim)
    dropped: list      # everything removed
    distractors: list  # subset of dropped flagged as misleading
    query: str
    stats: dict

    def __str__(self):
        return self.text


def subtract(query, context, *, backend="lexical", budget=None,
             keep_ratio=0.35, min_keep=1):
    """Subtract a context down to the sentences the query actually needs.

    Parameters
    ----------
    backend : "lexical" | callable
        "lexical" uses local TF-IDF relevance. A callable (from
        ``llm_backend(fn)``) lets a model do answer-impact selection.
    budget : int, optional
        Max tokens to keep (lexical mode honours it greedily). If omitted,
        lexical mode keeps sentences scoring within ``keep_ratio`` of the best.
    """
    chunks = split_sentences(context)
    raw_tokens = count_tokens(context)
    if not chunks:
        return SubtractionResult(context, [], [], [], query,
                                 {"raw_tokens": raw_tokens, "kept_tokens": raw_tokens, "ratio": 1.0,
                                  "n_chunks": 0, "n_kept": 0, "n_distractors": 0})

    distractors = []
    if callable(backend):
        kept, distractors = backend(query, chunks)
    else:
        scores = lexical_scores(query, chunks)
        order = sorted(range(len(chunks)), key=lambda i: scores[i], reverse=True)
        top = scores[order[0]] or 1.0
        chosen, used = [], 0
        for idx in order:
            if budget is not None:
                if chosen and used + count_tokens(chunks[idx]) > budget:
                    break
            elif len(chosen) >= min_keep and scores[idx] < keep_ratio * top:
                break
            chosen.append(idx)
            used += count_tokens(chunks[idx])
        kept = [chunks[i] for i in sorted(chosen)]

    kept_set = set(kept)
    kept_order = [c for c in chunks if c in kept_set]
    dropped = [c for c in chunks if c not in kept_set]
    text = "\n".join(kept_order)
    kept_tokens = count_tokens(text)
    stats = {
        "raw_tokens": raw_tokens,
        "kept_tokens": kept_tokens,
        "ratio": round(kept_tokens / raw_tokens, 3) if raw_tokens else 1.0,
        "n_chunks": len(chunks),
        "n_kept": len(kept_order),
        "n_distractors": len(distractors),
    }
    return SubtractionResult(text, kept_order, dropped, list(distractors), query, stats)

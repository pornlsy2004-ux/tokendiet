"""Local preprocessing for the subtraction experiment.

For each benchmark item: split the document into sentence-level chunks, count
tokens per chunk, rank chunks by lexical (TF-IDF) relevance to the question,
and locate the gold 'relevant' sentence within that ranking.

The key diagnostic is `topk_rank_of_gold`: where the genuinely useful sentence
lands in a relevance ranking. If it's often NOT rank 1, a relevance-top-k
baseline is being out-competed by distractors -- exactly the gap that
answer-impact subtraction is meant to close.

Pure standard library (+ optional tiktoken). Deliberately avoids numpy/sklearn,
which are ABI-incompatible in this environment, so TF-IDF is implemented直接.
"""
import json
import math
import re
from collections import Counter
from pathlib import Path

# Token counter: tiktoken if available/offline-cached, else a rough word estimate.
try:
    import tiktoken
    _ENC = tiktoken.get_encoding("cl100k_base")
    def ntok(s):
        return len(_ENC.encode(s))
    TOK = "tiktoken/cl100k_base"
except Exception:
    def ntok(s):
        return max(1, round(len(s.split()) * 1.3))
    TOK = "wordcount*1.3 (tiktoken unavailable)"

ROOT = Path(__file__).resolve().parent
WORD = re.compile(r"[a-z0-9]+")


def toks(s):
    return WORD.findall(s.lower())


def split_sentences(doc):
    """Paragraph-aware sentence split. Keeps each sentence as one chunk."""
    chunks = []
    for para in doc.split("\n\n"):
        para = para.strip()
        if not para:
            continue
        for p in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", para):
            p = p.strip()
            if p:
                chunks.append(p)
    return chunks


def build_idf(chunks):
    df = Counter()
    for c in chunks:
        for w in set(toks(c)):
            df[w] += 1
    n = len(chunks)
    return {w: math.log((n + 1) / (df[w] + 1)) + 1 for w in df}


def tfidf(text, idf):
    t = toks(text)
    if not t:
        return {}
    tf = Counter(t)
    n = len(t)
    return {w: (tf[w] / n) * idf.get(w, 0.0) for w in tf}


def cosine(a, b):
    if not a or not b:
        return 0.0
    num = sum(a[w] * b[w] for w in set(a) & set(b))
    na = math.sqrt(sum(x * x for x in a.values()))
    nb = math.sqrt(sum(x * x for x in b.values()))
    return num / (na * nb) if na and nb else 0.0


def main():
    data = json.loads((ROOT / "items.json").read_text(encoding="utf-8"))
    docs = data["docs"]
    out = []

    for it in data["items"]:
        doc = docs[it["doc"]]
        q = it["question"]
        chunks = split_sentences(doc)
        idf = build_idf(chunks)
        cvecs = [tfidf(c, idf) for c in chunks]
        qv = tfidf(q, idf)
        sims = [round(cosine(v, qv), 4) for v in cvecs]
        order = sorted(range(len(chunks)), key=lambda i: sims[i], reverse=True)

        rv = tfidf(it.get("relevant", ""), idf)
        rel_sims = [cosine(v, rv) for v in cvecs]
        gold = max(range(len(chunks)), key=lambda i: rel_sims[i])

        out.append({
            "id": it["id"],
            "doc": it["doc"],
            "question": q,
            "answer": it["answer"],
            "n_chunks": len(chunks),
            "raw_tokens": ntok(doc),
            "chunks": chunks,
            "chunk_tokens": [ntok(c) for c in chunks],
            "relevance_order": order,
            "relevance_sims": sims,
            "gold_chunk_idx": gold,
            "gold_chunk_tokens": ntok(chunks[gold]),
            "topk_rank_of_gold": order.index(gold) + 1,
        })

    (ROOT / "results").mkdir(parents=True, exist_ok=True)
    (ROOT / "results" / "prep.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"tokenizer: {TOK}\n")
    print(f"{'id':<5}{'doc':<11}{'chunks':<8}{'raw_tok':<9}{'gold_tok':<9}{'gold_rank':<10}")
    print("-" * 52)
    n_rank1 = raw_total = gold_total = 0
    for r in out:
        rank = r["topk_rank_of_gold"]
        n_rank1 += rank == 1
        raw_total += r["raw_tokens"]
        gold_total += r["gold_chunk_tokens"]
        print(f"{r['id']:<5}{r['doc']:<11}{r['n_chunks']:<8}{r['raw_tokens']:<9}"
              f"{r['gold_chunk_tokens']:<9}{rank:<10}")
    print("-" * 52)
    n = len(out)
    print(f"\n{n} items. Gold sentence ranked #1 by lexical relevance in {n_rank1}/{n} cases.")
    print(f"Raw total: {raw_total} tok | gold-only total: {gold_total} tok "
          f"({gold_total / raw_total:.1%} of raw).")
    print("Wrote results/prep.json")


if __name__ == "__main__":
    main()

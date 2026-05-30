"""Prepare a HotpotQA (distractor) subset for the subtraction evaluation.

Each item has 10 paragraphs (2-3 gold + distractors). We build, per item:
  - selector_input : all 10 numbered paragraphs (for answer-impact subtraction)
  - ans_raw_input  : all 10 paragraphs concatenated (upper-bound context)
  - ans_bm25_input : the BM25 top-3 paragraphs (a real retrieval baseline)
  - gold           : the answer + gold paragraph indices + BM25 picks

Diagnostic: how often BM25 top-3 covers ALL gold paragraphs — where it doesn't,
the answer is reachable only by subtraction-style selection, not keyword overlap.

Pure standard library. Usage: python prep_hotpot.py [N]   (default 50)
"""
import json
import math
import re
import sys
from collections import Counter
from pathlib import Path

H = Path(__file__).resolve().parent
N = int(sys.argv[1]) if len(sys.argv) > 1 else 50

rows = json.loads((H / "raw.json").read_text(encoding="utf-8"))[:N]
WORD = re.compile(r"[a-z0-9]+")
tok = lambda s: WORD.findall(s.lower())


def bm25(query, docs, k1=1.5, b=0.75):
    dts = [tok(d) for d in docs]
    nd = len(dts)
    df = Counter()
    for d in dts:
        for w in set(d):
            df[w] += 1
    idf = {w: math.log((nd - df[w] + 0.5) / (df[w] + 0.5) + 1) for w in df}
    avgdl = sum(len(d) for d in dts) / nd
    qt = tok(query)
    out = []
    for d in dts:
        tf = Counter(d)
        dl = len(d)
        s = 0.0
        for w in set(qt):
            if w in tf:
                s += idf.get(w, 0) * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * dl / avgdl))
        out.append(s)
    return out


sel, araw, abm, gold = [], [], [], []
for i, r in enumerate(rows):
    qid = str(i)
    q, ans = r["question"], r["answer"]
    titles, sents = r["context"]["title"], r["context"]["sentences"]
    paras = [f"{titles[j]}: {' '.join(sents[j])}" for j in range(len(titles))]
    scores = bm25(q, paras)
    order = sorted(range(len(paras)), key=lambda j: scores[j], reverse=True)
    top3 = sorted(order[:3])
    goldset = set(r["supporting_facts"]["title"])
    goldidx = [j for j, t in enumerate(titles) if t in goldset]

    sel.append({"id": qid, "question": q,
                "paragraphs": {str(j): paras[j] for j in range(len(paras))}})
    araw.append({"id": qid, "question": q, "context": "\n\n".join(paras)})
    abm.append({"id": qid, "question": q, "context": "\n\n".join(paras[j] for j in top3)})
    gold.append({"id": qid, "answer": ans, "gold_idx": goldidx, "bm25_top3": top3})

for name, data in [("selector_input", sel), ("ans_raw_input", araw),
                   ("ans_bm25_input", abm), ("gold", gold)]:
    (H / f"{name}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")

cov = sum(1 for g in gold if set(g["gold_idx"]).issubset(set(g["bm25_top3"])))
miss = len(gold) - cov
print(f"N={len(rows)} hard HotpotQA items prepared.")
print(f"BM25 top-3 covers ALL gold paragraphs in {cov}/{len(rows)} items "
      f"({miss} miss at least one — those are where subtraction can win).")
print("wrote selector_input / ans_raw_input / ans_bm25_input / gold .json")

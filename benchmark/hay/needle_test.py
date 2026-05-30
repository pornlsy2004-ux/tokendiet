"""300k-token needle-in-a-haystack: subtraction vs stuff-it-all / keyword / summarize.

Builds a ~300,000-token document of filler with ONE true answer buried in it, plus
four LEXICAL DECOYS (a blank field, a placeholder 00000, a different/older satellite,
a storage note) that share the question's keywords. Runs BM25 coarse retrieval and
writes hard_coarse.json (the candidate paragraphs an answerer sees).

Pure stdlib, seed=11 — fully reproducible. The answerer step is an LLM (Claude Haiku
in our run); recorded results (hard_result.json):

  stuff-it-all-in  300,059 tok -> exceeds the 200k window, won't fit
  keyword BM25 top-3   624 tok -> "blank / 00000"   WRONG (fooled by the decoys)
  subtraction  1 para  226 tok -> QX-7793-ZD         CORRECT

And subtraction vs summarize at the SAME budget (summary.txt = 182 tok): the summary
drops the needle ("not in the summary"); subtraction keeps it verbatim.

Usage: python needle_test.py
"""
import re, math, random, json
from collections import Counter
from pathlib import Path
try:
    import tiktoken; ENC = tiktoken.get_encoding("cl100k_base"); ntok = lambda s: len(ENC.encode(s))
except Exception:
    ntok = lambda s: max(1, round(len(s.split()) * 1.3))

rng = random.Random(11)
ORGS = ["Helios Logistics", "Northwind Capital", "the Meridian Council", "Acme Robotics", "Vantage Health", "Bluepeak Energy", "the Cascade Authority", "Orchid Biotech", "Granite Mutual", "Sintel Media", "the Tisbury Board", "Kestrel Aviation"]
TOPICS = ["the quarterly compliance review", "seasonal inventory turnover", "the regional staffing plan", "membership renewal rates", "the data retention schedule", "vendor onboarding timelines", "the facilities maintenance window", "cross-border shipping tariffs", "the annual safety audit", "customer churn in the northeast"]
VERBS = ["increased", "declined", "stabilized", "was deferred", "exceeded projections", "fell short of target", "was renegotiated", "remained flat", "was consolidated"]
TAILS = ["pending board approval.", "ahead of the fiscal close.", "despite supply constraints.", "under the revised guidelines.", "following the merger.", "across all three regions.", "per the updated policy.", "with no material exceptions."]
sentence = lambda: f"In Q{rng.randint(1,4)} of {rng.randint(2019,2026)}, {rng.choice(ORGS)} reported that {rng.choice(TOPICS)} {rng.choice(VERBS)} {rng.choice(TAILS)}"

TRUE = "Internal note: the uplink credential currently provisioned for the Orion program is QX-7793-ZD, valid through 2027."
DIST = ["The activation key field for the Orion satellite is intentionally left blank in the staging configuration.",
        "For Orion satellite integration tests, a placeholder activation key of 00000-00 is used and must never ship.",
        "The activation key for the older Saturn satellite uplink was QX-1120-AA before decommissioning.",
        "Do not store the Orion satellite activation key in the shared activation-key spreadsheet."]
QUESTION = "What is the activation key for the Orion satellite uplink?"
ANSWER = "QX-7793-ZD"

inject_frac = [0.30, 0.42, 0.55, 0.66, 0.78]
to_inject = [("TRUE", TRUE)] + [("DIST", d) for d in DIST]
specials, paras, tok, ii = {}, [], 0, 0
TARGET = 300_000
while tok < TARGET:
    if ii < len(to_inject) and tok > TARGET * inject_frac[ii]:
        label, text = to_inject[ii]
        para = " ".join(sentence() for _ in range(4)) + " " + text + " " + " ".join(sentence() for _ in range(4))
        specials[len(paras)] = label; ii += 1
    else:
        para = " ".join(sentence() for _ in range(rng.randint(10, 16)))
    paras.append(para); tok += ntok(para)
total = tok

WORD = re.compile(r"[a-z0-9-]+"); tk = lambda s: WORD.findall(s.lower())
def bm25(q, docs, k1=1.5, b=0.75):
    dts = [tk(d) for d in docs]; nd = len(dts); df = Counter()
    for d in dts:
        for w in set(d): df[w] += 1
    idf = {w: math.log((nd - df[w] + 0.5) / (df[w] + 0.5) + 1) for w in df}; avg = sum(len(d) for d in dts) / nd
    qt = tk(q); out = []
    for d in dts:
        tf = Counter(d); dl = len(d); s = 0.0
        for w in set(qt):
            if w in tf: s += idf.get(w, 0) * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * dl / avg))
        out.append(s)
    return out

scores = bm25(QUESTION, paras); order = sorted(range(len(paras)), key=lambda i: scores[i], reverse=True)
true_idx = [i for i, l in specials.items() if l == "TRUE"][0]
top3, top12 = order[:3], order[:12]
H = Path(__file__).resolve().parent
json.dump({"question": QUESTION, "answer": ANSWER, "total_tokens": total, "n_paragraphs": len(paras),
           "true_needle_idx": true_idx, "true_needle_bm25_rank": order.index(true_idx) + 1,
           "bm25_top3": {str(i): paras[i] for i in top3}, "bm25_top3_tokens": sum(ntok(paras[i]) for i in top3),
           "coarse_top12": {str(i): paras[i] for i in top12}, "coarse_top12_tokens": sum(ntok(paras[i]) for i in top12)},
          open(H / "hard_coarse.json", "w", encoding="utf-8"), ensure_ascii=False)
print(f"haystack: {len(paras)} paras, {total:,} tokens")
print(f"true needle BM25 rank #{order.index(true_idx)+1} (top-3 are all decoys); in top-12? {'YES' if true_idx in top12 else 'NO'}")
print("wrote hard_coarse.json -> answerer (LLM) results recorded in hard_result.json")

"""
Reproduce the Subtraction controlled test: does compressing context change accuracy?

  pip install anthropic        # or: pip install openai
  export ANTHROPIC_API_KEY=...  # or: export OPENAI_API_KEY=...
  python run.py

For each item in items.json, three conditions answer the SAME question:
  raw         - the full document
  compressed  - the document compressed by the model (told to preserve key info)
  subtracted  - only the one relevant sentence
Scoring is crude (key-token match); eyeball the printed MISSes. Raw run: results/controlled.json.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))

def call(prompt, max_tokens=400):
    if os.environ.get("ANTHROPIC_API_KEY"):
        import anthropic
        model = os.environ.get("SUBTRACTION_MODEL", "claude-opus-4-8")
        m = anthropic.Anthropic().messages.create(
            model=model, max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}])
        return m.content[0].text.strip()
    if os.environ.get("OPENAI_API_KEY"):
        import openai
        model = os.environ.get("SUBTRACTION_MODEL", "gpt-4.1")
        m = openai.OpenAI().chat.completions.create(
            model=model, max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}])
        return m.choices[0].message.content.strip()
    sys.exit("Set ANTHROPIC_API_KEY or OPENAI_API_KEY first.")

def compress(doc):
    return call("Compress the document below to roughly 30% of its length for an LLM's context "
                "window. Preserve all important information. Output ONLY the compressed text.\n\n"
                "DOCUMENT:\n" + doc, 400)

def answer(context, question):
    return call("Using ONLY the text below, answer the question. Reply with ONLY the specific value "
                "or short phrase. If the text does not contain it, reply UNKNOWN.\n\nTEXT:\n"
                + context + "\n\nQUESTION: " + question, 60)

def is_correct(resp, gold):
    norm = lambda s: re.sub(r"[^a-z0-9$%]", "", s.lower())
    key = norm(gold.split("(")[0].split("/")[0])[:6]
    return bool(key) and key in norm(resp)

def toks(s):
    return max(1, round(len(s) / 4))

def main():
    data = json.load(open(os.path.join(ROOT, "items.json"), encoding="utf-8"))
    docs, items = data["docs"], data["items"]
    comp_cache, agg = {}, {c: [0, 0] for c in ("raw", "compressed", "subtracted")}
    for it in items:
        doc = docs[it["doc"]]
        comp_cache.setdefault(it["doc"], compress(doc))
        ctx = {"raw": doc, "compressed": comp_cache[it["doc"]], "subtracted": it["relevant"]}
        marks = []
        for cond in ("raw", "compressed", "subtracted"):
            ok = is_correct(answer(ctx[cond], it["question"]), it["answer"])
            agg[cond][0] += ok
            agg[cond][1] += toks(ctx[cond])
            marks.append("%s:%s" % (cond[:3], "ok" if ok else "MISS"))
        print("%-4s %s" % (it["id"], "  ".join(marks)))
    n = len(items)
    print("\ncondition     accuracy   avg context tokens")
    for cond in ("raw", "compressed", "subtracted"):
        print("%-12s  %3.0f%%       %d" % (cond, 100 * agg[cond][0] / n, agg[cond][1] / n))

if __name__ == "__main__":
    main()

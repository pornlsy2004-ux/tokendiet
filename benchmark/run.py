"""
Run the Subtraction self-test against any model via API, and score it.

  pip install anthropic        # or: pip install openai
  export ANTHROPIC_API_KEY=... # or: export OPENAI_API_KEY=...
  python gen.py                # build haystacks + manifest.json first
  python run.py

The haystack is INLINED into the prompt (nothing to grep — this is the rigorous version).
Two questions per haystack: retrieve one code, and count the even codes.
"""
import json, os, re, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
MANIFEST = os.path.join(ROOT, "manifest.json")
OUT = os.path.join(ROOT, "results", "run.json")

def call_model(prompt):
    if os.environ.get("ANTHROPIC_API_KEY"):
        import anthropic
        model = os.environ.get("SUBTRACTION_MODEL", "claude-haiku-4-5-20251001")
        msg = anthropic.Anthropic().messages.create(
            model=model, max_tokens=64,
            messages=[{"role": "user", "content": prompt}])
        return msg.content[0].text.strip()
    if os.environ.get("OPENAI_API_KEY"):
        import openai
        model = os.environ.get("SUBTRACTION_MODEL", "gpt-4.1-mini")
        msg = openai.OpenAI().chat.completions.create(
            model=model, max_tokens=64,
            messages=[{"role": "user", "content": prompt}])
        return msg.choices[0].message.content.strip()
    sys.exit("Set ANTHROPIC_API_KEY or OPENAI_API_KEY first.")

def main():
    if not os.path.exists(MANIFEST):
        sys.exit("Run `python gen.py` first.")
    trials = json.load(open(MANIFEST, encoding="utf-8"))
    rows, sizes = [], {}
    for t in trials:
        hay = open(t["path"], encoding="utf-8").read()
        r_ans = call_model(hay + "\nEach line above gives a vault access code. "
                                  "Reply with ONLY the 4-digit code for %s." % t["target"])
        c_ans = call_model(hay + "\nEach line above gives a 4-digit vault access code. "
                                  "Reply with ONLY the integer count of how many are EVEN "
                                  "(last digit 0, 2, 4, 6, or 8).")
        r_hit = re.search(r"\d{4}", r_ans)
        retrieval_ok = bool(r_hit and r_hit.group() == t["answer"])
        c_hit = re.search(r"\d+", c_ans)
        count_err = abs(int(c_hit.group()) - t["true_even"]) if c_hit else None
        within1 = count_err is not None and count_err <= 1
        rows.append({"id": t["id"], "n": t["n_lines"], "retrieval_ok": retrieval_ok,
                     "count_answer": c_hit.group() if c_hit else None,
                     "true_even": t["true_even"], "count_err": count_err, "within1": within1})
        s = sizes.setdefault(t["n_lines"], {"r": 0, "w": 0, "k": 0})
        s["r"] += retrieval_ok; s["w"] += within1; s["k"] += 1
        print("%-8s retrieval=%s  count_err=%s" % (t["id"], retrieval_ok, count_err))

    print("\nsize   retrieval   counting(±1)")
    for n in sorted(sizes):
        s = sizes[n]
        print("%-5d  %3.0f%%        %3.0f%%" % (n, 100*s["r"]/s["k"], 100*s["w"]/s["k"]))

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(rows, open(OUT, "w", encoding="utf-8"), indent=2)
    print("\nwrote", OUT)

if __name__ == "__main__":
    main()

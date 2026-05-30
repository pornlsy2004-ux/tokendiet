"""
Build haystack inputs + a manifest (with ground truth) for run.py.

Each haystack is N near-identical lines:
    The vault access code for Outpost-NNNNN is DDDD.
Exactly one line is the needle (placed in the middle, the hardest position).
No model is called here. Reproducible via the fixed seeds.
"""
import json, os, random

ROOT = os.path.dirname(os.path.abspath(__file__))
HAY = os.path.join(ROOT, "hay")
os.makedirs(HAY, exist_ok=True)

SIZES = [50, 200, 500, 900, 1400]   # bump these toward your model's real context window
TRIALS = 3

def make(n, seed):
    rnd = random.Random(seed)
    ids, seen = [], set()
    while len(ids) < n:
        x = "Outpost-%05d" % rnd.randint(0, 99999)
        if x not in seen:
            seen.add(x); ids.append(x)
    codes = ["%04d" % rnd.randint(0, 9999) for _ in range(n)]
    ti = n // 2  # needle in the middle
    lines = ["The vault access code for %s is %s." % (ids[i], codes[i]) for i in range(n)]
    text = "\n".join(lines) + "\n"
    true_even = sum(1 for c in codes if int(c) % 2 == 0)
    return text, ids[ti], codes[ti], true_even

def main():
    manifest = []
    for si, n in enumerate(SIZES):
        for k in range(TRIALS):
            text, target, answer, true_even = make(n, seed=1000 + si * 10 + k)
            fn = "hay_%d_%d.txt" % (n, k)
            with open(os.path.join(HAY, fn), "w", encoding="utf-8") as f:
                f.write(text)
            manifest.append({
                "id": "%d_%d" % (n, k), "n_lines": n,
                "target": target, "answer": answer, "true_even": true_even,
                "path": os.path.join(HAY, fn),
            })
    with open(os.path.join(ROOT, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2)
    print("wrote %d trials across sizes %s" % (len(manifest), SIZES))

if __name__ == "__main__":
    main()

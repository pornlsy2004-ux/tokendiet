"""Score subtract vs keyword-top-2 predictions against gold.

Reproduces the comparison table in the README from the answers in
results/sub_pred.json and results/topk_pred.json (each system's answer per
item) and results/gold.json. Judging is keyword/number matching with a
separate completeness check for the two multi-part answers (C, G3).
"""
import json
from pathlib import Path

R = Path(__file__).resolve().parent / "results"
sub = {x["id"]: x for x in json.loads((R / "sub_pred.json").read_text(encoding="utf-8"))}
topk = {x["id"]: x for x in json.loads((R / "topk_pred.json").read_text(encoding="utf-8"))}
gold = {x["id"]: x["gold"] for x in json.loads((R / "gold.json").read_text(encoding="utf-8"))}

low = lambda a: a.lower()

CORRECT = {
    "A": lambda a: "340" in a,
    "B": lambda a: "30" in a,
    "C": lambda a: "not approved" in low(a) or low(a).lstrip().startswith("no"),
    "D": lambda a: "12" in a and "not stated" not in low(a),
    "E1": lambda a: "2,500" in a or "2500" in a,
    "E2": lambda a: "exclud" in low(a) or "not covered" in low(a),
    "E3": lambda a: "30" in a,
    "F1": lambda a: any(s in low(a) for s in ("best-effort", "no uptime", "no sla", "none")),
    "F2": lambda a: "25" in a,
    "F3": lambda a: "30" in a,
    "G1": lambda a: "non-refundable" in low(a) or "not refundable" in low(a) or low(a).lstrip().startswith("no"),
    "G2": lambda a: ("only one" in low(a) or "once" in low(a) or "one transfer" in low(a)) and "not stated" not in low(a),
    "G3": lambda a: "not allowed" in low(a) or "may not" in low(a) or low(a).lstrip().startswith("no"),
}
COMPLETE = {
    "C": lambda a: any(s in low(a) for s in ("audit", "sept", "q4")),
    "G3": lambda a: "keynote" in low(a) or "exception" in low(a),
}
IDS = ["A", "B", "C", "D", "E1", "E2", "E3", "F1", "F2", "F3", "G1", "G2", "G3"]


def score(pred):
    core = comp = 0
    marks = {}
    for i in IDS:
        a = pred[i]["answer"]
        c = CORRECT[i](a)
        full = c and (COMPLETE[i](a) if i in COMPLETE else True)
        core += c
        comp += full
        marks[i] = "OK" if full else ("~" if c else "X")
    return core, comp, marks


def main():
    cs, ms, rs = score(sub)
    ct, mt, rt = score(topk)
    print(f"{'id':<4}{'sub':<5}{'top2':<6}gold")
    print("-" * 60)
    for i in IDS:
        print(f"{i:<4}{rs[i]:<5}{rt[i]:<6}{gold[i][:42]}")
    print("-" * 60)
    n = len(IDS)
    print(f"core-correct  : subtract {cs}/{n}   top-2 {ct}/{n}")
    print(f"fully-complete: subtract {ms}/{n}   top-2 {mt}/{n}")
    ks = [sub[i].get("kept_count", 1) for i in IDS]
    print(f"subtract sentences/item: avg {sum(ks) / n:.1f}  (top-2 baseline = 2.0)")
    print("legend: OK=correct&complete  ~=core right but incomplete  X=wrong/can't answer")


if __name__ == "__main__":
    main()

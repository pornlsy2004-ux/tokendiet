# Benchmark — the self-test

A tiny, reproducible context-rot demonstration. Two tasks over the *same* haystack of
*N* near-identical lines (`The vault access code for Outpost-NNNNN is DDDD.`):

- **retrieval** — find the code for one specific Outpost (the easy case).
- **counting** — count how many codes are even (forces the model to use the *whole* context).

## What we found

Model under test: **Claude Haiku 4.5**, fresh context per trial, 3 trials per size.

| context size | retrieval | counting (±1 of truth) | behaviour at scale |
|---:|:---:|:---:|:---|
| 50 lines | 100% | 67% | actually counts |
| 200 | 100% | 33% | drifts |
| 500 | 100% | 0% | emits "250" (= N/2) |
| 900 | 100% | 0% | emits "450" |
| 1400 | 100% | 0% | emits "700" |

Retrieval doesn't rot. *Using* the context does — and past ~500 items the model quietly
abandons the task and returns the statistically expected number, looking confident the
whole time. Raw data: [`results/selftest.json`](results/selftest.json).

> **Honest caveats.** Small N, one small model, single needle position (middle). Our run
> had subagents *read the haystack file* and were instructed not to use search/code; that
> isn't sandbox-enforced. `run.py` below is the rigorous version: it **inlines** the haystack
> straight into the prompt (nothing to grep) and hits a real API. The peer-reviewed, heavy
> evidence is in [`../docs/receipts.md`](../docs/receipts.md); this is the poke-it-yourself version.

## Reproduce it

```bash
pip install anthropic          # or: pip install openai
export ANTHROPIC_API_KEY=...    # or: export OPENAI_API_KEY=...

python gen.py                  # builds haystacks + manifest.json (with ground truth)
python run.py                  # queries the model, scores, writes results/run.json
```

Pick the model with `SUBTRACTION_MODEL` (e.g. `claude-haiku-4-5-20251001`, `gpt-4.1-mini`).
Crank the sizes in `gen.py` up to your model's real context window and watch where *its*
counting falls off. That cliff is the line you should be subtracting back from.

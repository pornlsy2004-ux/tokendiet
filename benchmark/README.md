# Benchmark — the controlled test

**Does compressing your context change accuracy?** We ran the head-to-head instead of asserting it.

Same question, same model (Claude Opus 4.8), three context treatments:

- **raw** — the full document
- **compressed** — the document compressed by Opus (told to preserve all important info, ~30–50%)
- **subtracted** — only the one relevant sentence

13 questions, each answer a *buried detail* — an exception, an override, a negation. Blind, exact-match.

## What we found

| condition | accuracy | median context tokens |
|---|:---:|:---:|
| Raw | 85% | 218 |
| Compressed | 85% | 108 |
| Subtracted | **85%** | **28** |

A **null result on compression** — it neither helped nor hurt. Subtraction matched raw accuracy
at **~1/8 the tokens**. Full per-question data: [`results/controlled.json`](results/controlled.json).

We kept the honest failure modes too:
- **Compression once flipped a correct answer** while *keeping* the fact: it preserved "/export → 30/min"
  but the model still answered the salient default "600". Compression can strip the emphasis that tells
  the model which fact wins.
- **Over-subtraction failed twice**: cutting to a single sentence removed the bridge a question needed
  (e.g. that a "conference pass" *is* the "ticket"). Subtract to the relevant *unit*, not the shortest string.

> **Limits, stated plainly.** N=13, short documents, one model, hand-written items. This is a
> demonstration you can re-run, not a leaderboard. The heavy, peer-reviewed evidence that *long*
> context degrades accuracy is in [`../docs/receipts.md`](../docs/receipts.md) — that's the claim
> this repo actually rests on.

## Reproduce / break it

```bash
pip install anthropic          # or: pip install openai
export ANTHROPIC_API_KEY=...    # or: export OPENAI_API_KEY=...
python run.py                  # compresses each doc, answers in 3 conditions, scores
```

`items.json` is the input — add your own documents and questions. **Want to see compression
finally bite?** Make the documents long (tens of thousands of tokens) and the compression
aggressive; that's the regime the [context-rot literature](../docs/receipts.md) lives in.
Pick the model with `SUBTRACTION_MODEL` (e.g. `claude-opus-4-8`, `gpt-4.1`).

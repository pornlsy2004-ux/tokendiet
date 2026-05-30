<div align="center">

# Subtraction

### Same answer. A fraction of the tokens.

<img src="assets/demo.gif" alt="Subtraction demo — keep the relevant slice verbatim, drop the rest, same answer at a fraction of the tokens" width="840">

<img src="assets/subtraction-result.svg" alt="One fact in a 300K-token haystack: stuffing it overflows the window, keyword retrieval is fooled by decoys, subtraction answers correctly on 226 tokens" width="840">

The reflex is to cram everything into the context window — and when it won't fit, to
**compress** it so more does. But scale is the trap. Hide one fact in **300,000 tokens**
of look-alike noise: stuffing it all overflows the window, and keyword search gets fooled
by the decoys. **Subtraction keeps the one true line — 226 tokens — and answers correctly.**

The lever isn't how you pack the context. It's how little you put in it.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Reproducible](https://img.shields.io/badge/benchmark-reproducible-3fb950.svg)](benchmark/)
[![Stars](https://img.shields.io/github/stars/pornlsy2004-ux/subtraction?style=social)](https://github.com/pornlsy2004-ux/subtraction)

</div>

---

## TL;DR

- **At scale, including less is the only thing that works.** One fact in a **300,000-token** haystack: stuffing it all overflows the window, keyword top-3 gets fooled by look-alike decoys, and **subtraction answers correctly on 226 tokens.**
- **Compression is a no-op for accuracy.** In a controlled small-doc test, full / compressed / subtracted contexts all scored the **same** — compression didn't help *or* hurt.
- **Scale is the real enemy.** Peer-reviewed work shows every frontier model gets less reliable as input grows — even with *perfect* retrieval. ([receipts ↓](#the-part-thats-not-up-for-debate-scale))
- **So: include less, fetch on demand.** Subtraction + [think-in-code](#the-cure-subtract), not a better compressor.

---

## The reflex: stuff it, then compress it

Open GitHub and count the repos promising to **save you tokens**: semantic compressors, prompts rewritten to their densest form, even writing context in Classical Chinese for the character density. They all answer one question — *"how do I fit more in?"*

We started this repo believing the sharper version: *compression actively throws away the details your task depends on.* Then we tested it. We were wrong.

## We measured it — and it changed our mind

**One fact, buried in 300,000 tokens.** We hid a single answer — the activation key for the Orion uplink — in a 300K-token haystack of plausible business filler, then planted **four look-alike decoys** that share the question's keywords (a blank field, a `00000` placeholder, a *different* satellite's old key, a "don't store it here" note). Then we asked Claude Haiku the same question three ways:

| Method | Tokens to model | Answer | Correct? |
|---|:---:|:---:|:---:|
| **Stuff it all in** | 300,162 | *over the 200K window* | ✗ won't fit |
| **Keyword top-3** (BM25) | 624 | "blank / 00000" | ✗ decoy |
| **Subtraction** | **226** | **QX-7793-ZD** | ✓ correct |

Stuffing the whole document doesn't even fit the window. Keyword retrieval is cheap, but the decoys **outrank the truth** — the real line lands at rank #4, so the top-3 answer is a placeholder. Subtraction keeps the one line that actually answers the question: **226 tokens, correct.** Fully reproducible (seed=11) in **[/benchmark/hay](benchmark/hay)**.

**And a controlled null-result on compression.** On a separate small-doc set (13 questions, Claude Opus 4.8), the **full document**, a **careful compression** (~50%, told to preserve all important info), and **subtraction** all scored the **same 85%** — compression neither helped nor hurt accuracy; only the token bill moved (median 218 → 28). The whole run, including the cases where subtraction *didn't* work (over-subtract and you cut the bridge a question needs), is in [/benchmark](benchmark/).

> We're publishing the result that killed our own headline. That's the point — if a claim can't survive its own benchmark, it shouldn't be in your prompt either.

## The part that's not up for debate: scale

The needle test above runs at 300K — length is exactly where subtraction earns its keep. On what happens as context gets *long*, the literature is unambiguous.

**Same fact, different position — the middle is a dead zone:**

<div align="center">
<img src="assets/lost-in-the-middle.svg" alt="Lost in the Middle: accuracy high at the start and end of context, low in the middle" width="720">
</div>

**Even with *perfect* retrieval, length alone degrades accuracy:**

<div align="center">
<img src="assets/perfect-retrieval.svg" alt="Llama-3.1-8B accuracy collapses at 30K tokens even with the answer present" width="720">
</div>

Accuracy drops **13.9%–85%** as input grows **even when retrieval is perfect** (Du et al., EMNLP 2025). Chroma found the same across 18 frontier models. You don't compress your way out of that — a shorter-but-still-huge context still rots. You **subtract**.

## The cure: subtract

A discipline, not a tool:

1. **Default to less.** Justify what you include, not what you cut. Most of your context is dead weight.
2. **The relevant slice ≈ full accuracy at a fraction of the cost.** Spend your effort finding it, not packing everything.
3. **Don't over-subtract.** Our own test caught this: cut too far and you remove the sentence a question depends on. Subtract to the *relevant unit*, not the shortest string.
4. **Never bank on the middle.** If something must be there, put it at the edges.
5. **Think in code.** The scalable form of subtraction: instead of *handing* the model data, let it **write code to fetch the exact slice it needs**, so the bulk never enters the window. Anthropic's own guidance moved this way — present servers as code APIs so "intermediate results stay in the execution environment; the agent only sees what is explicitly returned." ([Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp), 2025).

## The library: `pip install` the discipline

The *principle* is a discipline. But the **selection** step — find the slice the task needs, drop the distractors — can be a tool. So we built one.

```python
from subtraction import subtract

# Local, zero-dependency baseline (TF-IDF relevance, no API key):
r = subtract("What is the hotel rate cap for Tokyo?", travel_policy)
print(r.text)     # the sentences the question needs, verbatim
print(r.stats)    # {'raw_tokens': 107, 'kept_tokens': 43, 'ratio': 0.402, ...}
```

For the hard cases, **bring your own model** — it picks the minimal sufficient set and flags distractors (the *answer-impact* mode):

```python
from subtraction import subtract, llm_backend
r = subtract(question, context, backend=llm_backend(my_model))
r.text          # minimal sufficient context
r.distractors   # the misleading sentences it removed
```

Kept sentences are **verbatim** — subtraction never rewrites your text, so the result stays quotable and inspectable.

### Does it work? An honest answer — the real benchmark is in progress.

A 13-item **sanity check** (one small model, *our own* questions, *our own* judging) lives in **[/benchmark](benchmark/)**: subtraction matched or beat a keyword baseline on every item and won outright where the answer was buried under distractors. Useful as a smoke test — but N=13 with self-authored questions and self-judging is a **demonstration, not evidence**, and we won't pretend otherwise.

The number to trust is the one we're running now: a real evaluation on **HotpotQA** — hundreds of questions, each deliberately padded with 8 distractor paragraphs, scored with standard answer F1, against a real BM25 baseline. It lands here when it's done.

## The receipts

Every external claim, sourced with exact figures, is in **[docs/receipts.md](docs/receipts.md)**. Our own run — including its limitations — is in **[/benchmark](benchmark/)**. Found a paper we're missing, or a counterexample? **[Open a PR.](CONTRIBUTING.md)**

## FAQ

**"So compression is useless?"** No — it's just not the lever. It saves tokens without changing accuracy, which is fine. But it can't beat subtraction on tokens, and it can't undo the rot that comes from a still-large context. Full answers: **[docs/faq.md](docs/faq.md)**.

**"Isn't 'just send the relevant part' obvious?"** The principle is. The *practice* is the opposite — we dump and compress by reflex. And the catch is real: subtraction assumes you can *find* the relevant slice. That's why think-in-code (let the model fetch it) matters.

**"N=13 is tiny."** Correct, and we say so. It's a demonstration you can re-run, not a leaderboard. The heavy, peer-reviewed evidence for the scale claim is in the [receipts](docs/receipts.md).

## Contribute

A living field guide. Add a receipt, a counterexample, a subtraction pattern, a war story. See **[CONTRIBUTING.md](CONTRIBUTING.md)**.

---

<div align="center">

**If this reframed how you think about context, ⭐ it — and go delete some.**

*Same answer. A fraction of the tokens.*

</div>

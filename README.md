<!--
  Before you publish:
  1. Replace every OWNER/REPO below with your GitHub path (e.g. yourname/subtraction).
  2. Hero + charts live in /assets (SVG, render inline on GitHub).
  3. Launch copy is in /launch. Receipts (the dunk-shield) are in /docs/receipts.md.
     The reproducible self-test is in /benchmark.
-->

<div align="center">

# Subtraction

### Stop compressing your context. Start subtracting it.

<img src="assets/context-rot.svg" alt="Accuracy falls as input context grows — you can't compress your way out of context rot" width="820">

The entire industry is racing to **compress** the context you feed an LLM.
They're optimizing the wrong variable. The bottleneck was never token *count* —
it's **context rot**, and you cannot compress your way out of rot.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)
[![Reproducible](https://img.shields.io/badge/benchmark-reproducible-3fb950.svg)](benchmark/)
[![Stars](https://img.shields.io/github/stars/OWNER/REPO?style=social)](https://github.com/OWNER/REPO)

</div>

---

## TL;DR

- **The wrong fix —** prompt/token compression (LLMLingua, token-compressors, "caveman speak," the classical-Chinese trick). All of it shrinks the *payload*.
- **The law —** every frontier model gets *less reliable* as input grows. Measured, peer-reviewed, and [reproduced here ourselves](#we-didnt-just-theorize--we-ran-it).
- **The cure —** **subtraction** (put less in front of the model) + **think-in-code** (let the agent fetch the rest *on demand*, so it never hits the context window at all).

> You can squeeze a 500K-token mess into 100K tokens. It is still a mess, and the model still rots on it.

---

## The whole field is optimizing the wrong variable

Open GitHub and count the repos promising to **save you tokens**: semantic compressors that "preserve meaning," tools that strip "predictable grammar," prompts rewritten in their densest possible form — even a viral genre that writes context in *Classical Chinese* because one character carries an entire English clause.

They all answer the same question: **"How do I fit *more* into the window?"**

That question is the bug. More-but-smaller is still more.

## The law: context rot

Models do **not** use their context uniformly, and they degrade as it grows — no matter how few tokens you've squeezed it into. This is the most-replicated finding in applied LLM research right now.

**Same fact, different position — the middle is a dead zone:**

<div align="center">
<img src="assets/lost-in-the-middle.svg" alt="Lost in the Middle: accuracy is high at the start and end of context, low in the middle" width="760">
</div>

**The line that kills the compression thesis — *perfect retrieval still rots*:**

<div align="center">
<img src="assets/perfect-retrieval.svg" alt="Llama-3.1-8B accuracy collapses at 30K tokens even with the answer present and distractors masked" width="760">
</div>

Accuracy drops **13.9%–85%** as input grows **even when retrieval is perfect** — even when every irrelevant token is masked out (Du et al., EMNLP 2025). If zeroing out *irrelevant* tokens doesn't save you, losslessly compressing the *relevant* ones won't either. And lossy "semantic" compression is exactly where negations, conditionals, and the one number that flips the answer go to die.

You cannot compress your way out of context rot. You can only **subtract**.

## We didn't just theorize — we ran it

We put a model (Claude Haiku) through a clean test: hide one fact in *N* near-identical lines, then ask it to (a) **find one code** and (b) **count how many codes are even** — a task that forces it to actually use the whole context. Three trials per size, fresh context each time.

<div align="center">
<img src="assets/selftest.svg" alt="Retrieval stays at 100% as context grows; counting accuracy collapses from 67% to 0%" width="820">
</div>

| context size | find one fact | count the whole context (±1) | what the model did at scale |
|---:|:---:|:---:|:---|
| 50 lines | 100% | 67% | actually counted |
| 200 | 100% | 33% | started drifting |
| 500 | 100% | **0%** | **gave up — answered "250"** |
| 900 | 100% | **0%** | **gave up — answered "450"** |
| 1400 | 100% | **0%** | **gave up — answered "700"** |

**Retrieval doesn't rot — *using* the context does.** Past ~500 items the model stopped counting entirely and just emitted the statistically expected number (exactly N/2). It looked confident every time. The whole run is reproducible against your own model/key in **[/benchmark](benchmark/)**.

## The cure, part 1 — Subtraction

A discipline, not a tool. The defaults:

1. **Default to less.** Every token you add is a token the model can drown in. Justify inclusions, not exclusions.
2. **Optimize relevance density, not token count.** 4K of pure signal beats 40K of compressed maybe.
3. **Never fill the middle.** If it has to be there, put it at the edges. The middle is where attention goes to die.
4. **One task, one minimal context.** Don't carry the whole session. Rebuild a tight context per step.
5. **Delete on a schedule.** Memory that only grows, rots. A small, fresh context beats a large, stale one every time.

## The cure, part 2 — Think in code

The frontier version of subtraction: stop *handing* the model data, and let it **write code to fetch exactly the slice it needs.** Intermediate results stay in the execution environment — only what the model explicitly returns ever touches the context window.

```python
# Don't: dump 50 files / 200K tokens into context and pray.
context = read_everything(repo)        # ← rots
answer  = model(context, question)

# Do: hand the model tools, let it fetch on demand.
# The 200K never enters the window — only the 200-token answer comes back.
answer  = agent.run(question, tools=[grep, read_lines, run_sql])
```

This isn't hypothetical. Anthropic's own guidance moved this way: present servers as **code APIs** the agent calls, so "intermediate results stay in the execution environment by default, and the agent only sees what is explicitly logged or returned." ([Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp), 2025). Context pressure becomes a *programming* problem, not a compression one.

## The receipts

Every claim above — sourced, with exact figures — lives in **[docs/receipts.md](docs/receipts.md)**: the context-rot research, the compression camp it refutes, and the think-in-code primary sources. Found a paper we're missing or a counterexample that bites? **[Open a PR.](CONTRIBUTING.md)**

## FAQ

**"Isn't this obvious?"** The phenomenon is documented; the *practice* isn't. The whole token-saving industry is built on ignoring it. Full objections, answered: **[docs/faq.md](docs/faq.md)**.

**"So compression is useless?"** No. If compression makes you put *genuinely less* in front of the model, that's subtraction by another name — we're allies. We're against compression-as-**cramming**: shrinking the payload so you can keep over-stuffing the window.

**"Isn't this just RAG?"** RAG is one way to subtract. Think-in-code is a stronger one: the model decides what to pull, when, in the execution environment — instead of you pre-stuffing retrieved chunks back into the prompt (where they rot like everything else).

**"Your self-test is small / it's only Haiku."** True, and we say so — it's a demonstration you can re-run, not a leaderboard. The heavy, peer-reviewed evidence is in the [receipts](docs/receipts.md); our run just shows the same direction on a model you can poke yourself.

## Contribute

This is a living field guide. Add a receipt, a war story, a counterexample, a subtraction pattern that works. See **[CONTRIBUTING.md](CONTRIBUTING.md)**.

---

<div align="center">

**If this reframed how you think about context, ⭐ it — so the next engineer reaching for a compressor finds this first.**

*Stop compressing. Start subtracting.*

</div>

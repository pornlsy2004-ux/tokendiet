# Reddit launch copy

> Reddit rewards substance and honesty, punishes marketing. Lead with the null result and the
> method; link last. Best subs: r/LocalLLaMA, r/MachineLearning ([D] flair).

---

## r/LocalLLaMA

**Title:** I tried to prove context compression hurts accuracy. Controlled test says it doesn't.

I went in convinced that compressing an LLM's context (to save tokens) throws away the specific
details a task depends on. Built a small controlled test to demonstrate it — and it came back null.

Setup: same question, same model (Opus), three context treatments — full document, an Opus
compression (~30–50%, told to preserve key info), and just the one relevant sentence. 13 questions,
each answer a buried exception/override/negation. Blind, exact-match.

- Raw: 85%
- Compressed: 85%
- Subtracted: 85%

Compression neither helped nor hurt — the careful summary kept the details. The only thing that
changed was tokens: subtraction matched full-document accuracy at ~1/8 the tokens (median 28 vs 218).

The takeaway I landed on: compression isn't the lever, *inclusion* is — and the reason that matters is
scale (long context degrades, per Du et al. EMNLP 2025 / Chroma / Lost-in-the-Middle). Writeup + the
reproducible harness (including where subtraction itself failed) here: https://github.com/OWNER/REPO

Genuinely want someone to push the docs long enough that compression finally bites — the harness takes
your own docs.

---

## r/MachineLearning · flair: [D]

**Title:** [D] Controlled test: context compression was a no-op for accuracy; the lever was inclusion, not packing

I ran a small controlled comparison (N=13, Opus, blind exact-match) of three context treatments for a
QA task where each answer is a low-salience detail (exception/override/negation): full document vs.
model-compressed (~30–50%, preserve-info instruction) vs. the single relevant sentence.

Accuracy was identical across all three (85%); only token count differed (median 218 / 108 / 28). So at
least in this short-document regime, lossy-but-careful compression preserved task-relevant detail, and
the gains attributed to "compression" are really just token reduction — which subtraction achieves more
cheaply, *if* you can identify the relevant unit.

I'm framing the actual motivation as the long-context degradation literature (Du et al. 2025; Chroma
context rot; Liu et al. 2024). Curious about results where careful compression *recovers* long-context
accuracy vs. raw, rather than just reducing cost. Harness + data: https://github.com/OWNER/REPO

# Reddit launch copy

> Reddit punishes self-promo. Lead with substance, link last, never use marketing voice.
> Best subs: r/LocalLLaMA (practitioners), r/MachineLearning (use [D] discussion flair).
> Reply with the receipts; let the thesis carry it.

---

## r/LocalLLaMA

**Title:** You can't compress your way out of context rot — subtract instead

I went down a rabbit hole building a prompt/context compressor and came out the other side
convinced compression is the wrong fix. Sharing the reasoning, curious what people running
big local contexts think.

The core problem isn't token count — it's that models degrade as input grows, period:

- Chroma tested 18 frontier models; all get less reliable as context grows.
- EMNLP 2025 (Du et al.): 13.9–85% accuracy drop as input grows *even with perfect retrieval*,
  even with irrelevant tokens masked. It's the length itself, not noise.
- "Lost in the Middle" (TACL 2024): the middle of long context is a dead zone.

So shrinking a long context into a shorter-but-still-long one doesn't escape rot, and lossy
compression tends to eat the exact tokens that matter (negations, conditionals, specific numbers).

The alternative I landed on: **subtract** (put less in front of the model) and **think in code**
(let the agent fetch what it needs at runtime so the bulk never enters the window).

Writeup + sources + counterargument slots here: https://github.com/OWNER/REPO

Genuinely want counterexamples — if your 200K-context setup works great, tell me why.

---

## r/MachineLearning  ·  flair: [D]

**Title:** [D] Compression vs. subtraction for long-context degradation — is "fit more in" the wrong framing?

A lot of recent tooling targets prompt/context *compression* to mitigate cost and long-context
issues. But the degradation literature suggests the problem is input length itself, not just
the presence of irrelevant tokens:

- Du et al. (Findings of EMNLP 2025) report 13.9–85% degradation with input length **despite
  perfect retrieval**, holding even when irrelevant tokens are masked.
- Chroma's "Context Rot" report: non-uniform context use across 18 models.
- Liu et al. (TACL 2024): positional U-shape.

If that holds, lossless compression of *relevant* context shouldn't recover much, and lossy
compression risks removing low-frequency, high-importance tokens. The framing I'm proposing is
"subtraction + runtime code-based retrieval" over "compression." Curious where this is wrong —
especially results showing compression recovering long-context accuracy rather than just cost.

Sources + writeup: https://github.com/OWNER/REPO

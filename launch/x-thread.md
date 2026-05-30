# X / Twitter thread

> Post the chart (assets/context-rot.svg, exported to PNG) on tweet 1 — image-first.
> One clean claim per tweet. Quote-tweet a compression repo to start a (civil) fight.

**1/**
Everyone's racing to compress LLM context to save tokens.

They're optimizing the wrong variable.

You can't compress your way out of context rot. 🧵
[attach: context-rot chart]

**2/**
The bottleneck was never token *count*. It's that models get less reliable as input grows —
no matter how few tokens you've squeezed it into.

More-but-smaller is still more.

**3/**
Receipt #1 — Chroma tested 18 frontier models (GPT-4.1, Claude 4, Gemini 2.5, Qwen3).

Every single one degrades as context grows. They don't use context uniformly.

**4/**
Receipt #2 (this is the one that killed my own compressor):

Accuracy drops 13.9–85% as input grows EVEN WITH PERFECT RETRIEVAL — even with every
irrelevant token masked out. (Du et al., EMNLP 2025)

It's the length itself.

**5/**
Receipt #3 — "Lost in the Middle" (TACL 2024): models attend to the start and end of
context and go blind in the middle.

Compression that shoves your key fact into the middle makes it worse.

**6/**
If zeroing out irrelevant tokens doesn't save you, losslessly compressing the relevant
ones won't either.

And lossy "semantic" compression eats your negations and conditionals — the bits that
flip the answer.

**7/**
The fix isn't smaller context. It's less context.

→ Subtract: justify what you include, not what you cut.
→ Think in code: let the agent fetch what it needs at runtime, so it never enters the window.

**8/**
I wrote it all up — the thesis, the receipts, the patterns — as a field guide.

Stop compressing. Start subtracting.

⭐ if it reframed how you think about context:
https://github.com/OWNER/REPO

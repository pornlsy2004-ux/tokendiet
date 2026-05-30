# X / Twitter thread

> Post the result chart (assets/subtraction-result.svg → PNG) on tweet 1. Lead with the
> honesty; the "I was wrong" hook outperforms a bold claim here.

**1/**
I tried to prove that compressing an LLM's context destroys the details your task needs.

I built the benchmark to show it.

The benchmark proved me wrong. 🧵
[attach: result chart]

**2/**
Setup: same question, same model (Opus), 3 context treatments —
• full document
• Opus compression (~30–50%, told to keep key info)
• just the 1 relevant sentence

13 questions, each answer a buried exception/override/negation.

**3/**
Result: all three scored the SAME accuracy (85%).

Compression didn't hurt. It kept the details. A clean null result.

I was ready to publish "you can't compress your way out." Good thing I ran it first.

**4/**
What actually moved: the token bill.

Subtraction — just the relevant sentence — matched full-document accuracy at ~1/8 the tokens.

Not magic. Just: most of your context is dead weight.

**5/**
The reason to care is scale. Peer-reviewed work (Du et al. EMNLP 2025; Chroma; Lost-in-the-Middle):
long context gets LESS reliable as it grows — even with perfect retrieval, 13.9–85% drops.

A shorter-but-still-huge context still rots. You subtract.

**6/**
And subtraction has a catch I won't hide: it assumes you can FIND the relevant slice.

Cut too far and you drop a bridge the question needs (my benchmark caught this twice).

The scalable fix: let the model fetch what it needs in code.

**7/**
Repo = the field guide + the benchmark that killed my own headline (including its failures).

Same answer. A fraction of the tokens.

⭐ if you'll go delete some context:
https://github.com/OWNER/REPO

# Show HN launch copy

> Post on a US weekday morning (Tue–Thu, ~8–10am ET). The honest "we falsified our own
> hypothesis" angle plays well on HN — lead with it, don't oversell.

## Title (pick one — plain, no hype)

- `Show HN: We tried to prove LLM context compression hurts accuracy. It doesn't.`
- `Show HN: Subtraction – same answer at 1/8 the tokens (and a null result on compression)`

## Body

I set out to show that compressing an LLM's context throws away the details your task depends on —
the "you can't compress your way out of context rot" argument. I built a controlled test to prove it.

It didn't prove it. It falsified it.

Same question, same model (Opus), three context treatments: the full document, an Opus compression
(~30–50%, told to preserve key info), and just the one relevant sentence. 13 questions, each answer a
buried exception/override/negation. Result: all three scored the same accuracy (85%). Compression
neither helped nor hurt — it kept the details.

The thing that actually moved was the token bill. Subtraction — just the relevant sentence — matched
full-document accuracy at about 1/8 the tokens. And the reason to care about that is scale: the
peer-reviewed work (Du et al. EMNLP 2025; Chroma; "Lost in the Middle") shows long contexts get
*less* reliable as they grow, even with perfect retrieval. You don't compress out of that. You include
less.

So the repo is a field guide for that, plus the benchmark that killed my original headline — including
the cases where subtraction itself failed (cut too far and you lose a bridge the question needs). It's
N=13 and reproducible; I'd genuinely like someone to push the docs long enough that compression finally
bites.

Repo: https://github.com/OWNER/REPO

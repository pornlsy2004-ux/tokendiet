# Show HN launch copy

> Post on a US weekday morning (Tue–Thu, ~8–10am ET). Reply to your own thread within
> the first 30 min with the strongest receipt. Engage every comment for the first 2 hours —
> early velocity is what trips GitHub Trending.

## Title (pick one — keep it plain, HN hates hype)

- `Show HN: Subtraction – stop compressing your LLM context, start subtracting it`
- `Show HN: You can't compress your way out of context rot`

## Body

I spent a couple of weeks building a context compressor. Token diet, semantic
minimization, the works — the goal was to cram big inputs into the window without
"losing meaning."

Then I actually read the recent research, and it kind of broke my project.

Du et al. (Findings of EMNLP 2025) show LLM accuracy drops 13.9–85% as input grows
*even with perfect retrieval* — even when every irrelevant token is masked out. Chroma
tested 18 frontier models and they all degrade as context grows. It's not noise you can
squeeze away; it's length itself. So compressing a long context into a shorter-but-still-long
one doesn't fix the rot — and lossy compression quietly eats your negations and conditionals.

So I deleted the compressor and wrote up the opposite approach: subtract (put less in front
of the model) and "think in code" (let the agent fetch what it needs at runtime so it never
hits the window). It's a field guide + the receipts, not a framework.

Curious where this breaks. If you've got a big-context setup that genuinely works, I'd love
a counterexample — there's a PR slot for exactly that.

Link: https://github.com/OWNER/REPO

# Objections, Answered

The honest version. If you came to dunk, start here — odds are it's already addressed.

### "This is obvious / everyone knows context rot."
The *phenomenon* is documented. The *practice* contradicts it daily. An entire genre of tooling exists to help you stuff more into the window, and "just add more context" is still the default reflex. Naming the law, sourcing it, and prescribing *subtract, don't compress* is the contribution — not discovering rot.

### "So compression is useless? That's a strawman."
No, and we say so in the README. If compression makes you put **genuinely less** in front of the model, it *is* subtraction — we're allies. The target is compression-as-**cramming**: shrinking a payload specifically so you can keep over-stuffing the window. LLMLingua-style work is good engineering pointed at the wrong goal.

### "Compression reduces length, and rot is about length — so compression should help."
Sometimes, at the margin. But (1) Du et al. show degradation **even with perfect retrieval and irrelevant tokens masked** — so a still-long context of *relevant* tokens rots anyway; (2) lossy semantic compression destroys exactly the fragile bits — negations, conditionals, the one figure that flips the answer; (3) the compression *mindset* encourages keeping everything "just smaller," when the win is in not including it at all.

### "Isn't this just RAG with extra steps?"
RAG is one way to subtract — good. But pre-fetched chunks stuffed back into the prompt rot like anything else. Think-in-code is stronger: the model pulls what it needs, when it needs it, in the execution environment, and only the result returns. Subtraction at runtime, not at index time.

### "Where's *your* benchmark? Why should I trust a README?"
Because it doesn't ask you to. It stands on peer-reviewed, reproducible work (see [receipts](receipts.md)); the Chroma toolkit runs against your own models. We deliberately don't grade our own homework — that's the dunk-shield, not a gap.

### "This is just a manifesto with no code."
Correct, by design — it's a field guide, not a framework. The thesis is the product. If you want runnable subtraction, the think-in-code section points at the real primary sources.

### "Counterexample: my huge-context setup works great."
Great — open a PR with the setup and numbers. The thesis is falsifiable on purpose. Real counterexamples make this stronger; we want them.

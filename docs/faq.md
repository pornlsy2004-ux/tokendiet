# Objections, Answered

The honest version. We changed our own mind once already (see the last entry) — so come at it.

### "So compression is useless?"
No — it's a **no-op for accuracy**, not a negative. In our controlled test it neither helped nor
hurt; it just made the context shorter. That's fine. The point is narrower than we first thought:
compression isn't the *lever*. It can't beat subtraction on tokens, and it can't undo the rot that a
still-large context causes at scale. Compress if you like — just don't expect it to make the model smarter.

### "Isn't 'just send the relevant part' obvious?"
The principle is. The practice is the opposite — we dump everything in and then compress to fit more.
And there's a real catch we don't hand-wave: **subtraction assumes you can find the relevant slice.**
If you can't, you're back to retrieval — which is exactly why think-in-code (let the model fetch what
it needs at runtime) is the scalable form of subtraction.

### "N=13 is tiny / you wrote the questions."
Correct on both, and we say so in the [benchmark](../benchmark). It's a demonstration you can re-run on
your own docs, not a leaderboard. The claim the repo actually rests on — that *long* context degrades —
is peer-reviewed and large-scale; see the [receipts](receipts.md).

### "Did you just pick a weak compressor to make it fail?"
The opposite — and it's why the result is a *null*, not a win. We compressed with a frontier model
(Opus) told to preserve all important information, at ~30–50%. It kept the details and accuracy didn't
move. Push the documents longer and the compression more aggressive and it will eventually bite; the
harness lets you find that line.

### "Isn't this just RAG?"
RAG is one way to subtract — good. Think-in-code is a stronger one: the model pulls what it needs, when
it needs it, in the execution environment, so the bulk never enters the window. Subtraction at runtime.

### "You changed your thesis halfway through."
Yes. We started believing compression actively destroys the details you need. Our own benchmark
falsified that. We kept the result and dropped the headline — which is the whole spirit of the repo:
if a claim can't survive its own test, it shouldn't be in your prompt either.

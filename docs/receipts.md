# The Receipts

Every claim in the README, sourced. Peer-reviewed and primary sources first.
PRs adding sources welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## The claim this repo rests on: long context degrades

### Context Length Alone Hurts LLM Performance Despite Perfect Retrieval
- **Authors:** Yufeng Du, Minyang Tian, Srikanth Ronanki, Subendhu Rongali, Sravan Bodapati, Aram Galstyan, Azton Wells, Roy Schwartz, Eliu A. Huerta, Hao Peng
- **Venue:** Findings of EMNLP 2025 (arXiv:2510.05381)
- **Link:** https://arxiv.org/abs/2510.05381
- **TL;DR:** The strongest result for subtraction. Performance degrades **13.9%–85%** as input length grows **even when retrieval is perfect** — even when irrelevant tokens are masked out. Concrete drops for Llama-3.1-8B at ~30K tokens: **Variable Summation 96% → 11%**, **HumanEval 57.3% → 9.7%**, **MMLU 63.2% → 39%**, **GSM8K 87.8% → 75.5%**. The damage is *length itself*. You can't compress a still-long context out of this; you subtract.

### Context Rot: How Increasing Input Tokens Impacts LLM Performance
- **Authors:** Kelly Hong, Anton Troynikov, Jeff Huber (Chroma) · **Date:** 14 July 2025
- **Link:** https://research.trychroma.com/context-rot · toolkit: https://github.com/chroma-core/context-rot
- **TL;DR:** 18 frontier models (GPT-4.1, Claude 4, Gemini 2.5, Qwen3) all grow less reliable as input length grows; context is not used uniformly. On LongMemEval, models score far higher on focused ~300-token prompts than on the ~113K-token full versions of the same task.

### Lost in the Middle: How Language Models Use Long Contexts
- **Authors:** Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang
- **Venue:** TACL 2024, vol. 12, pp. 157–173 · **Link:** https://aclanthology.org/2024.tacl-1.9/
- **TL;DR:** In multi-document QA, accuracy is highest when the answer sits at the very start (~75%) or end (~72%) of the context and sags in the middle (~55%) — a U-shaped curve, a 20+ point swing from position alone.

---

## Our own run — what it did and didn't show

### Subtraction controlled test (this repo)
- **Model:** Claude Opus 4.8 (also the compressor). **Code + data:** [`/benchmark`](../benchmark) · [`results/controlled.json`](../benchmark/results/controlled.json)
- **TL;DR:** 13 questions, each answer a buried detail. Raw / compressed / subtracted contexts **all scored 85%** — a **null result on compression** (it neither helped nor hurt). Subtraction matched raw accuracy at **~1/8 the tokens** (median 28 vs 218). Honest failure modes recorded: compression once flipped a kept fact by stripping emphasis; over-subtraction twice cut a needed bridge. Small (N=13) and reproducible by design — it demonstrates the token win and falsifies the stronger "compression destroys data" claim we started with.

---

## The compression toolkit (not the lever)

> Listed for reference. Good engineering — it just isn't where accuracy is won or lost.

- **LLMLingua / LongLLMLingua / LLMLingua-2** (Jiang et al., Microsoft — EMNLP 2023; arXiv:2310.05736, 2310.06839, 2403.12968): coarse-to-fine prompt compression, up to ~20x at "minimal" loss.
- **500xCompressor** (arXiv:2408.03094): compresses prompts into a few special tokens.
- **token-compressor**, **caveman-compression**, **MemChinesePalace**: the viral "save tokens" tier — instructive as concept-as-product, thin on substance.

---

## The cure — think in code

### Code execution with MCP: building more efficient AI agents
- **Author:** Anthropic (Engineering) · **Date:** November 2025 · **Link:** https://www.anthropic.com/engineering/code-execution-with-mcp
- **TL;DR:** Instead of loading every tool definition and piping intermediate results through the context window, present MCP servers as **code APIs** the agent calls. Intermediate results "stay in the execution environment by default; the agent only sees what is explicitly logged or returned." Subtraction, automated.

---

*Have a primary source — for or against? Open a PR. We especially want counterexamples.*

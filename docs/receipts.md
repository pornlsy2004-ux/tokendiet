# The Receipts

Every claim in the README, sourced. Primary and peer-reviewed sources first.
Format: **claim → finding → exact figure → link.** PRs adding sources welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Context rot — the law

### Context Rot: How Increasing Input Tokens Impacts LLM Performance
- **Authors:** Kelly Hong, Anton Troynikov, Jeff Huber (Chroma)
- **Date:** 14 July 2025
- **Link:** https://research.trychroma.com/context-rot · reproducible toolkit: https://github.com/chroma-core/context-rot
- **TL;DR:** Evaluates **18** state-of-the-art LLMs (GPT-4.1, Claude 4, Gemini 2.5, Qwen3, …). All of them use their context *non-uniformly*: as input length grows, performance becomes increasingly unreliable. On LongMemEval, models score far higher on focused ~300-token prompts than on the full ~113K-token versions of the *same* task. The decline is not about running out of window.

### Context Length Alone Hurts LLM Performance Despite Perfect Retrieval
- **Authors:** Yufeng Du, Minyang Tian, Srikanth Ronanki, Subendhu Rongali, Sravan Bodapati, Aram Galstyan, Azton Wells, Roy Schwartz, Eliu A. Huerta, Hao Peng
- **Venue:** Findings of EMNLP 2025 (arXiv:2510.05381)
- **Link:** https://arxiv.org/abs/2510.05381
- **TL;DR:** The cleanest refutation of the compression thesis. Performance degrades **13.9%–85%** as input length grows **even when retrieval is perfect** — and even when irrelevant tokens are replaced by whitespace or masked, so the model attends only to relevant tokens. Concrete drops for Llama-3.1-8B at ~30K tokens (essay distraction): **Variable Summation 96% → 11%**, **HumanEval 57.3% → 9.7%**, **MMLU 63.2% → 39%**, **GSM8K 87.8% → 75.5%**. The damage comes from *length itself*, not noise.

### Lost in the Middle: How Language Models Use Long Contexts
- **Authors:** Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang
- **Venue:** TACL 2024, vol. 12, pp. 157–173
- **Link:** https://aclanthology.org/2024.tacl-1.9/
- **TL;DR:** The foundational result. In multi-document QA, accuracy is highest when the answer sits at the very start (**~75%**) or end (**~72%**) of the context and sags in the middle (**~55%**) — a U-shaped curve, a 20+ point swing from position alone. Compression that reshuffles content into the dead zone makes things *worse*.

---

## Our own run — the self-test

### Subtraction self-test (this repo)
- **Model under test:** Claude Haiku 4.5, fresh context per trial.
- **Code + data:** [`/benchmark`](../benchmark) · raw results: [`/benchmark/results/selftest.json`](../benchmark/results/selftest.json)
- **TL;DR:** Hide one fact among *N* near-identical lines, then ask the model to (a) retrieve one code and (b) count how many codes are even. **Retrieval stayed at 100%** from 50 to 1400 lines. **Counting accuracy (±1) collapsed: 67% → 33% → 0% → 0% → 0%.** Past ~500 items the model stopped counting and emitted exactly N/2 (250 / 450 / 700) — confidently wrong. Small and reproducible by design; it demonstrates the same direction as the peer-reviewed work on a model you can poke yourself.

---

## The compression camp — what we argue against

> Not "useless" — but treating the symptom. Listed so you can judge for yourself.

### The LLMLingua family
- **LLMLingua** (Jiang et al., Microsoft — EMNLP 2023, arXiv:2310.05736), **LongLLMLingua** (arXiv:2310.06839), **LLMLingua-2** (arXiv:2403.12968).
- **TL;DR:** Coarse-to-fine prompt compression that drops low-information tokens, reporting up to ~20x compression at "minimal" loss. Good engineering — framed as "fit more in," the framing this repo pushes back on.

### 500xCompressor
- arXiv:2408.03094. **TL;DR:** Compresses long prompts into a handful of special tokens. Impressive ratios; same trap — the goal is cramming, not subtracting.

### The gimmick tier (instructive, viral)
- **token-compressor** (base76-research-lab) — rewrites prompts to "semantic minimum," 40–60% reduction, shipped as an MCP server.
- **caveman-compression** (wilpel) — strips "predictable grammar," keeping only unpredictable/factual tokens; ~50% fewer tokens.
- **MemChinesePalace** (Chandler-Sun) — compresses agent memory into Classical Chinese for density; the author labels it *"not a serious project"* — and it still spread. The purest example of concept-as-product: the idea travels, the substance is thin.

---

## The cure — think in code

### Code execution with MCP: building more efficient AI agents
- **Author:** Anthropic (Engineering) · **Date:** November 2025
- **Link:** https://www.anthropic.com/engineering/code-execution-with-mcp
- **TL;DR:** Instead of loading every tool definition and piping intermediate results through the context window, present MCP servers as **code APIs** the agent calls. Intermediate results "stay in the execution environment by default; the agent only sees what is explicitly logged or returned." Fewer tokens, less rot, lower latency — subtraction, automated.

---

*Have a primary source — for or against? Open a PR. We especially want counterexamples that test the thesis.*

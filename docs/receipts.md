# The Receipts

Every claim in the README, sourced. Primary and peer-reviewed sources first.
Format: **Claim → finding → exact figure → link.** PRs adding sources welcome — see [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Context rot — the law

### Context Rot: How Increasing Input Tokens Impacts LLM Performance
- **Authors:** Kelly Hong, Anton Troynikov, Jeff Huber (Chroma)
- **Date:** 14 July 2025
- **Link:** https://research.trychroma.com/context-rot · reproducible toolkit: https://github.com/chroma-core/context-rot
- **TL;DR:** Evaluates 18 state-of-the-art LLMs (GPT-4.1, Claude 4, Gemini 2.5, Qwen3, …). All of them use their context *non-uniformly*: as input length grows, performance becomes increasingly unreliable — even on tasks that should be trivial at short lengths. The decline is not about running out of window; it's about what long inputs do to attention.

### Context Length Alone Hurts LLM Performance Despite Perfect Retrieval
- **Authors:** Yufeng Du, Minyang Tian, Srikanth Ronanki, Subendhu Rongali, Sravan Bodapati, Aram Galstyan, Azton Wells, Roy Schwartz, Eliu A. Huerta, Hao Peng
- **Venue:** Findings of EMNLP 2025 (arXiv:2510.05381)
- **Link:** https://arxiv.org/abs/2510.05381
- **TL;DR:** The cleanest refutation of the compression thesis. Performance degrades **13.9%–85%** as input length grows **even when retrieval is perfect** — and even when every irrelevant token is replaced with whitespace or masked, so the model only attends to relevant tokens. The damage comes from *length itself*, not noise. If zeroing out irrelevant tokens doesn't save you, compressing relevant ones won't either.

### Lost in the Middle: How Language Models Use Long Contexts
- **Authors:** Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang
- **Venue:** TACL 2024, vol. 12, pp. 157–173
- **Link:** https://aclanthology.org/2024.tacl-1.9/
- **TL;DR:** The foundational result. Performance is highest when relevant information sits at the very beginning or end of the input and drops sharply when it's in the middle — a U-shaped curve. Position, not just presence, decides whether the model can use what you gave it. Compression that reshuffles content into the dead zone makes things *worse*.

---

## The compression camp — what we're arguing against

> Not "useless" — but treating the symptom. Listed so you can judge for yourself.

### The LLMLingua family
- **LLMLingua** (Jiang et al., Microsoft — EMNLP 2023, arXiv:2310.05736), **LongLLMLingua** (arXiv:2310.06839), **LLMLingua-2** (arXiv:2403.12968).
- **TL;DR:** Coarse-to-fine prompt compression that drops low-information tokens, with reported compression up to ~20x at "minimal" performance loss. Genuinely useful engineering — but framed as "fit more in," which is the framing this repo pushes back on.

### 500xCompressor
- arXiv:2408.03094. **TL;DR:** Compresses long natural-language prompts into a handful of special tokens. Impressive ratios; same philosophical trap — the goal is cramming, not subtracting.

### The gimmick tier (instructive, viral)
- **token-compressor** (base76-research-lab) — LLM rewrites prompts to "semantic minimum," 40–60% reduction, shipped as an MCP server.
- **caveman-compression** (wilpel) — strips "predictable grammar," keeping only unpredictable/factual tokens; ~50% fewer tokens.
- **MemChinesePalace** (Chandler-Sun) — compresses agent memory into Classical Chinese for maximum density (the author labels it *"not a serious project"* — and yet it spread). The purest example of *concept-as-product*: the idea travels, the substance is thin.

---

## The cure — think in code

### Code execution with MCP: building more efficient AI agents
- **Author:** Anthropic (Engineering)
- **Date:** November 2025
- **Link:** https://www.anthropic.com/engineering/code-execution-with-mcp
- **TL;DR:** Instead of loading every tool definition and piping intermediate results through the context window, present MCP servers as **code APIs** the agent calls. Intermediate results "stay in the execution environment by default; the agent only sees what is explicitly logged or returned." Fewer tokens, less rot, lower latency — context pressure reframed as a programming problem. This is subtraction, automated.

---

*Have a primary source — for or against? Open a PR. We especially want counterexamples that test the thesis.*

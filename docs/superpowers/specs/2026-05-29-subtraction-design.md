# Subtraction — 设计 Spec

- **日期**: 2026-05-29
- **状态**: 已批准(用户全权委托执行,放弃逐项评审)
- **一句话**: 一个"概念即产品"的纯内容仓库,用反直觉、有论文撑腰的论断蹭 context-engineering 热浪,目标是快速涨 star / 冲一次病毒尖峰。

## 1. 目标与成功指标

- **核心目标**: 纯冲 GitHub star,体验一次病毒式传播(用户明确诉求)。
- **成功指标**: star 增速 / 进 GitHub Trending / 上 Hacker News 首页 / 多渠道转发量。
- **非目标**: 长期维护、做成产品/SaaS、技术深度本身。这是一张"病毒彩票",下注最小、上限最高。

## 2. 策略定位

- **品类**: 纯内容 / 策展(历史 ROI 冠军:build-your-own-x 503k、awesome 469k、public-apis 436k、free-programming-books 388k、Karpathy 65 行 CLAUDE.md ~10 万星)。零代码、零维护。
- **原型**: 「反直觉概念钩子」(concept-as-product)= 反直觉论断 + 极轻实现 + 宏大叙事 + 可截图记忆点。
- **爆款铁律对照**: 反直觉论断 ✓ / 论文撑腰防 dunk ✓ / 可截图记忆点 ✓ / 5 分钟读完 ✓ / 踩中最热 context+agent 浪 ✓ / 公开树敌引讨论 ✓ / 工程极轻 ✓。

## 3. 论断(产品灵魂)

一句话武器: **"Stop compressing context. Start subtracting it."**

三段式叙事:
- **树敌**: 所有人都在*压缩* context(LLMLingua、token-compressor、caveman、文言文梗)——在优化错的变量。
- **立论(有论文)**: 瓶颈不是 token 数,是 **context rot**;压缩压不掉"烂"。
- **开方**: **减法**(喂得更少) + **think-in-code**(让 agent 写小脚本现取所需,而非灌文件)。

## 4. 范围(Tier 1,YAGNI)

**做**:
- `README.md` — 宣言 + 一张 context-rot 曲线图 + "证据表"(receipts)。
- `docs/` — 每篇关键论文一段 TL;DR(加深"收藏即 star"的书签价值)。
- `launch/` — Show HN / X 长推 / Reddit 三份发射文案(发射即产品的一部分)。
- `LICENSE`(MIT/CC)、`.gitignore`、`CONTRIBUTING`(让人 PR 加论文 → 社区涨星引擎)。

**不做(明确砍掉)**: 自己跑的基准、CLI/SDK/工具、web 面板、任何需要持续维护的东西。若日后爆了再考虑 Tier 2(补一个可运行基准)。

## 5. 仓库结构

```
README.md          # 宣言 + 图 + 证据表(核心产品)
assets/
  context-rot.svg  # 传播记忆点:越喂越笨曲线(标注来源)
docs/
  receipts.md      # 每篇论文 TL;DR + 准确引用
  faq.md           # 预先拆掉 dunk(“这不早知道了”/“方法论”)
launch/
  show-hn.md       # Show HN 标题 + 正文
  x-thread.md      # X 长推
  reddit.md        # r/LocalLLaMA / r/MachineLearning 版本
CONTRIBUTING.md
LICENSE
.gitignore
```

## 6. README 结构(写作要点)

1. **Hook** — 一行论断 + 那张图,首屏即记忆点。
2. **The wrong fix** — 点名压缩大军,指出它优化错了变量。
3. **The law: context rot** — 摆证据(带表/引用):Chroma 18 模型全退化;即便 100% 检索命中仍掉 13.9–85%;lost-in-the-middle 中段掉 30%+。
4. **The cure** — 减法原则 + think-in-code 范式(给可操作清单,而非空喊)。
5. **The receipts** — 证据表(论文/基准/工具,准确引用)。
6. **FAQ** — 预拆 dunk。
7. **Contribute** — 邀请补论文/反例 → 社区涨星。

## 7. 防 dunk(风险与对策)

- *"这不早就知道了"* → 新意在**①把分散研究策展成 canonical 单仓库 ②反压缩旗帜 ③think-in-code 药方**;且承认现象非原创、明确引用。
- *方法论被攻击* → 只引同行评审/一手来源,数字逐条标注出处;图标注"基于已发表数据,示意"。
- *"光说不练"* → 本就是"立场 + 证据档案",公认爆款格式;FAQ 正面回应。
- *彩票性质* → 中位数平淡,无法保证炸;只最大化赔率(钩子 + 防 dunk + 集中发射)。

## 8. 发射方案(part of product)

- **叙事**(个人故事多拿 3 倍赞): "我花几周做了个 context 压缩器,一测根本没用——下面是真正有用的。"
- **渠道**(同日集中引爆触发 Trending): Show HN + r/LocalLLaMA + r/MachineLearning + X 长推 + 相关 Discord。
- **时机**: 美国工作日早晨。
- **持续**: 每周 1 帖(换新模型重测 / 加新论文)养复利。

## 9. 用户需亲自完成(自动化替代不了)

1. 创建 GitHub 仓库并 `git push`(本地仓库我会备好)。
2. 按 `launch/` 文案在各渠道发帖,并在评论区互动。
3. 决定最终仓库名(默认 `Subtraction`)。

## 10. 待定 / 延后

- 仓库名最终确认(默认 `Subtraction`)。
- Tier 2(可运行基准)——仅在初步爆了之后再投入。

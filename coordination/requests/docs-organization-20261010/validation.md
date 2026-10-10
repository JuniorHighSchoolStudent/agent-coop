# 候选验证与作者边界

2026-10-10，Codex 实际执行。基线 a9bb474；候选 SHA 由后继评审绑定（本文件属于待冻结输入）。

- CodeBuddy / deepseek-v4-pro 新会话 `agent-coop-docs-organization-executor-20261010` 已正常退出，15 次工具调用、错误 0，num_turns 42；实际修改 AGENTS/README，交付原文见 [implementation-r1.txt](implementation-r1.txt)。num_turns 是 CLI 历史条目计数，不证明 max-turns 的硬预算实效；使用 max-turns 20，没有放宽权限。
- Codex 共创修正：目录权威表移除状态副本；明确草稿/冻结候选/原始回执/可维护结果入口的不同生命周期；明确替代指针方向、历史不改写、命名入口例外、HTML 与文本链接检查范围；README 改为直达历史入口和文档规范。实现者原交付只是此前作者快照，不作为最终版本通过证据；两位作者均不计独立票。
- 复用临时 verify-docs.ps1：96 个相对 Markdown 文件链接有效；design 验收 1–54 连续唯一；`git diff --check` 通过。该脚本不检查远程页面可用性或标题锚点。
- 新增 README 两个锚点手工对照精确标题：AGENTS 的「文档组织」、roadmap 的「历史交付入口」均存在且唯一，无重复标题后缀。
- 图集 HTML 的 21 个本地 href/src 及页内 id 目标检查通过；图文件与 SVG 未改动，之前图集视觉证据沿原版本，不声称本次重渲染。当前 design、runtime-adapters、diagrams、examples、CLAUDE 相对基线零差异。
- 阅读路径逐条核对：README→AGENTS；README→design；README→roadmap；README→runtime-adapters；README→配置草案；README→图集；README→roadmap 历史→请求/结果→评审原件；README→导入来源。bootstrap 历史入口经 request 显式指向 result-r2，不假定 result.md 最新。
- 目录责任覆盖 10 项既有路径；未新增第二规范文件、状态台账、模板、空目录或代码。公众来源已在线核对，研究记录保留 URL/核对日期/本地取舍，独立评审受只读工具限制不能冒充自行联网。

尚未进行本候选的两席正式评审/监督；本文件只陈述作者执行的测量，不是接收结论。无产品测试入口，未运行产品测试、未配置 CI、未开始 P0。

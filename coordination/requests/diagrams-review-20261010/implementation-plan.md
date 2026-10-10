# 图集修订实施计划

> 执行方式：沿 superpowers:subagent-driven-development 分离实现与独立复核，使用 roadmap 已绑定的真实运行时。用户在上一轮退回结论后要求“继续使用多agent 协作开发”，授权本次修订与验证；不重新发明产品合同。

目标：修复 [首轮结果](result-r1.md) B1–B3，并改善原图阅读入口。技术：继续手写 SVG + 无脚本 HTML，不新增依赖、生成器、调度器或台账。复用已有五张图、index、临时 Playwright 渲染与文档检查器；当前仍是文档切片，不绕过未完成的 P0。

## 范围与任务

- [ ] CodeBuddy/deepseek-v4-pro 修改 `docs/diagrams/03-request-to-dispatch.svg`：将授权 gate 和必要 workflow 评审 gate 串在 apply 前，条件可同时适用；已有授权常规任务无需重复审批。明确所有必需席位通过（至少两个独立非作者）、无 blocking、确定性校验和具权限接收。待批准/待评审/失败不得沿成功线进入 apply；校验失败与拒绝有具名出口。图文一致，避免箭头穿字。
- [ ] 同一实现者修改 `docs/diagrams/04-execution-and-handshake.svg`：offered 与 acknowledged 均连接 cancelled/expired；超时不证明进程停止、不由 Scheduler 代评审接受。保持现有 epoch/fencing/outbox 条件。
- [ ] 同一实现者修改 `docs/diagrams/01-architecture-overview.svg`：区分执行回传、coordinator 向证据栏的发布与只读引用，图例和箭头对应；入口品牌与正文对齐，CodeBuddy 不冒充已定义薄插件。SQLite 仍为建议、产品仍未实现。
- [ ] 同一实现者修改 `docs/diagrams/index.html`：为五图添加可键盘访问的原图链接（例如 `<a href="./01-architecture-overview.svg">打开原图 / 放大查看</a>`），可使用浏览器原生缩放，保留 alt、响应式与无脚本。图 3 摘要与修正后流程一致。不改图 2/5，不修改正文来迁就图。
- [ ] Codex 维护本请求与 roadmap 当前入口；首轮 result 原文归档为 result-r1.md，原始两票和监督不改。已完成角色/经验合同移到历史入口，B1–B3 直至新版本复核前仍未闭合。
- [ ] Codex 检查差异与 SVG XML、Markdown/HTML 本地链接、桌面及窄屏渲染，实际点击五个原图入口并核查箭头/文字。复用前轮临时脚本调整 root；无产品测试入口，不为此创建应用测试框架。冻结新 Git 候选及输入清单。
- [ ] CodeBuddy/glm-5.3 与 kimi-k3-2 新独立会话审核同一候选，均逐项 D1–D8 与 B1–B3 闭合；不得阅读彼此本轮意见。共享确定性验证证据不替代其独立判断，不能冒充独立渲染或重算哈希。
- [ ] 原生 Kimi Code 新只读会话监督实际实现、版本绑定、两票、修正闭环与状态。Codex 仅在全部必需意见无 blocking 后接收；本地提交保存交付，合入与否单独举证，不自动推送。

写入边界：实现者只改上述四个图集文件；Codex 只改协调记录和 roadmap，并承担必要集成修复（如发生必须公开作者身份、使旧票失效）。各文件仍只有一个维护入口。CodeBuddy 并发≤2，每次 max-turns 20；本次续作最多两轮修订/复审，超限保留具名阻断。原生 Kimi 并发1、每次十分钟人工看护；无 CLI 硬限字段不伪造。Claude Code 继续暂停。

验收：B1–B3 均有新版本原件与独立闭合意见；失败/等待无放行捷径，超时出口完整，读写图例自洽，五图可原尺寸打开；main 的54项合同不丢失；无产品实现/测试/合入的虚假声称。

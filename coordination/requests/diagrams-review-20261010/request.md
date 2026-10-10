# Diagrams 提交流程审核

用户最初要求审核最近 diagrams 提交；首轮仅审查与记录，不修改图、不合入、不运行产品。随后用户要求“继续使用多agent 协作开发”，授权修订。续作范围和步骤见 [implementation-plan.md](implementation-plan.md)，唯一当前状态见 [result.md](result.md)，首轮结论已归档 [result-r1.md](result-r1.md)。Codex 为派发与集成者，不占独立票；沿 roadmap 已有团队与预算，不创建新规则。

## 首轮固定输入（历史）

- 候选：`63ef2300ebf0d7873b75f0bddd095de7f656c4df`；原基线：`d38bdca9ca137a1d18b801f02e7088ffd45e568a`。
- 当前已接收合同基线：main `cb0793d5d703d2a21d21f18c01a2fc68e1a05814`。工作树根为候选原文；`.review-inputs/current-main/` 是该 main 的只读临时快照，不提交、不形成新 owner。
- 范围：README、design 的导航增量，五份 SVG 与 index.html；候选 AGENTS/design/roadmap/runtime-adapters 和当前 main 合同作为参照。旧基线本身不是缺陷，须指出实际冲突与影响。
- Git 作者元数据不能证明实际使用哪个 agent；作者 runtime/session unknown。两位 reviewer 均为本次新建只读会话，与作者无重叠。

## 首轮步骤及沿用覆盖

1. Codex 固定候选、检查差异与原件，核查图的渲染、链接和静态结构。
2. CodeBuddy glm-5.3 与 kimi-k3-2 独立只读审核，不读彼此意见；并发最多 2，每次 max-turns 20，本请求最多两轮，不把 num_turns 历史条目数当循环次数。
3. 两位均覆盖下表，逐项 PASS/BLOCK/有依据的 N/A，定位文件/行与合同出处；不凭工具退出成功判通过。
4. Kimi Code 独立监督输入、独立性、覆盖、原始意见、处置与状态；并发 1，每次十分钟人工看护，实际模型未暴露则 unknown。
5. Codex 汇总实际发现。存在阻断则保持 changes_requested，不能自行关闭独立意见；本次不代作者修改或合入。

| ID | 必需覆盖 |
|---|---|
| D1 | SSOT：图为辅助，正文权威；设计/实现边界，来源可追溯，无重复规则 owner |
| D2 | 总体架构：Scheduler 单写/派发权，三类 adapter，角色/runtime/provider 分离 |
| D3 | 需求流程：授权、设计评审、校验、apply、安全点及拒绝分支，不绕过必需评审 |
| D4 | attempt/握手：精确身份版本、ack/accepted/delivered 区分、异常恢复与发布条件 |
| D5 | 知识与改进：原项目权威、评审/评测/激活边界，不能扩大权限 |
| D6 | 当前 main 兼容：暂停/恢复、状态维护、阶段角色/触发/ABM/Jev；非穷尽图不强求画全部内容 |
| D7 | 可读性/可访问性/导航：SVG/HTML 结构、链接、图形表达；未实际渲染者明确限制 |
| D8 | 流程证据：范围/输入/独立性/未决项/当前状态准确；无产品测试或已合入的虚假声称 |

## 状态入口

唯一当前审核结论见 [result.md](result.md)。请求与回执不改产品合同；续作图修订使用新的候选及输入清单，旧票失效，沿用 D1–D8 并逐项核对 B1–B3 关闭条件。两组新独立评审与新 Kimi Code 监督均不得由实现者兼任。原始运行流在本机临时目录，不提交私有会话日志。

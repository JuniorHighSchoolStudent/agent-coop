# 文档组织：社区实践与本仓取舍

核对日期：2026-10-10。公开来源由 Codex 在线阅读；下列为摘要和本地推导，不是上游全文或官方对本仓的认可。

| 原始来源 | 采纳与落点 | 未采纳与理由 |
|---|---|---|
| [Diátaxis 五分钟入门](https://www.diataxis.fr/start-here/) | 用教程（学习）、操作指南（任务）、参考（准确合同）、解释（原因）区分读者需求，在 AGENTS 明确目的；README 导航按读者任务描述 | 不把开发治理、任务状态和审计原件硬塞进四类产品文档 |
| [Diátaxis 使用方式](https://diataxis.fr/how-to-use-diataxis/) | 渐进整理；有实际内容与需求才增加类型目录 | 不搭四个空目录，不因分类大规模搬迁稳定设计 |
| [GitHub README 文档](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes) | README 提供用途和起步入口；仓内采用相对链接并检查标题锚点 | 不迁往外部 Wiki；同仓版本评审更符合本仓证据需求 |
| [Michael Nygard：Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | 保留背景、决策、状态、后果和替代关系，以未来维护者能理解为准 | 不另开 ADR 编号/目录/审批链；已有 coordination/requests 可承载同一决策证据，生效规则仍回到相应 owner |

本地经验：此前 ABM 导航审计表明“链接/投影机械有效”和“人或 agent 能快速找到权威”需要分别验证；这里仅吸收该方法，不导入其业务台账、脚本或历史通过结论。当前仓库已核验入口是 AGENTS、README、design、roadmap、runtime-adapters、diagrams、examples 和 coordination/requests。

本轮选择 AGENTS 增加一节组织规范，README 补齐按任务导航，保留 design 的章节合同及稳定引用。拆分要由独立职责、读者任务或维护冲突驱动；文档不套用源码行数硬阈值。设计文档尚未实现，示例非权威，图集辅助阅读，任务原件是历史证据，这些差别必须在入口可见。

# Agent Coop

面向实际项目的轻量多 Agent 协作工具，通过可配置角色、可评审工作流和插件适配器，统一调度、监控、交接与经验积累。

> 下文描述完整产品目标。隔离样例已有实现；准确候选、接收、主线与live阻断以[实施路线](docs/roadmap.md)指向的当前结果为准，不等于完整平台交付。

用户描述需求，集成者与设计者结合项目事实、已有模板、社区实践和经验推荐 workflow；多个独立审核者通过后发布，由 Scheduler 按依赖、预算与资源约束派发。Web 展示流程、握手、阻断和知识改进，项目目录保存可人工审阅的证据。

## 产品组成

- **角色配置**：用户定义职责、能力与独立性，分别绑定 agent、模型和权限。
- **工作流模板**：推荐、设计、评审、发布与执行都有版本；支持增量插入节点。
- **项目适配器**：引用项目已有任务、规则、验证和证据，保持原项目权威。
- **Scheduler**：持久派发、资源互斥、事件/定时触发、取消和崩溃恢复。
- **状态监控**：Web、CLI/MCP 与项目文件使用同一状态来源。
- **知识与改进**：积累踩坑和有效经验，检索复用，经过独立评测再激活改进。

## 推荐执行者与扩展

实现/执行角色推荐 **CodeBuddy + DeepSeek V4-Pro**，模型 ID 为 `deepseek-v4-pro`。这是一项可替换的预设，不是硬编码执行器，也不是性能或成本排名。

用户可以按角色选择 Codex Desktop/CLI、Claude Code CLI、CodeBuddy、Kimi Code，或通过 RuntimeAdapter 接入 OpenCode 等 agent。同一 agent 可以配置多个模型 profile；角色、agent、模型、provider 和项目互不绑定。Kimi 的监督职责也可以替换。

评审团队推荐加入 **CodeBuddy + `glm-5.3`** 与 **CodeBuddy + `kimi-k3-2`** 两组独立会话，分别覆盖项目适配和执行可靠性，并对高风险交叉项复核。具体 ID 已经用户确认；这项职责分工是可调整建议，尚无本项目质量评测。多模型降低共同盲点风险，完整性仍需检查清单、证据覆盖和阻断闭环验证，不承诺零遗漏。

工具设计包含配置清单发现与推荐：从各 agent 的受支持入口获取可选模型、参数和能力，结合角色需求、项目约束及已有评测给出配置建议，显示依据与未知项。用户确认后建立版本化绑定；不会因清单刷新静默替换正在工作的模型。

| 接入目标 | 当前证据 | 本仓实现 |
|---|---|---|
| CodeBuddy / Kimi Code | 帮助调研、固定样例及受限实际调用证据 | 固定样例边界见[当前切片](docs/roadmap.md)，通用适配合同仍待实现 |
| Codex CLI / Claude Code | 前期本机帮助与相关协议调研 | 通用接入未实现，开发团队约束见实施路线 |
| Codex Desktop | 设计为薄插件与人工协作入口 | 未实现 |
| OpenCode / 用户扩展 agent | 扩展合同及官方 CLI 资料 | 未实现、未做本机验证 |

具体见 [运行时接入约定](docs/runtime-adapters.md) 和 [推荐配置草案](examples/executor-profile.proposed.yaml)。配置草案尚无解析器，不会自动启动 agent。

## 工程规范与当前开发安排

工程开发规则（SSOT、SOLID 审查项、代码/函数规模、质量门禁、文档组织）以 [AGENTS.md](AGENTS.md) 为唯一维护入口，本文件不复制阈值。当前开发团队角色绑定、临时调用上限与治理文档切片步骤见 [docs/roadmap.md](docs/roadmap.md)。

## 按任务导航

新读者按目的进入，无需逐文件阅读：

| 我想…… | 入口 |
|---|---|
| 了解产品目标与组成 | 上文「产品组成」与 [完整设计](docs/design.md) |
| 看当前进度、团队角色与下一步 | [实施路线](docs/roadmap.md) |
| 按工程规则参与开发 | [AGENTS.md](AGENTS.md)；Claude 会话见 [CLAUDE.md](CLAUDE.md) |
| 新增、拆分或归档文档 | [文档组织规范](AGENTS.md#文档组织) |
| 接入或核对运行时、模型与适配器 | [运行时接入约定](docs/runtime-adapters.md) |
| 看配置例子（草案，非权威） | [拟议配置](examples/executor-profile.proposed.yaml) |
| 看图辅助理解 | [图表索引](docs/diagrams/index.html) |
| 溯源决策、评审与监督证据 | [历史交付入口](docs/roadmap.md#历史交付入口)，再进入对应请求与有效结果 |
| 溯源调研与导入来源 | [调研导入记录](docs/research/design-import.json) |

本仓独立于 ABM 和 trading_system；它们是实践来源与未来项目适配对象。项目仓库为 [JuniorHighSchoolStudent/agent-coop](https://github.com/JuniorHighSchoolStudent/agent-coop)。实现成熟度由当前切片入口维护；尚未发布包或选择开源许可证。

用于仓库 About 的英文描述：

> A lightweight, project-aware multi-agent collaboration tool with configurable roles, reviewed workflows, pluggable runtimes, scheduling, observability, and reusable knowledge.

---
status: draft
owner: agent-coop-maintainers
created_at: 2026-10-10
implementation_status: not_started
---

# Agent Coop 产品与协作设计

## 1. 决策摘要

建议建设一个本机协作工具，暂称 `agent-coop`：小型持久调度内核负责执行身份、资源互斥和恢复，CLI/MCP 提供统一操作面，Codex 与 Claude 插件提供入口。角色、运行时、模型配置、项目工作流分别声明。首版接入目标覆盖用户当前组合：Codex Desktop/CLI、Claude Code CLI、CodeBuddy CLI、Kimi Code CLI；最终实现/执行者推荐 CodeBuddy + DeepSeek V4-Pro（model ID `deepseek-v4-pro`），这是可替换的用户推荐预设。CodeBuddy 可用不同模型配置承载不同角色，Kimi Code 默认承担独立监督者。OpenCode 及其他 agent 通过相同 RuntimeAdapter 扩展，不进入内核固定枚举。运行时能力可复用，监督职责单独建模。

用户操作尽量收敛为“选择项目模板、定义角色及绑定、启动团队”。模板承接依赖、交付物和完成判据；仅有角色 prompt 无法推导哪些任务可并行、谁能接收、何时结束。

产品明确由五部分组成：**角色配置 + 工作流模板 + 项目适配器 + Scheduler + 状态监控**。Scheduler 和状态监控均为首版必需能力；角色执行、运行监控、Kimi 语义监督分别承担不同职责。

五部分之上增加横向的**知识积累与受控改进闭环**：记录使用问题、踩坑、人工纠偏及有效经验，按适用范围检索，再将优化建议作为普通 ChangeProposal 经评测和版本激活生效。首版不训练模型权重，也不承诺迭代必然提升；知识积累、经验验证和行为变更分别有状态与证据。

**工作流自身可由多角色协作推荐、设计、评审及发布**：集成者整理实际项目约束，设计者结合可复用模板、社区资料和适用经验提出候选，多个独立审核者通过后才具备激活资格。该过程也是使用同一 Scheduler 的普通模板；通用内核不写入 ABM 或交易业务规则，具体见 §8.5。

这五部分共用一个面向用户的**需求与配置入口**：从自然语言或结构化配置提交新需求，形成增量变更预览，再按既有权限加入当前调度。新增功能优先以任务、角色绑定、插件或 workflow 节点接入，不覆盖旧定义或重启全部工作流，具体见 §8.1。

**首版包含轻量 Web 控制台，作为普通用户的主要操作面。** 它把需求入口、实时流程、角色握手、状态监控及插件管理放在一起；CLI/MCP 面向 agent 和进阶用户，项目文件面向人工审阅与追溯。三个入口共享同一后端，不分别维护状态。

各角色的握手、交接、阻断及当前状态必须落在项目目录内，人工无需打开宿主会话或查询数据库即可审阅。项目内的协作目录是统一阅读入口，配置、协议事件和当前投影分别管理，具体见 §5.1 与 §7.7。

本文件是独立仓库 agent-coop 的产品设计入口。2026-10-10 已获用户授权创建本地仓库；当前只完成文档与仓库初始化，Scheduler、Web、插件和运行时适配器均未实现或验收。设计中的命令及配置是拟议接口，不是可执行产品承诺；接口落地前仍需依照本设计完成多方评审。原 trading_system 草案保留为该项目接入待办入口，通用设计只在本仓维护。

本仓自身的开发规则以 [AGENTS.md](../AGENTS.md) 为唯一维护入口，当前开发团队与派发安排以 [实施路线](roadmap.md) 为准。引导阶段通过现有宿主会话人工协作，不代表 Scheduler 或 RuntimeAdapter 已实现、验收；开发团队的临时可用性变化不改变产品接入目标。

## 2. 实践来源与可复用边界

设计调研于 2026-10-10，参考用户在交易系统与 agent-based-microbench（ABM）的多 agent 协作实践。这里保留可复用结论；具体业务仓库内容、账户和工作机环境不是本工具安装依赖。

### 2.1 可复用经验

| 实践 | 通用化方向 | 边界 |
|---|---|---|
| 统一项目入口、角色地图、原验证与交接证据 | ProjectAdapter 读取原项目规则并绑定证据 | 不复制业务任务/完成台账 |
| 已有多宿主 ACP 传输、权限响应与进程管理 | 核对后提取单一维护依赖，或采用经过验证的上游客户端 | 不复制到新仓双维护，不沿用固定角色枚举 |
| 唯一集成 owner、隔离工作树、共享写入串行 | 角色槽位与资源/接收合同 | 具体 owner 由各项目指定，不固定宿主品牌 |
| 派发、交付、消费者接收、合入分别举证 | 明确调度状态与业务完成状态 | PID、exit 0 或心跳均不足以证明交付 |
| Kimi 独立监督及追加意见 | 事件触发、有作用范围的监督与复核 | 不替代消费者评审，不声称现已自动连接 |
| 知识候选、证据来源、独立评测及发布/撤回 | 项目内经验与受控改进闭环 | 保留既有知识 owner，不引入业务数据库依赖 |

ABM 的 proposer、runner、ingestor、verifier、exporter 是实验领域职责，不应成为通用内核的角色枚举。其已有规则与草案需由项目适配器区分，不能把设计文档当作运行事实。接入实现时重新核对实际版本及原权威入口。

### 2.2 本机探针与缺口

前期只做版本与帮助查询，观察到 Codex CLI、Claude Code、CodeBuddy、Kimi Code 的受支持执行入口；CodeBuddy 的当前帮助列出 `--acp`、模型选择、结构化输出和会话恢复。帮助声明不能证明账户可用或适配器已经实现，具体模型核对见 §6。

需要补齐的是跨宿主统一占用、可恢复交接、触发去重与可观测调度。仅增加定时 prompt 无法解决接收责任、重复开工和失效验证。实践中已有的领域治理由原项目继续持有。

## 3. 社区实践与取舍

以下为上游文档及选定源码静态核对，未安装运行，也未采信自报基准分数。来源按项目区分，近似名称不是同一产品。

| 项目 | 本次确认的机制 | 取用建议与限制 |
|---|---|---|
| [first-fluke/oh-my-agent](https://github.com/first-fluke/oh-my-agent) | `.agents/` 配置、按角色选择模型、独立 judge、artifact gate、追加事件 | 优先比较直接扩展的成本；不把模型的自报完成作为验收 |
| [OMA scheduler](https://github.com/first-fluke/oh-my-agent/tree/main/cli/commands/schedule) | 调度 manifest、运行记录、认证失败显式报错；有 Windows schtasks、systemd、launchd、crontab 适配 | 调度包装已存在，避免重造安装器；不由此推断它实现 ABM 接收合同或跨角色互斥 |
| [DeepSeek Harness](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/architecture.md) | Cordis 服务/提供者/消费者、插件卸载时释放 effects；模型、工具、session、loop 均可替换 | 借鉴接口与生命周期；现处 developer preview，需版本固定及适配测试 |
| [DSH subagents](https://github.com/deepseek-ai/deepseek-harness/blob/master/packages/subagent/README.md) | 进程内与跨进程委派、可继续子会话、消息与中断；文档列 ACP/Codex/Claude 等后端 | 可作为第二条宿主接入路径；不要求用户先迁移全部现有会话 |
| [Oh My OpenAgent 当前 dev 分支](https://github.com/code-yeongyu/oh-my-openagent/blob/dev/README.md) | 当前 README 已描述基于 senpi 的 OmO 5、类别路由和 agent graph | 不能继续按旧 OpenCode 插件教程评估当前分支；本轮只借鉴路由，不复制代码 |
| [Symphony SPEC](https://github.com/openai/symphony/blob/main/SPEC.md) | 仓库工作流、隔离执行目录、有界并发、派发前 reconciliation、退避和单一调度权威 | 最贴近本需求的控制循环；其规范的重启恢复不等于持久恢复所有活跃会话 |
| [ACP session config](https://agentclientprotocol.com/protocol/session-config-options) | 会话配置选项协商 | CodeBuddy 的模型选项从实际会话发现并验证，不维护另一份硬编码型号表 |
| [Reflexion](https://github.com/noahshinn/reflexion) | 将反馈与语言反思用于后续尝试的研究实践 | 借鉴经验反馈；反思内容仍是待证假设，不自动变为规则 |
| [DSPy GEPA](https://dspy.ai/api/optimizers/GEPA/) | 利用评测反馈探索程序提示配置的优化接口 | 借鉴固定评测集、反馈与候选选择；不是首版运行依赖，也不照搬其效果到本工具 |

证据定位：OMA 读取 `cli/commands/schedule/runner.ts`、`cli/io/schedule/adapters/schtasks.ts`、`cli/constants/vendors.ts`；该 vendor 列表核对未发现 CodeBuddy 条目。这只说明本次读取列表的缺口，不声称上游所有接入方式都不支持 CodeBuddy。

源码快照：OMA `main@268bb4a4738ef57467e78b8a5f59ddf2d4104832`；DSH `master@d743267388641bc76f17c45ce8b4c231aed1d32c`；OmO `dev@762839e5551317d04086bb7b4e49b25ad175bd92`。以上为调研期间 GitHub API 观测的分支 tip；页面读取并未全部锁定该 commit，实施选型须按选定 commit 重核。

### 三种路线

| 路线 | 优点 | 主要代价 | 裁定建议 |
|---|---|---|---|
| 直接扩展 OMA | 已有角色、调度、跨宿主入口和检查 | 要适配 CodeBuddy、ABM 原队列及接收权威；要证明其调度与本地单写约束吻合 | P0 做静态接口与小样本验证，满足条件优先复用 |
| 小内核加薄插件 | 沿用现有 CLI 与账号，项目状态留原仓库；容易做 Windows 有界运行 | 自己承担 claim、恢复、取消与适配测试 | 推荐产品边界；仅实现上游和本仓确实缺失的部分 |
| 以 DSH 为统一宿主 | 插件生命周期和 agent/session 能力完备 | 用户工作流迁移、preview 版本变化、现有 Desktop 会话接入仍需桥接 | 后续适配；不作为首版前置 |

推荐的是“小内核加薄插件”的产品边界，不预先决定所有代码自研。P0 若证明 OMA 能通过适配承载同一合同，则以 OMA 为运行底座；不能满足时才落独立 coordinator。两者不得同时持有同一项目派发权。

## 4. 用户操作与核心模型

用户先绑定一个项目模板，例如 `repo-delivery` 或 `abm-delivery`，再配置角色及候选执行配置。模板负责依赖、输出、评审和接收规则；agent 负责计划与实现，确定性内核只决定当前动作是否合法、是否具备资源与证据。

| 对象 | 唯一职责 |
|---|---|
| Role | 职责、能力要求、读写范围、交付物、评审独立性 |
| RuntimeProfile | 宿主/协议、模型选择、配置引用、账号组和能力声明 |
| WorkRef | 指向原仓库任务、范围、基线和验收合同；不复制领域状态 |
| Attempt | 一次固定输入与执行配置的执行身份，可失败、重试或交接 |
| Claim | 对工作项、会话、工作树、设备或发布面的有期占用与 fencing epoch |
| Handshake | 角色间一次具名请求与响应，绑定交付 revision、接收者和完成条件 |
| Receipt | 实际提交、验证、review 和接收原件的引用与摘要；不是自填 PASS |

能力分两类：协议能力（流输出、恢复、中断、权限回调、usage）由探针确认；任务能力（设计、实现、复核）由用户指定及实际任务评测建立，不能从厂商/模型名称推断质量。

角色与实例分离。同一个 CodeBuddy profile 可被多个角色引用，但每次派发创建独立 attempt/session；同一账号组的并发与预算共享。相同模型的两个会话只有上下文隔离，不自动证明方法独立或消除共同盲点。

### 4.1 角色完全可配置

角色 ID 是用户定义的稳定名称，不是内核枚举。`integrator / implementer / verifier / supervisor` 只是本文示例；用户可定义研究员、架构师、测试员、文档维护者、发布协调者等任意角色。增加角色通过配置完成，不修改调度器代码，不扩展现有 `core_modules.acp_agents.roles.ROLES` 来承载通用团队。

一份角色定义至少包含稳定 ID、职责/指令引用、RuntimeProfile 绑定、能力要求、项目资源与操作权限、输入与交付合同、触发策略、并发/预算以及独立性约束。可从内置模板派生，但最终解析结果和摘要必须可查看，不能靠多层隐式覆盖猜测实际权限。

工作流使用职责槽位，例如 `produce / review / supervise / accept`，再把槽位绑定到角色 ID；这些是某个模板的槽位，不是全部工作流必须拥有的固定阶段。用户也可自定义新的工作流阶段、DAG 依赖、失败出口和终止判据。角色名不授予权限，角色 prompt 不负责决定任务是否已验收。

单角色可服务多个工作流，一个职责槽位也可有显式候选角色。选择只在能力、权限、独立性和账号预算全部满足后发生，记录实际绑定；不以“最强模型”等主观标签作自动放行依据。首版不允许执行中的 agent 自行扩大角色权限、添加定时任务或更换审批身份。

角色配置的新增、编辑、启停、归档经校验后对未来 attempt 生效；停用角色停止新派发，在途 attempt 按显式 drain 或 cancel 处置。角色被其他模板或活动任务引用时不可直接删除，历史回执保留原配置身份。改模型/profile 是后继绑定，不能静默改写旧 attempt。

允许任意角色不代表项目约束可任意覆盖：ABM 的接收槽位仍须绑定 Claude Code 集成 owner；关键监督与独立核验不能由本包实现者兼任。多个角色若最终绑定同一会话/实际作者，独立性检查仍须拒绝自签。

## 5. 架构与唯一写入者

```text
Web 控制台 / Codex、Claude 插件 / 人工 CLI
                     │ 统一 CLI 或 MCP intent
                     ▼
          coordinator 本机进程
       ┌─────────────────────────────┐
       │ Scheduler：就绪、派发、恢复  │
       │ Monitor：观测、对账、告警    │
       │ Store：attempt/claim/events  │
       └─────────────────────────────┘
          │                │                │
    RuntimeAdapter    ProjectAdapter    GateAdapter
    Codex/Claude/     原任务、基线、      原验证入口、
    CodeBuddy/Kimi    工作树、接收       review 与证据
          │                │                │
          └──── 执行 attempt → 交付 → 评审 → 接收 ────┘
```

建议首版使用 Python、SQLite 和一个 coordinator 进程；原因是本机运行环境及现有 ACP 模块均为 Python。Scheduler 与 Monitor 是该进程内两个职责明确的模块，无需拆成两个服务。插件使用宿主要求的 manifest/MCP 包装，内核不依赖桌面 UI。若 P0 选择 OMA 承载，保留这些逻辑接口而不再并建 Python scheduler。

SQLite 只保存调度运行事实：triggers、attempts、claims、handshakes、events 及 evidence refs。事务内更新状态和追加发布 outbox；项目内可读协议记录与当前状态由该事务事件发布，不允许 agent 同时改数据库和状态文件。仓库任务是否完成继续以 ProjectAdapter 读取的原任务与原证据为准。运行库与可读状态均放在项目协作目录；用户工具目录只持安装、凭证引用和跨项目账号容量协调等机器级内容，不持有另一份项目进度。

ABM 的领域状态仍由 Claude Code 按公开入口更新。新工具的运行库不能出现另一份 `ED-xxx completed=true` 权威，也不直接改 `open-work.json`。ABM 当前计划禁止新增协调脚本，因此首版接入只读；待 owner 批准接入合同并回写原规范后，才能派发写入任务。

交易系统的模块角色沿维护角色表；本工具不导入 ResearchService composition root，不依赖 Mongo、研究 API 或交易服务作为启动条件。

### 5.1 项目内的协作文件

默认使用可直接浏览的 `coordination/` 目录，项目可显式重定位。下面是一般项目的目标布局；当前可在 `requests/` 下保存人工引导证据，不代表协议状态机或自动发布已实现；ABM 等已有权威载体的项目使用适配映射，不强制复制同一份状态。

```text
<project>/coordination/
  README.md                         # 人工入口、文件权威、操作说明
  team.yaml                         # 角色/profile/模板绑定及调度配置
  workflows/<name>.yaml             # 本项目自定义模板（需要时才创建）
  requests/<id>/                    # 原始需求、增量提案、校验与应用结果
  knowledge/
    INDEX.md                       # 可重建的经验索引与适用范围
    entries/<id>/<revision>.md      # 带元数据的不可变经验正文
    evaluations/<id>.json           # 评测输入、基线、指标与结果引用
  STATUS.md                         # 当前团队、任务、握手、阻断和下一动作
  state/current.json                # 与 STATUS 同 revision 的机器投影
  handshakes/<id>/
    000001-offered.json              # 不可覆盖的协议事件
    000002-acknowledged.json
    000003-accepted.json             # 或 changes_requested/rejected 等响应
  decisions/<id>.yaml               # 人工拟定的决定，导入后才生效
  .runtime/                         # Git 忽略；仍位于项目下
    state.sqlite                    # 本项目调度事务及发布 outbox
    logs/                           # 脱敏运行日志
```

`team.yaml` 是角色配置的唯一来源；需要复用外部角色文件时由它显式引用，禁止同一角色同时有互相覆盖的内联/外部定义。`STATUS.md` 只从同一 revision 的状态生成，至少呈现“任务、当前角色/模型、握手对象和状态、基线/交付 HEAD、阻断及责任人、最后实质进展、下一动作与时间、证据链接”。JSON 投影保留机器字段，人工通常只需读 Markdown 并沿链接查看交接事件。

三类权威分开：项目原任务/证据决定领域结论；SQLite 事务决定工具调度和握手状态；公开 JSON 事件与 Markdown 是可审阅记录/投影。原任务、监督意见已有正式文件时只链接其原件，不把它们复制到 `coordination/` 再维护。SQLite 不能被唯一当成“证据已公开”的证明。

发布采用单写入者及事务 outbox：先提交协议事件及待发布项，再按稳定事件 ID 写同目录临时文件、原子发布不可变事件文件，最后发布携带 revision 的 current/STATUS 投影。重复发布只接受同 ID 同摘要；不同摘要拒绝并报警。current 与 STATUS 不能跨文件原子替换，因此消费者必须比对 revision，不一致显示 `publication_pending`，不能拼成一个已闭合状态。关键握手只有在原件和匹配投影已发布后才允许解锁下游；中断由 outbox 重放恢复，发布失败不重新执行 agent。

协议事件包含 `schema_version / event_id / project_id / work_ref / handshake_id / attempt_id / revision / actor / timestamp / payload_digest`，业务字段见 §7.7。状态视图带 `state_revision / published_revision / observed_at / pending_publications`；离线/过期清晰标注，不让旧文件看起来仍在实时更新。未发布的内部变化不授予下游执行资格。

只有 coordinator 可发布工具状态。agent 通过 CLI/MCP 提交具名意图，人工可直接阅读全部文件，修改配置或编写 `decisions/<id>.yaml` 后显式导入。decision 导入校验操作者、目标 revision、输入摘要和授权，成功产生正式事件并关联原文件摘要；保存 YAML 不代表已批准。手改 STATUS/current/已发布事件被检测为漂移并停止受影响派发，不静默覆盖，也不把手写 accepted 当作握手成功。

Git 策略：配置、模板、README 跟踪；高频 STATUS/current、运行库、日志默认忽略；握手与决定按项目证据策略在里程碑显式纳入 Git，不能每次心跳自动提交。运行期间所有记录仍在项目内可见。ABM 的受跟踪输入参与 proof，故不得自动把高频协作文件纳入证明输入；交付快照的提交由集成 owner 在验证冻结窗口外安排。忽略记录不等于删除历史；清理仅在相关工作终结、有效保留策略满足且证据已归档后执行。

多 worktree 共用一个显式 `coordination_root`，默认是注册的项目主目录下 `coordination/`；业务树记录/展示指向该根的引用，不启动独立副本。coordinator 的授权写根仅增加该协作目录，不因此允许业务 agent 写主树源码。启动前核对 project_id、仓库身份、owner 与占用；Git 克隆或复制旧状态不能继承旧主机的 lease。首版限单主机本地文件系统，不把 SQLite/锁放在网络共享上。

## 6. 运行时接入

角色 → 执行 profile → RuntimeAdapter 的绑定独立于工作流拓扑。推荐 executor profile 使用 CodeBuddy + `deepseek-v4-pro`；用户可替换为 OpenCode 或其他已通过能力验证的 agent，无需改 Scheduler 或复制业务模板。模型、provider、账号组、凭证引用、权限和版本均属于 profile，不以模型名判断能力或授予权限。预设未通过本机可用性验证时保持 blocked，不静默切换模型。

2026-10-10 本机 `codebuddy --help` 明确列出 `deepseek-v4-pro`，DeepSeek [官方 API 文档](https://api-docs.deepseek.com/)亦列出该模型 ID；这仅核对标识，不代表已验证账号额度或任务质量。扩展契约及配置清单推荐见 [运行时接入约定](runtime-adapters.md)。配置建议基于宿主可选清单、角色要求与有出处的能力/评测证据；未知项明确展示，用户选择后形成新绑定，清单刷新不替换在途模型。

| 接入 | 首选执行面 | 首版约束 |
|---|---|---|
| Codex CLI | `codex exec --json`，后续可升级 app-server | 固定 cwd、模型、权限、session_id；解析结构化事件，不能只读最终文字 |
| Claude Code CLI | `claude -p` 的结构化流或既有 ACP 适配器，按版本验证后选其一 | 恢复精确 session；交互权限需求转 blocked，不能后台挂死 |
| CodeBuddy CLI | 原生 `--acp`，协商 configOptions 与模型，print 流作为显式降级路径 | profile 可多份；切模型/配置形成新 attempt，记录实际解析值，不静默回退 |
| Kimi Code CLI | `kimi acp`，沿既有引擎声明核对配置协商 | 独立监督 session；只读被分派证据，意见走限定追加入口；不使用历史 Python kimi-cli 的参数假定 |
| OpenCode（扩展目标） | 官方 CLI/ACP 能力作为接入候选，版本探针后选定传输 | 用户按安装版本选择 provider/model；未实现、未运行验证，缺能力明确阻断 |
| Codex Desktop | 插件调用同一 MCP/CLI，查看、认领、交接及人工接管 | 不假设独立 app-server 能控制已经打开的 Desktop 任务 |

依据：[Codex 非交互模式](https://developers.openai.com/codex/noninteractive/)、[Codex app-server](https://developers.openai.com/codex/app-server/)、[Claude 程序化运行](https://code.claude.com/docs/en/headless)、[CodeBuddy CLI](https://www.codebuddy.ai/docs/cli/cli-reference)。本机帮助与网站可能不同，`doctor` 必须同时固定 executable version 与解析能力。

Desktop 作为协作者时，认领具体 WorkRef 并持有会话 claim。后台同一任务不得再派给 CLI。Desktop 原生自动化可在已支持且明确启用时仅调用 `tick`/领取队列；本工具不直接修改 Codex 私有数据库或 automation 文件。应用关闭时该入口可能不可用，coordinator 保持可运行；转交 CLI 必须显式释放/核验旧 claim 和工作树。

Codex/Claude/CodeBuddy/Kimi 都使用各自受支持登录方式；配置只保存 credential/profile 引用。进程环境白名单注入，既不复制整个配置目录，也不把 token 写入团队 YAML 或日志。[Kimi Code 当前仓库](https://github.com/MoonshotAI/kimi-code)确认 ACP stdio 入口；运行时不能因为命令同名就混用历史 kimi-cli 的协议假设。

### 既有 ACP 的复用策略

先复用 `core_modules.acp_agents` 的公共传输、身份和进程能力做本仓只读适配验证。需要独立分发时，把通用层提取成单一维护的依赖包并让原模块兼容导入，或采用经验证的上游 ACP 客户端；不复制一份 client/procs/policy 到新仓长期双维护。通用化迁移必须另有接口兼容测试，不能在首版调度工作中顺手改写研究业务。

## 7. 调度与恢复合同

### 7.1 一个项目一个触发权威

Windows Task Scheduler 只拉起/守护 coordinator；**工具自身有持久 Scheduler**，负责每条工作流及角色任务的排队、到期和派发，不能把 OS 计划任务当作全部调度实现。每个角色不是一个相互竞争的 OS 定时任务。实际工作优先由提交/交付/评审等事件触发，定时 tick 用作恢复与外部条件复查。默认示例为 60 秒确定性检查，未变化不调用模型、不发消息。

每个 tick 顺序为：核对存活与 claim → 验证配置 → 读取原任务及依赖 → 合并重复触发 → 资源准入 → 派发有限 attempt → 发布变化事件。配置失败停止新派发，但继续观察和取消已运行任务。

Scheduler 接收手动 run、固定 interval、带时区的 cron、上游交付事件、retry_due 与 unblock 六类触发；工作流模板可为角色声明触发策略。调度不让 LLM 自行决定抢锁或改写队列。就绪选择顺序为已满足前置的接收/复核、阻断解除的续作、常规实现；同等级按等待时间排序，配置老化提升防止持续新工作饿死旧任务。

每次未派发必须返回具名原因：`dependency_pending / opinion_blocking / account_busy / workspace_busy / awaiting_owner / budget_exhausted / capability_missing / project_paused`。外部阻断与资源排队分开；恢复条件由模板/ProjectAdapter 给出，不用定时“再问一遍”替代依赖变化。触发和 next_due_at 持久化，内部存 UTC，展示明确项目时区；重复/缺失的本地墙钟时窗按 coalesce 策略处理。

触发使用 `(project, work_ref, action, input_digest)` 作为语义去重键；cron 另记时窗。宕机错过多次定时只合并检查一次，不补发一串相同 prompt。显式重试引用原 attempt 并增加序号，不能靠改变去重键无限续命。

### 7.2 进程、会话和证据分开

attempt 状态为 `queued / claimed / running / awaiting_review / awaiting_owner / delivered / failed / interrupted / cancelled`。调度状态不表达 `merged` 或领域 sign-off；那些由项目原证据投影。进程 exit 0 只证明正常退出；缺少要求的提交/产物/验证时，不能进入 delivered。

同一事务取得 claim 和启动意图后才起进程；启动前生成 attempt_id 并绑定进程运行标记。进程启动但句柄登记前崩溃时，恢复先按 attempt 标记、PID 创建时间、session 和 cwd 对账，禁止立即再派。无法确认时进入 interrupted 等待恢复，不因 lease 到期就认定旧进程已经停止。

claim 使用递增 epoch；过期 worker 的回执不能提交新状态。fencing 只能保护工具持有的状态写入，不能自动阻止任意 CLI 的 Git/文件副作用；所以每个 writer 仍需独立工作树，集成发布按唯一 owner 和入口串行。重启前后都不得出现两个存活 writer 共享同一树。

取消先停止本 attempt 的真实进程树并确认退出，再释放资源。未知状态保留占用/隔离树并报告，不自动 reset、clean、stash 或删除任务树。授权外的已有进程不接管、不终止。

### 7.3 资源与预算

至少支持 `account:<group>`、`worktree:<path>`、`project:<id>:integration`、`device:thor` 四类容量。默认总并发 2、单 writer/树、单 integration writer；具体值可配置。CodeBuddy 多模型配置若使用同一账号，共享该账号组容量。

预算首版硬执行墙钟、attempt 数和并发；token/cost 若运行时能提供则记录 measured，否则为 unknown。要求硬 token/cost 上限而运行时不可计量时拒绝该任务，不将 unknown 当 0。账号额度耗尽转 `awaiting_owner` 或显式可恢复等待，不静默换账号/模型。

首版连续无新增证据上限为 2 次、单切片自动 attempt 上限为 3 次，达到任一上限停止重复执行并具名报告原因。瞬时通信错误才可退避重试；权限拒绝、架构裁定缺失、输入变更及测试断言失败不能当网络错误重复跑。

### 7.4 评审和接收

交接至少包含 WorkRef、base_commit、task_head、receiving_ref、观察到的接收提交、显式改动路径、合同/消费者、验证命令/退出码/输入摘要、未闭合项及恢复点。

独立 reviewer 使用新上下文并绑定同一 task_head；作者不能通过换 role 名自签。多模型只是评审策略的一部分，实际消费者仍需评审自身接口。接收前若 HEAD 或相关输入改变，旧评审不能直接放行。只重验受影响范围，沿用 ABM selector，避免 OMA 式每轮全部重验成为新全量成本。

集成 owner 对最新接收基线做差异与依赖核对。无关前进可复用有效证据；真实重叠进入 intake；基线非祖先且无等价证明则停止自动接收。工具不把无回复判定为同意。

### 7.5 Kimi 监督者

`supervisor` 是团队里的监督角色；后台进程在实现中命名为 `coordinator`，避免把进程守护与语义监督混为一谈。Kimi 默认绑定此角色，后续可按相同合同绑定其他已批准 profile。

监督者检查五件事：是否推进既定出口、是否越过唯一写入边界、是否漏验或重复计算、是否放宽正式范围/判据、通过与关闭是否有原件和独立资格。它面向执行者、评审者和集成者，不能只审实现代码。

触发点为切片选定、可审阅批次提交、申请接收、关键合同/判据/输入变更，以及提出全量验证/重采。运行故障恢复和到期未处理 blocking 也触发复查。内核合并相同输入事件；普通每次编辑不增加一次监督审批，定时无变化不调用 Kimi。监督输入限明确交付的提交/差异、原活动项、已有回执及相关意见，不能假定可读取其他宿主的私有会话。

监督输出为 `SupervisionOpinion`：唯一 ID、作者及会话/profile、WorkRef、精确输入、违反合同、受影响消费者、证据引用、反例/未审范围、最小修正、恢复条件和意见种类。种类为 `advisory / blocking / escalation`，生命周期为 `open / resolved / retracted`；种类与生命周期分轴。正文按 ABM 的“范围与主张；直接定位及证据；反例核对与未审查项；结论与恢复条件”四段表达。

ABM 项目继续使用原 `verification/signoff/diagnostics/supervision-opinions.md` 作为意见通道，不新建监督台账。意见由实际审阅身份提交，只追加，不改写旧正文；追加入口须串行校验文件前置摘要和唯一 ID，不能借追加工具冒充其他作者。调度库只保留原意见引用和可重新生成的阻断投影。无法可靠解析原意见/处置关联时显示 unknown 并阻断相应接收，不能从一段摘要猜测已闭合。

Kimi 的源码和业务状态访问为只读；仅允许经限定意见入口追加内容，不授予通用 Edit/Shell 写权限。监督者不得修改阈值、源码、状态投影、操作 Thor、合并或终止他人进程。其 blocking 经项目合同授权后阻止受影响的验收/接收，不能无依据冻结无关工作。监督本身的失败不作为领域失败。

修复者追加修复证据，原审阅者或具名、未参与修复的替补复核后追加闭合；实现者和集成者不能擅自把监督 blocking 改为 resolved。被反证推翻的意见保留原文并追加撤回/更正与受影响结论。正确性争议回原语义 owner/用户裁定，escalation 不等于放行。

Kimi 不可用时，仅需要监督的关键前置/批次接收保持 `awaiting_review`，无依赖工作继续。Claude Code 可沿原通道安排符合独立性条件的具名替补；不得自动把普通 reviewer 升为监督者或把缺席记为通过。衡量监督效果用证据可复核性、漏检反例闭合和错误结论纠正，不用心跳频率或意见数量。

### 7.6 状态监控

Monitor 是首版确定性模块，消费 runtime 流事件、进程句柄、原任务和证据引用；不以模型周期自报状态作为监控数据源。其观测至少拆成六个维度：

| 维度 | 数据依据 | 不可混淆的情形 |
|---|---|---|
| 主机与进程 | coordinator heartbeat、PID 与创建时间、退出码 | PID 存活不等于模型在推进 |
| 会话活动 | runtime session_id、最近结构化事件、权限等待 | 流输出活跃不等于产物完成 |
| 工作进展 | 原任务阶段、最新提交、有效 artifact/checkpoint | 重复输出和仅心跳不算新进展 |
| 证据当前性 | 输入摘要、review HEAD、receipt digest | 测试曾通过不等于对当前提交仍有效 |
| 依赖与阻断 | 原任务前置、监督意见、owner 与恢复条件 | 等待 owner 不算进程卡死 |
| 资源与预算 | claim、账号组并发、墙钟、usage 来源 | unknown 不能显示成零消耗或空闲 |

监控记录 `observed_at / last_runtime_event_at / last_progress_at / next_due_at`；没有观测时显示 unknown，数据过期显示 stale。活跃执行使用单调时钟计算 timeout，重启后结合持久 UTC 时间重新对账，不因系统时钟跳变直接判定租约安全过期。

Monitor 产生 `process_exited / runtime_stalled / progress_stalled / evidence_stale / blocked_overdue / auth_required / budget_reached` 等事件；**只有 Scheduler 修改调度状态和决定重试/取消**。Kimi 可以读取这些事件开展语义核验，不能凭自己的巡检文字更新 PID/usage 等机器观测。执行、监控、监督三类事件分开显示。

无流事件不立即等于 stalled：长工具运行、明确权限等待和外部阻断有独立状态与截止条件。超过配置阈值先触发对账；无法证明旧 writer 已停止时隔离并具名报告，不自动重启第二个 writer。

首版提供 Web 实时流程和 `status --watch`、MCP 状态查询；三个入口展示同一后端投影，至少包括角色/实际模型、任务/阶段、进程/会话健康、工作树与基线、等待原因/责任人、最近进展、下一调度、预算和证据链接。增加 `why <work-ref>` 解释不派发原因，`events <work-ref>` 查看有界时间线。Web 的页面与交互边界见 §8.3。

#### 当前状态的维护与过期处置

集成者负责当前工作状态的准确性与可操作性：派发前核对现有任务、输入版本及未闭合意见；交付、评审、接收、合入、取消和用户变更后，在同一发布检查点更新有效任务、候选指针、责任人、阻断与下一动作。监督者独立核对这些状态是否有原件支撑，发现滞后、冲突、失效票据或已被替代的工作后提交具名意见，并按 §7.5 复核监督阻断的闭合。二者共同承担维护责任，但不成为两个状态写入者：集成者提交 typed intent，监督者提交限定意见，Scheduler 校验权限、expected_revision 与证据后按 §5.1 单写及发布投影。原业务状态仍由 ProjectAdapter 指向的 owner 维护，不能用本工具结论覆盖。

默认“当前工作”视图只保留有效活动项、未闭合阻断及需要用户处理的事项，按 WorkRef 与语义事件去重；已完成、取消、撤回、被替代或合并的项在状态发布后移入历史视图并保留终态依据、原意见与 `supersedes/superseded_by` 引用。替代任务必须明确承接范围和剩余义务，不能通过关旧开新丢失阻断。过期观测/评审标为 stale 或 unknown，退出有效通过票及可复用证据集合；如果影响当前工作，仍在待处理区显示原因、owner、复核条件与 next_due_at。过期不是已解决，隐藏历史不是删除原件。

当前投影及供 agent 交接的摘要由同一 revision 生成：包含有效任务和当前候选、最近实质进展、未闭合意见、下一步与责任人；历史只按需要通过引用展开。不把已完成任务、重复心跳、旧失败或旧建议反复注入后续 prompt。旧结论是否仍适用由输入/版本和未完成义务判断，不能单凭年龄截断上下文或删除有效约束；有依赖的旧证据仍保留引用。

处置由实际状态变化、输入失效、到期复核触发；相同输入合并，空闲时不循环召唤模型“维护状态”。矛盾尚未对账或文件发布未完成时显示 `reconciliation_required`/`publication_pending`，阻止依赖矛盾事实的派发与接收，继续无关工作。前端展示“最后核验时间、谁负责、下一动作”，允许查看历史但不将历史失败计入当前阻断数量；单条未闭合阻断即使久未处理也保留在当前待办。过期阈值与期限由项目/任务策略显式绑定，不暗设统一过期即关闭规则。

告警只针对状态变化、失败、超出约定时限、需要 owner 的决定及完成；相同告警按任务和原因合并。默认在本地状态面和已启用插件显示，不自动发送外部邮件/聊天消息。暂停项目后保持监控，停止新派发；Monitor 自身故障导致观测不可信时冻结新写任务。

### 7.7 角色握手与交接

工作流的跨角色依赖使用显式握手，不能只靠消息发送成功或看到某个文件存在。典型握手包括任务指派、实现交付、评审请求、监督请求、修改回复和接收申请；模板声明每一类的发起者、接收者、必要证据、响应权限及截止条件。

```text
offered → acknowledged → accepted
                       → changes_requested
                       → rejected
offered / acknowledged → cancelled / expired
```

`offered` 表示请求与证据已发布；`acknowledged` 表示指定接收者已领取该精确 revision；`accepted` 表示接收者按本类握手合同完成判断。ack 不是评审通过，接受任务不代表任务完成，评审 accepted 也不代表已集成。协议类型和证据合同决定 accepted 能解锁哪个下一动作。

每次握手记录 `from_role / to_role / sender_actor / recipient_actor / work_ref / attempt_id / subject_revision / base_commit / task_head / evidence_refs / requested_action / acceptance_criteria_ref / response_due_at / idempotency_key / supersedes`。actor 由已认证运行绑定或人工操作入口提供，不相信模型在 payload 中自报他人身份。自定义角色沿同一协议，不在代码中按角色名称分支。

发起者只能发布、补充后继请求或撤回自己的未终态请求；接收者只能响应分派给自己的 revision；Scheduler 负责派发、期限与状态机检查，不能替评审者接受；监督者提出的 blocking/闭合继续受 §7.5 权限约束。CLI 返回成功前须满足 §5.1 的公开发布条件；超时/失联不生成 accepted。

请求领取同时取得对应 session/worktree claim。发件人发布交接不会自动转移源码写权，接收者 ack 也不自动允许同时写同一树；实现者需交付固定提交并释放写入，接收方取得独立树或明确移交后的 claim 才能继续。只读评审与仍在进行的实现可并行，但必须针对不可变交付提交，不能把之后的 WIP 混入评审。

重复请求按 idempotency_key 复用同一 handshake，相同 key 不同内容拒绝；响应使用 expected_revision 比较并交换。多名必需消费者各有独立握手，全部所需响应满足才解锁；未分派的第三方意见不冒充具名消费者接收。

返工产生新的 attempt/交付 revision 和后继 handshake，引用前一次 `changes_requested` 与修复证据；旧事件保持原文。输入改变后旧 accepted 保留为历史，当前性投影标记失效并请求后继复核。配置变更、换模型或换接收者也必须显式重新绑定，不能让迟到响应解除新一轮阻断。

超时策略由模板给出：提醒、升级到 owner、具名重新分派或停止。达到期限只产生 expired/告警，不推断旧进程退出；真正重派仍满足 claim 与进程对账条件。`STATUS.md` 明确列出“谁等待谁、等待多久、缺哪份证据、恢复条件是什么”，并链接双方请求与响应原件。

## 8. 配置与命令草案

下例是提议的配置合同，尚无实现；模型通过本地 profile 显式绑定，示例不代表已登录或已获调用资格。

```yaml
version: 1
project:
  id: sample-project
  root: .
  adapter: repository
  workflow: repo-delivery
  mode: observe
  integration_role: integrator
  coordination_root: coordination

profiles:
  claude-main:
    runtime: claude-code
    config_ref: local:claude-main
    account_group: claude-personal
  codex-main:
    runtime: codex-cli
    config_ref: local:codex-main
    account_group: codex-personal
  cb-implementation:
    runtime: codebuddy
    model: deepseek-v4-pro
    config_ref: local:cb-implementation
    account_group: codebuddy-personal
  cb-review:
    runtime: codebuddy
    model: glm-5.3
    config_ref: local:cb-review
    account_group: codebuddy-personal
  kimi-supervision:
    runtime: kimi-code
    config_ref: local:kimi-supervision
    account_group: kimi-personal

roles:
  integrator:
    profile: claude-main
    contract_ref: repo:AGENTS.md
    requires: [structured_events, cancellation]
    max_active: 1
  implementer:
    profile: cb-implementation
    requires: [structured_events, scoped_write, cancellation]
    workspace: isolated-worktree
    max_active: 1
  verifier:
    profile: codex-main
    requires: [structured_events, read_only, cancellation]
    independent_from: [implementer]
    max_active: 1
  specialist-reviewer:
    profile: cb-review
    enabled: false
    requires: [structured_events, read_only, cancellation]
  supervisor:
    profile: kimi-supervision
    requires: [structured_events, read_only, cancellation]
    independent_from: [integrator, implementer, verifier]
    write_via: project-supervision-append
    max_active: 1

# 以下角色名均可改为用户自定义 ID；职责槽位由所选模板定义。
workflow_bindings:
  produce: implementer
  review: verifier
  supervise: supervisor
  accept: integrator

scheduler:
  timezone: Asia/Shanghai
  reconcile_every_seconds: 60
  max_parallel: 2
  coalesce_missed_ticks: true
  notifications: meaningful_changes
monitor:
  sample_every_seconds: 15
  stale_after_seconds: 90
  runtime_idle_timeout_seconds: 600
  progress_warning_after_seconds: 1800
budgets:
  wall_seconds_per_attempt: 1800
  max_attempts_per_slice: 3
  max_no_progress_attempts: 2
```

`local:*` 是待实现的显式配置引用机制，不读取模型 secret 值；doctor 输出已解析模型 ID、来源、配置摘要、运行时版本、协议能力与权限方式。缺失引用阻断启动，不偷偷采用厂商默认模型。配置热更新仅用于未来 attempt，在途配置冻结。

拟提供以下命令，不在本轮执行：

```text
agent-coop doctor --config team.yaml
agent-coop roles list --config team.yaml
agent-coop roles validate --config team.yaml
agent-coop status --config team.yaml
agent-coop status --config team.yaml --watch
agent-coop why <work-ref>
agent-coop events <work-ref>
agent-coop tick --config team.yaml --dry-run
agent-coop start --config team.yaml
agent-coop claim <work-ref> --role <role> --session <id>
agent-coop handoff <attempt-id> --receipt <path>
agent-coop handshake offer --request <path>
agent-coop handshake ack <id> --expected-revision <revision>
agent-coop handshake respond <id> --decision <path> --expected-revision <revision>
agent-coop decision import <path>
agent-coop pause --project <id>
agent-coop resume <attempt-id>
agent-coop cancel <attempt-id>
```

MCP 暴露同一组语义操作。pause 停止新派发，cancel 停止指定执行，两者不能混同；start/register 属显式操作，安装插件本身不启动计划任务。

### 8.1 需求与配置的统一入口

Web 与插件都提供“提交需求”“调整团队/工作流”“查看变更和排队结果”三个入口，背后统一调用 intent API，CLI/MCP 使用同一应用层。用户可以说“这个任务在评审前增加一次性能检查，交给 CodeBuddy 的指定模型”，也可直接提交 YAML。Web 用表单和图上差异预览承接普通用户，宿主对话及文件入口承接进阶用户。入口保留原始需求、提出者、项目与明确授权范围，不能把模型生成的解释当成用户原话。

```text
用户需求/配置
  → 定位原任务、现有角色、模板及插件
  → 形成增量 ChangeProposal
  → 预览影响、依赖、权限、预算及插入位置
  → 校验并按既有授权应用
  → Scheduler 在合格节点接入
  → STATUS 显示排队、握手和执行结果
```

自然语言解析由一个可配置的 intake/planner 角色完成；结构化输入可直接进入校验。该角色只提出建议，不持调度写权、不自行扩大权限。已有明确授权且满足项目策略的普通任务可直接入队；需要新权限、接收权变更或既有合同要求 owner 裁定的变更进入原审批出口。不是每个新任务都增加一次人工批准，也不能让 LLM 替用户批准插件安装。

需要推荐或设计新 workflow、修改既有节点合同/依赖/完成判据的请求，进入 §8.5 的多角色设计与评审。结构化输入只能跳过自然语言解析，不能绕过必要评审；按已发布模板创建普通实例不重复开展模板设计评审。

入口先检索可复用定义，再选择最小变更类型：

| 类型 | 动作 | 对原定义的影响 |
|---|---|---|
| 新任务 | 创建/引用原项目 WorkRef，绑定现有模板及角色，申请调度 | 不改模板 |
| 新参数或模型配置 | 建立 profile/参数的后继绑定 | 在途 attempt 保持原绑定 |
| 新角色 | 新增角色并绑定已有职责槽位，或为新节点指定角色 | 不改其他角色定义 |
| 插入节点 | 以已有节点 ID 指定前驱/后继，提交有界图补丁 | 生成后继 workflow 版本，旧版本保留 |
| 新能力插件 | 注册新 capability、角色模板或节点模板，显式启用后被引用 | 安装本身不替换 active provider 或触发任务 |
| 新工作流 | 复用已有节点/子流程组合成新模板 | 不克隆一整套实现代码 |

`ChangeProposal` 至少携带 request_id、WorkRef、base_workflow_version/digest、预期项目配置 revision、patch、角色/profile/plugin 版本引用、权限/预算增量、受影响节点与消费者、验收条件、应用时机及回退点。用户预览须同时显示“立即可执行的部分、等待的前置、在途任务保持什么、哪个后继动作会改变”，不能只展示一段自然语言确认。

请求记录保存在 `coordination/requests/<id>/`：`request.yaml` 保存原始输入及身份，`proposal.yaml` 保存结构化补丁，`validation.json` 保存校验，`result.json` 保存 applied/queued/blocked/rejected 结果及新版本/任务引用。它们沿 §5.1 的事务发布协议写入；已有项目需求库时 request 只引用其原件，不另建业务需求权威。`applied` 表示定义/入队已生效，不表示需求已经实现。

### 8.2 插入节点与在途工作流

节点以稳定 ID 引用角色槽位、输入/输出合同、执行 capability、必需证据、预算及失败出口。模板组合这些节点；插件提供可复用节点类型，而不是为每个项目复制一份完整工作流。

```text
旧版本： implement → review → accept
后继版： implement → performance_check → review → accept
```

对边 `U → V` 的插入明确转换为 `U → N → V`，保留其余未涉及边、分支条件及 join 语义。新增 N 的输入必须能由 U/已存在工件满足，V 的合同若要改变须显式列入 patch；不能因插入节点就悄悄降低原验收。多前驱、多消费者与条件边必须逐项声明，不猜测插在哪一条路径。

定义以不可变版本及解析后摘要绑定；可用原版本加小补丁存储，解析结果须可复算，不能运行时读取可变的“latest”。校验至少包括重复节点 ID、缺失引用、循环依赖、不可达必需节点、输入输出不兼容、角色能力、独立性、插件版本、权限与预算。模型提议合法不等于校验通过。

变更分 prepare → validate → activate：candidate 阶段不改 active pointer；激活以 expected_revision 原子比较并交换，失败不覆盖他人的修改。Scheduler 只消费已激活定义。应用失败保留原版本和队列，不出现半条依赖边。没有冲突的多个请求仍须顺序应用并各自记录基线；冲突返回精确节点/字段，不自动 last-write-wins。

| 当前执行位置 | 应用方式 |
|---|---|
| 尚未启动的实例 | 绑定后继版本后正常排队 |
| U 已完成、V 尚未启动或认领 | 在调度安全点暂停该路径的新认领，核验既有工件，追加 RunAmendment，再从 N 继续；已完成 U 的有效证据可复用 |
| V 已被认领或正在执行 | 默认对未来实例生效；如需影响当前实例，显式等待安全点/撤回未开始 claim 或按既有取消流程处置，不能把旧 V 追认为已经过 N |
| 新需求与当前路径独立 | 挂接独立子流程，复用角色/资源池并正常排队，不改当前 DAG |
| 当前实例已经终结 | 新建后继实例或任务，不修改旧成功记录 |

RunAmendment 是同一 run 下的追加记录，绑定旧/新定义摘要、切换前沿、保留的已完成节点、需要重验的证据和批准身份。已有 attempt 的输入/profile 不变，新节点的 attempt 绑定新定义；监控显示此次边界。旧握手不能为新增义务签字。所需插件失效、进程未能停止或依赖无法复用时，只阻断受影响路径。

定义回退只是将未来派发指回已验证旧版本，不撤销已经发生的文件修改、提交或外部副作用。需要补偿的动作由节点声明或 owner 处置；首版不提供假定任意 workflow 可自动回滚的按钮。

拟提供的统一操作命令如下，插件可调用同一意图接口：

```text
agent-coop request submit --project <id> --text <requirement>
agent-coop request submit --project <id> --file <request.yaml>
agent-coop request preview <request-id>
agent-coop request apply <request-id> --expected-revision <revision>
agent-coop request status <request-id>
agent-coop workflow inspect <workflow-id> --version <version>
```

### 8.3 Web 流程与状态控制台

Web 属于首版产品交付，不是后续附加看板。定位为本机轻量控制台：一个前端构建包，由 coordinator 的本地 HTTP 入口提供静态资源、状态查询、事件订阅和操作 API；无需独立数据库、账号体系或新增前端运行服务。前端技术栈在实施计划中按现有资产选择，不以画图工具的渲染实现倒推整个产品架构。

借鉴 archify 的可展开图、明确主路径、搜索聚焦、依赖追踪和明暗主题。archify 适合设计图与可分享快照；实时产品图必须绑定节点 ID、运行版本及后端事件，不把静态 HTML 的动效当成执行事实。首版导出可为带时间和 revision 的审阅快照，始终标明其非实时性质。

默认进入“项目工作台”，以当前实例为中心；需求、团队和插件作为同一应用的明确入口，避免普通用户需要理解多个控制面。

| 页面/区域 | 普通用户能完成什么 |
|---|---|
| 项目工作台 | 看清总体进度、当前等待、下一调度与需要自己处理的事项；提交新需求 |
| 流程主画布 | 查看当前节点、分支、依赖、正在运行的角色，以及下游为何未启动 |
| 节点详情抽屉 | 查看职责/实际模型、输入输出、握手双方、证据、阻断及允许的下一动作 |
| 需求与变更 | 输入自然语言/表单，预览新节点与受影响边，校验后入队，查看应用结果 |
| 团队与配置 | 新增自定义角色、选择运行时/profile、设置触发与预算、查看能力缺口 |
| 插件与定义 | 查看已安装/启用版本、使用者、升级影响及 drain 情况；检查模板和节点定义 |
| 经验与改进 | 查看问题与修正证据，检索踩坑经验，提出优化，比较评测/试用效果并查看撤回记录 |

工作台概念布局：

```text
项目 / 当前工作流 / 运行版本       连接状态与观测时间       [提出新需求]
需要你处理：2 项      运行：2      等待：1      下一调度：具体时间
┌─────────────────────────────────┬────────────────────────┐
│ 当前流程                        │ 选中节点               │
│ 需求 → 实现 → 性能检查 → 评审    │ 执行角色 / 实际模型    │
│                         ↓       │ 握手：等待谁确认       │
│                   监督 → 接收   │ 阻断原因 / 下一步      │
│ [当前运行] [定义] [变更预览]     │ 输入、产物与证据链接   │
└─────────────────────────────────┴────────────────────────┘
最近事件：交付已发布 / 对方已领取 / 等待复核 / 需要人工决定
```

示意路径只解释页面组织，真实布局由所选 workflow 的 DAG 生成，不固定为这几个角色或必经阶段。模板、运行和变更预览为三种明确模式：当前运行显示实际已绑定版本；定义显示模板；变更预览对新增节点/边作标注，不能把尚未应用的节点混成正在执行。

节点默认显示工作名称、角色和人类可读状态；接收阶段的“已验收”与执行阶段的“已交付”分开。点开后再展示执行 attempt、握手、原领域结论三个维度，避免把细粒度技术状态全部堆在图上。边可显示“等待领取/等待评审/已接收/需修改”等握手进展；一条边只承载有明确对应关系的协议，普通依赖不能伪装成已经沟通。

绿色只表示该节点要求的证据已满足；进行中、排队、等待人工、阻断、失败、未知/过期均有文字和图标，不仅靠颜色区分。项目总体进度来自明确节点/义务分母，未定义分母时只显示完成/运行/阻断数量，不生成虚假百分比。语义监督和机器健康分别显示，Kimi 在线不能让业务节点变绿。

图大时按子流程分组，默认突出当前活动路径与阻断，不一次展示全部历史 attempt。提供搜索、缩放、键盘导航及等价任务列表；移动端使用列表和详情。正文对比度目标至少 4.5:1，状态变化不强制跳转选中节点；默认低动效并遵循 reduced-motion。流程箭头不持续奔跑制造假活跃。

### 8.4 前后端状态一致性与操作

后端提供同一 revision 的项目/运行快照，以及有序事件增量；首版可用 HTTP 查询加 SSE。客户端按 event_id 去重、按 cursor 续订，缺事件或版本不一致时重新拉取完整快照。订阅恢复以前显示“连接中断/数据停留于某时”，不把断线解释成任务结束或空队列。

Web、CLI 和 STATUS 文件都携带相同语义 revision；关键握手尚未完成文件发布时，Web 也显示 publication_pending，不能绕过项目文件审阅条件。浏览器关闭不停止后台 Scheduler，后台停止后网页保留明确标记的最后观测并禁用执行操作。

所有写操作提交 typed intent，携带 expected_revision 和幂等请求 ID；后端返回应用/排队/拒绝回执后再刷新状态。按钮 loading、防重复提交及确认文案只是交互措施，真正的权限、独立性、资源与握手校验仍在后端。用户不能通过拖动节点直接改变运行中的 DAG；“插入节点”先生成 §8.2 patch 预览，应用后在安全点接入。

首版最小操作集：提交需求、编辑/校验角色配置、预览/应用节点插入、领取/响应人工握手、查看/处理监督意见、暂停新派发、恢复或取消具名任务、启停插件。只有项目授权允许的操作才可执行，拒绝时给出具体原因和恢复路径。配置凭证字段只接受引用，不在前端返回 secret。

本地入口默认仅监听 loopback，使用启动时绑定的会话凭据与同源校验保护写操作；只读工件读取限定为已注册项目的获准路径，禁止任意绝对路径读取。远程访问、多用户权限、互联网部署不纳入首版。UI 直接链接或展示项目状态文件与证据的获准内容，不另写一套“前端完成状态”。

### 8.5 工作流推荐、协同设计与多方评审

工作流定义也是可评审的交付物。默认提供一个可复用的 `workflow-design` 模板，使用已有请求、角色槽位、握手、Scheduler 和发布协议；不新增专用编排引擎。用户可在 Web 选择“根据当前项目推荐工作流”，描述目标、限制和已有团队，由此创建普通设计任务。

```text
需求 + 项目事实快照 + 可用能力 + 社区依据/适用经验
  → 集成者形成设计输入
  → 设计者推荐复用/增量修改/新建方案及理由
  → 生成候选 workflow 与结构化差异
  → 确定性校验 + 多个独立审核者评审
  → 必要返工与新版本复审
  → 集成者核验接收条件、发布版本
  → 在授权范围和调度安全点激活
  → 运行反馈进入知识闭环
```

| 职责槽位示例 | 责任 | 交付物 |
|---|---|---|
| 集成者 | 识别目标、原项目权威、已有流程和约束；协调依赖；收齐评审后接收发布 | 有来源的项目画像、设计任务书、接收/发布回执 |
| 设计者 | 检索已有模板和经验，比较方案，定义职责、DAG、输入输出、失败出口和验收 | 候选定义、差异、依据、取舍与验证计划 |
| 项目适配审核者 | 核对项目实际入口、消费者、写入边界、原证据与完成判据 | 独立评审意见及逐项证据 |
| 执行与可靠性审核者 | 核对可调度性、资源、权限、握手、恢复、版本切换与预算 | 独立评审意见及失败场景 |
| 可选专业审核/监督者 | 按项目增加安全、性能、数据或研究方法等检查；监督未解决阻断 | 专项意见和闭环证据 |

这些是模板职责槽位，不是内核固定角色枚举。用户可以改名、增加角色，按能力绑定 Codex、Claude Code、CodeBuddy 的模型 profile 或 Kimi。ABM 的唯一集成 owner 由 ABM 适配器带入；其他项目按自己的权限定义集成者，不继承 ABM 的人员或宿主绑定。Kimi 可承担一个独立评审槽位或额外监督，监督“在线”不能替代有效评审意见。

#### 推荐依据与业务解耦

ProjectAdapter 形成带 revision/digest 的设计输入快照，至少包括项目目标、入口规则、原任务/证据 owner、允许写入面、现有验证入口、可用 runtime/plugin 能力与预算。缺少必要业务信息时保留待确认项，不能靠社区模板补写项目事实；缺项会阻断依赖该事实的发布。

设计者先查模板注册表及已验证经验；需要社区参考时保存来源 URL、版本或获取时间、适用条件及采用/不采用理由。外部资料只是设计依据，不是项目授权。方案需说明为何复用、增量修改或新建；简单请求只需一个有依据的最小补丁，不强制生成多份相似方案。

通用模板只引用 capability、职责槽位、工件合同与 gate；业务命令、目录、领域证据和特有规则由 ProjectAdapter/GateAdapter 或项目配置绑定。同一模板可在不同项目使用不同 gate，完成条件仍须由各自项目明确。跨项目共享的是去除私有数据后的模板与适用合同，不能把一个项目的审核结论视为另一个项目已通过。

#### 多方通过与发布条件

设计任务创建时固定 ReviewPolicy 的版本与摘要，声明必需审核槽位、检查维度、独立性约束和通过条件。新建及变更 workflow 的默认门槛为：至少两个独立评审身份，所有必需槽位均通过、无未解决 blocking、确定性校验通过，以及具权限集成者的接收。可增加审核者；非阻断建议可以记录取舍，但不能用多数票覆盖必需审核者的反对。权限或原项目规则要求人工裁定时沿原出口执行，普通发布不额外强制人工审批。

独立身份指不同受派评审会话和可核验的 actor/attempt，作者不得计入自己的通过票，同一评审身份切换 role/model 不能算两票。独立审核者可以使用同一模型，但这不证明推理多样性；需要异构模型时在策略中明确。集成者参与设计时不能占用该候选的独立审核席位，也不能替他人签字。

用户确认将 CodeBuddy + `glm-5.3` 与 CodeBuddy + `kimi-k3-2` 作为两组推荐审核配置，实际职责可按项目和评测调整。它们各自建立独立 actor/attempt/session，不能复用执行者会话再自签。不同模型可能共享 CodeBuddy 账号额度和相同工具盲点，统一纳入账号组限额；CodeBuddy 中的 Kimi 模型 profile 与 Kimi Code CLI 的独立监督 session 是两种运行配置。

评审采用可核验覆盖矩阵：需求/合同条目 → 主审席位 → 交叉复核席位（按风险要求）→ 证据 → 结论。必需条目只能为通过、阻断或有理由且被策略允许的不适用，未检查和缺证据不能算通过。两组先独立形成意见，再讨论分歧；争议保留原意见与解决依据。多模型不是零遗漏保证，也不替代确定性校验与项目专项测试。

每份意见绑定 proposal revision/digest、项目输入快照、ReviewPolicy、插件/角色引用与证据，并通过现有握手发布。首版对任何候选内容修改均使旧通过票对新候选失效，必须复审；项目约束或依赖能力发生相关漂移也需刷新快照并重审。超时/缺席/无法复现是待处理状态，不算通过；可按既定策略更换审核者，但保留原意见和未解决问题。返工轮数与资源有上限，超限转待 owner 处理，不无限互审。

工具提供随发行版本固定的最小引导模板与评审策略，经项目 owner 首次选择绑定后即可使用；它不在每次运行时递归设计自己。对设计模板或 ReviewPolicy 自身的更改，必须由当前已授权的策略审查，新策略不能批准自身变更，不能通过生成一个更宽松的候选规避门槛。

`review_passed`、`published`、`active`、`run_succeeded` 分别表达评审通过、版本可引用、可供派发和实例成功。集成者发布以旧基线及 expected_revision 为条件，并引用完整通过回执；并发冲突重新核验，不把旧批准套在新配置上。真实启用仍遵守 §8.2 的安全点、原授权和资源限制；dry-run 与评审通过不冒充真实项目交付。

设计输入、候选、评审与发布原件复用 `coordination/requests/<id>/`，通过稳定 revision 文件保存历史；具体角色交接引用既有 `handshakes/`，不另建审批台账。Web 在候选流程旁显示依据、差异、各审核维度、有效票数/必需席位、阻断与返工轮次；点击发布前可确认确切的已审版本及生效范围。发布后的效果与失败继续引用同一请求进入 §9.1 的经验积累。

## 9. 插件边界与小型化约束

首版只设三类扩展接口：RuntimeAdapter（探针/启动/事件/取消/恢复）、ProjectAdapter（原任务/基线/工作树/证据定位）、GateAdapter（原有验证及接收判据）。Scheduler、Monitor、trigger、store、claim 和预算是固定内核。避免一开始把日志、锁和每张表都拆成插件。

插件注册声明 `id/version/api_version/capabilities/config_schema`；载入时验证兼容版本和必需能力，缺失 fail-closed。卸载先停止新派发、等待或取消本插件 attempt、释放资源，保留历史 receipt；不允许运行中替换实现后继续沿用旧版本身份。

角色定义、workflow 节点/模板也可作为声明式插件贡献，由同一 manifest 持有命名空间及版本；节点引用现有 RuntimeAdapter/ProjectAdapter/GateAdapter 的受支持 capability，不另造第四套执行引擎。插件可处于 registered、validated、enabled、draining、disabled 状态。启用/升级产生新可选绑定，active workflow 仍引用原版本；旧版本被在途 attempt 引用时保留到 drain 完成。名称冲突、配置 schema 变化及权限扩张须明确处理，不覆盖已存在的角色或模板。

插件管理入口提供 list/inspect/validate/enable/disable 与升级影响预览；依赖图显示“哪些角色、节点、workflow/run 正在使用该版本”。停用会阻止新的相关派发，已有任务采用显式 drain/cancel 策略；无法移除仍被引用的实现后假装运行可恢复。

默认只从本机明确安装的插件加载；任务文本不决定安装、升级或权限扩张。语言层插件不是安全沙箱，执行隔离仍靠 CLI 权限与 OS/容器。文件 allowlist 若只写进 prompt，只能叫约定；必须经宿主强制策略或隔离与接收检查才能形成可验证限制。

不建设多租户系统、消息总线集群、向量记忆库、插件市场或自己的模型 tool loop。首版包含轻量 Web 控制台、CLI 和宿主插件；Web 是同一状态投影的图形入口，不成为第二套任务权威。

### 9.1 知识积累与受控改进

闭环为：**运行观察 → 复盘候选 → 核验证据 → 检索复用 → 改进提案 → 对照评测 → 有界试用 → 激活或撤回**。它复用现有 Scheduler、角色、请求、握手和插件版本机制；“复盘者/改进者”只是可选角色模板，用户可按项目定义。Kimi 可发现问题或交叉监督，不能独自批准自己提出的改进。

#### 积累什么

| 层级 | 内容与证据 | 权威边界 |
|---|---|---|
| Observation | 失败码、超时、返工、握手缺件、版本冲突、人工纠偏、有效交付等原事件引用 | 已观察到的事实；不自动证明根因 |
| Lesson | 症状、原因/假设、适用条件、尝试及失败路径、修正、验证与反例 | 可复用经验；不能覆盖项目规则 |
| Improvement | 修改 prompt、路由、重试参数、增加检查节点、完善模板/插件的具体 patch | 引用 Lesson 的 ChangeProposal；未经激活不改变运行 |

经验条目包含稳定 ID、revision、作者、project/runtime/model/plugin 适用范围、问题指纹、来源 attempt/commit/事件、复现条件、原因是否已验证、修正及验证证据、反例、有效期限/复核条件、supersedes/retraction 引用。没有证据的原因明确标 hypothesis；记录失败的修复尝试，避免只保留成功故事。

运行终态、人工纠偏、新错误指纹和监督 blocking 可触发复盘。相同问题按指纹关联已有条目，每次出现只增加原事件引用；不每次心跳生成一篇总结。自动采集限工具已经授权可见的运行事实，脱敏后保存必要片段或引用；不抓取各宿主私有历史，不收集密钥、账户配置或完整敏感 prompt。

知识正文在项目的 `coordination/knowledge/entries/` 内按 revision 保存，可在 Git 中显式审阅；生命周期指针与评测回执沿 SQLite/outbox 发布，INDEX 为派生。新条目先是 draft，核验证据后可为 verified，再由检索策略显式选为 active；retracted/superseded 仍保留出处且不默认检索。验证为真与选择供任务使用是两回事，不能仅凭反馈点赞晋级。

项目已有 KB 时由 ProjectAdapter 指定原知识条目作为内容 owner，协作目录只存引用/索引；不新建同一 Lesson 的正文副本。涉及“系统应该怎么做”的结论，仍走原架构/规范变更；不能直接写进 AGENTS 或 skill 就绕过正式审核。

#### 怎样复用

在任务准入、失败恢复和交接时，根据项目、职责、问题指纹及运行时版本筛选经验，再进行关键词/全文检索；首版使用 Markdown 元数据与 SQLite 可重建索引，不引入向量数据库。只注入少量相关条目和证据锚，记录本 attempt 实际使用的 knowledge IDs/revisions/digests。任务中途新增经验供下一 attempt 使用，不悄悄改变当前输入。

检索内容按引用资料处理，不当作系统指令或额外授权。过期、冲突、撤回或版本不匹配的条目显式排除或标记待核，不在证据不足时强行挑一个。若关键安全原因撤回了在途任务使用的经验，按原撤回/暂停策略处置，不静默替换上下文。单次成功不扩展为所有模型、系统或项目都适用。

分三种范围：项目经验、运行时/插件通用经验、agent-coop 自身缺陷与改进。跨项目发布必须显式抽象适用条件、脱敏并获得对应共享授权；普通项目运行不会自动把内容写进用户全局知识库。本设计不读写 Codex 私有 memories；工具通用经验也不能隐式成为各业务项目规则。

#### 怎样优化与迭代

改善目标包括成功率、返工/交接缺件次数、有效完成耗时、可计量成本与人工介入量；先由 owner/既有评测策略固定主指标、不能退化的约束和样本范围，不能只追求“更快”而放宽验收。

改进者从 Lesson 生成最小 ChangeProposal，附原基线、候选版本和验证方法，走 §8.1 的请求入口。评测者与改进者分离，生成者不能修改测试集、评分器或结果。冻结评测集/holdout、输入、环境与运行时版本，记录无改动基线；调优案例与保留验收案例分开。离线回放只有覆盖相同语义时才可证明效果，否则以隔离样例或预授权的有界真实试用补证。

对非确定性模型至少记录试验次数、离散程度和失败样例；一次命中或不同难度任务之间的差异不能宣称改进。成本未知仍为 unknown；不能计量的指标不能作为自动晋级条件。候选数量、评测墙钟、调用次数和无改善停止条件预先有界；无新增证据不重复优化同一候选。

| 自动化等级 | 可自动完成 | 激活边界 |
|---|---|---|
| 记录与建议（默认） | 采集引用、去重、生成 draft Lesson 和改进提案 | 不自动改运行定义 |
| 离线优化 | 在授权预算内运行独立评测、比较候选、生成结果 | 评测通过形成待激活候选 |
| 有界自动试用 | 在预授权项目、参数范围、样本数和时窗内试用可逆配置 | 满足固定门槛后按既定策略激活新版本，否则停止/回退未来派发 |
| 规则或代码演进 | 可提出源码、插件、权限或规范变更并生成受审补丁 | 走正常工程评审与发布；不得自行修改审批、评分、权限、锁或沙箱来“优化通过率” |

自动试用沿已有 workflow 版本、RunAmendment 和 plugin pin，运行中的 attempt 不切换配置。模型/账号更换、权限扩张、验收阈值放宽、生产动作、Scheduler/claim 核心代码修改不属于默认自动激活集合。回退只影响未来派发，已经发生的副作用仍按 §8.2 处理。

学习工作作为低优先级、有独立预算的正常 workflow 进入同一 Scheduler；仅在存在新证据/有界评测任务时启动，不另开常驻 LLM 循环。自身优化也可暂停、追溯和撤回；不得因为标为“改进”而绕过项目并发、权限和握手。

#### Web 与人工操作

“经验与改进”页按问题、适用范围、证据状态和使用效果检索。条目展示来源、失败尝试、修正、反例、在哪些任务被引用，以及候选评测的基线/新值和未验证范围；可提出修正、请求复核、生成改进提案、查看试用和撤回。可从流程失败节点一键进入已有相关经验，也可将新的人工说明提交为待核候选。

例如：多次观察 CodeBuddy 交付缺少 task_head → 形成带原握手引用的经验 → 提议在交付前插入确定性校验节点 → 对历史正常/缺件样例评测并独立复核 → 在已授权样例 workflow 试用 → 发布模板新版本。旧任务继续沿旧绑定，未通过候选保留失败原因，不成为默认经验。这个例子说明流程，不代表本次已观察到该故障或已获得改善数据。

## 10. 按依赖推进的实现切片

| 切片 | 交付物 | 退出条件 |
|---|---|---|
| P0 复用裁定 | OMA 扩展点核对、四运行时能力矩阵、ACP 依赖提取边界、Desktop 接入验证 | 固定一个派发底座；无“先自研再比较”；四端版本和权限合同可验证 |
| P1 只读纵向贯通 | 协作文件、项目设计输入快照、候选/需求预览、原任务 reader、Scheduler dry-run、Monitor、Web 流程/详情及经验文件入口 | 页面与文件同 revision，原业务状态只读，能定位问题证据 |
| P2 有界真实执行 | 四运行时、握手、监督、终态/纠偏观察采集与 draft Lesson | 真实交付可复核；复盘引用真实来源，未核原因不升格为规则 |
| P3 持久协同 | Scheduler/恢复、Web 操作、增量入队、安全点插入、按范围检索经验 | 在途身份稳定；经验引用可追溯，撤回/不适用条目不默认注入 |
| P4 插件与项目接收 | 角色/插件管理、workflow-design 模板与多方评审发布、Desktop/ABM 接收、改进提案与独立离线评测 | 至少两种不同业务的隔离样例经适配器使用同一模板；不重复派发；候选不自评自激活，效果可与基线比较 |
| P5 可选受控优化 | 预授权范围内的有界试用、版本激活与撤回 | 配置预算/指标/停止条件齐备才启用；无实证改善不晋级，不扩大权限 |

最小试点选“一个文档/代码切片 → 一个独立评审 → Kimi 监督一个预置证据缺口 → 修复与独立复核 → 一个 owner 接收”，先在隔离样例仓库验证；ABM 先 observe，随后才选无 Thor、无共享 proof 写入的有界业务包。交易系统不以线上研究/交易运行作为首个试点。

## 11. 必须可否决的验收

1. 同一任务重复触发及两个 coordinator 同时启动，只产生一个有效 claim；新配置不改变在途身份。
2. child 已启动而 coordinator 未登记完即退出，重启能识别旧 attempt，不再起第二个 writer。
3. lease 过期但旧进程仍活着，不抢同一树；迟到回执因 epoch 失配被拒。
4. 取消后无本 attempt 残留进程；不终止人工或其他会话的进程，不删除未提交工作。
5. CLI exit 0 但无要求产物、假 PASS 文本、review 缺席、review HEAD 陈旧都不能交付/接收。
6. CodeBuddy 的两个模型 profile 共用账号组容量；模型不可用、usage unknown、认证过期均可明确解释。
7. Desktop 已认领时 CLI 不能同时派发；Desktop 离线不自动证明其工作树可回收。
8. ABM 无关主线提交不触发全量验证，相关输入改变只走原 selector 的差集；所有领域状态仍由原 owner 写入。
9. 外部裁定阻断允许切换无依赖备用包；没有就绪任务不反复调用 LLM“继续”。
10. 工作机睡眠/重启后合并错过的 tick；路径含空格和中文、Windows 进程树及 stdin UTF-8 均实际验证。
11. 插件升级、权限策略变化及新增依赖只用于新 attempt；缺能力不降级成 unrestricted。
12. 运行库损坏或丢失时暂停自动写入，依据进程与仓库原证据恢复；不推断所有任务未开始而全量重派。
13. Kimi 发现预置 blocking 后，受影响接收被阻止而无关切片继续；实现者伪造 resolved、缺席监督、过期输入意见均不能放行。
14. 同一监督输入只触发一次有效审查；并行意见追加不覆盖历史；纠错保留原文和反证链；换监督会话不重跑相同验证。
15. 人工权限等待、长工具执行、进程假活、无新进展和观测过期在监控中可区分；监控离线不显示全绿，不触发第二 writer。
16. why 的等待原因、下一调度和实际 Scheduler 决定一致；暂停仍可观察状态；定时与事件同时触发不重复执行；老任务不会因不断接收新任务永久饥饿。
17. 不改代码即可新增自定义角色并绑定模板槽位；角色改名不改变权限，循环依赖/缺失角色引用/不满足能力或独立性时拒绝派发；停用和配置变更不篡改在途 attempt。
18. 请求已发但未 ack、ack 后无评审结果、接收者错误、输入 revision 过期和重复 key 内容冲突均不能解锁下游；返工保留前一轮完整握手。
19. 数据库提交后文件发布失败，重启只补发同 ID 记录，不重复执行；current/STATUS revision 不一致明确显示 publication_pending，关键下游继续阻断。
20. 两棵业务 worktree 使用同一协作根；人工能从 STATUS 追到双方原件和证据；手改生成状态不会静默生效，决定文件必须经显式校验导入。
21. 新需求复用现有模板直接入队；插入 N 时仅改变显式依赖边，原版本可追溯；V 已运行时不能宣称当前实例已满足新增前置。
22. 并发配置变更通过 expected_revision 拒绝冲突；新插件不覆盖已有命名，升级不改变在途绑定，disable/drain 不丢失待处理握手。
23. 人工从 request 原文、patch、校验和结果追到新调度任务；模型曲解的需求可在应用前纠正，applied 不显示成业务完成。
24. Web、CLI、文件对同一 revision 展示一致；丢失 SSE/重复事件/重连不误显示完成；断线明确 stale，浏览器关闭不终止调度。
25. 普通用户不读 YAML 即可提交需求、预览新增节点、选择角色、看到握手阻断并处理本人有权决定的事项；所有操作可追到原文件与后端回执。
26. 图与任务列表语义相同，键盘可达，状态不只靠颜色区分；未应用节点、旧版本、未知状态与真实运行不能混淆。
27. 相同故障去重但不丢原始引用；hypothesis/draft 不能冒充已验证经验；运行时版本不匹配、撤回和相互冲突的知识不静默进入任务上下文。
28. 改进者不能修改评分器或自签结果；失败/退化候选不能激活；单次成功不宣称普遍提升，成本未知不算更省钱。
29. 知识与改进记录位于项目下，Web 能追到来源/适用范围/基线及结果；跨项目分享需要显式授权，密钥和私有宿主历史不自动采集。
30. 自动优化占用既有调度资源并有独立硬预算；权限/规则/核心代码变更进入正常工程审核；激活/撤回不改写在途 attempt 或历史证据。
31. 推荐方案引用可核验项目快照、模板与经验/社区依据；必要事实缺失不能生成假定已成立的可发布方案。同一通用模板经两种项目绑定运行，内核不含领域命令或固定宿主角色。
32. 少于两个独立审核身份、作者自审、同身份重复投票、缺必需席位、存在 blocking、票据版本过期或校验失败均不能发布；结构化配置入口也不能绕过此门槛。
33. 候选修改、相关项目约束漂移与并发基线冲突不能复用旧通过票；审核超时不视为接受，返工到达上限停止自动迭代。
34. 设计流程的引导模板可直接运行而不递归生成自身；候选不能修改审查自己的策略；Web 分开展示已评审、已发布、已激活和实例实际成功。
35. 更换执行者为 OpenCode 或其他已注册适配器时，保留角色和工作流合同；所需能力缺失、模型标识未解析或账号不可用时明确阻断，不改内核、不静默回退。
36. 模型建议引用当前清单快照与能力/评测出处；未知能力不冒充已验证，静态可选不冒充账号可用；用户确认的绑定不被清单刷新覆盖，在途 attempt 保持原配置。

## 12. 评审点与后续吸收

推荐确认三个相互关联的决定：小型独立工具加薄插件的产品边界；原项目任务/证据继续为权威；首版先只读纵向贯通再开启真实调度。语言和目录选择是实现建议，P0 可用复用证据修正。

仓库初始化已获授权；各实现切片仍需形成可执行计划并完成相应设计评审。通用实现由本仓维护，交易系统与 ABM 的接入规则仍由各项目维护；若提取 ACP，则由独立迁移变更同步共享内核架构与现有消费者。当前不修改既有角色表、ABM 计划、研究平台权限或宿主自动化设置。

社区资料随版本变化。尤其 OMA/OmO 的名称和宿主变化、DSH preview 接口、Claude session 调度语义均需固定版本核对。[Claude 调度文档](https://code.claude.com/docs/en/scheduled-tasks)明确区分 session 内任务、Desktop 任务与云端 routines；不能把一种载体的恢复能力外推给另一种。

## 13. 研究来源与当前交付边界

本设计从交易系统会话草案提取，保留可复用结论、社区来源及未验证范围。业务项目路径、账户与工作机配置由用户显式绑定，不作为公开文档中的安装依赖。来源摘要见 [导入记录](research/design-import.json)。

原项目草案的生命周期及 R19 检查仅证明原文档治理有效，不证明本工具实现。本仓初始化验证覆盖文档链接、YAML 示例、默认执行者配置与 Git 状态；未启动真实 agent、后台调度或 Web 服务，未完成任何运行时验收。

后续每个切片在 [实施路线](roadmap.md) 更新实际完成证据；产品设计、实现通过、多方批准、发布激活分别报告。

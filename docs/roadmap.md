# 实施路线

这是产品切片路线，不是已批准的逐步实施计划。完整验收条件见 [产品设计](design.md)。

## 当前交付

- 2026-10-10：用户授权新建独立仓库；通用设计从交易系统草案提取。
- 仓库初始化包含 README、统一 agent 入口、设计、扩展约定和拟议配置示例。
- Scheduler、Web、CLI/MCP、插件、知识检索和 RuntimeAdapter 均未实现。

## 当前开发团队与调用约束（2026-10-10）

以下为本仓当前唯一绑定位置；属 Scheduler 未实现前的临时人工协作安排，不是已实现的 Scheduler。产品实现后由 design §5.1 的 `team.yaml` 承接角色绑定，roadmap 届时只引用它，禁止形成双权威。

| 角色 | 绑定 | 职责与独立性约束 |
|---|---|---|
| 集成者 / 派发者 | Codex | 负责拆分、排序、工作树分配、派发 CodeBuddy、收集交付、组织评审、验证与集成；维护准确的当前工作状态；参与作者时不能算独立评审票 |
| 实现 / 执行 | CodeBuddy + `deepseek-v4-pro` | 负责受派实现；本轮规范初稿由其修订，不能占用独立评审席位 |
| 项目适配 / SSOT / SOLID 主审 | CodeBuddy + `glm-5.3` | 独立 actor/session，不得是作者 |
| 执行可靠性 / 边界 / 验证主审 | CodeBuddy + `kimi-k3-2` | 独立 actor/session，不得是作者 |
| 独立监督者 | Kimi Code CLI | 监督派发、实现、评审、集成的边界及证据；核对当前状态并推动过时/矛盾项处置；使用独立会话，不兼任本轮作者或必需评审席位 |

- 当前由 Codex 人工派发不冒充产品 Scheduler；产品实现后，Codex 通过 Scheduler 入口提交请求，由 Scheduler 执行身份、资源与状态校验。
- 两组评审须为独立 actor/session，且都不能是作者本人。
- Kimi Code 已由用户明确要求加入本仓开发：Codex 在规范/计划接收前及关键实现批次交付时，派发有界只读监督。检查是否推进既定出口、越过唯一写入边界、漏验或重复计算、放宽范围/判据、通过及关闭是否有原件。意见保存在同一请求目录；有 blocking 时阻断对应接收，修正后由该监督会话或具名独立替补复核。它不替代两组 CodeBuddy 必需评审，也不以监督在线代替有效意见。所需监督缺席时保持待监督，不自动降级或冒充通过。
- Claude Code：用户声明额度耗尽，暂停所有新派发；不自动恢复，恢复需经显式配置变更与可用性核验。
- 共享 CodeBuddy 账号额度设临时调用上限：并发 2、每轮 max-turns 20；额度充足不代表无限并发预算。本次修改与复审合计最多 2 轮，超限交 owner 具名处置。
- Kimi Code 与 CodeBuddy 的 `kimi-k3-2` 是不同 runtime/session，分别核验能力和实际模型身份；当前 Kimi Code 使用宿主已配置的默认 profile，调用时记录可观测的模型信息，未知保持 unknown，不静默替换。监督并发 1、单次最长 10 分钟，由 Codex 手工看护和在超时后停止本次调用；CLI 未提供 turns/token 硬限时明确记为未实施，不宣称产品预算门禁已实现。
- 当前分配仅适用于本仓，不继承 ABM owner。

## 当前产品切片：隔离纵向样例（G0已接收，离线实现中）

用户于2026-10-10授权继续实现，并选定仅隔离样例跑通多agent、归档、本机副本与清理。Codex集成，CodeBuddy实现/双席评审、原生Kimi监督。当前为 [复用裁定](../coordination/requests/isolated-workflow-20261010/reuse-decision.md) 与 [具体计划](../coordination/requests/isolated-workflow-20261010/implementation-plan.md) 的G0已接收，证据见[接收记录](../coordination/requests/isolated-workflow-20261010/result-g0.md)；当前进入测试先行的离线实现，尚未通过G1或实跑。计划先验证只读/模拟层，再经G1审核开放有界实跑；不宣称完整P1/P2/P3已交付，不启用OS定时任务。

最近交付的接收与 Git 集成证据见下方历史入口；本节只维护有效下一步，不复制回执或另建状态台账。

## 历史交付入口

- 开发交流与归档（communication-archive-20261010）：候选 `8e8f6f054c972e27dd234adf31a29ffbf12471bd` 已接收，社区依据、两席评审、原生监督与本人澄清、集成状态见 [结果](../coordination/requests/communication-archive-20261010/result.md)。AGENTS 维护人工操作，design §5.2 维护技术合同；自动采集、归档备份、保留清理尚未实现。

- 文档组织规范（docs-organization-20261010）：候选 `25690df055a09ea71c7edb4dba163e191b5e9857` 已接收，规则归 AGENTS、导航归 README；社区取舍、两席独立评审、Kimi Code 监督与 Git 集成状态见 [结果](../coordination/requests/docs-organization-20261010/result.md)。自动门禁尚未落地，继续沿 P0/P1 出口推进。

- 图集修订（diagrams-review-20261010）：新候选已接收，首轮 B1–B3 已闭合，候选、实现、两席复审、独立监督与合入状态统一见 [结果](../coordination/requests/diagrams-review-20261010/result.md)；未实现产品功能。

- 阶段角色、触发与经验吸收（role-experience-review-20261010）：已接收并在 main cb0793d 合入，证据见 [结果](../coordination/requests/role-experience-review-20261010/result.md)；design §4.2/§7.1/§7.4/§7.5/§7.6/§9.1 及验收47–54继续有效。Jev 仍沿 P0 调研→P4 离线评测→P5 受控激活，未启用。

- 工程规范与团队自举（bootstrap-engineering-20261010）：已接收，规范与团队约束继续有效，候选及评审链见 [请求](../coordination/requests/bootstrap-engineering-20261010/request.md)；已完成步骤退出当前视图。
- 前端续作与状态维护（frontend-state-contract-20261010）：已接收，其合同继续有效，证据见 [请求](../coordination/requests/frontend-state-contract-20261010/request.md)；当前合同补充入口已由 role-experience-review-20261010 取代。

## 按依赖推进

| 阶段 | 范围 | 退出证据 |
|---|---|---|
| P0 复用裁定 | 核对 oh-my-agent 与其他候选底座、既有 ACP 提取边界、四运行时和 OpenCode 扩展面、配置目录发现 | 固定一个底座；许可证/依赖边界、能力矩阵和选择理由明确；没有先重复自研再比较 |
| P1 只读纵向贯通 | 项目快照、状态文件、候选流程、dry-run、轻量 Web；探索项目与配置推荐仅提供只读表单/dry-run（无真实模型驱动，见 design §8.1） | 同 revision 的状态投影与证据导航；不执行真实模型任务；前端首版可见但未实现动作明确禁用/演示，不假活跃 |
| P2 有界执行 | 推荐执行者、其他初始运行时、交付握手、独立评审、Kimi 监督、观察采集；实际模型驱动自然语言探索/推荐与真实启动/暂停/恢复（受控样例，见 design §7.8/§8.1） | 隔离样例实际交付、取消与缺证据阻断；真实启动/暂停/恢复可复核，不冒充生产接入 |
| P3 持久协作 | 调度恢复、资源与权限、动态入队/节点变更、适用经验检索；崩溃后持久恢复（暂停持久、断续开发续作，见 design §7.8） | 崩溃不重复派发；在途身份稳定；状态可解释；暂停与断续开发跨重启持久恢复 |
| P4 插件与通用流程设计 | 多角色推荐与多方评审、插件管理、Desktop/项目接收、离线改进评测 | 两类不同项目使用同一通用模板；评审与发布版本可追溯 |
| P5 可选受控优化 | 有预算的试用、效果对照、激活与撤回 | 无实证改善不晋级；不扩大权限 |

P0 复用裁定、能力证据与隔离样例的具体计划已形成候选，见上方当前切片。G0 接收前不写产品源码；接收后按该计划先验证只读/离线层，经 G1 后开放隔离样例实跑。

2026-10-10 用户授权的隔离纵向样例在限定范围内承接 runner、执行适配与只读 Web；它不代表上述完整产品切片均已完成。先选型/计划审核、再离线验证、再受审实跑的依赖顺序保持有效。

“最终执行者推荐 CodeBuddy + DeepSeek V4-Pro”不意味着设计、集成和审核全部交给它。团队角色按用户配置，各项身份独立性及项目原 owner 合同保持有效。


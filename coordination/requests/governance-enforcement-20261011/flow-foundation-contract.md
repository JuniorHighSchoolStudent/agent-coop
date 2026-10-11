# 流程观察与阶段职责基础合同

状态：后继待审候选，未批准、未实现；本文件只规定两个可独立实施的小包，不授予模型调用资格。维护责任：本请求合同集成者；实际作者为受派 CodeBuddy + `deepseek-v4-pro`，独立双席及 native 监督沿当前请求规则。当前状态仍由 [result.md](result.md) 维护。

依据：[design §4](../../../docs/design.md#4-用户操作与核心模型)、[§7.6](../../../docs/design.md#76-状态监控)、[§8.2](../../../docs/design.md#82-插入节点与在途工作流)、[流水线提案](pipeline-amendment.md)、[实施合同](implementation-contract.md)。本候选不改变在途输入，不以旧票放行新增范围。

## 1. 复用裁定和交付边界

已检索 `agent_coop/`、`tests/`、既有实施计划：当前没有 Monitor、通用阶段职责校验、ChangeProposal 或 RunAmendment 的产品实现。`sample.py` 的固定四角色是样例；`gates.py` 是样例接收，均不承担新通用职责。
复用 `store.py` 的 `_mutate`、revision、events/outbox、`publish`；复用 `runner.py` 为唯一驱动入口。当前 Store events 保存状态快照，Runner 同步执行固定步骤，尚不具备本合同完整闭环，不能直接删锁并行调用旧样例。

| 包 | 唯一产品和测试写集 | 独立交付 |
|---|---|---|
| M 确定性流程观察 | 新 `agent_coop/monitor.py`、新 `tests/test_monitor.py` | 纯值观测分类、变化事件和请求提案建议；不读进程、不执行取消或派发 |
| T 阶段职责合同 | 新 `agent_coop/stage_contracts.py`、新 `tests/test_stage_contracts.py` | 可配置职责、绑定、DAG 和声明覆盖的静态校验；不判断实际履责或审批完成 |

M/T 无相互实现依赖，接口冻结并独立准入后可先派这两个就绪作者；总作者容量沿当前可配置最多并行4的安排，不建立固定2路上限。其他已就绪独立包可使用剩余容量。各包须有效作者 final、相关验证和独立评审；纯接口完成不等于监控到补发已产品化。

## 2. 共用值规则

接口只接收普通 dict/list/str/int/bool/null；不读文件、环境、时钟、网络、Git、Store 或进程，不调用模型，不修改入参。输入对象只允许下表字段；缺键、未知键、错误类型以 `ValueError` 拒绝，不能先返回部分成功报告。
`ID` 为非空字符串；`SHA` 为64位小写十六进制；`N` 为非负精确 int，bool/float 不合格；`P` 为正精确 int。所有列表为有序列表，除明确允许空外非空，同一标识不得重复。
`Ref` 精确为 `{artifact_id: ID, sha256: SHA}`；只绑定源身份，不携带可执行路径。純函数不证明源存在、真实或已经授权；C/D 必须从固定原件装载并重核。`Refs` 为非空、按 artifact_id 唯一的 Ref 列表。
通用摘要使用现有 `store.canonical_digest` 的同等规范语义：UTF-8、键排序、紧凑 JSON、ensure_ascii=False、拒绝非有限数；不得为了纯函数导入产生 Store 实例或 I/O。实现可复用该现有纯函数，不另建摘要工具模块。

## 3. M 输入：`evaluate_flow(observation, policy, previous)`

`observation` 精确字段如下；所有时间差使用调用者采集的同一 clock_epoch 单调毫秒，不把 UTC 时间用于耗时判断。

| 字段 | 类型与含义 |
|---|---|
| schema | 固定 `flow-observation/1` |
| observation_id、work_ref、attempt_id、clock_epoch | ID；调用者绑定真实工作/attempt，一次采样ID不得跨不同内容复用 |
| subject_digest | SHA；固定候选身份 |
| now_ms、sampled_ms | N；分类时刻与最后真实采样时刻，sampled_ms ≤ now_ms |
| source_refs | Refs；支撑本观测的原始记录，不接受模型自报替代机器事实 |
| process | 固定对象 `{status, identity_ref}`；status 为 alive/exited/unknown；identity_ref 为 Ref 或 null，非 unknown 必须非 null |
| runtime | 固定对象 `{status, started_ms, last_event_ms, activity_deadline_ms}`；status 为 running/tool_running/auth_required/blocked/unknown；后三值为 N 或 null，started_ms/last_event_ms 不得大于 sampled_ms |
| progress | 固定对象 `{last_progress_ms, artifact_refs}`；前者 N 或 null且不大于 sampled_ms；后者 Ref 列表可空；非 null 必须有实际进展工件引用 |
| evidence | 固定对象 `{status, checked_ms}`；status 为 current/stale/unknown；checked_ms 为 N 或 null且不大于 sampled_ms；current 必须有 checked_ms |
| blockers | 可空列表，每项 `{blocker_id: ID, owner_role: ID, status, due_ms}`；status 为 open/closed/unknown，due_ms 为 N 或 null；blocker_id 唯一 |
| resources | 固定对象 `{status, reason}`；status 为 available/blocked/unknown；reason 为 capacity/budget/null；仅 blocked 时 reason 必须非 null，其余必须 null |

`policy` 精确为 `{schema:'flow-monitor-policy/1', policy_ref:Ref, runtime_idle_ms:P, progress_idle_ms:P, evidence_max_age_ms:P, observation_max_age_ms:P}`。阈值必须来自已审配置，不提供暗设默认值；这些诊断阈值不替代 runtime 单次硬截止或资源准入。
`previous` 为 null 或 `{clock_epoch:ID, sampled_ms:N, policy_ref:Ref, active_reasons:[reason...]}`；active_reasons明确可空，reason见第4节，key唯一且须按本次工作/attempt/候选重算一致，policy_ref须等于本次policy_ref。同epoch的sampled_ms不得倒退；这是同Store上次报告的投影，不是第二状态库。
observation 内非 null 单调时间全部属于声明的 clock_epoch；上游不能将重启前时钟值改标签复用。纯函数只能验证结构/顺序，不能证明实际采集来源。

## 4. M 输出和精确分类

输出精确为 `{schema:'flow-monitor-report/1', observation_id, work_ref, attempt_id, subject_digest, clock_epoch, sampled_ms, policy_ref, active_reasons, events, recommendations, unknowns}`；身份/时钟字段及policy_ref按输入逐值保留，跨epoch例外见下文；后四个列表均可空。
每个 reason 为 `{key:SHA, kind:ID, subject_id:ID, source_refs:Refs}`；kind 只允许下列判据产生的值。subject_id 普通原因为 attempt_id，单个 blocker 原因为 blocker_id；key 对 `[work_ref,attempt_id,subject_digest,kind,subject_id]` 规范摘要。
每个 event 为 `{key:SHA, transition:'opened'|'resolved', observation_id:ID}`；本次新增 key 产生 opened，上次存在而本次不再成立且已获明确反证的 key 才产生 resolved。重复采样不会持续产生 opened；S 以 observation_id 和内容摘要再核重放冲突/幂等。

| 事实与判据 | active reason / unknown；不包含取消或重试权限 |
|---|---|
| now_ms - sampled_ms > observation_max_age_ms | `observation_stale`；不据本次其他陈旧维度产生新原因或 resolved，保留previous reasons为未决，unknowns含observation，不推断进程退出/资源释放 |
| 新鲜采样，process.status=exited | `process_exited`；不等于成功、final、tree_empty 或接收 |
| process=alive、runtime=running | 以 last_event_ms 为起点；为 null 时用 started_ms；两者皆 null则 runtime unknown；now_ms-起点 ≥ runtime_idle_ms 产生 `runtime_stalled` |
| process=alive、runtime=tool_running | activity_deadline_ms 非 null且 now_ms ≥ 它才产生 `runtime_stalled`；无截止为 runtime unknown，不沿 idle 阈值误判长工具 |
| runtime=auth_required | `auth_required`；不同时以流静默产生 runtime_stalled |
| process=alive、runtime=running、last_progress_ms 非 null | now_ms-last_progress_ms ≥ progress_idle_ms 产生 `progress_stalled`；重复流事件不刷新进展；进展起点未知则 progress unknown |
| evidence=stale，或 current 且 now_ms-checked_ms > evidence_max_age_ms | `evidence_stale`；unknown/缺采样不能当 current |
| blocker=open 且 due_ms 非 null、now_ms ≥ due_ms | 对该 blocker 产生 `blocked_overdue`；未知状态或未知 due 保持 unknown |
| resources=blocked | reason=budget 产生 `budget_reached`，reason=capacity 产生 `capacity_wait`；unknown 不当可用 |

`unknowns` 是去重 ID 列表，值限 clock_changed/observation/process/runtime/progress/evidence/resources 或 `blocker:<blocker_id>`。未知维度不能使其 previous reason resolved；blocked/auth/tool_running 对 progress 是不评估，保留旧 progress 原因未决。process_exited 原因在该 attempt 后续观测中不可清除；冲突 alive 输入记录 process unknown并保留该原因，不复活旧attempt。
跨epoch优先于表中判据：仅保留previous reasons、unknowns含clock_changed，events/recommendations为空，报告保留previous的clock_epoch和sampled_ms，不能用本次时钟替旧原因重新标期。须由S具名对账后另行建立新epoch基线，不在M自动重启计时或解除原因。
新成立reason使用本次source_refs，未决旧reason保留原source_refs。process/runtime/evidence/resources的unknown状态均加入同名unknown；runtime=unknown/blocked时不评价流静默，保留旧runtime原因；process=unknown时同时不评价runtime/progress，保留相关旧原因。
每个 recommendation 精确为 `{action:'request_proposal', cause_keys:[SHA...], affected_work_refs:[ID...]}`；仅本次新 opened 的 runtime_stalled/progress_stalled 生成一个合并建议，cause_keys 排序，affected_work_refs 固定 `[work_ref]`；其他原因不自动提出拆包。建议不是批准，不含子包、修改、模型选择、预算增加或启动动作。
同epoch新鲜采样解除observation_stale；runtime已按表评估且未超阈值解除runtime_stalled；progress已按表评估且未超阈值解除progress_stalled；runtime=running/tool_running解除auth_required；evidence=current且未过期解除evidence_stale；blocker=closed解除该blocked_overdue；resources=available解除budget_reached/capacity_wait。其余情形保留旧原因，包括退出后的未决原因，记录消失不构成闭合。返回排序固定：reasons/key、events/key再transition、unknowns字典序；recommendations 为零或一个。

## 5. T 输入：`validate_stage_contracts(workflow, roles)`

本包只验证模板声明的业务/工程职责覆盖；它不复制 development-review-policy 的必需审核/Read 条件。工具角色、业务职责、runtime/profile和账号仍分别绑定。
`workflow` 精确为 `{schema:'stage-contracts/1', workflow_id:ID, revision:P, workflow_bindings, coverage_requirements, stages}`。
`workflow_bindings` 为非空 `{slot_id:role_id}` 映射，键和值均 ID，均由模板配置；无内核保留角色名或 gstack 枚举。未被 stage 引用的 slot 拒绝，防止未解释的绑定。
`roles` 为非空 role_id 映射；每值精确 `{contract_ref:Ref, profile_ref:Ref, requires:[ID...], independent_from:[role_id...]}`；两列表可空且唯一。role_id 自定义；允许未被本 workflow 使用的角色存在，但所有 independent_from 引用须存在且不能自指。
每个 stage 精确为 `{id:ID, slot:ID, depends_on:[stage_id...], input_contract_refs:Refs, output_contract_refs:Refs, coverage_ids:[ID...]}`；depends_on和coverage_ids可空，列表唯一；stages非空且 id唯一。
每个 coverage requirement 精确为 `{coverage_id:ID, contract_ref:Ref, required_stage_ids:[stage_id...]}`；coverage_requirements非空且 coverage_id唯一，required_stage_ids非空且唯一。它是同一已版本化 workflow 内的声明，不另建职责台账或独立可变 policy。
每个 stage.slot必须存在且映射到已有 role；依赖须存在、非自指、无环。每个 stage.coverage_ids必须引用已有 coverage_id；每条 requirement 的全部 required_stage_ids必须存在并实际声明该 coverage_id；其他 stage允许额外声明同一已知coverage。
结构正确但上述引用/覆盖/DAG语义不成立时返回报告中的 violations，不抛半途异常；schema/类型错误仍按共用规则 ValueError。所有 Ref 只检查声明身份，不判断自然语言职责、输入输出语义兼容或 profile实际能力。

## 6. T 输出与职责隔离

输出精确为 `{schema:'stage-contract-report/1', workflow_id:ID, revision:P, valid:bool, coverage_mapping, violations}`；后两个列表可空；valid仅表示上述静态合同检查无 violations，禁止解释成 approved/accepted。
coverage_mapping为按 stage_id排序的列表，每项 `{stage_id:ID, role_id:ID, coverage_ids:[ID...]}`；只输出可完整解析引用的stage，coverage_ids排序。映射源于模板slot绑定，不从职责文字、模型名称或role_id猜授权。
每项 violation 精确为 `{code:ID, location:ID, related_ids:[ID...]}`；code限 UNKNOWN_ROLE/UNKNOWN_SLOT/UNUSED_SLOT/INVALID_INDEPENDENCE/UNKNOWN_DEPENDENCY/DEPENDENCY_CYCLE/UNKNOWN_COVERAGE/UNKNOWN_REQUIRED_STAGE/MISSING_COVERAGE；location采用字段路径，related_ids排序；整体按code/location/related_ids排序。
工程、QA、体验、性能、产品等业务职责由 contract_ref/coverage_id 表达；produce/review/supervise等仅为模板可选slot。新增业务职责或角色不修改本模块枚举；同人兼任是否违反实际审核独立性仍由A核actor/session原件，T不得替A签票。

## 7. 必须执行的有意义测试

M：同值输入确定且深拷贝比较无入参修改；healthy→healthy且previous.active_reasons为空；阈值恰等/前后边界；长工具/权限等待；有流无产物进展；缺值unknown；跨epoch不误闭合；旧采样不生成退出/释放；观察重复与开闭再开；同attempt已退出后alive冲突；建议不含自动派发；严格int/未知键/坏Ref拒绝。
T：非预设角色和职责可成立；一个角色多slot、两个角色同profile声明不冒实际独立；缺覆盖/未知slot/悬空依赖/环/独立性自指；必需覆盖跨多个stage全AND；无源码、文件或进程I/O；无入参修改；同值确定；错误类型与未知字段拒绝。
两包各用表驱动fixture覆盖正反例，遵循AGENTS规模标准；不得用压缩行凑指标。复用现有 unittest 命令入口，分别运行 `python -B -m unittest -v tests.test_monitor` 与 `tests.test_stage_contracts`；作者记录真实结果，不以计划命令冒测试通过。

## 8. 后继接线、依赖和闭环验收

本片M仅为attempt观察；“有ready工作但零执行者”“待审积压”不在本接口输入范围，不能宣称已经识别。它们由本请求必需后继M-Q承接：同monitor.py owner顺序增加`evaluate_queue(queue_snapshot, policy, previous)`，S提供同revision队列/全部角色claim及既有准入结果，M-Q只分类等待与积压，X唯一补发。准确字段及判据在该片派发前独立冻结；不另建队列、状态或资源算法。该项与S/X接线均是本请求未完成工作，不移作可选远期功能。“从未有checkpoint”本片保持unknown，不能冒充已知起点后的progress_stalled。

R2唯一采集可信进程/流/终态；M不复制原生parser或进程看护。S唯一在现有DB保存观测报告、去重事件和待办；previous由该Store读取，重复observation_id不同内容拒绝，重放不能再扣预算或派发。
D消费M建议，绑定配置中的提案角色，沿既有ChangeProposal准备准确基线、原因原件、拆分写集/依赖/剩余验收和未闭合finding。T校声明；C重核原件并调用A/B，A仍唯一核角色、阶段、独立票和必需前置。提案可拒绝拆包而采用具名诊断，不能将确定性阈值当业务根因证明。
S在批准后CAS应用RunAmendment及后继就绪动作；X作为唯一协调入口消费事件、统一claim并补发，不另建循环/Store。旧writer身份未知时禁止同写集新派；新版本不得继承无效旧票或清空用量/blocking。暂停、账号容量、资源互斥和实际依赖receipt仍约束全部角色。
原S/D/X/A/C/R2/C2写集owner不变；本次不授权M/T改它们。扩大的S/D/X应由各owner顺序交付依赖小片，不并行写同文件，也不将整条链塞入一个20-turn包。M/T可先独立开发接收；接线需要真实上游并重新受审，不用mock报告冒组合通过。
最终必须举证：可信观察→原因事件→准确拆包提案→独立双审及监督→批准版本应用→Scheduler补发；快包审核不等慢包、局部返修不阻断无关包、重复/乱序事件幂等、暂停后不启动、未知旧进程不重试、共享账号不超额。纯测试之外须由受管入口实际派发必要工作并独立验收；此前只能称M/T基础接口完成，不能关闭整条治理闭环。

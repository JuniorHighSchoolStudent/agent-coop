# S1现场问题最小后继修订提案（未批准）

范围：S1准备与运行暴露的会话声明、读取计划派生、严格final和看护身份问题；维护者：Codex合同调查/集成者；状态：候选，待S1结果汇总后具体审批，不是已修复、已正式复审或新增调用准入。基于冻结候选`dc37ae62a0aa8b40e0d881a364a6ddd190c0e146`的[后继合同](implementation-contract.md)、[运行时计划](runtime-integration-plan.md)与[分批计划](dispatch-sequence.md)。本文仅新增，不修改S0/S1输入、模型原票或历史调用。

现有两轮S0/S1双席调用已经使用，共4次CodeBuddy、0次native；S1两席均已结束，但完整final严格JSON无效且真实读取缺17–18行，尾部PASS均不计有效票。本文提出下述一次性追加复核申请，不自行授权任何调用；原拟议52/8亦不是可自行支用的额度。状态、最终证据指针与批准仅在原[result](result.md)维护。

## 1. fresh native未请求session ID，不可倒填

**现场与边界。** 已只读核`run-supervision-g1.ps1`第26行：fresh分支仅传agent-file/prompt/output-format，没有session参数；第28行也标明实际session要等resume_hint。`requested_session_id=null`表示本次未指定原生会话，不表示actual未知，更不能据此断言整个runtime不支持预选。旧[contract](contract.md)第76行未定该字段类型，第88行无条件写requested/actual不符即无效，存在歧义；长期design的准确实际身份与独立性要求不变。

**最小合同澄清。** 仅明确既有字段：requested_session_id为非空字符串或null。有明确原生请求时actual必须等值；null只允许有实际参数原件证明未指定session的fresh调用。actual_session_id仍须从原生raw取得、非空、无冲突，满足所有必需席独立性及excluded集合。调度attempt/claim标识不能冒充runtime session。禁止完成后用actual回填requested；确切恢复调用继续严格核其请求目标。无需新schema、额外probe或模型回退。

**owner与验收。** N1共享观察负责准确actual，B核invocation与实际请求语义，A核身份独立性；runtime/D如实记录请求，不能猜session。有证据的fresh/null＋准确独立actual是正例；缺actual、冲突resume_hint、重复他席session、nonnull requested不匹配及事后倒填均必须拒绝。该澄清须正式审阅后才成为实现依据，本文不自签native准入。

## 2. 冻结读取计划到prompt的派生同步（GOV-09/04）

**实际已核。** S1的`S1-ADMISSION-DRAFT.md`有18行；[required-reads-s1.json](required-reads-s1.json)中对应范围为offset=1/limit=18，但实际`prompt-glm.txt`第56行仍为`S1-ADMISSION-DRAFT.md 1 16 # s1-admission`。GLM原生第94条、Kimi第27条事件均按offset=1/limit=16调用Read。第17行为空，第18行包含64Read/预算风险及不得删必读范围的说明，因此不能以“只差空行”抹去缺读。根发包前核原件hash和计划准确，没有核出派生prompt表的滞后；这是准备与产品门禁应共同修复的问题，不归因于模型自报。

**最小合同变化。** required-read计划继续复用现有输入索引/读取计划，不增加第二套规则或脚本。计划的权威输入只能是固定policy的逐席required_evidence、准确artifact字节与受审dialect；prompt中的必读表是该计划的确定性派生，不能独立手写维护。源、范围或投影变化必须同时重算计划和prompt，再固定原件及pin；任一旧摘要/旧表残留在派发前阻断，不能启动后补几行而声称原输入完整。

| 现有owner | 最小产品责任与有意义回归 |
|---|---|
| F `development_preflight` | 以实际源字节和固定必读范围生成逐席读取分片及估算；每项保留artifact ID/source hash/offset/limit/投影关联。相同输入确定性输出，不能从prompt倒推required。真实18行源生成覆盖到18；源从16增长到18后旧计划必须失效；有意受审的lines范围仍按policy而非盲读整文件 |
| C `development_audit` | 冻结并核读取计划与policy/源/hash一致，将规范计划交给派生消费者；复用现有required-reads原件，不另建状态。核源18/计划18/prompt16必须非0，不能仅因三个文件各自hash正确通过；重新生成一致18范围是恢复正例 |
| D `development` | 单一prompt装载/渲染owner消费C/F规范计划；现有renderer显式增加读取计划输入，正文中的必读表只能由该输入确定性生成并回核，不能沿用复制的旧表。启动前核完整实际prompt字节与固定计划一致。读取义务少一项、少两行、换同名源、使用旧source hash均拒绝 |

A仍判必需条件，B仍核实际Read正文；预检或派生同步通过不等于真实读过。上述职责不迁移为新调度器，不要求Codex写临时产品生成脚本，也不以“以后人工记住更新表”关闭。尚走bootstrap的审核流必须如实标人工准备；产品交付后要以本次真实失配回放，并在本项目下一适用调用前实际消费其检查。

## 3. 原生success不是严格治理final；自报64Read不是覆盖

**实际已核。** GLM S1原生JSONL第151条、Kimi第144条result均为subtype=success、is_error=false，但正文先有声称64块已读的散文再接JSON。Kimi原句为“全部64块必读材料已独立实读完毕。给出本席裁定。”。两份**完整result正文**严格JSON解析均在char 0失败；不能把流成功或exit0写成有效development-final。两席对S1准入文件的真实Read均仅覆盖1–16，未满足固定1–18范围，亦不因自报64块而补齐。

**最小合同要求与owner。** N1保留完整原生final_text与事件定位，协议success仅表达该层事实。B继续对整个final_text严格解析，允许JSON自身合法空白，但不得查找最后一个左花括号、截尾JSON、去掉散文/代码围栏或另取更早片段来通过；B同时从配对Read正文计算缺项。A/C必须保留“协议成功、治理final无效、必读不全”的独立事实并拒绝该席，不接受summary的全读声明。本项沿既有严格JSON合同落实，不新增输出强制模式或提示词兼容开关。

**必需回归。** 将本次真实raw及固定读取要求作为负例：完整正文严格失败，目标文件缺17–18，模型自报无效。另用明确标synthetic的完整合法JSON＋真实完整读取作恢复正例；只移除散文但仍缺读、只补读但仍散文、将外层success改绿，均不能恢复。实际后继有效票只能由获准的原责任席产生，不能人工加工本次原票或据此追加模型调用。历史投影可无损展示失败原文，但不能转换成有效v2票。

## 4. watcher创建时间格式差异（GOV-06）

**现场依据。** GLM的watch-completion原件记576次poll而first_child_observed_at=null，且只记录wrapper身份；运维后继`watcher-correction-kimi.json`说明GetProcess.StartTime保留100ns位、CIM.CreationDate字符串只有微秒精度，字符串全等比较失败，导致后代发现没有建立。该记录属于对bootstrap看护缺口的运维处置，不证明W/R2已经实现，也不能回填较早时间段为全程看护。根将把完整真实原件/适用时间与结果绑定到原finding。

**最小产品承接。** W仍唯一负责操作系统原句柄/创建身份与进程包含边界，R2消费该实际进程对象并持有完整生命周期；不复制TEMP watcher成为第二产品执行器。身份不得靠不同来源的格式化时间字符串全等或PID单值决定。既有contained+suspended→持久化身份→resume、控制者退出/父先退/树确认结束合同保持；时间显示归一化只能用于展示，不能用宽松时间容差掩盖PID复用。

**验收。** 真实无模型子进程实验覆盖：同一进程的100ns/微秒显示差异不导致漏管，PID/创建身份不一致不能误认受管进程，父先退或控制者故障仍由原句柄/包含边界处理，缺身份/无法确认树清空不回成功。R2回执定位实际句柄身份和处置，不以ready标志替全生命周期。运维修补与产品回归、产品真实模型使用分别记录；W/R2独立双席及native复核后方可关闭产品子项。

## 5. 无效Kimi原文中F1–F6线索的静态核对

以下只是从失败原件提取的可调查建议，经本地原件交叉核对后纳入现有owner；不是接受该席尾部PASS或其“均不阻断”的裁定，不另建finding台账。

| 原文线索与核对结果 | 最小后继要求、owner及验收 |
|---|---|
| F1：确认`bootstrap-policy.json`的plan/accept required_evidence均未包含当前policy；index仅有其寻址/hash，subject.artifacts亦未含当前policy。prompt安排实读不能替机器必需条件 | A/C将各阶段必需审核/监督席读取准确当前policy纳入固定义务，B核实际覆盖。沿既有字段为该policy artifact声明full、source_sha256=null；先冻结不含自身hash的policy，再将其真实字节hash加入subject.artifacts并计算subject。condition的权威源仍是已固定旧规则，不将当前policy自身hash写回policy。F/D据此派生读取表。缺当前policy义务、只读旧policy、只在prompt要求而机器集合缺项均拒绝；修改policy后旧subject/票失效。此为后继候选修正，不能改S1原件或以native口头确认替代 |
| F2：确认B1 batch-config.model_call_limit=16；分批预算16含设计双席2，其余作者/修复/内容审最坏14。不能把16整体再当设计后可新增额度 | S/D沿既有剩余额度/authority_ref合同核全请求与本批两层预算；C核预算批准来源。明确16是批总口径，14仅在恰好已消耗该批设计2次且无其他扣减时成立，不机械改为固定14。S0/S1失败及本提案追加均计入准确全局已用；Store启用晚于B1时不能重新发B1额度。回归已用2后拒第15次新增、本批与全局余量取共同约束、失败计数及重复初始化不清零；纯预算计数测试无需模型 |
| F3：未确认丢源。`PREPARED-SOURCE-MAP.json`已将runtime-plan映射到准确`dc37ae6…:coordination/requests/governance-enforcement-20261011/runtime-integration-plan.md`，字节hash为`9e1e0e43539c82e0d6d86069c4f78dd6572d3653f7842d26d4733df12c6a1115` | C复用单一artifact ID/准确源映射，不因展示重命名再造权威。验收该真实改名映射通过；同名错hash、无映射的必需链接目标、从显示名猜latest均拒绝。包内相对链接不自动证明原仓文件已读 |
| F4：确认冻结source-test-runtime.py为409物理行，N2继续增加回归有硬上限风险 | N2作者在现有专属写集内先说明测试组织与增量规模；A/C消费既有具名规模检查证据，独立审核仍审内聚性。若预计或实际越500须停止并提出明确写集调整/精确局部例外，未批准前不新建测试文件或压行。409不是已越硬上限，也不是未来增量已获准 |
| F5：W实现尚未发生，重型Windows路径超过目标/20轮风险是估算，不能写成实际超限或实现已可行 | W交付必须有真实无模型进程验收及准确文件/函数物理行数，遵守300/500与40/80及独立局部例外规则；F保留预算估算和unknown。超响应预算或硬规模上限不得靠隐藏续跑、删注释或未审拆分通过 |
| F6：profile-supervisor已pin TEMP agent_file；当前文件存在。既有runtime._verify_hashes已有agent_file/agent_file_sha256检查，不能另造校验器或从当前存在推断未来启动仍安全 | R2复用既有启动前实测，D绑定受审profile及只读权限；缺文件、字节变化、权限profile变更在启动前拒绝，准确原件恢复才可继续。N1/B仍核真实fresh actual身份；agent-file哈希正确不证明实际模型/读取/最终票有效 |

**不采用structured flag。** 静态调查原件为`TEMP/agent-coop-governance-20261011/codebuddy-structured-output-static-evidence.json`，状态static_only_no_probe_no_admission，绑定headless实现SHA `f9affe2aed036a3a3ee8486b82e77b176a2a4b21f7bed721074c1c1e4a312e65`。其中SO-01–04显示`--json-schema`依赖额外StructuredOutput工具及独立`result.structured_output`字段；缺结果时stop hook最多自动续跑3次，尚不能证明max-turns为包含续跑的总上限。SO-05另见schema校验器失败可能退回generic参数。现有Read/Glob/Grep工具集、完整result严格JSON合同及无隐藏重试预算均不覆盖此行为。本请求不加该flag、不改变解析字段、不作模型probe，不用它挽救S1原票；保留该实证供既有runtime/预算负例，不新增可选输出平台。

## 6. 一次性追加复核的具体申请（尚未授权）

[roadmap](../../../docs/roadmap.md)第27行规定每次max-turns20、评审最多2轮；S1准入原件的停止边界同样不授权第三轮。S0/S1已经用完两轮。为审上述具体修订，拟仅申请本请求**额外一次双席设计复核，共新增2次CodeBuddy**：原GLM/Kimi独立只读，各最多20响应轮、600秒，无自动重试、不使用json-schema隐式续跑；任一失败即保留原件并停止，不自动补调。不改全局两轮规则，也不自动授权native或作者。

只有用户对这次具名追加明确授权后，才可冻结修订候选/完整读取计划并走原派发准入；S0/S1已用4次，追加后此设计复核累计最多6次。若保留其余13包原设计预算，整体候选上限从52CB/8native变为**54CB/8native**，基本口径从31/8变为**33/8**；这是待批准预算提案，不是本次2调用之外的支用授权。未来作者仍须各批有效计划、必需双席和native门禁，后续实际用量只沿原请求result及同一Store承接。

## 7. 审批与证据承接

上述事实的原流仍在本机受权TEMP路径，本文不复制私有执行日志。双席来源为`agent-coop-governance-s1-run-20261011/review-governance-s1-{glm,kimi}-r1.jsonl`、同名前缀receipt/invocation/completion；watcher来源为同目录watch-completion-glm.json和watcher-correction-kimi.json；会话请求来源为`agent-coop-isolated-workflow-20261010/run-supervision-g1.ps1`。仓内[GLM原文](review-s1-glm.txt)、[Kimi原文](review-s1-kimi.txt)及[真实回归记录](review-s1-regressions.json)保留失败事实；完整原件/准确hash与最终状态沿[result](result.md)引用，不用此提案摘要代原件。

后继审批应明确：哪些是字段语义澄清、哪些改变派生产品接口、哪些是既有合同的真实回归；覆盖受影响A/B/C/D/F/N1/N2/W/R2/S消费者和独立关闭责任。产品/测试仍由实际CodeBuddy作者实现；Codex只提交文档、核验证据与集成。S0/S1已用调用不撤销、不改写，也不被此提案转换成新范围批准。未获新准入前只可准备可审材料，不能补票、派作者或把本文件标为“已修”。

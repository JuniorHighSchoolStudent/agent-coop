# 开发治理产品修复实施合同（后继候选）

范围：GOV-01–09及GOV-S0-I01的产品责任、共享接口与失败/恢复验收；维护者：Codex合同集成者；状态：依用户最新指令推进至目标完成，后继准确候选仍须独立双席复核及native监督；不以历史票准入实现。旧[contract.md](contract.md)为`ee94914543e9248d17c9fde670869744173ea22a`送审原件，本文件不修改、覆盖或倒签它。原两席S0的PASS仅覆盖原scope，不证明本后继合同已获审。当前状态、调用预算、写集分包和顺序分别由[result](result.md)及实施计划维护。

需求依据：[范围补充](scope-amendment.md)、[调查](investigation.md)、[AGENTS](../../../AGENTS.md)、[design](../../../docs/design.md)。本文件是后继接口候选，不另建问题、批准、PASS或进程状态台账；长期规则仍归AGENTS/design，通用状态仍归现有Store/Runner，原件沿同一request保存。

用户最新指令取代固定review/repair轮次：设计、作者修复、内容审查及监督按未闭合finding持续推进，轮次标签仅为序号，不设总调用次数来变相封顶。每次CodeBuddy调用仍最多20响应轮/600秒，native仍保持真实可执行的600秒边界及未知能力声明；每次准确版本、权限、独立性、暂停和异常处置不变。无进展须先调查并修改受审输入/修复方案，禁止对同一失败盲重试。旧S1冻结内容保留在`dc37ae62a0aa8b40e0d881a364a6ddd190c0e146`及原送审树/原票；[现场提案](s1-correction-proposal.md)的事实沿用，其“额外2票审批/54次”候选限制已被用户指令替代，不再作为本合同门禁。

## 1. 承接与变化

旧合同中以下要求全部保留：旧策略独立pin、未被用户明确替代的有效旧条件完整继承、准确角色/候选/原件绑定、逐席实际Read正文、作者有效final、独立审核与监督、unknown可见、无豁免入口、严格JSON和类型敏感摘要、有限阶段依赖、纯观察不得执行动作、实际使用和独立关闭。预算不足、内容PASS、native PASS或临时行政例外均不能抵消缺项。既有失败和Git合入事实不改写。

| 后继变化 | 原缺口与明确边界 |
|---|---|
| 加入不可省略的监督依赖不变量及单独证据包摘要 | 修GOV-S0-I01；原subject继续排除意见，监督输入绑定同subject的已完成审核attempt，而非把未来原票塞回subject |
| 共享原生序列观察由RuntimeAdapter唯一维护 | 修GOV-07并避免B复制parser；旧产品parse与B共同消费，旧样例路径也必须获得修复 |
| 产品化容量预检、受控开发执行和动作准入 | 承接GOV-06/08/09；复用现有runtime/Store/Runner，不另建通用Scheduler平台或第二启动器 |
| 分阶段交付但所有finding仍属于本请求 | 三包只读检查不再被描述为全部治理完成；每项均须实现、回归、真实使用、独立关闭 |

只新增必要的v2协议：`development-review-policy/2`、`development_audit/2`、`development-invocation/2`、`development-final/2`、`development-observation/2`、`development-report/2`；原`development-delivery/1`继续承接。report在旧字段外增加batch_id/evidence_bundle_digest（无监督时null），B新增字段见下文。未列变化的字段、精确类型、摘要算法和拒绝未知字段规则仍依旧合同。v1原件只能作为历史证据或旧scope回放输入，不能静默升级成满足新监督不变量；不要求补造历史v2 final。

v2的role_bindings另增加`profile_artifact_id`（manual为null）与`prompt_body_artifact_ids`（stage→artifact ID，stage仅plan/dispatch/accept）；前者指向当前subject内已审profile文件，后者是所有作者/审核/监督已审正文的唯一定位。任何拟准备或调用的role/stage必须有非空body ID且其准确文件/hash在subject.artifacts，不从artifacts枚举或文件名猜选；manual不调用模型时映射为空。实际动作必须消费该准确文件/hash，不能只比adapter/model名。profile依现有配置/权限schema，新增dialect定位见第6节。policy没有新增关闭监督最低要求或partial_accept的开关。

策略修订由旧授权规则受审，不能由待审policy自行授予放宽权限。后继policy继续逐值承接有效原条件；本次[scope-amendment](scope-amendment.md)所记录的用户指令只具名替代固定审核/修复/自动attempt次数限制。新policy.authority_refs必须pin该用户指令及准确旧规则，送审材料逐项列旧条件来源、被替代文本和新语义；旧原件保留，新request.conditions完整对应新受审policy，不能让已失效次数条件继续阻断。A按独立批准的新policy与条件摘要核验，不解释自然语言自行override；用户指令不能被扩大为豁免作者final、必读、准确版本、独立性或看护。双席与native须核这条授权链及差异，模型/集成者无自签放宽入口。分组read_coverage只合并同角色同阶段的机器条件，不删其required_evidence，各条仍全部AND。request.conditions始终保留完整policy列表，不能因为当前阶段不claim历史义务而删条件。

## 2. 最低不变量与可配范围

以下是产品最低判据，不是可由policy关闭的开关，也不按CodeBuddy/Kimi品牌硬编码：

1. 阶段若包含kind=supervisor和必需kind=reviewer，监督输入必须覆盖该阶段**全部必需reviewer**的准确有效final及完整逐席原生观察/coverage。少一席、旧候选、摘要替原件或监督未实际读到均阻断。A验证审核者存在不替代监督的独立判断。
2. policy确定角色、独立性、每阶段条件和额外必读源；它可以增加监督材料，不能取消上一条。plan/accept每个必需reviewer及supervisor均必须完整读取准确当前policy，A/C拒绝实例漏配，B核其实际正文覆盖，不能仅在prompt要求或用旧policy替代。两个角色重命名或复用同session/raw不产生独立票；作者、审核者、监督的独立性延续旧合同。
3. 旧规则/旧准入条件使用固定源hash；变化的候选源使用subject内准确hash。plan历史调查可由accept沿prior链重算，不要求每席再读全部历史；accept仍直接核适用旧条件、当前候选、验证、作者交付及本轮finding，不能用plan票代内容票。
4. 成功仅属于明确层次：原生进程/协议结束、有效作者交付、审核完成、监督完成、产品动作许可、动作完成、合入分别举证。临时check报告不变成批准本身，也不自动更改当前状态。

当前policy必读使用既有required_evidence：固定artifact ID、coverage=full、source_sha256=null；condition权威引用准确旧规则。先冻结不含自身hash的policy，再把其实际hash加入subject.artifacts并计算subject，外部独立pin仍核policy字节。policy中不得嵌入自己的hash；缺subject绑定、旧hash、缺任一必需席读取均阻断。该有向依赖没有policy→自身摘要循环。

## 3. 监督证据的无循环绑定

保留`subject_digest`作为候选内容、策略、条件、包定义的共同身份；它不包含本阶段审核/监督意见、调用结果、证据包或最终检查报告。同subject可发布后继不可变evidence-index，显式承接已完成attempt；不覆盖原索引，也不按文件名/latest猜当前索引。

同阶段的处理顺序固定为：冻结候选→完成全部必需reviewer→生成准确监督证据包→监督读取并给意见→最终阶段判定。plan和accept均如此；dispatch依旧重算prior plan，不凭空要求未来作者session/final。审核者可并行，监督依赖其完成。重新审核改变任何必需reviewer原件后须新证据包及新监督意见，旧监督不能沿用。

### 3.1 证据包最小schema

`development_audit/2`在原字段外新增`supervision_bundles`，为stage→bundle artifact ID的映射；只允许plan/accept。没有监督的阶段不要求包，正式阶段判定中，含监督和必需reviewer的阶段必须有且只有一个被当前索引显式选择的包。第6.1节仅生成本阶段reviewer读取计划的准备态允许未来包尚不存在；该准备态不能进入正式eligible/动作接收。该包是本次输入原件，不是状态库。原artifacts.kind增加`review_bundle`；可读票据/coverage仍为projection。

`development-review-bundle/1`准确字段如下，未知字段拒绝：

| 字段 | 语义 |
|---|---|
| schema/request_id/stage/subject_digest/policy_digest | schema为development-review-bundle/1；stage为plan或accept，全部绑定当前阶段候选 |
| reviewers | 按role_id排序的非空列表，恰好覆盖policy该阶段全部必需reviewer，无多余替补或重复 |
| reviewers每项 | role_id、attempt_id、raw_artifact_id、raw_sha256、invocation_artifact_id、invocation_sha256、final_artifact_id、final_sha256、coverage_artifact_id、coverage_sha256 |

包本体不含自身digest；`bundle_digest`是其严格canonical JSON摘要。raw/invocation指向该role该阶段同subject的已完成原件；final/coverage指向第4节产品确定性投影。C重新读取并重算，不信任包内用户填的通过结论。每个当前阶段/角色只选择一个有效attempt；被替代attempt留在历史索引，不能混入当前有效票。包不含监督自身attempt/final、最终DevelopmentReport、可变result，也不递归引用其他监督包。

`development-invocation/2`在旧精确字段之外新增`execution_invocation`与`prompt`（均为ArtifactRef，分别指实际启动原件和完整prompt原字节），并与`development-final/2`各新增`evidence_bundle_digest`：监督为准确bundle_digest，其余角色为null。A核二者相等且等于C重算值；监督raw中的实际Read须覆盖包、每席final投影及coverage投影，不能只读bundle清单。这里是独立于subject的附加证据绑定，允许所有人审核同一个候选又避免future-vote/self-reference循环。

监督的内置required_evidence由C根据固定policy角色及重算包派生，再由A检查其完备；不得只依赖policy实例手工列出。其artifact/hash来自已完成同subject attempt及重算投影，不套用旧合同“source_sha256=null只能来自subject”的候选源规则；该例外仅适用于上述内置监督依赖，不能用于任意附件。policy原有required_evidence的hash规则不变。

### 3.2 依赖检验与能力边界

C必须先重算reviewer的共享序列观察、B覆盖和final，再构造并核对包，之后才观察监督；任何unknown/failed/missing都不能通过包包装成成功。prior plan/dispatch仍按有限深度2重算；监督包内部只依赖同阶段已完成reviewer，没有新增无限依赖图。

人工bootstrap阶段由旧规则完成必要核对，标为bootstrap。v2工具形成后对真实原件重算；输入不足则blocked/unknown。不能将新格式补写进旧模型原票，也不能以补材料为名突破既定调用预算。首次新格式调用前必须把准确摘要和final格式写入受审prompt。

## 4. 可读原票与coverage投影

正式原票是共享adapter从原生最终事件定位的准确`final_text`及其解析对象；人工摘要、解释性result、模型自报已读都不能替代。B负责纯函数`render_review_evidence(observation, representation)`，representation只允许`final`或`coverage`，返回UTF-8 bytes。输出schema为`development-review-evidence/1`，两种表示共用attempt_id/role_id/stage/subject_digest/policy_digest/raw_sha256/representation，记录源事件ordinal。

- final表示：包含完整原生final正文的`text_chunks`，按Unicode码点每256字符一段，空正文不合法；依次拼接必须逐字符等于共享观察的final_text，并严格解析为同一个final对象。分片仅解决工具长行截断，不改原文、不取摘要、不新增结论。
- coverage表示：包含该席每一required_evidence的condition_id/artifact_id/source_sha256/required_ranges/covered_ranges/missing_ranges/status/success_basis/projection_id，以及贡献或失败Read的event_ordinals/call_id。保留全部violations和未知项，不只输出complete行。源内容验证由B基于raw与准确artifact实际重算；投影逐值等于该结果，不能从用户填写的coverage复制。
- 序列化固定indent=2、ensure_ascii=False、allow_nan=False和键排序；列表顺序按合同稳定ID/事件ordinal。长自由文本仅以规定text_chunks表达，不能因显示限制删行。严格JSON拒重复键与bool/int/float混同；原投影JSON值等价和编号文本规则继续有效，但不能替代本节对来源的重算。

为便于审核，final表示另提供`final_object`及`summary_chunks`：final_object保留解析后的全部字段，仅将字符串summary替换为null；summary_chunks保存该summary原字符串的256字符分片，非字符串summary则保持原值且summary_chunks为null。检查器复原后与准确final对象作类型敏感逐值比较，任何字段、限定语或判定改变均拒绝；完整text_chunks仍保留且独立比对。若其它字段包含超过显示硬限的字符串，本版本不得删掉它或声称pretty足够，应由容量检查报告不可读并提交受审的确定性扩展。

本次S0的`review-s0-glm.txt`单行JSON与`review-s0-kimi.txt`长summary、各约83KB的coverage原件是必须回归的真实fixture。pretty不能解决JSON长字符串，Read offset不能切开一条被工具截断的行。原票和coverage字节不改；紧凑coverage从其对应native raw和required集合重新计算，完整保留逐项结果、未知/失败和事件定位，不重复抄全部事件正文。native读取可核紧凑视图及必要定位原件即可，不要求全文重读83KB重复事件。本回归可验证历史材料的无损可读表示，不将旧final冒称v2有效票。

历史v1原票允许用同一final分片算法展示：即使B因旧治理schema缺失而final判unknown，共享Trace仍可给出实际final_text；renderer完整保存它及原raw/旧invocation定位，不用人工摘要替代。历史缺失身份/摘要字段保持null/unknown，不填成本轮绑定。当前bundle准入仍要求有效v2 final及全部准确字段，历史展示件不加入当前attempts或有效reviewer集合。产品尚未实现时，S1材料可按此明确算法由受权准备者生成并标bootstrap投影；必须独立反向拼接与原件比对，不能称产品生成能力已实现。

观察投影的验证不是“hash相等所以真”：C先从原生raw重算B，再逐字节比对产品应生成的投影。篡改、遗漏某条要求或用另一席结果替换，即使同步修改附件hash仍失败。监督实际Read投影的内容由B按普通成功Read覆盖核对；未读某席、仅读文件名/工具计数均不满足。涉及争议或无法决定的源事件可追加定点Read；不能把未审部分写成已独立核验。

生成与核验是不同动作：readonly `verify-development`不写文件；准备动作只通过现有请求证据出口写不可变projection/bundle，已存在不同内容拒绝覆盖。新增产品命令`prepare-development-evidence --stage <plan|accept> --index <path> --policy <path> --policy-sha256 <sha> --output-dir <path>`仅装载、重算并生成本节原件，不调用模型、不接收、不改变Store状态；只能写显式请求证据目录。输出准确artifact引用供发包人冻结监督输入，不能自动批准自己生成的材料。该入口与readonly入口共用C组合逻辑，避免另建脚本生成器。

两个CLI命令均只归实施计划中**最后CLI接线包**，不能让原C与最后包并发写cli。C唯一维护development_audit装载/组合及其专属测试，并先交付两个公开API：`verify_development(stage, index_path, policy_path, policy_sha256)`返回DevelopmentReport，只读；`prepare_development_evidence(stage, index_path, policy_path, policy_sha256, output_dir)`返回`{bundle_digest, bundle_artifact, evidence_artifacts}`，后两者分别为ArtifactRef和ID→ArtifactRef，仅写本节显式证据目录，不改源index、Store或接收状态。生成前必须完成reviewer证据检查，不能因为尚无supervisor就把其余缺项一并忽略。

C包受审后可以由受权发包人直接调用上述公开API构造真实监督材料，不另写临时装载/渲染脚本；后续动作包复用它，最后CLI包仅接线。在CLI尚未交付前明确记作公开API实际使用，不声称verify-development命令已可用。准备命令/API的有界写入是本后继合同显式扩展，需独立复核；原只读API/命令仍不写。

## 5. 共享观察与A/B/C边界

以下函数名与责任供并行作者消费；容器为普通dict/list/bytes，不用新增框架。A/B与共享原生观察均不得文件IO/网络/子进程，不得修改入参。旧parse的签名和正常返回合同尽量兼容，错误终态的历史误接受必须纠正。

| owner/API | 最小输入输出与唯一责任 |
|---|---|
| RuntimeAdapter：`adapters.observe_native(adapter, raw_bytes)` | 输出NativeTrace：adapter、actual_model、actual_session_id、terminal（success/failed/unknown）、final_text、final_event_ordinal、paired_tools、violations、raw_sha256。paired_tools每项含call_id/name/input/result/is_error/call_event_ordinal/result_event_ordinal；缺少结果保留null和违规，is_error未知为null。只解释真实协议与事件顺序，不解释development-final/业务PASS |
| 旧`adapters.parse(profile, stdout, session_id)` | 必须消费同一NativeTrace，核profile工具/身份并解析现有业务结果；不得保留另一套“取最后result即可成功”的序列判据。Runtime实际exit码仍由runtime核，Trace的terminal只是协议终态 |
| B：`observe_development(trace, invocation, requirements, artifacts, launch_evidence)` | v2改变首参数，直接消费NativeTrace；requirements仍为evidence/projection_rules，artifacts仍为ID→{path,bytes}。launch_evidence由C按下述固定映射提供，B纯核实际argv/prompt/请求身份关系。输出DevelopmentObservation，承接原NativeObservation字段，另含role_id/stage/subject_digest/policy_digest、final_text/final_event_ordinal及第4节coverage定位字段；核实际Read内容、治理final和进程退出，不重解析provider序列 |
| B：`render_review_evidence(observation, representation)` | 只渲染第4节确定性原票/覆盖证据，不加载文件、不决定准入、不提供人工可编辑PASS |
| A：`evaluate_development(stage, policy, request, observations)` | 延续纯schema/阶段/身份/条件判定；request envelope保留index/declarations/prior_results/policy_digest，增加supervision_bundle（C重算的包或null）。observations为attempt_id→B结果；A独立检查最低监督集合、摘要、final声明与覆盖，不只相信C已检查标志 |
| A：`evaluate_review_evidence(stage, policy, request, observations)` | 供证据准备使用，复用同一schema/版本/作者交付及必需reviewer判据；尚无supervisor是此准备步骤允许的唯一未完成后继。返回`{decision:ready|blocked|invalid, findings}`，ready仅表示可生成监督输入，绝不等于plan/accept eligible，也不供Store动作授权 |
| C：装载/组合/CLI | 严格解码、核pin/hash/文件不变、按reviewer→bundle→supervisor顺序调用共享观察/B/A；只读命令早于Store/Runner返回，准备命令仅指定证据输出。复杂文件装载/组合可由专属development_audit模块承接，不能堆入cli或把协议解析复制出来 |

共享观察需先严格JSONL验证，再复用既有_events；本轮只有一个原生序列owner。必须识别调用/返回配对、冲突身份、失败或重复final、final后新assistant/tool、未完成工具；Kimi最终assistant后仅允许已观测的meta/session.resume_hint白名单。缺能力保持unknown，不从init工具目录推断实际调用成功。工具本身失败可作为负例证据，但失败Read不贡献覆盖。

必要消费者合同测试包括旧sample parse、治理B和原生真实fixture：同一个坏序列两条消费者均拒绝，同一个合法序列两者对身份/工具次序一致；治理final schema不强加给旧sample业务final。B仍须核True/1/1.0、长行截断、错误路径、角色独立覆盖和经审定等价投影。

启动证据复用既有wrapper的execution invocation，不另造进程协议或把规范invocation自述当事实。新增两个ArtifactRef须存在于当前index.artifacts并核准确字节hash；它们属于attempt证据，不进入subject.artifacts（完整prompt含subject，不能反向自引用）。C严格JSON解码execution原件，并加载准确UTF-8 prompt；不得沿可变latest或capabilities.source_ref猜出处。C传B的内存`launch_evidence`准确字段为`execution_sha256`、`cwd`、`candidate`、`argv`（string列表，保持原顺序/字节文本）、`prompt_path`、`prompt_sha256`、`prompt_bytes`、`requested_session`、`requested_resume`；后两者为string或null，只由下列原件字段映射。C核两引用/hash、规范路径与prompt_path一致，且cwd/candidate分别匹配该attempt受审profile根和受派subject的commit、argv入口匹配准确profile.entry；不能将别的候选启动原件借给本次。B核请求与argv、完整prompt内容及同invocation的身份关系，缺件/未知映射/矛盾均invalid或unknown而不满足要求。

| C受支持窄映射 | 准确来源与B交叉核验 |
|---|---|
| CodeBuddy现有execution原件 | `root→cwd`、`candidate`、`actual_argv→argv`、`prompt→prompt_path`、`prompt_sha256`、`requested_session`、`resume→requested_resume`（空字符串规范为null）。B核唯一`-p`参数后的完整文本等于prompt_bytes严格UTF-8解码结果；fresh的唯一`--session-id`必须与requested_session及规范requested_session_id一致；恢复选择器只有经准确原件/已审方言证明才接受，不能从resume自述推断 |
| native Kimi现有execution原件 | 同样取root/candidate/actual_argv/prompt/prompt_sha256，`requested_resume→requested_resume`，requested_session置null表示该原件没有此字段。B核唯一`--prompt`完整文本等于prompt原文；fresh应无`--session`/恢复选择器且requested_resume为空/null，有实际agent-file参数；resume的`--session`值必须与requested_resume及规范requested_session_id相同。`session='unknown until actual resume_hint'`只是旧占位，绝不能映射为actual或有效请求 |

仅以上已核形态被支持；参数选择器重复、冲突、缺值或不受支持形式拒绝，不能猜“最后一个生效”。实际raw才是actual身份来源。外层execution ArtifactRef SHA是原件完整性权威；旧actual_argv_sha256及argv_hash_encoding保留在原件供定位，当前不把不同PowerShell序列化算法当统一canonical摘要，也不声称验证未实现的内部编码。B逐元素核实际argv，不由旧内部hash单独证明它。C/B只消费上述白名单字段，额外原件metadata不授予权限；治理invocation自身仍拒未知字段。原件可信生产仍归实际wrapper/runtime观察，离线checker不声称认证OS进程。

已核实据为S1 `review-governance-s1-glm-r1.invocation.json`与旧`supervision-product-permission-final.invocation.json`；后者是resume实例，fresh仅静态核`run-supervision-g1.ps1`分支，不冒称已有fresh成功样本。旧native原件若无actual_argv，只能历史展示，不能作为fresh/null充分证据。R2开发执行沿同一runtime证据出口记录上述最小启动事实，D将原件/完整prompt引用绑定到治理invocation，不建新台账；日志、报告不展开完整argv/prompt/env或敏感内容，仅给获准路径/hash与差异定位。回归必须覆盖丢引用、换prompt且重填自述hash、argv缺session但规范非null、native占位倒填、重复selector、旧无argv原件及准确fresh/resume恢复例。

`development-invocation/2.requested_session_id`明确为非空字符串或null。有显式原生请求时actual必须相等；null仅表示经实际argv证明本次fresh调用没有请求session ID，不表示actual可缺失或runtime普遍不支持预选。N1从原生raw取得非空无冲突actual，B核请求语义，A核独立性/excluded；禁止用actual事后倒填requested，调度attempt/session标识不能冒充原生实际session。恢复调用仍核其准确请求目标。

B严格解析完整final_text，仅允许JSON自身合法空白；散文后JSON、代码围栏、截尾选对象或另取更早final均不得通过。N1协议success、进程exit0与B治理final有效性分别举证。S1两席真实raw必须回归：GLM第151条/Kimi第144条result均success但完整正文char 0解析失败；第94条/第27条Read准入文件仅1–16而固定要求1–18。自报64Read不补缺读；只修JSON或只补Read均不能恢复。不同角色最终字段和准确subject仍依既有合同，不启用json-schema/StructuredOutput：已核实现可能隐式续跑3次、增加工具并换用structured_output字段，不在本次权限/预算/解析合同内。

## 6. 容量预检与实际动作边界

本节只冻结消费者边界及验收，不在本文件展开全部执行工程。具体平台和现有实现迁移由运行时提案、实施计划及正式审核决定；未实现不得用人工操作冒称产品能力。

### 6.0 单请求分批，禁止任意部分接收

总request保留全部GOV义务；每个批准批次有自己的`batch_id`、固定packages、plan subject和policy pin。`development_audit/2`新增`batch_id`（非空字符串）及`batch_dependencies`（下述列表），subject新增同值batch_id及dependencies_digest（对列表canonical摘要）。**同一批**plan/dispatch/accept的packages和dependencies逐值不变，accept必须完成该批全部包和所有必需席；不同批的package集合可以不同。没有partial_accept/skip_package开关。

本候选采用保守的逐批准确plan准入：前批接收后才冻结后批准确40位base_commit，不引入全局plan预授权未知未来commit的抽取协议。总体设计审核不能自动当每批未知基线的有效plan票；具体调用预算与批次由实施计划明确。

每个batch_dependencies条目准确含`request_id`、`batch_id`、`accepted_subject_digest`、`source_kind`（bootstrap_acceptance/product_acceptance）、`acceptance_receipt_artifact_id`、`acceptance_receipt_sha256`；不得依赖自身、后继或循环批次。它只引用同总request中已独立接收前批的准确原件，不引用“预计会完成”的当前状态。本批plan必须批准该列表，变动须新plan，不在accept临时忽略依赖。旧合同有限深度2的prior规则仍限定本批plan→dispatch→accept，跨批不自动继承旧票到新候选。

只读A/C可核准确依赖声明、原件hash和版本关联，不能仅凭文件自述accepted证明产品状态。产品可用前，前批按旧规则接收后发布`development-bootstrap-acceptance/1`：schema/request_id/batch_id/subject_digest/policy_digest/index（ArtifactRef）/evidence_refs（全部作者、双席、native原件）/acceptance_record（具名受权接收记录ArtifactRef）。尚无Store时，后批plan可以明确source_kind=bootstrap_acceptance并固定该**已经存在**原件的hash；不要求尚不存在的产品receipt，也不回填旧依赖。

产品可用后，公开`development.import_bootstrap_acceptance(store, source_ref, expected_revision)`重新加载原索引、调用C/A/B核完整证据，并核source_ref在初始化配置的已批准bootstrap_acceptance_refs中，才调用同Store专属事务建立`source_sha256→accepted event`映射。记录original_source_ref、原request/batch/subject及当前import revision；这是后验产品确认，不能改原件、倒签自动执行或补掉失败条件。重复准确输入幂等，不同source/subject冲突拒绝；不提供任意历史PASS导入入口。后批原bootstrap依赖继续引用原hash，产品动作在claim/accept事务内核其映射；product_acceptance依赖则核原产品event/receipt。两者查不到匹配的已提交accepted记录均阻断。

为避免真实使用循环，实施计划保留**必要的最后CLI/消费者接线包**为后批：前批action实现、真实验证、双席和监督完成后先独立接收，再通过其稳定公共Runner API派发这个必要作者包。不能把所有包塞一个plan又在接收时忽略末包；不能等工作做完临时造canary。真实内容审核调用只能验证审核调用场景，不能替代实际作者写集/有效交付闭环。

### 6.1 派发前容量

纯API `assess_development(requirements, artifacts, dialect, budgets)`返回ReadinessReport，包含decision（eligible/blocked/unknown）、按席位的字节数/最长行/需读范围/分片数量、估算tokens及输出量、工具/turn下界与明确假设、findings及规范read_plan。read_plan为按artifact_id/offset/limit/projection_id排序（null排序键为空字符串）的分片列表，每项准确含artifact_id/source_sha256/path/read_sha256/offset/limit/projection_id（后者可null）；path为实际Read目标规范绝对路径，read_sha256为该目标准确字节hash；无投影时指源，有投影时指经B重算验证的投影，source_sha256始终绑定原源，offset/limit为正int；由逐席policy要求、准确源字节和dialect确定性生成，不能从prompt反推或跨席并集。dialect和计数规则绑定准确runtime文件hash/版本及原能力证据，不接收临时env自填阈值；budgets由已批准包提供。

dialect是准确profile引用的已审配置：`schema=development-dialect/1`、`adapter`、`implementation_file`（准确path/sha256）、`read_limits`（max_lines/max_chars_per_line/max_estimated_tokens）、`token_estimator`、`turn_counter`、`source_artifact_id`、`source_sha256`。限值为正整数非bool或null；计数方法为受实现支持的版本ID或null，未知不可偷偷选默认值。原profile仅增加`development_dialect`对象，保留其现有permissions/environment/executable/executable_sha256/entry/entry_sha256/max_turns/timeout_seconds/output_limit_bytes，以及native已有agent_file/agent_file_sha256。开发runtime每次启动前除原_verify_hashes外实测implementation_file，证据源也须hash吻合；不能把一个安装版本的Read限制泛化到另一个版本。

本机已核CodeBuddy的node executable、CLI entry、实际Read方言实现dist/codebuddy-headless.js是三个不同文件（已见hash前缀分别63c…、426186…、f9affe…）。本合同不改变其可执行entry或假定headlessJS可直接启动。implementation_file必须定位真正承载已审方言的文件并由原证据说明其与入口的加载关系；未知则容量unknown。claim.runtime_digest定义为canonical_digest({executable_sha256,entry_sha256,dialect_implementation_sha256,agent_file_sha256})，后者对不适用角色为null，各实测值须与profile相等；不是任意一个node或JS的裸hash。budgets准确为max_turns、timeout_seconds、output_limit_bytes，分别沿现有profile精确类型和范围规则，profile与budgets逐值相等。

重复要求可按同一席同一准确artifact/range合并读取计划，但不能跨席合并或删除义务。已知长行截断、无法表达必读内容、确定超硬限制须blocked；无法估算的关键项标unknown并交受权入口，不能默认为足够。估算不保证完成，不把CLI num_turns当max_turns，不把工具调用数当模型轮次。恢复只能通过受审的范围/等价表示/预算调整并重算，不自动缩减required或加模型调用。

C新增只读公开API `prepare_development_read_plan(stage, role_id, index_path, policy_path, policy_sha256)`：严格装载/核pin、当前policy必读不变量和准确源，调用F，返回ReadinessReport。准备结果只表示材料readiness，不是阶段eligible。reviewer准备允许本阶段尚未产生的reviewer/监督意见及未来supervision bundle缺席；不允许缺其要读的源、accept必需作者交付或上游准入。supervisor准备必须先按evaluate_review_evidence核全部必需reviewer有效，并由C重算完整bundle及投影，只允许该supervisor自身最终意见尚不存在。author dispatch准备核有效prior plan，允许该作者未来final缺席。所有角色均严格核源/schema/pin，不能以准备态忽略其他缺陷；不写index或Store。D消费此read_plan生成prompt；C/F均不生成另一份prompt。源从16增至18时旧计划失效，源18/计划18/prompt16虽各自hash正确仍须拒绝。此接口供真实计划审核材料准备及后继开发动作共用，不另建脚本。

S2补充：材料可读不等于能通过Windows启动传输。D先生成最终完整prompt，R2沿现有adapter/profile生成准确argv，再由W唯一纯函数`windows_command_line(argv)`得到实际命令行；argv必须包括argv[0]完整executable、entry、所有flags及完整prompt。W是唯一Windows quoting owner，本切片复用Python subprocess.list2cmdline，F/D/R2不得另写转义编码器。F新增纯函数`assess_windows_command_line(command_line)`，返回decision（eligible/blocked）、utf16_units_with_nul、limit_utf16_units=32767、command_line_sha256（该字符串UTF-8字节SHA-256）、findings；仅对W的准确字符串计UTF-16 code units并加终止NUL的1单位，不用UTF-8字节数或Unicode码点len代替，embedded NUL拒绝。R2在spawn前消费此结果；命令行连终止NUL超过32767即blocked。[CreateProcessW官方边界](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)仅适用于该直接启动路径，有更窄的受审launcher限制仍须核验，不借它担保任意shell。

W的`spawn_contained(argv,cwd,env,*,expected_command_line_sha256)`复用同一windows_command_line入口，并在CreateProcessW前核实实际使用字符串与预检摘要相等、长度及NUL有效；不重新走不同拼接或shell编码路径。完整prompt/argv在这两次核对间变化即拒绝；报告保留长度/摘要/限制和版本，不展开秘密。native最终监督prompt同样独立核完整argv，不能拿作者/CodeBuddy长度、body或模板估算代替。F只计量不序列化argv，W只处理进程参数不解释治理角色，D仍唯一渲染prompt。

本次S2原prompt34681/34682 UTF16、参数下界35005/35009及只去缩进后完整命令行33032/33036均是失败回归，不能放行；§6.4的保真columnar测量只证明该批准确输入可容，新candidate须重新生成全部派生原件并重新核完整命令行，不借旧尺寸。反例包括prompt单独可容而完整argv超限、引号/反斜杠扩张、emoji双UTF16单位、embedded NUL、32766单位命令行加NUL与再多1单位的边界。拒绝须发生在spawn前，不产生目标进程started事实；恢复还须read_plan反解逐值不变及无模型argv往返精确。

### 6.2 执行、看护与状态

开发执行继续使用现有runtime/adapter/environment边界，增量接入独立cwd与受控evidence_root；不要求业务开发树伪造sample marker，也不删除sample原有保护。对外开发调用拟为`runtime.invoke_development(profile, prompt, cwd, evidence_root, attempt_id, session_id)`，具体最小扩展由运行时提案固定。它必须真实消费准确profile/runtime/write-set/session及预算，不只是写一份watchdog参数。

看护/进程包含边界必须在子进程可运行前建立并持续至整个受管树确认结束；控制者退出、父进程提前退出或PID复用不能失去子孙身份。超时、输出越界、看护失败须终止受管树并确认，不得仅杀父进程后回成功。S1运维watcher将GetProcess的100ns创建时间与CIM微秒字符串全等比较，造成first_child=null；W必须用原句柄/准确创建身份维护包含边界，R2消费同一进程对象，不靠格式字符串/PID单值或宽松时间容差判断所有权。真实无模型回归须覆盖显示精度差异、PID复用、父早退、控制者故障及无法确认树清空；运维修补不冒充产品修复。不支持的宿主能力fail closed，不能以“最佳努力taskkill”声称无看护空档。实际平台API、资源释放与崩溃窗口须有官方依据和真实无模型子进程反例，不在本合同凭散文判定Windows实现已成立。

S3诊断回归沿GOV-06/W/R2承接，准确原件、撤回准入及当前状态只由[result](result.md)链接维护：目标node实际已创建，但bootstrap watcher捕获ArgumentException后仅输出`descendant disappeared before identity could be bound`并停止两席；原catch没有entry PID/name/parentPID/创建身份、异常原文或具体失败API。该摘要不能证明某个短寿辅助进程退出，更不能猜测是哪一个bash/pwsh。15个已绑定进程退出不等于未观察后代已清空；两席raw为0字节，无init/final/Read，不能由目标创建推断原生调用或审核成功。原S3冻结材料不改，产品实现尚未开始。

W/R2须在既有日志、outcome及violations证据出口区分目标创建、目标绑定、原句柄/创建身份、包含状态及辅助后代发现失败，不增加新接口或台账。异常保留原文、发生API和当时已观察到的进程身份/父子关系；未获得的PID、名称、parentPID或创建身份明确unknown，不用错误分类文案补造。无模型回归覆盖目标已创建而辅助发现失败、身份查询/绑定阶段抛错、已观察进程退出但未观察后代unknown、原流为空而无原生终态；各自应能定位失败API与已知/未知身份，不能将所有ArgumentException归成“已退出”。恢复必须有准确原身份/包含边界及可核树终态；放宽PID匹配、吞掉异常或将未观察项忽略后报PASS均拒绝。诊断充分性与实际包含/终止成功分别举证，运维文案改善不替产品回归及独立关闭。S4复合身份判据的反例还要求在抛错前保存已获得的各比较操作数、查询数量及实际失败子条件；不能仅保存复合API名称，而将fresh identity和held creation等数值只写在成功路径。未取得的值明确unknown，产品回归验证失败路径证据足以区分缺席、身份冲突与取值失败。

S3后续无模型原件`watch-property-getter-repro.json`证明PowerShell 7.6.5/.NET 10.0.11中，已退出Process的`.SafeHandle`可静默返回null，而显式`get_SafeHandle()`抛出InvalidOperationException；`-not $null.IsClosed`仍为true。旧`handle_retained`布尔值不能独立证明有效持柄，15个登记对象的退出观察也不能补成每个句柄均已有效持有；这不反推S3每个实际句柄都为null。`watch-argumentexception-api-repro.json`另证实GetProcessById的not-found与无关ArgumentException可落入同一宽catch，不能据后续复现倒填S3缺失的具体失败API。原件及当前结论沿[result](result.md)。W/R2回归须拒绝null/错误类型/invalid/closed句柄被写成retained，分别保存GetProcessById、显式句柄获取、创建身份查询的实际失败点和异常；缓存StartTime或持有Process对象不替代有效原句柄。产品W继续使用受审stdlib/ctypes原生句柄与原子Job方案，不依赖宿主CodeBuddy私有组件。

既有轮询式受限行政恢复沿[旧合同](contract.md)的bootstrap人工核对及[S0准入](s0-admission.md)的先ready、准确身份、单次deadline规则，只允许修正既有临时watcher的诊断/属性取值和候选分类，不授予作者或产品接收权限。仅当目标已经准确绑定且原句柄仍有效，正PID的**从未绑定辅助候选**在具体GetProcessById处得到可核not-found、同源CIM复查亦不存在时，才可记该候选unknown并继续看护已绑定对象；不能声称其身份已绑定或整树清空。保留快照PID/name/parentPID/CreationDate、查询时点、精确API与异常。存活候选必须核快照与fresh CIM的同源身份字段一致，再按明确的微秒精度投影关联原Process创建时间；过期快照、身份冲突、权限/未知错误、null或失效句柄、已绑定对象失联、首次目标发现失败仍停止，禁止秒级容差及宽catch吞错。扫描间生灭/脱链后代unknown的既有bootstrap限制不升级为产品包含证明。集成者/发包人可准备最小差异和无模型反例，独立交叉核后以准确新版本重新准入只读审核；撤回的S3不恢复有效。变更上述停止条件或其他旧门禁须先走旧授权的独立审核，不借行政修正自签放宽。后继必读材料必须包含S3原终态/原观察、上述诊断、准确恢复差异与正负例；片段测试通过不等于已安装、正式票或GOV-06关闭。

**Job行政恢复候选（仅后继只读审核）**：S4继续被辅助候选身份查询阻断后，拟以本机已安装`windows-job.cjs`/`job-object.node`的准确版本承担临时包含，不继续扩大轮询catch。来源、实测及S4未决诊断由[result](result.md)链接；现成组件不是产品W依赖。每席使用独立owner与PS watcher、独立日志，复用同一参数化行政脚本；具名owner进程直接加载已pin binding，要求`ensureKillOnCloseJob() === true`且`isProcessInJob(self) === true`，不得使用会warning后回退的`no-orphans.install()`。随后才创建固定PS watcher；核其属于本owner的具体Job后，发送一次stdin GO，GO前不得创建wrapper/CLI。PS watcher记录真实ready并保持固定wrapper及实际direct-node目标的原句柄/创建身份；owner、watcher、wrapper和CLI分别记身份，controller创建不冒称CLI init。owner/外层看护的准确seat绑定、作用范围、组件/脚本/输入hash和单次限制由新准入固定，不附加宿主其他进程。

该候选只以受测的原生Job继承替代**辅助CIM轮询作为持续包含权威**的做法；辅助发现仍留诊断unknown，不再因其瞬时取样失败推断整个包含失败。不是把旧错误改记成功：Job初始化/成员证明失败、GO前误启动、真实目标未绑定或原身份/句柄失效、看护失效、超时、输出越界及已知终止失败仍阻断。ready在wrapper前、从本席owner起算且不由GO重置的单调600秒、每席8MiB、CodeBuddy20响应、准确profile/只读工具/输入及独立双席/native门禁不变。owner退出关闭Job的行为、嵌套Job、父早退、控制者强杀、PTY及Git Bash后代由本机无模型原件独立核验；供应商测试通过只支持其实际fixture，原生源码未分发的属性不伪装成源码审查。现接口无枚举、显式terminate或`tree_empty`，已知对象退出、受测终止机制与全树已确认清空分别记录；tree_empty保持unknown，任何影响后继安全的已知存活或终止未知仍停止并调查，不以exit0/member=true补成清空。

准备、无模型实证和独立技术交叉核不等于启动许可；按AGENTS旧变更规则说明替代依据与保留条件，经准确新行政准入后仅允许唯一发包人派只读复核，原S4准入及失败不复活。禁止在同一入口开放作者、借宿主私有组件改变产品选型或关闭GOV-06。产品W/R2仍须按原stdlib/ctypes、创建时原子Job关联、原句柄及真实整树验收实现，由真实CodeBuddy作者交付、双席与native独立关闭。

派发动作复用现有Runner/Store，拟`Runner.dispatch_development(action)`在内部装载原件并重算A/B/容量，不接收调用者填好的PASS/Observation。`Store.claim_dispatch(expected_revision, claim)`在同一现有DB事务内核revision、输入、预算和资源并记录claim；claim绑定request/attempt、subject/policy/profile/runtime/write-set/session及预算，不能先启动再补claim。不能沿现有整轮run.lock阻塞所有独立作者；并发资源与同写集互斥由同一Store准确事实控制，默认CodeBuddy容量4是可配置团队值。

动作启动前须再次核对claim仍有效；输入、暂停、预算或资源变化令许可失效。故障后先核真实进程与原件，再决定终止/承接/明确新attempt，不能自动重跑未知存活调用。产品接收动作同样在内部重算当前accept，不直接消费旧报告；输出/发布失败沿现有事务及发布恢复，不能因此重新执行模型。状态投影取同一Store/request原件，不增加development-status.json或第二PASS数据库。

产品强制范围是它管理的派发与接收入口；不能宣称阻止用户或宿主任意shell/git。外部操作不自动获得“本产品已批准/已接收”的状态；若需要更强OS边界，必须另有明确合同，不由本次工具隐式扩大权限。

### 6.3 当前开发动作最小输入/回执

以下不是新调度平台schema，只是现有Runner/Store对本请求开发动作的明确入参；未知键、bool冒整数、非有限数和摘要不符均拒绝。路径是规范绝对路径，hash为小写64位SHA-256，字符串ID非空。`ArtifactRef`准确为artifact_id/path/sha256，必须能回指已冻结request索引；调用者不能用另一个同名文件替代。

| 对象/API | 准确字段或行为 |
|---|---|
| `development-action/1` | schema、action_id、request_id、batch_id、kind（dispatch/accept）、expected_revision（非负int）、subject_digest、index（ArtifactRef）、policy（ArtifactRef）、policy_digest、package_id、attempt_id、session_id、prompt（ArtifactRef或null）、profile（ArtifactRef或null）、evidence_root。dispatch后五个可空字段均须具名/非null且匹配本批包/作者；accept的package_id/attempt_id/session_id/prompt/profile均为null |
| 动作装载 | index原字节hash与action一致；policy_digest与独立批准pin及policy实测hash相同；subject与该stage重算一致。profile必须等于policy.role_bindings中profile_artifact_id及subject固定文件；prompt来自第6.4节受审body的固定产品渲染，完整字节须与action.prompt吻合，不能拼入未审核新权限。runtime入口hash、环境、工具、精确写集全部由该profile承接 |
| claim（Store内部构造） | action_id/request_id/batch_id/package_id/attempt_id/session_id/subject_digest/policy_digest/profile_digest/runtime_digest/write_set_digest/prompt_digest/index_digest/cwd/evidence_root/account_group_id/resource_keys/batch_config_digest/budgets/dependencies及expected_revision；digest均从已装载值计算，不接受caller传claim补缺项；dependencies为本批准确batch_dependencies，账户和资源见第6.4节 |
| `Store.claim_dispatch(expected_revision, claim)` | 同一事务核revision、已接收依赖、会话/attempt唯一、预算及准确写集资源无冲突，提交不可变claimed事件并预留一次调用额度；返回claim_id、revision、上述绑定。预留不是实际模型启动；启动后按原进程证据将该预留转为已用，不能重复计数。claimed但未启动要保留明确终态/原因，是否归还预约只能由已审预算规则处理，不能静默减数制造额外调用 |
| `Runner.dispatch_development(action)` | 持有现有Store；内部重算review和容量、CAS claim、启动边界复核、调用runtime、将准确outcome提交原Store；不跨整个模型调用持有全局DB/Runner锁。失败保留原件/部分日志，不返回假成功或自动第二次调用 |
| `Store.mark_dispatch_started(expected_revision, claim_id, process_identity)` | 在进程已受包含且挂起、尚未resume时CAS记录真实创建身份，将该claim的一次reserved原子转为used；状态表示started_suspended，不伪称模型已响应。相同identity幂等，不同identity拒绝。runtime仅在提交确认后resume；CAS冲突只对同一挂起进程重读/重核，不能再创建一次进程 |
| `development-outcome/1` | schema、claim_id、attempt_id、process_identity、started_at、ended_at、exit_code、termination_reason、tree_empty、stdout/stderr（各ArtifactRef或null）、receipt（adapter结果或null）、violations。process_identity由runtime实际采集且含pid/creation identity/containment identity；未启动时相关字段null，exit_code为int非bool或null，tree_empty为true/false/null。null不得解释成成功 |
| `Store.finish_dispatch(expected_revision, claim_id, outcome)` | 只接受原claim身份与原件一致的outcome；同一准确终态幂等，不同终态冲突拒绝。共享Store其它并行claim引起revision变化时只重读/CAS提交本claim结果，绝不能因此重启模型；进程存活未知保留reconciliation_required |
| `Runner.accept_development(action)` | 内部重算本批准确accept和依赖；实际调用`Store.accept_development(expected_revision, admission)`，不接收caller的PASS，不执行Git合并 |
| `Store.accept_development(expected_revision, admission)` | admission由重算产生，包含action/request/batch/subject/policy/index摘要及准确report和必需票据引用；同一CAS事务核依赖和本批未闭合条件，写accepted事件，不消耗模型额度、不修改历史意见 |
| `development-acceptance-receipt/1` | schema、event_id、revision、request_id、batch_id、subject_digest、policy_digest、index（ArtifactRef）、report（ArtifactRef）、evidence_refs（全部必需作者/审核/监督原件的ArtifactRef）。由现有Store发布，不由模型或命令调用者填accepted；跨批依赖固定该原件hash并由Store核对应记录 |

claim单次预算来自已批准profile；并发及显式配置的成本额度由同一Store控制。总调用限额为null时不比较总次数上限，但每次仍记录reserved/used并核暂停、资源和准确准入，不能把“不限审核轮次”当“不限单次执行”。尚未结束的调用继续占用资源，不因超时文字或父进程已退出便释放。action_id/attempt_id重复必须幂等返回原定位或冲突拒绝，不能二次启动。

S2观察到wrapper后代conhost不等于目标runtime/CLI已启动。process_identity只能来自本次准确executable/argv对应的CreateProcessW返回进程/线程句柄及包含身份；wrapper/conhost等辅助进程观察不触发目标on_created或started_suspended。即使目标runtime进程创建成功，也不证明CLI完成初始化、原生握手、模型请求或provider计费；各层需各自原件，无证据保持unknown。必须回归“wrapper/conhost存在但目标创建失败”“目标挂起已建而resume失败”“目标运行但无native init”，不可合成success或以子孙数量证明模型调用。

runtime通过受控`on_created(process_identity)`回调执行上述Store记录，顺序必须是contained+suspended创建→看护/日志就绪→持久化启动身份→resume。创建失败不计真实启动，保留claim失败；记录失败立即终止尚未运行的受管树，不能先resume后补记录。创建及记录成功但resume失败，used保留并记录resume_failed，不退回额度暗中重试；实际是否有模型/provider活动单列unknown或具证据的未发生，不把calls_used冒充供应商计费。控制者在记录/恢复窗口崩溃须靠包含边界终止或由原claim对账，不能静默释放未知进程资源。`invoke_development`因此增加具名参数`on_created`，只允许动作owner传入此生命周期回调，不执行调用者任意模型代码。

`evidence_root`必须是显式批准的请求证据根，与cwd和permissions.root分开；仅准许在该根下按不可混淆attempt_id创建专属目录，拒绝路径逃逸、已有冲突、原始reparse/symlink链。检查顺序沿既有paths/adapters canonical规则，不能先resolve后隐藏reparse；证据目录不授予模型源码写权，也不继承sample marker假设。日志路径启动前独占，运行中保留增量/partial字节及原hash，异常不能覆盖旧stdout/stderr或删失败事实；读取/清理各自沿既有权限入口。

S2 wrapper的StandardOutputEncoding错误独立保留，不能因同时发现argv超限就归因于长度，也不能修短prompt便关闭编码缺陷。R2沿既有原始字节收集/明确解码边界验证启动参数、stdout/stderr配置与实际异常时点；W只提供准确标准流句柄/原始流，不复制PowerShell wrapper。无模型回归覆盖配置失败、中文/emoji往返及无效字节留原流；启动失败不能写成目标运行，未知根因保持未决，并在原GOV06/GOV09证据链分别定位，不新增台账。

### 6.4 唯一Store的开发配置来源与写集owner

已检索事实：现有Store.initialize只校dict和非空steps，并冻结config/config_digest；sample.initialize另有固定schema2、四角色、model_call_limit=4与sample marker。开发不能调用sample初始化伪造样例，也不能由S/D各建一套配置。**S包唯一修改store.py及其专属测试**，新增以下开发模式校验/事务；**D包唯一维护development.py及其专属测试**，装载已审文件、调用C及Store；**R1单写paths.py**承接证据根，**R2单写runtime.py**核profile/方言/启动回调；具体依赖见实施计划。不能通过裸Store.update(data/calls_used/config)绕过开发专属事务；sample原语义单独保持兼容。

开发控制根仍只有`.runtime/state.sqlite`和现有events/投影。D公开`initialize_development(control_root, config_path, config_sha256)`严格加载独立批准pin，交S的`Store.initialize_development(config)`；后者校完整开发schema再复用现有初始化事务及`steps=['development']`，拒绝覆盖已存在DB。旧Runner.run/sample handlers不消费此development步骤，新动作使用专属方法；同一request的后续批只注册到这一个Store，不能各批新建DB清空总预算。配置文件由受权集成者按已审计划准备，产品校验并冻结；模型不自设额度。

`development-store-config/1`准确字段：schema、request_id、control_root、evidence_root、authority_ref（ArtifactRef）、model_call_limit（非负int或null）、account_groups（非空ID映射，每项capacity为正int、model_call_limit为非负int或null）、bootstrap_acceptance_refs（已获审ArtifactRef列表）。字段必填，bool/float、负数、缺字段拒绝。null明确表示该scope没有用户设置的调用次数上限，不是unknown、0或免记账；当前全局/账户组/批次均应为null，不生成新数字替代被取消的轮次限制。0表示明确不准新增调用；数值只允许来自用户显式成本预算，不由模型/发包人为限轮推导。sample原有受审model_call_limit=4不因此改变。

若存在明确数值，Store初始化及批次注册时该scope的model_call_limit均表示该检查点已审剩余额度，须扣除此前实际用量和在途预约；authority_ref（批次由plan_admission证据引用）绑定准确授权、实际消耗及对账，含S0/S1失败、所有修复，不只含accepted。null时仍绑定用户无次数上限指令及完整对账，报告剩余为null，不能显示无穷余额或unknown变0。历史计数、本Store reserved/used与供应商实际计费分别报告；模型活动无法确认保持unknown，对进程/资源先对账而非盲重启。初始化前冻结检查点，外部新调用令旧对账失效；成本额度只在显式数值scope核reserved+used不超剩余，null scope仅持续计数。

容量仍核在途claim；同一账号不同模型不能拆组规避并发，默认容量4为受审团队配置。authority_ref不是本config自摘要。一个request固定一个control_root，既有DB拒重初始化；导入bootstrap接收不二次计调用、不清空历史。config_digest受Store保护，后续实际成本限制或根路径变化须准确受审迁移，不提供临时改限入口。S/D/X须回归null下超过旧两轮/旧总次数仍可在有效准入时继续、数值成本边界精确阻断、失败计数、暂停/资源冲突及重复初始化不能清账。没有次数上限绝不允许同一失败无调查自动重试。

bootstrap_acceptance_refs只允许本请求产品Store尚未可用时、作者/双席/监督全部有效且已具名接收的早期批次原件；缺作者final的旧B27等历史例外不符合导入条件。该列表在初始化时固定；Store可用后的新批必须使用正式产品接收，不借bootstrap入口减掉门禁。S提供`Store.import_bootstrap_acceptance(expected_revision, verified_admission)`的CAS写入，D仅在第6.0节重算和pin检查后调用，不直接改data。

每批plan的subject必须包含固定ID`batch-config`及准确字节hash，profile文件和prompt body亦在该subject.artifacts中。`development-batch-config/1`准确字段：schema、request_id、batch_id、model_call_limit（非负int或null，语义同上）、author_bindings（package_id映射）；每个binding含profile_artifact_id/cwd/account_group_id/extra_resource_keys（非空字符串的去重列表，可空）。package集合来自同批受审index，不在config再维护另一份；binding必须恰好覆盖这些包，account_group_id必须存在全局config，cwd必须等于该profile.permissions.root并落在本包已准备工作树，不能从action临时替换。

D公开`register_development_batch(store, plan_index_path, policy_path, policy_sha256, expected_revision)`，从已完成的准确plan装载batch-config并调用C验证；S的`Store.register_development_batch(expected_revision, batch_config, plan_admission)`核同request、唯一batch ID及批准关联，追加不可变配置与摘要到同一Store的data.development，不改全局config。plan_admission包含准确plan subject/index/policy与必需票据引用；batch-config本体不含未来plan票或index hash，避免自引用。重复同摘要幂等，不同摘要拒绝。后续claim必须与已注册batch_config_digest完全相同。

profile定义真实可执行入口、模型、工具、环境、精确permissions与单次预算；batch-config只把包绑定到该profile/cwd/账户组，不能再覆写。D根据已审package.allowed_paths与cwd规范化并核对profile.permissions.write_files逐值相等，然后派生强制排他资源`file:<规范绝对写路径>`；再加入受审extra_resource_keys。账户组容量单独消耗，不能把它当全组互斥锁导致4并行退化为1。Store只接受与已注册包推导结果相同的resource_keys，不接受caller删掉冲突路径。读者无需占作者排他写锁，具体读写协调沿受审包依赖。

此次候选从author_bindings删除prompt_body_artifact_id，所有角色统一由policy.role_bindings[role_id].prompt_body_artifact_ids[stage]定位；作者profile重复引用须与policy同值，不能形成两份可不同的权限来源。此为明确schema修订，旧含author body字段的batch-config不得静默当新候选通过。

prompt正文来源唯一为上述role/stage映射的UTF-8 bytes，不手工维护第二份必读表；D纯函数改为`render_development_prompt(body_bytes, context, read_plan)`。输出固定为一行canonical JSON context、两个换行、read_plan的确定性columnar JSON（sort_keys=True/separators=(',',':')/ensure_ascii=False/allow_nan=False）、两个换行、原body bytes。context准确含schema=development-prompt-context/1、request_id、batch_id、package_id（非作者为null）、role_id、stage（plan/dispatch/accept）、subject_digest、policy_digest、evidence_bundle_digest（监督为准确bundle，其余null）。read_plan来自C/F本角色本阶段重算结果；body不得再含独立维护的必读范围表。与旧renderer相比，这是明确接口变化，原prompt不能默默沿用。

columnar仅改变prompt中的传输表示，不改F规范read_plan对象。准确对象为`{columns,rows}`；columns固定顺序为`[artifact_id,source_sha256,path,read_sha256,offset,limit,projection_id]`，rows逐行按原read_plan顺序取全部7个原值。拒绝多/少/重排/重复列、缺字段、行长非7、额外字段、重复JSON键、类型变化和非法数值；反解后必须与F原plan类型敏感逐值相等，不省略null、范围、路径或完整hash。D唯一实现该表示并回核；不得手改展示件或用摘要代字段。context/body UTF-8原字节保持，完整prompt随准确候选重新pin。

S2独立无模型测量中80×7全部原值保持，原plan canonical SHA为`eef5610061aa620d873144ee93ee7720c0cb689d7590bf92dcc575511257063a`；wire22212 UTF16、完整prompt24225/24226、包含exe/正确转义/NUL的subprocess.list2cmdline长度25279/25283，另用always-quote保守测量25315/25319，argv往返准确；根已独立复算前一组及全部原值。此为旧S2输入的表示可行性证据，不是下一候选准入或产品已实现；每个后继实际输入均重算§6.1完整容量。不得因此省略读取要求、缩hash/path、引入stdin新传输或复用旧prompt摘要。

body不含自己的最终hash或可变候选摘要；实际完整prompt在动作前沿请求证据出口冻结并由action/invocation绑定，D从准确context/read_plan/body重算逐字节一致性。源变化、计划漏项、旧source hash或实际prompt范围缺17–18均启动前阻断。生成表不证明实际读取，B仍逐席重算Read正文。D是唯一渲染owner；C只装载/核证据并提供F计划及launch_evidence，A/B比较实际绑定/覆盖，不另生prompt。bootstrap尚无产品时明确人工准备并独立反向核表；产品可用后的下一适用审核及B4作者实际消费该能力。

## 7. 分阶段接口依赖与规模

先冻结共享序列观察与治理证据接口，再允许互斥写集作者并行。共享adapter及其专属测试由一个包单写；B依赖已冻结NativeTrace，不能同时改adapter；A可独立纯判定；C仅维护development_audit公开装载/组合API及专属测试，最终C2独占cli.py/test_cli.py接线。容量纯检查可独立开发；平台进程包含边界先验证，再由runtime接入；实际Runner/Store动作最后消费上述已验证能力。具体包数、文件写集、作者与预算以实施计划为准，本合同不重复排工程日程。

产品和测试由实际受派CodeBuddy实现；Codex根负责合同、验证、集成和协调，不现场补产品或测试。每包只有一个明确变化原因和最小写集；新增文件要说明owner/消费者/为何现有入口不能承接。源码目标≤300行、函数≤40行；>500/>80按AGENTS阻断或精确受审局部例外。不能为满足两文件承诺把schema、IO、adapter、runner全塞入一个模块，也不能为凑行数复制协议或抽成无职责utils。写集重叠者按依赖串行，不用并发写入赌合并。

## 8. finding到产品验收与独立关闭

所有finding共享同一关闭链：现场原件→准确实现提交→失败与恢复回归→本项目真实消费→独立审核关闭。表中R为独立GLM/Kimi双席内容复审，S为native监督；原监督blocking依既有权限由原监督或具名无冲突替补复核。作者/集成者不自签。未触发真实场景标未验证，不补造调用；synthetic反例与实际模型使用分别报告。

| finding | 产品owner/失败与恢复 | 本项目实际使用与关闭 |
|---|---|---|
| GOV-01 | A/B/C：无作者final且测试绿/双席PASS仍拒绝；准确有效交付后恢复 | 本轮作者/修复final与delivery进入accept；R＋S |
| GOV-02 | A/B：缺旧准入/授权原件拒绝；实际读到准确旧源恢复 | 本轮计划/最终监督各核适用旧条件；R＋S |
| GOV-03 | A＋动作owner：变policy/候选/写集后旧许可拒绝；准确重新批准后恢复 | 本轮实际修复派发（若发生）及接收消费；R＋S，不把只读判定当自动止动 |
| GOV-04 | B：缺一席正文、截断、错路径或他席补读均拒绝；原席有效补审恢复 | 本轮每席raw独立重算；R＋S |
| GOV-05 | A/C＋Store发布：未知/漏席不能标eligible，状态与原件冲突拒绝接收；对账和发布恢复 | 本轮报告、动作与当前状态逐层核对；R＋S，不把Git事实改成治理通过 |
| GOV-06 | runtime：看护未ready、父先退、控制者崩溃、超时/输出上限与子孙未结束反例；身份不丢且确认清空后恢复 | 产品入口实际作者调用从启动前到整树结束证据；R＋S |
| GOV-07 | 共享adapter＋原parse：旧final后悬挂工具/尾随失败两消费者均拒绝；合法native尾随resume_hint通过 | 原sample及治理消费者实际调用修复路径；R＋S，不能只修B |
| GOV-08 | Runner/Store：绕过批准、stale、重复claim、预算/资源冲突不得派发/接收；合法一次执行及崩溃对账恢复 | 本项目真实动作由产品入口完成并消费准确许可；R＋S |
| GOV-09 | 容量owner：真实已知截断/超硬限制/关键unknown拦截；受审等价投影或预算方案重算后恢复 | 下一实际包先经预检，记录估算与真实差异；R＋S，估计不当成功保证 |
| GOV-S0-I01 | 最低监督不变量：双席全PASS但漏一席/旧票/自引用/人工摘要/监督未读必须拒绝；完整同subject包及真实读取恢复 | 本轮后继计划与最终监督实际消费产品证据包；R＋S，原S0 PASS不代本项关闭 |

还须有两个防空转反例：人工修改投影及其hash但raw不变，重算拒绝；只跑单元测试/离线报告而实际派发绕过产品入口，不能关闭GOV-06/08/09。完成记录分别报告合同获审、代码有效交付、旧消费者修复、产品检查、真实动作、监督与合入。全部finding满足其适用完成链才可结束本请求；后续登记或人工规约不是替代实现。

## 9. S1四项现场缺陷的产品关闭条件

四项均属本请求必修，不能仅更新文档后关闭。漏读由F/C/D生成并核计划到prompt，B核实际正文；无效审核输出由N1保留全文、B严格解析、A/C阻断；看护漏管由W/R2原句柄包含与真实生命周期修复；策略自读缺口由A/C最低集合＋F/D派生＋B实际覆盖闭合。每项必须具有本次真实失败fixture、明确恢复正例及独立双席/native关闭证据，且在本项目后继真实审核/必要C2作者链消费已交付产品。S1原失败票不变成有效票。

N2冻结旧测试409行及W复杂度风险须在具体交付按既有300/500、40/80审查，不能用去注释或无语义拆分绕过；native agent_file启动前复用runtime._verify_hashes并验证缺失/变字节阻断，当前存在不是未来启动证明。准确源映射已存在的runtime-plan改名不得误报丢源，C继续按原件ID/path/hash核验。这些验收仍使用既有13包，不新增相似调度器、台账或未审写集。

## 10. 全角色流水接线后继接口草案

状态：未准入、未实现，须独立审核后才能派发本节实现；不修改§6历史接口，不改变已冻结`57eddd8`的M/T材料、作者树或在途调用。S1/D1/X1是原S/D/X各自的顺序小片，不是新角色或新调度器；写集仍为原Store/dispatch_claims、development、Runner及各自已声明测试。M/T及完整流水线的边界见[基础合同](flow-foundation-contract.md)和[流水线提案](pipeline-amendment.md)。

### 10.1 共同约束与版本

本节采用新的`development-action/2`、`development-batch-config/2`、`development-store-config/2`、`development-outcome/2`。未明确改变的字段类型和拒绝未知键规则逐值继承§6；新schema不得接收旧字段别名。旧v1和S6行政原件只能沿既有适用范围核验，不根据内容猜测升级，也不因只改schema标签获得新权限。
下文`ID`为非空字符串，`SHA`为64位小写十六进制，`N`为非负精确int，`P`为正精确int，bool/float不作整数。`Ref`为§6的ArtifactRef，不采用M/T只有ID/hash的短Ref；凡引用M/T模板，D须从已pin索引补足路径并核ID/hash，不改变其原件。
审核阶段`review_stage`仅为plan/dispatch/accept，指本次动作所针对的治理证据阶段及该角色正文键；`node_id`是受审workflow节点ID，`role_id`是可配置协作角色ID，slot由workflow解析。三者不能互换：例如模板review槽位执行的是模型dispatch动作，其review_stage可以为accept，不能据此直接执行接收。

### 10.2 全角色节点绑定与容量

`development-batch-config/2`准确字段为schema、request_id、batch_id、model_call_limit、workflow（Ref）、roles（Ref）、node_bindings；不再接收author_bindings。workflow/roles引用T的准确输入原件，作为本单包subject内固定artifacts；不把运行中队列、意见或未来接收结果写入配置摘要。
node_bindings是node_id→binding的非空映射，必须恰好覆盖该workflow.stages的节点。每个binding准确为`{role_id, review_stage, profile_artifact_id, cwd, account_group_id, extra_resource_keys, access, session_request}`；前三个ID字段及cwd/账户/资源沿§6类型，extra_resource_keys可空、唯一；review_stage沿上段。
access仅为`read_only`或`package_write`；session_request仅为`explicit_fresh`或`implicit_fresh`。本片不支持resume；后继resume须另有准确许可与接口，不能把已有session当fresh。
binding.role_id必须等于workflow节点slot经workflow_bindings解析的角色；profile_artifact_id必须与policy.role_bindings[role_id].profile_artifact_id及roles[role_id].profile_ref的准确ID/hash相同。角色、profile、cwd、账户任一缺失或冲突拒绝；不能从模型名/slot文字补默认值。
角色prompt仍唯一来自policy.role_bindings[role_id].prompt_body_artifact_ids[review_stage]，不增加第二正文配置。review_stage不授予任何前置豁免；A须核本动作适用条件及阶段证据，D不能仅凭有正文就放行。
`development-store-config/2`在§6原顶层字段增加`executor_parallelism:P`、`global_parallelism:P|null`、`role_parallelism:{role_id:P}`，并按下段替换account_groups每项结构。executor_parallelism是本地作者并发配置，配置准备的默认值4，可由用户调整；只累计policy中kind=author的在途claim，不是全角色总上限或服务商账号上限。global_parallelism的null表示未设置本地团队总限额，role_parallelism可为空，仅显式列出的角色有限额；均不表示服务容量已验证为无限，不能默认给每个审核/监督角色固定1个实例。
v2的account_groups仍为非空ID映射，每项准确为`{model_call_limit:N|null, local_parallelism:P|null, service_limit, unknown_limit_policy}`；删除无来源的capacity字段。service_limit精确为`{status, capacity:P|null, evidence_ref:Ref|null}`：status为verified/unknown/stale；verified必须有非null capacity及证据，unknown/stale的capacity必须null，证据可为null。证据必须支持该账号适用范围内的限制，成功跑过若干并发只证明该次成功，不证明服务最大容量。不同模型/角色共享同账号的claim统一计数。
unknown_limit_policy仅为hold或use_local_limit：账号限制unknown/stale时，hold阻止该账号新claim并报告capacity_unknown；use_local_limit仅在local_parallelism非null且authority_ref明确批准按该本地限额承担未验证服务限制的不确定性时允许，仍显示服务限制unknown/stale。缺该授权或local_parallelism为null均阻断，不能取executor默认4充当账号额度，也不臆造1路兜底。verified时仍同时执行显式本地限额和已证服务约束；所有适用约束与资源互斥取交集。
本地限额和服务证据分别冻结进config_digest；S只证明受本Store管理的claim不超适用限额，不将本地claim数冒充供应商全账号实时用量。已知外部占用/服务限流或证据失效必须沿原观测/对账入口处理，未知外部用量不补零，不承诺远端不会拒绝。unknown_limit_policy不豁免运行时能力、权限或身份unknown门禁。
最小兼容：§6的v1 account_groups.capacity及“容量4”原文保留为旧候选，不静默映射为v2已证服务限制；迁移须按原授权证据将其归为明确本地配置或verified服务证据，无法区分则unknown。v2不接收旧max_parallel/role_capacities字段；同一成本model_call_limit仍沿§6记账，与并发配置分离。此处承接运行时计划§4.1的执行者配置/真实账号限制分离，不新增真实账号上限。
初始化仍拒覆DB，注册仍是同request的不可变追加；容量/绑定修改不提供裸Store.update出口。旧配置迁移与容量降低期间的在途处置不在S1自动实施，见10.7待决项。

### 10.3 动作及会话身份

`development-action/2`准确字段为schema、action_id、request_id、batch_id、kind、expected_revision、subject_digest、index、policy、policy_digest、package_id、node_id、role_id、review_stage、attempt_id、requested_session_id、prompt、profile、evidence_root；删除v1的session_id，不允许caller提交actual_session_id。
kind仅dispatch/accept。dispatch的package_id为本固定单包ID；node_id/role_id/attempt_id非空，review_stage有效，prompt/profile为非null Ref；其余字段沿§6并匹配已注册节点、准确subject和原件。D不能接受caller自由组合一个未注册节点。
accept的package_id/node_id/role_id/review_stage/attempt_id/requested_session_id/prompt/profile全部为null；仍由Runner重算该固定单包的全部接收条件，不执行模型、不以某个reviewer节点意见直接接收。
explicit_fresh要求requested_session_id为非空ID，精确argv中存在已审方言要求的唯一fresh session selector；implicit_fresh要求其为null，精确argv不得有session/resume选择器且满足该方言fresh必要参数。两者都须有固定profile能力证据；null不代表跳过会话独立性。
actual_session_id只能来自N1/N2核过的原生流，非空ID或null；未知时保持null。显式请求与实际值不等即身份冲突；fresh实际会话若与本Store已记录其他attempt会话相同，保留原始outcome并标违规，不能覆盖旧身份或计为独立有效意见。
`development-outcome/2`在§6的全部字段上增加`actual_session_id`和`session_evidence`（Ref或null）；actual非null时session_evidence必非null，引用产生该身份的已冻结raw；实际提取和原件hash由R2/N1/N2证明，不接受调用者自报。未知actual不阻止失败原件落盘，但不得满足要求实际身份的接收条件。
S1在finish事务登记已证实际会话及碰撞事实；本片不宣称在原生init出现瞬间已完成跨进程会话隔离。启动前只核请求身份唯一和fresh能力，启动后最终独立性仍由A/B判断；实时会话绑定回调若被要求，须先冻结R2/S新增接口。

### 10.4 逻辑动作键与原子claim

dispatch的logical_key由D对`[request_id,batch_id,subject_digest,node_id,role_id,review_stage]`作既有规范摘要，Store以已注册配置重算；action_id、attempt_id、requested_session_id、expected_revision不参与该键，避免换ID绕过重复动作。
§6内部claim删除session_id，增加node_id/role_id/review_stage/logical_key/requested_session_id，其余字段保留。S1以logical_key、attempt_id、非null请求会话及原资源分别校唯一；隐式fresh的null不是一个共享会话锁，也不能伪造session字符串填充。
同逻辑键且相同绑定的重放返回原claim/attempt定位，不新增预算、进程或派发；同键不同attempt/profile/prompt/index等绑定拒绝冲突。相同action_id被用于不同键也拒绝。CAS revision冲突只能重新核同一动作，不得因此生成新attempt启动。
本片只提供每个固定逻辑动作的一次受管执行及幂等定位；失败后的显式后继attempt授权转换尚不在该接口中，不能靠换action_id绕过。该限制不形成review/repair次数上限；继续修复须先由后继状态转换合同承接，而非临时移除幂等。
claim→contained+suspended→mark_dispatch_started→resume→finish的顺序沿§6；全角色统一reserved/used计数。退出码、有效final、接收、供应商计费和整树清空分别举证；unknown在途资源不因角色是只读而释放。

### 10.5 权限与材料装载

package_write仅允许当前policy中具作者身份且对本包获写权的角色，规范化profile.permissions.write_files须逐值等于本包allowed_paths；写入资源由D派生，caller不得删减。未赋权角色即使slot叫produce也拒绝。
read_only要求profile.permissions.write_files为空、工具与运行时实际只读能力符合原合同；reviewer/supervisor在本片必须read_only。其cwd可以是本包固定只读材料/候选树，但必须等于已注册cwd及profile.permissions.root，源字节/hash固定，不能读正在变化的作者工作树冒准确候选。
environment白名单、runtime/方言hash、权限root、完整prompt/read_plan和Windows容量预检仍走原R1/R2/F/C，不允许D为审核临时扩大权限、加入未批准目录或使用bypass。只读不占作者文件写锁，不占作者专属executor_parallelism；但仍计入同账号、显式配置的全局/角色限额及资源，不能因只读漏账。
D1沿既有公开装载入口生成动作和内部claim，C/A内部判定需要的动作上下文为`{node_id,role_id,review_stage}`，必须由已注册binding导出并与action比对；不向用户开放预填PASS/NativeObservation。A/C需正式支持此上下文后，才能核非作者dispatch，不能复用旧“目标包作者”分支假称全角色已支持。

### 10.6 小片依赖与验收

S1独占原S写集实现v2配置/注册/全角色claim/计数与终态会话登记；D1独占原D写集消费A/C/F及真实S1；X1独占原X写集消费D1/S1/R2，实现一个已准入动作的安全启动与终结。不先加第二poll loop、队列库或模板Scheduler；同owner后继S2/D2/X2顺序交付。
必要回归：默认4仅约束作者，第5作者受限而审核在其余明确约束允许时仍可启动；用户调executor_parallelism生效；同账户跨角色统一计数；unknown服务限制不变成无限/已满，hold拒绝、具名授权且有local限额才允许use_local_limit；4次并发成功不得自动写成verified最大值；非作者写权限拒绝；同逻辑键更换attempt拒绝；重复终态不重复计费；native fresh null不占伪共享session；显式请求/实际会话冲突；未知actual留证但不计有效票；错误node/role/review_stage/body零spawn；暂停后不resume；启动记录CAS冲突不重复创建进程。
组合验收必须调用真实A/C/F/R2而非caller PASS；用自有受控进程证明顺序和失败保真，再由既有批准流程选择必要真实模型工作dogfood。M/T单测、S1事务测试及X1单动作成功均不能宣称队列流水或调整闭环完成。

### 10.7 明确未决及后继承接

本节字段是可审核草案，以下必须在对应实现派发前具体冻结：A/C对每类node的准入前置/未来意见允许缺席边界；显式返修后继attempt的授权和旧claim终态转换；v1已有DB迁移及容量变更。未知不放行，不要求为此改动已冻结M/T。
S2将完成事实、有效交付及后继就绪在同Store内原子衔接；D2组织ChangeProposal，S3核独立批准后CAS应用RunAmendment；M-Q消费S2的一致队列快照；X2统一消费事件并即时补发。具体queue/amendment schema不由本节暗设，须各片独立准入且仍是本请求必需交付，不能移为远期可选。
完整验收保持：快包双审不等慢包、双意见齐备才监督、返修只影响本包及真实依赖、暂停/重复事件/未知进程不越界、受审调整后实际补发。不得把S6旧意见、v1动作或M/T结构valid作为本节实现或接收证明。

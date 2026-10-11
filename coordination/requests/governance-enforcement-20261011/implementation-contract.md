# 开发治理产品修复实施合同（后继候选）

范围：GOV-01–09及GOV-S0-I01的产品责任、共享接口与失败/恢复验收；维护者：Codex合同集成者；状态：待后继独立双席复核及native监督，未授权新增模型调用或实现。旧[contract.md](contract.md)为`ee94914543e9248d17c9fde670869744173ea22a`送审原件，本文件不修改、覆盖或倒签它。原两席S0的PASS仅覆盖原scope，不证明本后继合同已获审。当前状态、调用预算、写集分包和顺序分别由[result](result.md)及实施计划维护。

需求依据：[范围补充](scope-amendment.md)、[调查](investigation.md)、[AGENTS](../../../AGENTS.md)、[design](../../../docs/design.md)。本文件是后继接口候选，不另建问题、批准、PASS或进程状态台账；长期规则仍归AGENTS/design，通用状态仍归现有Store/Runner，原件沿同一request保存。

## 1. 承接与变化

旧合同中以下要求全部保留：旧策略独立pin、旧条件完整继承、准确角色/候选/原件绑定、逐席实际Read正文、作者有效final、独立审核与监督、unknown可见、无豁免入口、严格JSON和类型敏感摘要、有限阶段依赖、纯观察不得执行动作、实际使用和独立关闭。预算不足、内容PASS、native PASS或临时行政例外均不能抵消缺项。既有失败和Git合入事实不改写。

| 后继变化 | 原缺口与明确边界 |
|---|---|
| 加入不可省略的监督依赖不变量及单独证据包摘要 | 修GOV-S0-I01；原subject继续排除意见，监督输入绑定同subject的已完成审核attempt，而非把未来原票塞回subject |
| 共享原生序列观察由RuntimeAdapter唯一维护 | 修GOV-07并避免B复制parser；旧产品parse与B共同消费，旧样例路径也必须获得修复 |
| 产品化容量预检、受控开发执行和动作准入 | 承接GOV-06/08/09；复用现有runtime/Store/Runner，不另建通用Scheduler平台或第二启动器 |
| 分阶段交付但所有finding仍属于本请求 | 三包只读检查不再被描述为全部治理完成；每项均须实现、回归、真实使用、独立关闭 |

只新增必要的v2协议：`development-review-policy/2`、`development_audit/2`、`development-invocation/2`、`development-final/2`、`development-observation/2`、`development-report/2`；原`development-delivery/1`继续承接。report在旧字段外增加batch_id/evidence_bundle_digest（无监督时null），B新增字段见下文。未列变化的字段、精确类型、摘要算法和拒绝未知字段规则仍依旧合同。v1原件只能作为历史证据或旧scope回放输入，不能静默升级成满足新监督不变量；不要求补造历史v2 final。

v2的role_bindings另增加`profile_artifact_id`（manual为null），指向当前subject内已审profile文件；实际动作必须消费该准确文件/hash，不能只比adapter/model名。profile依现有配置/权限schema，新增dialect定位见第6节。policy没有新增关闭监督最低要求或partial_accept的开关。

策略修订由旧授权规则受审，不能由待审policy自行授予放宽权限。后继policy继续逐值承接有效原条件；分组read_coverage只合并同角色同阶段的机器条件，不删其required_evidence，各条仍全部AND。request.conditions始终保留完整policy列表，不能因为当前阶段不claim历史义务而删条件。

## 2. 最低不变量与可配范围

以下是产品最低判据，不是可由policy关闭的开关，也不按CodeBuddy/Kimi品牌硬编码：

1. 阶段若包含kind=supervisor和必需kind=reviewer，监督输入必须覆盖该阶段**全部必需reviewer**的准确有效final及完整逐席原生观察/coverage。少一席、旧候选、摘要替原件或监督未实际读到均阻断。A验证审核者存在不替代监督的独立判断。
2. policy确定角色、独立性、每阶段条件和额外必读源；它可以增加监督材料，不能取消上一条。两个角色重命名或复用同session/raw不产生独立票；作者、审核者、监督的独立性延续旧合同。
3. 旧规则/旧准入条件使用固定源hash；变化的候选源使用subject内准确hash。plan历史调查可由accept沿prior链重算，不要求每席再读全部历史；accept仍直接核适用旧条件、当前候选、验证、作者交付及本轮finding，不能用plan票代内容票。
4. 成功仅属于明确层次：原生进程/协议结束、有效作者交付、审核完成、监督完成、产品动作许可、动作完成、合入分别举证。临时check报告不变成批准本身，也不自动更改当前状态。

## 3. 监督证据的无循环绑定

保留`subject_digest`作为候选内容、策略、条件、包定义的共同身份；它不包含本阶段审核/监督意见、调用结果、证据包或最终检查报告。同subject可发布后继不可变evidence-index，显式承接已完成attempt；不覆盖原索引，也不按文件名/latest猜当前索引。

同阶段的处理顺序固定为：冻结候选→完成全部必需reviewer→生成准确监督证据包→监督读取并给意见→最终阶段判定。plan和accept均如此；dispatch依旧重算prior plan，不凭空要求未来作者session/final。审核者可并行，监督依赖其完成。重新审核改变任何必需reviewer原件后须新证据包及新监督意见，旧监督不能沿用。

### 3.1 证据包最小schema

`development_audit/2`在原字段外新增`supervision_bundles`，为stage→bundle artifact ID的映射；只允许plan/accept。没有监督的阶段不要求包，含监督和必需reviewer的阶段必须有且只有一个被当前索引显式选择的包。该包是本次输入原件，不是状态库。原artifacts.kind增加`review_bundle`；可读票据/coverage仍为projection。

`development-review-bundle/1`准确字段如下，未知字段拒绝：

| 字段 | 语义 |
|---|---|
| schema/request_id/stage/subject_digest/policy_digest | schema为development-review-bundle/1；stage为plan或accept，全部绑定当前阶段候选 |
| reviewers | 按role_id排序的非空列表，恰好覆盖policy该阶段全部必需reviewer，无多余替补或重复 |
| reviewers每项 | role_id、attempt_id、raw_artifact_id、raw_sha256、invocation_artifact_id、invocation_sha256、final_artifact_id、final_sha256、coverage_artifact_id、coverage_sha256 |

包本体不含自身digest；`bundle_digest`是其严格canonical JSON摘要。raw/invocation指向该role该阶段同subject的已完成原件；final/coverage指向第4节产品确定性投影。C重新读取并重算，不信任包内用户填的通过结论。每个当前阶段/角色只选择一个有效attempt；被替代attempt留在历史索引，不能混入当前有效票。包不含监督自身attempt/final、最终DevelopmentReport、可变result，也不递归引用其他监督包。

`development-invocation/2`和`development-final/2`各新增`evidence_bundle_digest`：监督为准确bundle_digest，其余角色为null。A核二者相等且等于C重算值；监督raw中的实际Read须覆盖包、每席final投影及coverage投影，不能只读bundle清单。这里是独立于subject的附加证据绑定，允许所有人审核同一个候选又避免future-vote/self-reference循环。

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
| B：`observe_development(trace, invocation, requirements, artifacts)` | v2改变首参数，直接消费NativeTrace；requirements仍为evidence/projection_rules，artifacts仍为ID→{path,bytes}。输出DevelopmentObservation，承接原NativeObservation字段，另含role_id/stage/subject_digest/policy_digest、final_text/final_event_ordinal及第4节coverage定位字段；核实际Read内容、治理final和进程退出，不重解析provider序列 |
| B：`render_review_evidence(observation, representation)` | 只渲染第4节确定性原票/覆盖证据，不加载文件、不决定准入、不提供人工可编辑PASS |
| A：`evaluate_development(stage, policy, request, observations)` | 延续纯schema/阶段/身份/条件判定；request envelope保留index/declarations/prior_results/policy_digest，增加supervision_bundle（C重算的包或null）。observations为attempt_id→B结果；A独立检查最低监督集合、摘要、final声明与覆盖，不只相信C已检查标志 |
| A：`evaluate_review_evidence(stage, policy, request, observations)` | 供证据准备使用，复用同一schema/版本/作者交付及必需reviewer判据；尚无supervisor是此准备步骤允许的唯一未完成后继。返回`{decision:ready|blocked|invalid, findings}`，ready仅表示可生成监督输入，绝不等于plan/accept eligible，也不供Store动作授权 |
| C：装载/组合/CLI | 严格解码、核pin/hash/文件不变、按reviewer→bundle→supervisor顺序调用共享观察/B/A；只读命令早于Store/Runner返回，准备命令仅指定证据输出。复杂文件装载/组合可由专属development_audit模块承接，不能堆入cli或把协议解析复制出来 |

共享观察需先严格JSONL验证，再复用既有_events；本轮只有一个原生序列owner。必须识别调用/返回配对、冲突身份、失败或重复final、final后新assistant/tool、未完成工具；Kimi最终assistant后仅允许已观测的meta/session.resume_hint白名单。缺能力保持unknown，不从init工具目录推断实际调用成功。工具本身失败可作为负例证据，但失败Read不贡献覆盖。

必要消费者合同测试包括旧sample parse、治理B和原生真实fixture：同一个坏序列两条消费者均拒绝，同一个合法序列两者对身份/工具次序一致；治理final schema不强加给旧sample业务final。B仍须核True/1/1.0、长行截断、错误路径、角色独立覆盖和经审定等价投影。

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

纯API `assess_development(requirements, artifacts, dialect, budgets)`返回ReadinessReport，包含decision（eligible/blocked/unknown）、按席位的字节数/最长行/需读范围/分片数量、估算tokens及输出量、工具/turn下界与明确假设、findings。dialect和计数规则绑定准确runtime文件hash/版本及原能力证据，不接收临时env自填阈值；budgets由已批准包提供。

dialect是准确profile引用的已审配置：`schema=development-dialect/1`、`adapter`、`implementation_file`（准确path/sha256）、`read_limits`（max_lines/max_chars_per_line/max_estimated_tokens）、`token_estimator`、`turn_counter`、`source_artifact_id`、`source_sha256`。限值为正整数非bool或null；计数方法为受实现支持的版本ID或null，未知不可偷偷选默认值。原profile仅增加`development_dialect`对象，保留其现有permissions/environment/executable/executable_sha256/entry/entry_sha256/max_turns/timeout_seconds/output_limit_bytes，以及native已有agent_file/agent_file_sha256。开发runtime每次启动前除原_verify_hashes外实测implementation_file，证据源也须hash吻合；不能把一个安装版本的Read限制泛化到另一个版本。

本机已核CodeBuddy的node executable、CLI entry、实际Read方言实现dist/codebuddy-headless.js是三个不同文件（已见hash前缀分别63c…、426186…、f9affe…）。本合同不改变其可执行entry或假定headlessJS可直接启动。implementation_file必须定位真正承载已审方言的文件并由原证据说明其与入口的加载关系；未知则容量unknown。claim.runtime_digest定义为canonical_digest({executable_sha256,entry_sha256,dialect_implementation_sha256,agent_file_sha256})，后者对不适用角色为null，各实测值须与profile相等；不是任意一个node或JS的裸hash。budgets准确为max_turns、timeout_seconds、output_limit_bytes，分别沿现有profile精确类型和范围规则，profile与budgets逐值相等。

重复要求可按同一席同一准确artifact/range合并读取计划，但不能跨席合并或删除义务。已知长行截断、无法表达必读内容、确定超硬限制须blocked；无法估算的关键项标unknown并交受权入口，不能默认为足够。估算不保证完成，不把CLI num_turns当max_turns，不把工具调用数当模型轮次。恢复只能通过受审的范围/等价表示/预算调整并重算，不自动缩减required或加模型调用。

### 6.2 执行、看护与状态

开发执行继续使用现有runtime/adapter/environment边界，增量接入独立cwd与受控evidence_root；不要求业务开发树伪造sample marker，也不删除sample原有保护。对外开发调用拟为`runtime.invoke_development(profile, prompt, cwd, evidence_root, attempt_id, session_id)`，具体最小扩展由运行时提案固定。它必须真实消费准确profile/runtime/write-set/session及预算，不只是写一份watchdog参数。

看护/进程包含边界必须在子进程可运行前建立并持续至整个受管树确认结束；控制者退出、父进程提前退出或PID复用不能失去子孙身份。超时、输出越界、看护失败须终止受管树并确认，不得仅杀父进程后回成功。不支持的宿主能力fail closed，不能以“最佳努力taskkill”声称无看护空档。实际平台API、资源释放与崩溃窗口须有官方依据和真实无模型子进程反例，不在本合同凭散文判定Windows实现已成立。

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

claim预算字段来自已批准profile；总次数/并发可用额由同一Store受审批次配置控制，不能仅检查单次max_turns。尚未结束的调用继续占用资源，不因超时文字或父进程已退出便释放。action_id/attempt_id重复必须幂等返回原定位或冲突拒绝，不能二次启动。

runtime通过受控`on_created(process_identity)`回调执行上述Store记录，顺序必须是contained+suspended创建→看护/日志就绪→持久化启动身份→resume。创建失败不计真实启动，保留claim失败；记录失败立即终止尚未运行的受管树，不能先resume后补记录。创建及记录成功但resume失败，used保留并记录resume_failed，不退回额度暗中重试；实际是否有模型/provider活动单列unknown或具证据的未发生，不把calls_used冒充供应商计费。控制者在记录/恢复窗口崩溃须靠包含边界终止或由原claim对账，不能静默释放未知进程资源。`invoke_development`因此增加具名参数`on_created`，只允许动作owner传入此生命周期回调，不执行调用者任意模型代码。

`evidence_root`必须是显式批准的请求证据根，与cwd和permissions.root分开；仅准许在该根下按不可混淆attempt_id创建专属目录，拒绝路径逃逸、已有冲突、原始reparse/symlink链。检查顺序沿既有paths/adapters canonical规则，不能先resolve后隐藏reparse；证据目录不授予模型源码写权，也不继承sample marker假设。日志路径启动前独占，运行中保留增量/partial字节及原hash，异常不能覆盖旧stdout/stderr或删失败事实；读取/清理各自沿既有权限入口。

### 6.4 唯一Store的开发配置来源与写集owner

已检索事实：现有Store.initialize只校dict和非空steps，并冻结config/config_digest；sample.initialize另有固定schema2、四角色、model_call_limit=4与sample marker。开发不能调用sample初始化伪造样例，也不能由S/D各建一套配置。**S包唯一修改store.py及其专属测试**，新增以下开发模式校验/事务；**D包唯一维护development.py及其专属测试**，装载已审文件、调用C及Store；**R1单写paths.py**承接证据根，**R2单写runtime.py**核profile/方言/启动回调；具体依赖见实施计划。不能通过裸Store.update(data/calls_used/config)绕过开发专属事务；sample原语义单独保持兼容。

开发控制根仍只有`.runtime/state.sqlite`和现有events/投影。D公开`initialize_development(control_root, config_path, config_sha256)`严格加载独立批准pin，交S的`Store.initialize_development(config)`；后者校完整开发schema再复用现有初始化事务及`steps=['development']`，拒绝覆盖已存在DB。旧Runner.run/sample handlers不消费此development步骤，新动作使用专属方法；同一request的后续批只注册到这一个Store，不能各批新建DB清空总预算。配置文件由受权集成者按已审计划准备，产品校验并冻结；模型不自设额度。

`development-store-config/1`准确字段：schema、request_id、control_root、evidence_root、authority_ref（ArtifactRef）、model_call_limit（非负int）、account_groups（非空ID映射，每项capacity为正int、model_call_limit为非负int）、bootstrap_acceptance_refs（已获审ArtifactRef列表）。**这里全局及账户组model_call_limit均是Store启用时已审剩余额度，不是整批历史总上限**；初始calls_used=0仅表示本Store尚未执行调用。authority_ref必须绑定初始化前的实际用量/剩余额度对账，含已批总额、此前已用、仍在途预约及差额，覆盖S0、失败、修复等全部实际调用，不能只统计accepted批。未知消耗先保守占用并阻断无法确认的剩余额度，不能补0。初始化前冻结对账检查点，其他渠道有新调用则旧剩余快照失效，须重新获准后初始化。

全局及各账户组分别核本Storereserved+used不超过上述剩余限额，容量核在途claim；同一账号的不同模型不能拆组规避并发。group是受审显式配置，不按agent品牌推断；默认容量4只是当前团队配置值。authority_ref定位原授权和准确启用对账，不是本config自己的摘要。报告分别列“启用前已用/在途”“本Store已用/预约”“剩余额度”，不把bootstrap接收导入变成再次消耗或补回预算。一个request固定一个control_root，既有DB拒绝重初始化；换目录重建不能被认作新的额度池。config_digest由Store计算并保护，任何后续限额/根路径变化均须新受审配置迁移，本切片不提供临时改限入口。

bootstrap_acceptance_refs只允许本请求产品Store尚未可用时、作者/双席/监督全部有效且已具名接收的早期批次原件；缺作者final的旧B27等历史例外不符合导入条件。该列表在初始化时固定；Store可用后的新批必须使用正式产品接收，不借bootstrap入口减掉门禁。S提供`Store.import_bootstrap_acceptance(expected_revision, verified_admission)`的CAS写入，D仅在第6.0节重算和pin检查后调用，不直接改data。

每批plan的subject必须包含固定ID`batch-config`及准确字节hash，profile文件和prompt body亦在该subject.artifacts中。`development-batch-config/1`准确字段：schema、request_id、batch_id、model_call_limit（正int）、author_bindings（package_id映射）；每个binding含prompt_body_artifact_id/profile_artifact_id/cwd/account_group_id/extra_resource_keys（非空字符串的去重列表，可空）。package集合来自同批受审index，不在config再维护另一份；binding必须恰好覆盖这些包，account_group_id必须存在全局config，cwd必须等于该profile.permissions.root并落在本包已准备工作树，不能从action临时替换。

D公开`register_development_batch(store, plan_index_path, policy_path, policy_sha256, expected_revision)`，从已完成的准确plan装载batch-config并调用C验证；S的`Store.register_development_batch(expected_revision, batch_config, plan_admission)`核同request、唯一batch ID及批准关联，追加不可变配置与摘要到同一Store的data.development，不改全局config。plan_admission包含准确plan subject/index/policy与必需票据引用；batch-config本体不含未来plan票或index hash，避免自引用。重复同摘要幂等，不同摘要拒绝。后续claim必须与已注册batch_config_digest完全相同。

profile定义真实可执行入口、模型、工具、环境、精确permissions与单次预算；batch-config只把包绑定到该profile/cwd/账户组，不能再覆写。D根据已审package.allowed_paths与cwd规范化并核对profile.permissions.write_files逐值相等，然后派生强制排他资源`file:<规范绝对写路径>`；再加入受审extra_resource_keys。账户组容量单独消耗，不能把它当全组互斥锁导致4并行退化为1。Store只接受与已注册包推导结果相同的resource_keys，不接受caller删掉冲突路径。读者无需占作者排他写锁，具体读写协调沿受审包依赖。

prompt来源唯一为已审prompt_body_artifact_id的UTF-8正文；D纯函数`render_development_prompt(body_bytes, context)`在正文前添加一行canonical JSON上下文、两个换行，再拼接原body字节，不作自由模板替换。context准确为schema=development-prompt-context/1、request_id、batch_id、package_id、role_id、stage=dispatch、subject_digest、policy_digest、evidence_bundle_digest=null。body不含自身最终hash或可变候选摘要；实际完整prompt在动作前沿请求证据出口冻结，action.prompt引用其hash，D重算字节一致性。这样计划批准正文与生成规则，最终prompt绑定准确候选却不会把自己的hash塞回subject。新增文字、权限或不同渲染规则均拒绝。

D是上述prompt渲染/装载的唯一owner；A/B仅比较实际final与invocation的角色、subject、policy等绑定，C只准备证据投影，不另生成prompt。

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

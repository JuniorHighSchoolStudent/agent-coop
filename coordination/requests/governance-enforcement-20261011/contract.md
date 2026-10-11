# 开发治理确定性检查合同（候选）

范围：人工开发流程的plan/dispatch/accept只读前置检查；维护者：Codex合同集成者；状态：待fresh双CodeBuddy设计审核及fresh native监督，不是已实现能力或writer许可。来源：[调查GOV-01–05](investigation.md)、[AGENTS](../../../AGENTS.md)、[design §5.2/§7.4/§7.5/§8.5](../../../docs/design.md)、[当前团队](../../../docs/roadmap.md)。调查基线`9a4855a39121f2483e1630082bc36533a2165a5e`。

## 1. 选择、非目标与权威

选择“原请求索引＋两个纯检查模块＋单一只读CLI”。只改prompt不能证明执行；直接引入通用Scheduler会扩大当前切片。保留现有Store、Runner、产品sample及产品parser，本次不迁启动器、不发模型、不写状态、不自动接收/合入。检查器不是OS沙箱、身份认证服务或防恶意宿主系统。

本切片**不支持豁免入口**：缺作者有效final、旧条件、必需席、必读证据或明确能力，一律阻断依赖动作。C2/native PASS、预算耗尽、历史先例及“仅本revision例外”不抵消缺项。旧批已发生的测试、接收和合入仍是历史事实，本合同不倒签，也不通过新命令撤回Git。

权威不新增副本：AGENTS维护人工操作规则，design维护长期权限/监督/独立性语义，roadmap维护团队及当前切片，原请求保存冻结policy、原件与input-index，原result维护当前结论。待本候选通过后，需长期生效的条款回写相应owner；本文作为本次schema/API冻结原件。CLI报告仅是对准确输入的派生检查结果，不成为新PASS台账。

## 2. 三个小包与唯一接口

| 包 | 唯一产品/测试写集 | 输入、输出与消费者 |
|---|---|---|
| A：阶段策略 | `agent_coop/review_policy.py`、`tests/test_review_policy.py` | `evaluate_development(stage, policy, request, observations)`返回DevelopmentReport；只校验schema、版本、阶段、角色、独立性和必需前置，消费B的确定性观察，由C调用 |
| B：原生证据覆盖 | `agent_coop/review_coverage.py`、`tests/test_review_coverage.py` | `observe_development(adapter, raw_bytes, invocation, requirements, artifacts)`返回NativeObservation；复用`adapters._events`解码，核实际终态/配对Read/返回内容，不改adapters现有产品parser，由C调用 |
| C：只读组合入口 | `agent_coop/cli.py`、`tests/test_cli.py` | 新命令`python -m agent_coop verify-development --stage <stage> --index <path> --policy <path> --policy-sha256 <sha256>`，stage为plan/dispatch/accept；加载/校验原件→B→A→stdout JSON，早于Store分支返回 |

A/B使用本合同的同一数据表示可并行，不共享写文件；C可按API开发，但组合接收必须等待A/B准确交付。每包真实作者为受派CodeBuddy，根只运行验证和集成；每个后继修改均须有效作者final。现有文件规模约束继续适用；若C的组合代码使cli接近硬限，须在派发前审核是否新增仅承担文件装载/组合的`development_audit.py`，不能作者自行扩写集，也不能复制A/B逻辑。当前默认不增加该文件。

纯函数接收普通dict/list/bytes值，不读磁盘、不调用Git/Popen/网络、不改入参或全局环境。相同字节输入产生相同语义报告，不把当前时间放入决定条件。测试可构造显式fixture；生产CLI不得接受用户预填NativeObservation替代B重算。

## 3. 信任起点与摘要

受权调用者从已发布的旧策略选择`--policy`及独立固定的`--policy-sha256`；policy不能由待审请求自己选取。CLI校验policy原文件字节SHA与独立pin相等，再校验其受支持schema。人工发包人必须在依赖动作前核对这两个参数来自旧授权入口；随手给任意文件及其hash不构成合法授权。纯本地checker只能证明所给固定原件一致，不能证明机器外授权或防止调用者伪造整套raw；此信任边界必须在报告中保留。

通用摘要均用小写64位SHA-256；Git提交是完整40位十六进制。artifact摘要覆盖实际字节。语义摘要统一为UTF-8、无BOM、JSON键排序、无多余空白、ensure_ascii=False、allow_nan=False；重复键、NaN/Infinity、错误类型拒绝，bool不当整数。换行属于原件字节，不静默CRLF归一化。

`subject_digest`只覆盖request中的`subject`对象；其中含准确base/subject commit、受审文件的路径/字节SHA、policy_digest、原条件摘要及包定义摘要。它不包含意见、调用、检查输出或自身摘要。policy原件不含自身摘要，外部pin承接。request manifest不收录自身index、可变result或本次报告，避免自引用。输入声明了排除项也不能排除policy要求的文件/条件；required集合从固定policy求出，不从最新manifest猜测。

纯接口中的`policy_digest`由C对已pin的policy原字节计算，置于第7节的内存request容器，不添加到拒绝未知字段的policy原对象。报告不得引用自己的摘要。raw日志、invocation metadata和作者结束后的交付快照均独立冻结，原件自身不带自引用hash。

## 4. 固定策略schema：development-review-policy/1

policy位于原请求的已审声明文件，不建全局注册表。只接受下表字段，未知顶层字段拒绝；没有`waiver`、`override`或`allow_missing_final`字段。

| 字段 | 准确语义 |
|---|---|
| `schema` | 字符串`development-review-policy/1` |
| `policy_id`、`revision` | 非空稳定ID，正整数revision；与原授权入口一致 |
| `authority_refs` | 非空artifact ID列表，定位批准该旧策略的已有原件；首次bootstrap由明确用户指令＋原规则入口固定，不能引用本次候选自己的PASS作授权 |
| `role_bindings` | 以角色ID为键；每值含`actor_id`（唯一发包人绑定的非空身份）、`kind`（integrator/author/reviewer/supervisor）、`adapter`（codebuddy/kimi/manual）、`model`（字符串或null）、`model_required`（bool）、`required_capabilities`（字符串列表）、`dispatch_capabilities`（下述profile证明映射；非作者可为空）；manual集成者的必需能力可为空，但不能占原生必需审核/作者/监督席 |
| `stages` | 准确包含plan/dispatch/accept；每值含`required_roles`、`required_condition_ids`、`required_evidence`、`required_decision`；required_decision固定`pass` |
| `conditions` | 按稳定condition_id列对象：`source_artifact_id`、`source_sha256`、`kind`、`applies_to`、`owner_role`；kind本切片仅为author_final/role_decision/read_coverage/identity/version/policy_unchanged；无自然语言解释器 |
| `independence` | `distinct_review_sessions=true`、`author_not_reviewer=true`、`supervisor_not_author_or_required_reviewer=true`、`excluded_session_ids`；前三值不可关闭，排除集合不得由request缩小 |
| `projection_rules` | 已获旧策略认可的有限规则列表，每项含projection_id/source_artifact_id/projected_artifact_id/algorithm；仅本节所列算法，无自由代码或LLM等价判断 |

role必需能力至少可表达`native_read_content`、`terminal_completion`、`tool_call_pairing`；本轮实际状态为supported/unsupported/unknown，来源由B的原生观察及受权invocation绑定给出。init工具目录不是能力；未知不能当支持。native模型不可观察时允许model=null、model_required=false并显示unknown，但这不豁免其余必需能力。CodeBuddy当前作者/两审核席要求实际模型与绑定一致。角色名不能授予能力。

dispatch尚无作者调用，不要求其未来session或NativeObservation。仅核旧规则审定的准确profile证明：`dispatch_capabilities`以capability为键，每项准确含`source_artifact_id`、`source_sha256`、`scope`（固定`profile`），adapter/model继承该role绑定。这些映射是受审policy的一部分，源必须是设计审核已核对的实际能力原件；未知或未经审定的能力不能填入映射。C校原件hash，A核required_capabilities被该固定证明完整覆盖；缺失则CAPABILITY_UNKNOWN。它仅证明所给adapter/model配置的已审能力范围，不证明未来session成功，也不声称B重验了历史probe。历史原件不加入本轮attempts、不要求development-final/1、不新增模型调用；现有矩阵等原生证据可依旧规则受审复用。accept再由本轮B核实际session/能力/有效final，不允许profile证明替代本轮观察。

`required_evidence`每条准确字段为`condition_id`、`role_id`、`artifact_id`、`source_sha256`、`coverage`（full或lines）、`ranges`（full时空列表；lines时闭区间正整数列表）、`projection_id`（字符串或null）。`source_sha256`非null时固定旧源字节，必须与实测hash相等；为null时仅表示policy允许该artifact是变化的候选源，真实hash必须来自本阶段subject.artifacts并与装载字节相等，不能取未绑定的导航字段。policy仍固定角色/ID/范围和完整required集合；每阶段意见绑定subject_digest，因此代码字节变化需要新阶段票，不需更改policy。变化源优先full，避免旧行范围漏掉新增部分。该要求属具体席位，不可取所有人覆盖并集。一个artifact可能被多个角色要求；只有策略明确的角色分工生效。

必读基线包括AGENTS相关规则、design相关权限/监督合同、roadmap当前角色、准确候选计划/接口、承接的旧准入条件、相关原finding与修复依据；其artifact ID、SHA及需读范围由本请求plan冻结。最新prompt可以追加材料，不能减掉这些条件或范围。文本说明和machine条件必须同版供独立审核；机器只校验已声明结构，不声称理解任意散文。

## 5. 请求索引扩展：development_audit/1

复用当前请求`input-index.json`，增加一个`development_audit`命名空间；旧索引其他字段仅作导航，不参与授权。该对象仅包含：

| 字段 | 准确语义 |
|---|---|
| `schema`、`request_id`、`policy_digest` | schema为`development_audit/1`；request ID非空；policy_digest须等于独立pin |
| `subject` | `base_commit`、`subject_commit`、`artifacts`（artifact_id/path/sha256）、`policy_digest`、`condition_digest`、`package_digest`；只含本阶段受审对象，不含意见或自身index |
| `subject_digest` | 对subject对象的上述语义摘要，C重算 |
| `conditions` | 从固定policy承接的完整条件对象；ID、来源和含义逐值相等，request不得删除、改义或以新C2条件覆盖；condition_digest对该有序列表重算 |
| `packages` | 按package_id排序的非空列表，每项含`package_id`、`author_role`、`allowed_paths`、`base_commit`；package_digest对该列表重算。三阶段保持逐值相等，plan绑定由prior_stages承接，不放回包摘要形成自引用；allowed_paths只用于交付审计，不授予运行时写权 |
| `target_package_id` | dispatch为packages中一个ID，plan/accept为null；一次dispatch检查只为具名包给结果 |
| `artifacts` | 非空ID映射；每项为`path`、`sha256`、`kind`（source/policy/condition/raw/invocation/delivery/projection/index）；路径相对index所在请求目录或明确绝对路径，CLI规范化后只读核对，不猜latest |
| `attempts` | 列表，每项为`attempt_id`、`role_id`、`stage`、`subject_digest`、`raw_artifact_id`、`invocation_artifact_id`、`delivery_artifact_id`（非作者为null）；不含passed/full_coverage等预计算结果 |
| `prior_stages` | 条目准确字段为`index_artifact_id`、`subject_digest`、`package_id`。plan为空；dispatch只有一个plan引用（package_id为null）；accept每个package准确一个dispatch引用。C从原字节重算，不信任保存的旧CLI eligible字段 |

同一request仅一个当前候选指针，由原result指向，不用文件名排序选择。`artifacts`用于寻址，不决定必需集合。CLI对重复ID、找不到引用、摘要不符、未知键、JSON重复键以及路径读取失败明确报错。

invocation原件由唯一发包人实际进程观察产生，准确字段为`schema=development-invocation/1`、`attempt_id`、`role_id`、`actor_id`、`adapter`、`requested_model`、`requested_session_id`、`process_exit_code`、`raw_sha256`、`input_subject_digest`、`policy_digest`、`capabilities`。process_exit_code是int非bool或null；capabilities每项记录state和source_ref。source_ref必须可定位准确证据，声明不能覆盖B检测到的反例或unknown。未退出保持null，不当0。人工摘要不可伪装原生事件。

作者final绑定其实际受派`input_subject_digest`与package_id，不要求作者预知根稍后生成的集成commit。`delivery`原件由发包人在作者退出后捕获，包含`schema=development-delivery/1`、`attempt_id`、`package_id`、`input_subject_digest`、`subject_commit`、`files`（path/sha256）及`capture_ref`。C从准确候选读取files并核hash；A检查其属于包写集及本candidate。仅delivery快照不能替作者final；有效final也不能替实际产物审计。原件的可信生产责任归发包人，本checker不声称通过文件内容认证了操作系统进程。

## 6. B观察API与实际Read覆盖

`observe_development(adapter, raw_bytes, invocation, requirements, artifacts)`：adapter为codebuddy或kimi；raw_bytes必须是原生JSONL完整字节；invocation为已核hash对象；requirements准确含`evidence`（本角色本阶段的固定required_evidence列表）及`projection_rules`（固定policy中对应规则列表）。artifacts是C装载的artifact_id→`{path, bytes}`映射，path为与原索引核对后的规范绝对路径，bytes为原件字节；这是内存值，不写回JSON索引。B据此核路径、内容及投影，不读文件。B不接受已算coverage、摘要票、calls-summary代替raw。输入不支持或缺raw必须保留unknown并不满足要求，不能抓取私有会话补历史。

B先严格验证每条非空JSONL（重复键、NaN/Infinity及非对象均拒绝），再复用`adapters._events`解码；现有_events及canonical_digest默认行为不能当严格JSON验证器。C对JSON输入亦先严格验证，A/B入参再核精确类型；通过验证后才可复用既有摘要实现且需确认其序列化与第3节一致。在独立模块观察原生顺序、call ID、结果和返回正文，不调用`adapters.parse`的最终成功结论。当前切片不修完产品parser；同一raw即使旧parser接受，B仍须拒绝陈旧final、尾随失败和未完成工具。

归一化顺序必须满足：

1. CodeBuddy从init观察actual_model/session；Kimi从原生resume_hint观察session，缺模型保留null。多个互相矛盾的init/身份、缺必需身份、requested与actual不符均无有效完成。
2. CodeBuddy配对assistant的tool_use.id与user的tool_result.tool_use_id；Kimi配对assistant.tool_calls.id与tool.tool_call_id。缺ID、重复ID、未知结果、悬挂调用、错误次序均记录原因，不靠工具数量匹配。
3. CodeBuddy完成须有最后一个有效result（subtype=success且is_error严格false）、进程exit0、结果JSON可解析且在全部工具结果之后。失败result、Max turns、final后再发工具/模型内容、重复或冲突final均不通过；不能选择较早成功片段。
4. Kimi完成按明确支持的原生方言要求最后一个不含tool_calls的assistant最终正文、进程exit0、所有先行工具已配对、之后无新assistant/工具活动。允许其后仅出现已观察方言的`role=meta,type=session.resume_hint`，可由该记录取得session_id；重复或冲突身份拒绝，其content中的恢复提示不计新的assistant正文。不能扩大为任意meta白名单。正文必须是本合同最终对象；缺明确最终正文或出现未完成工具时无有效final。无法辨识的方言是unsupported/unknown，不猜测。
5. 工具失败不自动令整个审核失败：审核者可以读取反例；但该次失败Read不能计覆盖。不存在成功Read覆盖时，模型自报“已读”不能补足。

有效最终对象准确字段：`schema=development-final/1`、`role_id`、`stage`、`input_subject_digest`、`policy_digest`、`decision`（pass/changes_requested/blocked）、`condition_ids`、`blocking_ids`、`summary`；作者另含`package_id`、`changed_paths`，非作者不得声明替作者交付。condition_ids必须覆盖自身固定义务，blocking_ids非空时不能有通过效果。decision只是原意见，不是checker授权；结构完整仍须身份、版本、覆盖和前置全部满足。

Read覆盖只来自匹配的原生Read调用及其结果正文。B核其请求路径实际对应哪个已冻结artifact，采用规范绝对路径比较，不用basename、摘要标题或模型给出的artifact_id替代。Read成功至少具备：已匹配调用、无明确错误/截断信号、返回正文与目标准确字节或获准投影相符。CodeBuddy显式is_error为true即失败；未提供成功状态时不能仅凭无error字段断言成功，须采用已识别方言的完整文本相等证据并报告`success_basis=content_match`。无法可靠提取正文则unknown。

支持的返回显示形态仅为原文本、或逐行`行号+tab/箭头+原行文本`；具体方言通过有意义raw fixture锁定，不任意剥离文字。去除的是工具显示包装，不改原件内容；行号须连续、与请求offset/limit（若存在）相符，长行被省略/截断不能算完整。full要求全部源行及每行完整文本均覆盖，lines仅计算指定闭区间；多次成功Read可并集，但不同角色/attempt不能拼成一个席位的覆盖。Grep/Glob/模型转述/Read参数本身不贡献正文覆盖。源无末尾换行与工具的显示尾行区别必须显式处理并记录，不能借此忽略内容差异。

实际native兼容依据为上一批`supervision-product-permission-final.jsonl`原件：第1条为system.version，第24条为assistant正文，第25条为唯一resume_hint身份；Read参数位于function.arguments.path，结果为无is_error字段的`N\t文本`且不保留显示末尾换行。该事实只锁定工具方言，不使旧票符合新的final schema；无需新probe即可构造有意义的最小fixture。归档定位沿原请求输入索引，本合同不复制日志。

只接受旧policy固定的两种投影规则：`json-value-v1`（严格JSON、禁止重复键/非有限数、递归类型敏感值等价，bool/int/float不混同）和`numbered-text-v1`（给原文本添加行号的可逆显示）。先对原件及投影各自hash校验，再由B独立计算等价，不信任projection_index的equal=true。投影只替代同一必需源的可读表示，不替代该席Read；观察者读过而审核者未读仍缺席。任意摘要、字段删减或其它变换本切片不支持。

NativeObservation准确字段：`schema=development-observation/1`、`attempt_id`、`adapter`、`actual_model`、`actual_session_id`、`terminal`（success/failed/unknown）、`final`（已解析对象或null）、`capabilities`、`coverage`、`violations`、`raw_sha256`。coverage每条为condition_id/artifact_id/covered_ranges/missing_ranges/status/success_basis/projection_id；status为complete/incomplete/unknown。violations含稳定code与原生event序号/call_id，定位不用完整敏感原文。观察不生成PASS票、不修改raw。

## 7. A纯判定API、阶段与报告

`evaluate_development(stage, policy, request, observations)`只接收C已加载的声明与B重算观察；stage只允许plan/dispatch/accept。这里request是C在内存组装的准确四字段容器：`index`（本节development_audit对象）、`declarations`（artifact_id→已解析invocation/delivery对象）、`prior_results`（依prior_stages顺序的重算DevelopmentReport列表）、`policy_digest`（实测policy字节摘要）。observations为attempt_id→B输出映射。A仍校验各输入schema和交叉引用，不能因调用者传观察对象就忽略类型、版本或身份冲突。CLI禁止从index直接导入Observation/prior_results，必须递归重算；它们是纯函数调用值，不是新的持久化schema或台账。A不读取raw、文件或环境，也不重写B的原生状态。

| 阶段 | 必需检查与阶段主体 |
|---|---|
| plan | 准确候选计划/接口/写集以及旧policy/原条件全部冻结；两独立设计审核席和独立监督对同一plan subject给有效意见且完成各自必读；集成者即使设计作者也不能占独立席。用于“计划可接收”，不是自动启动作者 |
| dispatch | 重算准确prior plan的全部必需条件，不能只看旧报告eligible；包绑定已审plan、准确基线/写集/作者角色及已审profile能力，无新条件变化；角色/adapter/model配置变化或profile能力unknown则拒绝。此阶段不要求尚未发生的作者session/Observation/final，不把未来sessionunknown算作已失败；只表示具名包可交发包人，CLI不启动模型 |
| accept | 准确候选与每包delivery绑定、所有作者有有效final；两必需内容席和独立监督对同一accept subject完成自己的义务，旧条件完整继承且无blocking；验证证据是各席必读项，CLI不重跑测试也不相信用户填passed。生成只读eligible报告，不执行接收/main/live |

prior_stages从accept指向每包dispatch，从dispatch指向同一plan；有限深度2，循环/缺层/重复包、不同plan或subject不匹配拒绝。C自底向上递归读取原索引和原件，调用B/A重算各阶段，不能复用保存的报告或后来可变内容。plan批准与accept批准引用不同subject是正常的，但不得用plan票满足accept内容席。作者final绑定dispatch输入，delivery再把其产物绑定accept候选，不能要求作者自行预测集成SHA，也不能用任意旧作者final接新产物。A逐项匹配prior_results的stage/subject/policy及eligible，不相信用户提供的passed字段。

每个stage所需角色由policy确定：reviewer至少两个不同actor绑定且不同原生session；author与全部reviewer不同session；supervisor既不是作者也不能计入两个必需reviewer。角色改名/模型切换/重复引用同一raw不产生新票；excluded_session_ids中的旧本轮作者/待复核监督不可占fresh复核席。actual_model未知只按policy明确允许的模型可观测性处理；required capability未知无替代路径。测试成功、监督成功、另一席覆盖不得替代缺失席。

DevelopmentReport准确字段：`schema=development-report/1`、`stage`、`request_id`、`policy_digest`、`subject_digest`、`decision`（eligible/blocked/invalid）、`roles`、`findings`、`limits`。roles逐角色列actual identity、terminal、missing_condition_ids和missing_evidence；findings逐项含code/condition_id/role_id/evidence_refs/reason；按稳定ID排序。limits固定包含“只核所给固定原件，不提供身份认证，不运行模型，不修改状态，不授予合入/live”。不得在输入或输出以overall_passed/full_coverage布尔掩盖细项。

最小稳定失败码：`POLICY_PIN_MISMATCH`、`SCHEMA_INVALID`、`SUBJECT_MISMATCH`、`OLD_CONDITION_MISSING`、`POLICY_CHANGED`、`REQUIRED_ROLE_MISSING`、`INDEPENDENCE_VIOLATION`、`CAPABILITY_UNKNOWN`、`AUTHOR_FINAL_MISSING`、`NATIVE_TERMINAL_FAILED`、`TOOL_SEQUENCE_INVALID`、`REQUIRED_EVIDENCE_MISSING`、`READ_COVERAGE_INCOMPLETE`、`PROJECTION_UNSUPPORTED`、`BLOCKING_OPEN`。同一失败可归多个相关条件，不能因没有匹配枚举而默认为通过。

## 8. CLI与人工操作约束

C使用现有argparse命令树；verify-development分支必须在Store导入/构造、paths.checked样例marker要求和Runner动作前返回。读取指定JSON/JSONL/source/projection并验证hash，不调用Git或其他子进程、不创建fixture、工作树、运行库、报告文件、缓存或第二索引；默认stdout一个UTF-8 JSON报告，stderr仅不敏感诊断。退出码0=eligible、1=blocked、2=invalid/输入读取或schema错误；异常不得变成成功，也不得把unsupported吞成空列表。

仓内对象由唯一发包人按subject_commit提供已冻结的文件快照及交付capture_ref，CLI对实际快照逐字节比对清单；commit到快照的真实采集责任归发包人，CLI不伪称认证了Git。临时raw允许显式路径+hash，缺件阻断而不抓取私有历史。CLI文件加载错误注明artifact_id，不打印凭据或完整env值。索引/source读取前后hash变化立即invalid，不输出部分eligible；不声称跨文件原子快照。调用者可显式重定向报告归档到原请求，checker自身不写。

人工阶段唯一发包人必须在plan接收、每次作者dispatch、最终accept前运行并留准确输入/输出引用；blocked/invalid不得通过新prompt、手改报告或补一个PASS绕开。本切片尚不能阻止操作者绕过CLI直接运行外部工具；因此机器校验接入与人工入口遵守分别举证，不宣称已实现Scheduler强制授权。

本候选的fresh两组设计审核及fresh native监督需先按旧规则实际完成，不能用尚未实现的checker自签设计。新工具通过后可离线回放本批和历史缺口，但回放通过不倒签历史授权，回放失败也不改原票。预算和实际调用仅在本请求计划/result维护；输入变化、合同再审或预算不足转具名等待，不自动扩调用。

## 9. 本轮开发自身的产品验收

本仓开发流程就是本产品的真实需求来源；不是仅交付人工规约、静态报告或synthetic测试。GOV原件见[调查](investigation.md)，当前处理状态仅在本请求finding/result引用，本文不新增状态账簿。

| 现场缺陷 | 必须形成的产品行为及实现包 | 必须拒绝的负例 | 本轮实际消费 |
|---|---|---|---|
| GOV-01：无作者final后以C2例外接收 | A固定旧条件、B核有效终态、C失败非0；无豁免字段 | 真失败raw＋测试绿/内容PASS/native PASS仍缺final | 收集本轮每作者原生终态；修复派发前（若发生）及最终accept实跑，缺项立即停 |
| GOV-02：监督只读选定材料而漏旧门禁 | A每席必需源、B实际Read正文、C从原索引装载 | 删除C1条件或只给C2摘要 | fresh监督的旧源/本轮合同读取由B实际重算，缺读不能以监督结论覆盖 |
| GOV-03：条件变化到依赖动作之后才处理 | A阶段/版本/旧策略pin、C递归重算上游 | 换policy或包写集后继续旧dispatch | 本轮如出现修复，使用准确候选checker检查该派发；accept检查每包dispatch链；未发生派发不补造记录 |
| GOV-04：他席/native补读替缺读席 | B按attempt/角色独立覆盖、A逐席要求 | 只有另一席完整、截断长行、自报full_coverage | 本轮双席与native真实raw分别算覆盖；缺读原席继续blocked |
| GOV-05：状态叙述没有开发门禁支撑 | C单一入口、A细项拒绝、B原生顺序 | 旧final后悬挂工具、缺必需席、unknown能力 | 同一候选执行verify-development真实A/B链，根/发包人在相应检查点消费退出码及findings，结果由原result引用 |

工具未实现前的S0和最初作者派发必须按旧规则逐项人工核对，标明bootstrap，不能伪造机器通过。工具形成后，在本批真实原件上运行；若旧原件缺新的结构化绑定或required覆盖，应如实blocked/unknown，不回填原票，也不能靠读取完整的摘要改成通过。需要补的实际交付/意见仍由原责任席完成且计入既定预算；额度不足则具名待处理。

真实成功路径、本轮真实缺件拒绝、synthetic反例分别报告。只读入口不能自动阻止任意shell/git操作，但唯一发包人与集成者必须在已约定操作点实际消费它；仅运行测试或离线生成一份JSON不关闭本轮使用缺口。旧生产sample parser的尾随工具缺陷、开发runner全程看护及更完整Scheduler强制授权仍为具名未决产品缺陷，在原finding/result保留owner和后续切片，不因三包交付隐藏。

## 10. 最小验收反例与完成边界

1. 缺作者final、只有exit0/文件/测试绿/C2 PASS/native PASS，accept必须blocked；无waiver字段或隐藏默认值可以覆盖。
2. request删除旧condition、改policy或用最新prompt少列必读源，plan/dispatch/accept拒绝；旧策略hash不得由待审index自行替换。
3. 缺必需审核席、同session换角色、作者占review、监督替第二review、excluded旧监督占fresh席，均拒绝。
4. Read失败、只有Grep/Glob、工具计数足够但正文缺行、长行截断、读错同名文件、模型自报全文、用户填full_coverage，均不计完整覆盖。
5. 最早成功final后出现新工具但未完成、尾随失败result、重复/错误ID、结果先于调用、CodeBuddy Max turns或进程仍运行，均不能有效完成。旧sample parser仍可能接受的raw，B必须检出，不能宣称原parser已修复。
6. 一席缺读而另一席/native全读，仍阻断缺读席；获准类型敏感JSON投影可接受，删字段/True与1/1与1.0/未知变换拒绝。
7. plan旧票不能接收新源码；作者final与不同dispatch绑定、delivery越出写集、candidate/hash变化均拒绝。合法“dispatch final→准确delivery→accept双席”正例通过。
8. model未知保留可见；策略允许native模型不可观察不等于其Read/终态能力默认supported。缺所需能力必须blocked。
9. CLI对eligible/blocked/invalid分别返回0/1/2，调用前后仓库及索引原件字节不变，mock Store/Runner/Popen均证明未触达。各包测试由实际作者编写，单一`python -m agent_coop verify`继续供本地/CI消费。
10. 报告只声称准确输入下的检查结果；不得把14/15等调用数量、模型自述、原件存在或一次回放当治理已全面实现。完成记录须分别报告合同获审、代码有效交付、反例覆盖、CLI实际接入和人工执行范围。

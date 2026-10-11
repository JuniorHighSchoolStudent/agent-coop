# 开发动作运行时接入实施计划（后继候选，未准入）

范围：GOV06–09在本请求内实现、反例验证和本项目实际使用；接口合同见[implementation-contract.md](implementation-contract.md)，原始问题见[investigation.md](investigation.md)，当前状态仅见[result.md](result.md)。基线为 `ee94914543e9248d17c9fde670869744173ea22a` 的产品源码。本文件是受审的实施拆分，不改写原S0输入，也不是已经实现或获准调用的证明。

责任：Codex调查、合同、验证与集成；dispatcher_next唯一正式发包；所有产品/测试实现和修复由实际CodeBuddy作者完成，独立两席和native分别审核、监督。每包请求20 turn，作者无有效final即未交付，不以行数通过或其他席PASS代替。包数增加须由根在旧规则下重订调用预算后才能派发。

## 1. 目标与复用裁定

目标是让本仓真实开发动作在创建模型进程之前实际消费准确策略、证据、材料预检与原子预留，并从进程创建到全部受控子进程退出保持看护。不能仅把GOV06–09保留在后续列表而结案。产品完成、真实调用、审核、接收及main合入分别举证。

选定方案：扩展既有adapter、runtime、Runner和同一Store；新增模块仅承接当前缺失的原生观察、材料预检、Windows进程容器和开发动作适配职责。拒绝两种替代：复制TEMP wrapper成为第二套执行器；原样套用sample.initialize/dispatch以获得假样例marker和另一份预算状态。

| 既有入口 | 已有责任与消费者 | 本次处理 |
|---|---|---|
| `agent_coop/adapters.py:144/170/229` | JSONL解码及产品receipt；由runtime.invoke消费 | 共同原生序列观察成为唯一协议解释入口，旧parse和新B共同消费 |
| `agent_coop/runtime.py:45/77/132/182` | 子进程输出、超时、终止；sample与checks消费 | 保留单一收集/看护算法，增加受控Windows进程对象；不复制另一份轮询循环 |
| `agent_coop/runtime.py:27/210` | sample日志根检查、日志落盘 | 开发路径由显式证据根适配；启动前独占预留日志，已有原件不得在运行之后才报覆盖冲突 |
| `agent_coop/runtime.py:221/236/248` | runtime文件摘要、cwd、adapter argv、环境白名单 | 开发调用复用相同验证及环境生成；不提供无校验的任意argv执行入口 |
| `agent_coop/paths.py:42/53/70` | sample marker、重解析点、路径边界 | `checked`原sample语义保留；提取可复用路径边界时不能移除marker或增加全局绕过开关 |
| `agent_coop/store.py:174` | SQLite短事务、revision及同事务events | 派发预留和终结仍在同一Store内原子更新，不建dispatch.db或另一套PASS台账 |
| `agent_coop/runner.py:14/22` | 固定sample整轮锁和顺序步骤 | 保留sample.run；新增同owner开发动作方法，短事务预留后释放，不持整轮锁等待模型 |
| `agent_coop/sample.py:211` | 固定四角色、固定文件和四次预算 | 不直接复用该业务派发函数；抽取与调用通用底层，固定样例合同不扩成通用开发策略 |
| `agent_coop/verification.py:49` | unittest自动发现、规模和文档检查 | 新具名测试自动发现；不新建验证命令或计数台账 |

源码当前规模：runtime318行、adapters289行、Store402行、Runner71行、CLI75行。新源码目标≤300行，>500阻断；函数目标≤40行，>80阻断。Store没有容纳一个完整scheduler的余地：仅增加所需原子原语，纯条件计算在具名模块，状态写入仍归Store。规模例外不能由作者或集成者自签。

## 2. 冻结接口及唯一owner

以下名称作为分包接口建议；与implementation-contract不一致时先由合同owner统一并重新冻结，作者不得各自选一种解释。JSON字段的类型、必填与拒绝规则由合同单一维护，本文件不复制一份完整schema。

### 2.1 共同原生观察

`adapters.observe_native(adapter, raw_bytes) -> NativeTrace` 是公开消费入口。内部实现可由具名 `native_events.py` 承接，两者不能各写一套解析器。Trace至少提供实际model/session、terminal、final_text、配对工具记录、事件序号、原始SHA和violations；配对记录保留call_id、name、input、result、显式错误状态。读取内容不因模型自述而补齐。

旧 `adapters.parse(profile, stdout, session_id)` 从同一Trace生成既有receipt，并保持产品result格式；B `observe_development` 从Trace做artifact路径/正文/范围/投影匹配及治理final检查。共享层不理解治理角色、condition_id或政策PASS。实际退出码由runtime持有，不从JSONL自报补成0；无退出码的Trace只能表达协议终态。

CodeBuddy必须拒绝矛盾init、重复/未知/悬挂工具、错误次序、非success result和final后模型/工具活动。Kimi允许明确的尾随session.resume_hint，保留model unknown；不能复用更早assistant final覆盖后续未完成工具。已配对的失败Read不自动令整个审核失败，但不能计读取覆盖。现有测试里缺ID/配对或subtype的成功fixture需要迁移成真实完整结构，不能留兼容豁免。

### 2.2 材料预检

`assess_development(requirements, artifacts, dialect, budgets) -> ReadinessReport` 为纯函数，owner为 `development_preflight.py`。输入artifacts复用C装载的准确path/bytes；每席独立计算，不把三席材料合成一个已读集合。输出包含明确阻断、未知、每席数据量、最长必读行、估算token、建议区间、块数和轮数下界/假设。

dialect由受审adapter/runtime摘要绑定能力参数；不得由caller任选更宽阈值。按implementation-contract §6.1，`development_dialect.implementation_file`独立定位实际方言文件，R2启动前实测它及原executable/entry/适用agent_file；claim.runtime_digest按合同规定的四项摘要计算。CodeBuddy的Node、CLI entry和headless dist不同，不能互相代替或擅自改启动entry。复用B的源/投影等价接口，预检不另造投影。超过已知单行上限、必读范围无法表示、摘要不符、缺必需原件均在启动前拒绝。请求20 turn仍固定；每响应5–8个Read、模型速度与推理余量不是硬保证，必须明确假设，不能据此宣布必定完成。检查包含为最终结构化交付预留的预算，不能把全部轮数都分给读取。

预检仅判输入可执行性，不是阅读覆盖证明。GOV09材料预算与并发容量是两种事实：前者在纯预检，后者由同一Store原子预留。没有账号查询、探针模型或自动重试。

### 2.3 原子派发预留

`Store.claim_dispatch(expected_revision, claim) -> persisted_claim`、`Store.finish_dispatch(expected_revision, claim_id, outcome)` 沿implementation-contract的写接口。claim固定request/package/role/session、subject/policy/input/profile/runtime摘要、cwd、写集、日志地址、预算和资源键。具体字段由合同冻结，不能存成调用者自报PASS。

同一 `BEGIN IMMEDIATE` 中校验expected_revision、配置/政策绑定、attempt唯一性、预算余额、资源冲突及实际并发上限，再记录reserved与递增revision/events。总默认容量4、账号组共享限额、单writer工作树及session互斥都必须可见；不能因为模型不同重复计算账号额度。失败不退成未调用，不自动创建替代attempt。预算在预留时保守占用；创建失败可分类为未启动，但不得隐式释放为可重试次数。

`Store.mark_dispatch_started(expected_revision, claim_id, process_identity)`沿合同§6.3在contained+suspended创建后、resume前原子记录身份，将该预留转为used。并发revision冲突只对原挂起进程重核/CAS，不能再创建进程。身份记录失败须终止未恢复的树；记录成功而resume失败保留used及resume_failed，模型/provider是否实际活动另行举证，不把used当计费。

初始化、批注册和bootstrap导入均沿合同§6.4：S提供同一Store的专属事务，D唯一装载批准配置并调用，禁止裸update绕过。Store初始化只接纳启用检查点已审核的剩余额度，authority_ref覆盖S0、失败、修复和在途占用，不将calls_used=0解释为此前未用。前批固定bootstrap原件通过D重算、S建立source→accepted事件映射；不回填旧依赖hash、不导入缺作者final的例外、不另建DB清空预算。

实际并发记录仍归当前请求同一个Store，正文/原始流保留外部不可覆盖证据引用。预留后未启动、启动后未终结、控制者崩溃均保留可对账状态；重启不能盲重派。终结只能匹配原claim，失败、unknown和成功分开。开发动作不滥用sample的current_step让第一个完成的包宣告全部完成。

### 2.4 Runner与开发action

Runner增加 `dispatch_development(action_input)`，调用受审开发适配模块装载并重算A/B报告和材料预检，拒绝caller传入已算Observation/PASS，取得Store原子claim后才调用runtime。执行顺序固定为：原件装载和前置核验→预检→原子预留→启动前再次核验实际使用bytes/权限/入口→日志独占预留→contained+suspended创建→看护就绪及Store记录启动身份→resume→原始流/终态留证→原claim终结。`runtime.invoke_development(profile, prompt, cwd, evidence_root, attempt_id, session_id, on_created=...)`通过动作owner的生命周期回调完成上述Store记录，不接受任意调用者代码替代门禁。

开发适配模块建议为 `development.py`，只负责该动作的组合，复用C的 `development_audit` 装载/校验入口，不复制文件加载器；不含等待队列、调度循环、另一套SQL或模型选择。CLI只解析参数并调用Runner；不能让CLI本地先返回PASS再调用另一条不核验的启动函数。profile的精确写文件、环境白名单和四memory覆盖复用现adapter/runtime，不硬编码agent品牌作为核心权限规则。

D的公开初始化、批注册、bootstrap导入和prompt渲染API直接沿合同§6.4，字段不在本计划复制。prompt只由已审body及固定context规则生成并核完整字节；D唯一维护，不让C或临时wrapper另拼提示词。D同时核批绑定的profile/cwd/账户组，并从准确写集派生强制排他资源交Store核验；账户组容量不能被实现成全组互斥锁。

每次CLI动作只启动它被授权的一个attempt。四个独立工作包可由四个调用并发进入相同Store，事务只保护claim/终结，不跨模型运行持锁。相同写树/session或共享容量不足者拒绝并解释等待原因；不另建后台dispatcher。sample原 `run` 的锁和顺序语义不改。

产品接收动作 `Runner.accept_development(action_input)` 同样内部装载并重算当前accept，再按expected_revision在同一Store记录准确接收范围；不启动模型、不执行Git、不把旧PASS报告当现许可。接收投影发布失败沿既有events/outbox恢复，不重做已提交的接收或派发。

## 3. Windows进程生命周期方案

本切片选择Windows10+/Server2016+的明确实现，POSIX原路径保持既有合同；未验证平台显示unsupported，不能静默退回较弱看护。新增 `win_process.py` 只提供Windows进程容器，不理解policy、Store或角色。

公开建议 `spawn_contained(argv, cwd, env) -> ContainedProcess`：暴露供runtime复用的stdout/stderr、pid、poll/wait，以及resume、terminate_tree、tree_empty、close。对象持有process/thread/匿名Job句柄；创建时间随原生进程句柄记录，PID仅用于审计，不靠重新按PID搜索对象再杀。

1. 先创建不可继承的匿名Job，配置KILL_ON_JOB_CLOSE，不允许breakaway；准备准确白名单env、显式executable/cwd和标准流句柄白名单。
2. 使用CreateProcessW和STARTUPINFOEX的JOB_LIST，在创建时关联Job；同时CREATE_SUSPENDED、CREATE_NO_WINDOW、CREATE_UNICODE_ENVIRONMENT。启动失败立即保留原因并释放所有已取得句柄，不能改走裸Popen。
3. 持有进程和初始线程句柄，完成输出读取器与单调deadline准备，经on_created确认Store启动身份持久化后ResumeThread；准备或记录失败则终止Job并等待退出，不让目标CLI运行。恢复失败也终止Job，按已记录启动事实保留used和准确失败原因。
4. 监督以整个Job是否仍有活动进程为边界。父进程exit0但子进程仍在运行、管道尚未结束，不算成功；同一deadline内等待，超时/超输出/读取失败终止Job并有界等待empty。
5. 控制者正常关闭或异常退出时，最后一个Job句柄关闭触发整体终止；Job句柄不能被子进程继承。保留执行失败、终止失败和管道未收束的不同结果；unknown不得作成功。

日志目录和stdout/stderr以独占方式在创建目标进程前打开，收集过程中按总字节上限增量保留已接收流；正常失败保留原始片段和分类。控制者骤停可能留下不完整流，必须标明partial/unknown并结合Store未终结claim对账，不能把部分日志称为完整模型终态，也不能用新调用覆盖它。

方案依据与限制：微软说明Job默认涵盖CreateProcess创建的子进程，关闭最后句柄可终止Job及嵌套Job；但其他进程代理/WMI创建的进程不因此自动纳入。此方案是对受控CLI及其正常子进程树的生命周期管理，不是恶意逃逸或OS权限沙箱。[Job Objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects)

JOB_LIST在CreateProcess期间指定Job，要求Windows10+/Server2016+；本方案不用“先运行再Assign”冒称无空档。若平台或嵌套Job限制导致创建/关联失败，启动被拒绝，不添加breakaway绕过。[UpdateProcThreadAttribute](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-updateprocthreadattribute)

CreateProcessW必须使用可写命令行缓冲、正确STARTUPINFOEX/标准流及显式Unicode环境；process/thread句柄由调用者关闭。创建挂起线程在ResumeThread之前不执行应用入口。[CreateProcessW](https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-createprocessw)、[Suspending Thread Execution](https://learn.microsoft.com/en-us/windows/win32/procthread/suspending-thread-execution)

Python公开Popen STARTUPINFO属性只明确支持handle_list，不承诺暴露初始thread句柄或JOB_LIST。实现选择窄ctypes Win32绑定，不读取Popen私有属性拼装权限保证；argv引用/反斜杠、空值、中文和env往返必须有真实子进程测试。不得让可继承句柄跨并发创建泄漏。[Python subprocess](https://docs.python.org/3/library/subprocess.html#subprocess.STARTUPINFO)

## 4. 小包、写集和依赖

下列为实施候选。每包独立作者、精确写集和有效final；独立包最多4路，不为凑4路启动有真实依赖的包。所有新增文件均有具名职责，不是版本副本或通用utils。

| 包 | 精确候选写集 | 交付与验收 | 前置 |
|---|---|---|---|
| N1 原生序列内核 | 新`agent_coop/native_events.py`、新`tests/test_native_events.py` | 唯一NativeTrace、两种方言配对/终态负例；无治理角色语义 | 观察API冻结 |
| N2 既有parser接入 | `agent_coop/adapters.py`、`tests/test_runtime.py` | observe_native公开入口、旧parse消费N1、迁移缺ID旧fixture；不复制N1 | N1 |
| F 材料预检 | 新`agent_coop/development_preflight.py`、新`tests/test_development_preflight.py` | 每席必读能力/预算拒绝、准确估计与unknown、复用投影入口 | B投影接口及方言字段冻结；真实组合须B可用 |
| W Windows进程容器 | 新`agent_coop/win_process.py`、新`tests/test_win_process.py` | 创建时Job关联、挂起/恢复、句柄生命周期、父退出/控制者退出子树清除 | Windows接口与测试边界冻结 |
| R1 路径与原件预留 | `agent_coop/paths.py`、`tests/test_paths.py` | 在保留sample checked语义下支持显式开发证据根；拒重解析/越界，唯一目录预留 | 开发cwd/evidence_root合同冻结 |
| R2 runtime接入 | `agent_coop/runtime.py`、新`tests/test_runtime_development.py` | 同收集算法消费ContainedProcess；方言implementation_file实测、on_created成功后resume；开发invoke与样例路径分开、失败留流与终态 | W、R1、N2；启动回调接口冻结 |
| S 原子claim | `agent_coop/store.py`、新`agent_coop/dispatch_claims.py`、新`tests/test_dispatch_claims.py` | Store唯一写入；开发初始化/批注册/bootstrap映射、claim/mark_started/finish/accept；dispatch_claims为事务内纯校验/转换，不读写DB | 合同§6.3–6.4冻结 |
| D 开发输入组合 | 新`agent_coop/development.py`、新`tests/test_development.py` | 消费C的真实A/B装载共享入口；唯一初始化/批注册/bootstrap导入装载及prompt渲染；preflight和启动输入复核，不接caller PASS | A、B、C、F及S冻结API；实组合须S可用 |
| X Runner动作 | `agent_coop/runner.py`、新`tests/test_development_actions.py` | claim后runtime、终结原claim，四独立调用并行，拒绝先spawn后核验；accept内部重算并条件提交 | D、S、R2 |
| C2 动作CLI接线 | `agent_coop/cli.py`、`tests/test_cli.py` | 唯一CLI写入包；同一CLI动作调用X，失败非零/证据可定位，不能绕过门禁 | X；C仅维护development_audit装载/组合及专属测试 |

N1/A/R1/W是首批可独立就绪的4路候选，A为既有纯政策判定包；F及S按发包计划的后续批准批次进入，不能仅因有空槽提前跨批启动，也不能用未验B的替身输出作集成成功。N2和R2是依赖小包，不让单作者在20 turn里同时完成新Win32、旧parser迁移和动作编排。S有三个文件是因为Store402行，事务纯规则需要明确承接模块；不能让该模块自行建连接或保存第二份状态。

N2拥有旧测试fixture迁移，其他包不得复制其测试类。新测试文件只覆盖新职责，复用现有fixture工厂时只导入工厂/常量，不能导入TestCase导致重复发现。新旧统一verify必须检查测试ID唯一，原201项的迁移/新增/替代逐项说明，不能以数量相等掩盖删测。

每包统一交付步骤：先提交对应最小反例和实际实现，由根运行该包的 `python -B -m unittest tests.<对应模块> -v`；失败交回原作者，不由根补源码。合体停止全部writer后只运行同一个 `python -B -m agent_coop verify`，修复影响再针对性复验。作者声明文件/函数软目标、职责和消费者；超硬上限或无final即阻断依赖包，不延长20 turn或隐式补调用。

## 5. 必需负例和实际使用

| 范围 | 必须拒绝/保持失败的反例 | 有效正例与真实证据 |
|---|---|---|
| GOV07 | early final后悬挂工具、重复ID、未知result、冲突session/model、错误subtype、final后再次模型/工具输出 | 合法尾随Kimi resume_hint、配对的失败工具后正常final；产品parse与B对共同序列结果一致 |
| GOV09 | 3559字符必读行、21526估算token单块、缺范围/旧SHA、未知CLI方言、零final预留、伪造成功估计 | 现真实S0材料按每席重算，不发模型探针；预检输出与事后raw覆盖分别存证 |
| GOV06 | 已有日志目录、junction逃逸、Job创建/句柄设置/恢复失败、父退出子仍活、超时、总stdout+stderr超限、控制者崩溃、读取线程失败 | 真实临时Python父子进程，用句柄/等待和独立ready信号证明创建/终止；只看异常字符串不够 |
| GOV08 | stale revision、政策/输入改变、同attempt重放、伪造PASS/Observation、容量/账号预算满、同写树/session冲突、claim后崩溃 | 同一Store四独立资源claim可并存，第五个拒绝；四个真实受控测试进程可同时运行，预算不超发，终结只更新自己claim |
| 失败恢复 | 崩溃后无terminal却自动重派、旧PID被复用后盲杀、失败日志被下次覆盖、错误receipt当成功 | 无自动重试；残留reserved/running明确待对账，原进程身份不可确认则unknown，旧证据不可覆盖 |

Job/句柄继承/父退出/控制者退出/timeout/输出上限/真实env及argv必须用真实本地子进程验收；mock只能注入特定API失败，不能证明生命周期。Windows宿主不支持时保留阻断，该包不能用skip宣称已治好。身份/版本/解析/预检主体可用准确微型fixture，不需要模型调用。

实际本项目使用须在新受控入口就绪并获对应准入后发生：由dispatcher_next通过产品开发action发起本请求已批准的C2必要作者调用，保留策略/输入/预检/claim、准确argv和环境键来源、runtime摘要、原始stdout/stderr、真实终态及独立Read覆盖。依赖未完成的前批作者不能倒填成“已由新入口派发”。不得额外调用canary或用旧wrapper成功代替新入口实用证据。

保留必要消费者C2为真实使用包：X及其依赖先完成对应内容审核与监督准入，dispatcher_next通过已受审的Python公共Runner动作API派发C2作者，C2把该API接入最终CLI。该操作使用已批准的准确API调用与输入，不增建传输wrapper或调度脚本。如此不要求尚未实现的CLI启动自身作者，也不人为增加canary。该依赖安排未获批准时保持阻断；正式审核调用不能替代实际作者写集和有效交付闭环。

真实C2作者动作及有效交付证明入口被消费；四路并发能力另用四个真实受控Python进程证明，不为凑并发模型证据强开无任务调用。若验收策略要求真实四作者并行，应由根在实际四个独立就绪包和预算内安排，不能用测试进程替代该更强声明。

本轮尚未发生的修复派发不能伪造发生，但GOV06–09的代码、反例及适用实际使用必须齐备后才可关闭。报告通过不自动赋予merge、push、live或生产任务权限；本批不实现生产OS任务、全局memory、账号代理、跨项目容量服务或完整Scheduler。

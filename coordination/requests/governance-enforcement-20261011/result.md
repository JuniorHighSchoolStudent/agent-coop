# 开发治理修复当前状态

范围：本仓开发失效的产品修复；维护者：Codex集成者；状态：**S5两席实际初始化并结束，但必读材料在cwd外导致权限拒绝，0/142必需读取完成；撤回S5后续启动效力，准备仅修正材料位置的S6**。来源：[用户请求](request.md)及[全部问题产品落地要求](scope-amendment.md)。截至本检查点，确认6次CodeBuddy模型调用、0次native；另有S2两次launcher失败、S3及S4各两次目标Node已启动后看护中止，均未观察到原生模型初始化，后端活动/计费未知。S5已知owner/watcher/wrapper/CLI退出，tree_empty仍unknown。用户已取消固定审核轮数，后继调用须按修正原因、准确候选及原独立门禁推进。

## 当前结论与下一动作

GOV-01–09及GOV-S0-I01均须经过产品实现、失败/恢复回归、本仓真实使用和独立关闭。当前只完成调查、实施候选和两轮实际设计审核；没有产品修复完成，不以文档、临时看护或尾部PASS代替交付。

- main保持`9a4855a39121f2483e1630082bc36533a2165a5e`。治理工作在`codex/governance-enforcement-20261011`；原用户工作树、`.workbuddy`及旧证据保留，本轮未合入main或push。
- 原冻结S1候选`dc37ae62a0aa8b40e0d881a364a6ddd190c0e146`和S2候选`f1b5f967238290fbe3a1945da5e8cea20f634096`保留在独立送审树与Git历史；轮次与四项必修要求已于`9092a8b`提交。当前核准[实施合同](implementation-contract.md)、[运行时计划](runtime-integration-plan.md)、[分批派发计划](dispatch-sequence.md)：13包、4个完整接收批次，首批N1/A/R1/W四路，N2等待N1有效交付。五个首批作者树只完成隔离准备，没有作者运行。
- Codex负责调查、合同、证据、验证和集成；dispatcher_next唯一正式发包；实际CodeBuddy + deepseek-v4-pro实现/修复，CodeBuddy + GLM/Kimi独立交叉审核，native Kimi独立监督。默认执行容量4可配；Claude暂停。
- S4已真实启动但失败，现转入既有Job组件复用调查，后续依新准确准入；不得使用已撤回的[S3准入](s3-admission.md)原样重跑。候选ec64819及唯一governance-s3输入作为历史保留，容量与读取计划核验仍只证明准备事实。[S1最小修订提案](s1-correction-proposal.md)中的读取计划派生、会话声明、严格final及看护身份回归仍须完成。用户最新指示已取消固定轮次，原追加2票问题不再待答复；[范围补充](scope-amendment.md)保留原话，[当前路线](../../../docs/roadmap.md)维护有效团队约束。旧52/54总次数不是新的隐藏上限；实际消耗保留，单次运行与资源约束继续执行。下一轮四项必达为漏读、无效审核输出、看护漏管及策略自读缺口；需要有效双席意见和native监督后才派作者。

最新派发检查点：候选`ed527d872b6fc130583d99b223cc0db3f60ef888`及既有Job载体已实际运行S5双席，但`D:/project/ac5-input`在只读cwd `D:/project/ac-s5`外，实际材料被拒。[S5准入](s5-admission.md)保留原件，后续启动效力撤回；同一候选下一步仅把完整材料物化到新短cwd子目录并重绑版本/容量，不放宽权限、不新增看护逻辑、不增加审核主题。native和作者尚未准入。产品W/R2仍未实现，当前实际并行实现者0，四个结构就绪包被审核/监督上游阻断，不能以三名Codex协调人员冒充开发并行。

### 用户纠正：临时修补越权与协调空转

来源：2026-10-11当前用户指出“看护的连续修补也是应该派发给执行者”“这也是开发的问题需要在产品中解决”。集成者确认临时看护被连续归为行政准备，实际上包含实现修改；后续立即停止这种例外，既有源码保留真实作者归属，不追认为CodeBuddy交付。执行已有命令、核验和状态维护继续由协调角色负责，新增或修补执行逻辑必须回到具名CodeBuddy工作包。

本次偏差沿既有finding承接，不另建台账，也不修改已经冻结的S5输入：GOV-06/W/R2承接看护故障与执行者修复；GOV-08/D/X承接角色、写集、工作包和修复派发绑定，行政/临时标签不能绕过作者权限；GOV-S0-I01及GOV-09承接监督漏管和准备活动膨胀。必须分别显示实际运行的实现、评审、监督和协调数量，记录ready包未派发的具体依赖/责任人；有协调活动不等于功能进展。新增产品判据须进入后继受控合同及独立审核，当前只是开放需求，不能声称S5已覆盖或产品已修复。

只读审计定位到具体合同缺口：角色段仅限制“产品/测试”，而行政恢复段允许协调者准备watcher差异。后继修订按是否改变可执行行为划界，TEMP位置或“准备”标签不构成豁免；GOV-01/03由A/C/D/X承接受管动作的作者、原件和写集核验，GOV-05/08由S/X/C2区分结构就绪、获准、reserved、进程创建、原生init与终态。监督必须给出可执行修复提案的owner、写集、前置和验收，不以再加一轮审核代替处置。产品只约束它管理的动作，不宣称禁止宿主任意shell修改。

## S5实际读取权限失败

2026-10-11两席Job ready约07:10:01Z，watcher ready约07:10:03Z，原生init观察到准确GLM `glm-5.3`/session尾`31a0e86d`与Kimi `kimi-k3-2`/`c7b249f3`。两owner分别281.1309632秒、97.451409秒正常退出，已知对象退出与Job关闭原件保留，不宣称tree_empty。原始流位于`C:/Users/june/AppData/Local/Temp/agent-coop-governance-s5-run-20261011/`各席目录；GLM raw SHA `550cf494e043b312a66527b9955986c809c42c72cfedb7cd6bd87dd69089b378`，Kimi raw SHA `abee5de7e0885f78798cf6aa8522c4d4cd77bb3c6fa6e6a4946398316e06018e`。

GLM实际14Read、Kimi12Read并不等于必读成功：S5表内材料均因非交互权限审批不可用被拒，两个142项计划均0完成。GLM另作cwd内Read/Glob对照，不能把它的全部工具结果统称失败。GLM完整final可解析为JSON且自报blocked，缺读与condition清单未核使其不能批准；Kimi完整final带代码围栏，严格JSON失败，不截尾救票。root遗漏材料路径与有效读取root的联合核验，产品GOV-09/F及R1/R2须承接启动前拒绝与位置修复正例，现有argv容量检查不能替代权限可读性。

## S4实际结果与停止点

watcher于2026-10-11T06:40:49.6859408Z ready，PID40980；两wrapper随后启动，GLM目标node23688、Kimi40684均已绑定。两份实际invocation加exe共20参数，发包人逐值核与planned相等。两席分别在8.9061958/9.9490421秒停止，wrapper exit -1；raw/stdout及stderr均0字节，无init、实际model/session、final或Read。没有有效票，不能把目标进程启动计为已确认模型调用。

两席末事件为`fresh CIM candidate identity / microsecond projection`，候选分别是bash.exe PID32504/parent45824与PID11988/parent4600；保存了snapshot creation、API及InvalidOperationException。但该复合判据未保存fresh count/identity与held ticks，无法区分复查缺席、字段变化或创建时间不一致；短寿进程只是待验证解释，不能据此回填根因。此缺口继续归GOV-06，不以已取得API名称宣称诊断充分。cleanup记录14个已知对象exited/disposed且errors为空；发包人另查这14个PID及watcher均不存在，仍不证明未观察后代清空。

准确本机原件位于`C:/Users/june/AppData/Local/Temp/agent-coop-governance-s4-run-20261011/`：GLM/Kimi watch-completion SHA-256分别`9f37cf4cf8298906ec23ca9b3118ef9cd1f90ca84f432c0bf6241f5d69fa1d61`、`5de35ae2a759bce92c0cdcc4dd31c175082243844bbbddebf1d0ff4ad158d51b`；cleanup为`e209ff14a26cb73ae9f00c95f9e8ce2d7c040b7ca03714afc3cff8c26c19d3b4`。保留冻结输入、失败准备和实际运行原件；本机TEMP不是长期备份。后继调用须有针对本次失败的恢复证据与新准入，不能沿S4原许可续跑。

后续成熟组件调查：现成`windows-job.native-test.cjs`在本机实际10/10通过、exit0，覆盖正常/强制退出、父先退、嵌套Job、Worker、IPC、PTY及Git Bash前后台子孙；没有模型调用或包/产品改动。原件目录`C:/Users/june/AppData/Local/Temp/agent-coop-governance-native-job-20261011/`，测试stdout SHA-256 `ceb88836fa10bed1cf92bfc3175bc10fbab108e6312da527846ff5e0a510c5d9`。直接binding建立Job返回true且self membership为true；独立兄弟Job的动态查询返回false，支持该固定组件的限定成员语义，但native源码未随包提供，不能宣称源码级验证。`no-orphans.install()`会降级warn/false，不作为严格准入入口。候选行政恢复采用每席独立owner直接严格核binding后承载watcher，具体方案与新准入仍待完成；产品W不依赖宿主私有组件，不把这些测试当GOV-06产品关闭。

## 宿主自动继续入口

2026-10-11用户要求建立自动化任务派发修复。已通过Codex宿主工具创建并回读自动化`agent-coop`（名称“Agent Coop 派包与修复闭环”），创建时状态ACTIVE、每15分钟唤醒同一任务。准确配置及暂停状态以宿主自动化为权威，本处仅保留建立事实，不复制维护另一份prompt或调度状态。

该入口先对账在途工作并按当前result的有效下一动作推进，准入有效后沿现有唯一发包、CodeBuddy实现、双席交叉审核及native监督流程继续。2026-10-11已通过宿主工具移除提示中固定S3的旧优先项并回读验证，15分钟周期、ACTIVE及原目标任务保持；不将该配置更新当实际触发成功。它不恢复已撤回准入，也不代表产品Scheduler或看护修复已实现；当前产品阻断仍按本结果前文维护。目标独立关闭后暂停；确需用户或外部条件才能恢复时明确原因并暂停；无变化不重复通知。本次仅验证宿主配置创建与回读，尚无首次定时触发成功或自动修复完成证据。

## S3实际启动与看护中止

S3 watcher于2026-10-11T05:42:42.6897501Z ready，早于两wrapper。根独立核实际invocation的20个argv元素（含exe）与计划逐字符一致；GLM目标node PID47088、Kimi PID49468实际创建并持有句柄，说明本次完整参数容量已越过启动边界，不能据此推断CLI初始化、模型调用或审核完成。

watcher分别于6.2743377/5.6561078秒输出`descendant disappeared before identity could be bound`并停止两席。该文字由`run-admitted-s3.ps1:56`的ArgumentException捕获产生；现场未保存失败候选PID、名称、父PID、创建身份、原异常或发生API，无法判定具体哪一步、哪一个候选失败。正常短寿辅助进程退出只是可能解释，不能作为已证根因；已有目标node失联也不是原件所证明的事实。此诊断缺口沿GOV-06/W/R2承接，不能通过忽略异常、按PID猜身份或放宽判据关闭。

两席原生stdout及stderr均0字节、无init、无实际模型/session、无final、0/90 Read；没有有效票。原记录列出15个已绑定对象，发包人另查其PID已不存在；后续发现原句柄有效性表达式存在假阳性，因此不能仅按原记录宣称全部对象持续持有有效句柄。未绑定/扫描间脱链后代仍unknown。native、作者和后继模型调用均未启动，S3原准入的后续启动效力由本结果撤回，不改写原件。

本机原件位于`C:/Users/june/AppData/Local/Temp/agent-coop-governance-s3-run-20261011/`。根核`watch-completion-glm.json` SHA-256 `f7dd7c4a774cb0f2704c2228e87adbf1aa340fefac4b90e7fdc1e04de11da5d9`、`watch-completion-kimi.json` SHA-256 `5824fcc1a3a98784ac8ed85769aa1370a1eeb43c3f3e729ae7bd0b383de2a80b`及实际参数。各调用原件保留，不生成审核receipt，不把本机TEMP当长期备份。

行政限制另记：写入S2无模型诊断汇总`diagnosis.json`曾被自动审批拒绝，工具只返回`blocked by policy`、未给细因；该文件未生成且没有重试或换路径生成替代品。既有诊断原件直接进入S3准确输入，不能引用不存在的汇总。

### S3后续无模型调查与恢复边界

2026-10-11三方继续调查确认两个缺陷：原宽catch把整段操作中的ArgumentException均归为后代消失；PowerShell 7.6.5的`.SafeHandle`属性读取失败可返回null，而`-not $null.IsClosed`实测为true。显式`get_SafeHandle()`暴露真实异常。自有短寿node自然退出的正反例证明上述行为，没有模型调用或产品改动；它们不能还原S3缺失的候选身份与实际失败API。

准确原件位于同一S3运行目录：`watch-argumentexception-api-repro.json`及`watch-property-getter-repro.json`，后者SHA-256为`86995a8ec3110cc9a96b8837a627c41f01d8a2408d84f9197a8f816119b15920`。GOV-06/W/R2承接显式getter、非null/invalid/closed句柄检查及分API异常保真，仍须产品回归和独立关闭。

恢复沿旧bootstrap的受限人工看护入口：唯一发包人准备同强度行政修正，独立无模型核验后，集成者按新候选、读取材料、完整参数和看护版本另立只读准入。仅准确证明未绑定候选的GetProcessById not-found，且目标早已准确绑定、原身份及有效句柄持续保持，才可记录候选unknown并继续；首次目标未绑定、权限错误、未知异常、身份冲突或已绑定身份丢失仍停止。旧S3不追认，产品atomic Job验收不豁免；有效双席和native监督仍先于作者。

另发现CodeBuddy安装中已有Windows Job绑定与现成原生测试，是W的复用调查输入；本次未动态验证，也未确认S3实际安装成功，不能作为已包含证据。当前本地片段及分支检查属于行政恢复准备，不是产品W实现、正式审核票或新调用准入。

## S2启动失败与准入撤回

[S2准入原件](s2-admission.md)绑定候选`f1b5f967238290fbe3a1945da5e8cea20f634096`；该原件记录历史授权，本段撤回其后续启动效力，不改写失败前原件。2026-10-11T05:21:18Z双席wrapper启动后分别于0.8886/0.8706秒exit1，仅观察到conhost后代，没有node、原生init或终态，两份CLI输出均为0字节；因此没有有效审核票，也不启动native监督或作者。

实际报错为`StandardOutputEncoding is only supported when standard output is redirected`，位置为既有`run-review.ps1:119`。另独立确认完整prompt分别34681/34682个UTF-16代码单元，仅argv元素与分隔符下界已达35005/35009，超过Windows命令行容量；尚未包含可执行文件、引号转义和NUL。不能将该独立容量阻断直接宣称为实际报错的已证根因。根此前核对了来源与读取表，但漏做操作系统传输容量检查，原准入不代表完整预检已通过。

失败摘要与传输静态证据原件留在本机`C:/Users/june/AppData/Local/Temp/agent-coop-governance-s2-run-20261011/`：`s2-launch-failure-summary.json` SHA-256 `c0612e3464e9762b265f96d5fda41891c7be58f4324f45250218b714f0063b02`，`s2-transport-static-evidence.json` SHA-256 `5edcdd3a2b6738e41d1699744f4bb2e702dd2069dd9e3be4c68854d0787ccc1e`。保留冻结S2输入与原始调用记录；TEMP不是长期备份。

无模型诊断已复现异常遮蔽：PowerShell 7.6.5/.NET 10.0.11下，父进程重定向开/关均为短参数成功、34681字符长参数失败；直接.NET启动显示Win32Exception 206。另一次同形PowerShell调用的FirstChance原件记录先206、再StandardOutputEncoding异常，根已读取核对。该记录是后续诊断，不是S2现场曾捕获内层206；现场错误与独立容量证据均保留。诊断原件位于本机`C:/Users/june/AppData/Local/Temp/agent-coop-governance-s2-startup-diagnosis-20261011/firstchance-long.json`。无需复制PowerShell启动器到产品；完整参数容量预检及原始启动异常分层由现有运行时路径承接。

运行时调查员和根分别验证：仅去缩进仍超限；保真columnar表保留80行全部7字段，反解与原计划一致，context/body原字节不变；根以subprocess.list2cmdline重算含exe/转义/NUL长度25279/25283。只是旧S2输入表示可行性的无模型证明，不是新候选准入。合同审计员已将表示、最终容量核验及回归写入既有合同。S2容量拒绝归GOV-09/F/D/R2，conhost存在不能证明目标CLI启动归GOV-06/W/R2。只在后继候选与完整输入重新核验后继续；不截断材料、不静默切stdin，也不以固定轮数终止目标。

## S1实际证据与拒绝原因

[调用索引](review-s1-calls-summary.json)和[真实回归输入](review-s1-regressions.json)保留准确摘要及本机原件定位。两席实际身份与[S1准入](s1-admission.md)一致：GLM `glm-5.3` / `agent-coop-governance-glm-s1-20261011-6b339fd5`；Kimi `kimi-k3-2` / `agent-coop-governance-kimi-s1-20261011-78780920`。

| 事实 | GLM | Kimi | 准入含义 |
|---|---|---|---|
| 进程退出及原生终态 | exit0 / success，330.535秒 | exit0 / success，480.422秒 | 仅协议成功 |
| 原生result事件序号 | 151 | 144 | 原件定位，不是模型轮数 |
| 完整final正文严格JSON | 失败，散文前缀 | 失败，散文前缀 | 两席均没有有效治理final |
| Read及返回结果 | 64 / 64 | 64 / 64 | 工具数量不能证明内容覆盖 |
| 必需内容缺读 | s1-admission第17–18行 | s1-admission第17–18行 | 第18行有实质预算说明；两席均不完整 |

[GLM原票](review-s1-glm.txt)、[Kimi原票](review-s1-kimi.txt)按完整正文留存；尾部JSON意见均写pass，但不得截取为有效票。逐席[GLM覆盖](review-s1-glm.reading-coverage.json)/[Kimi覆盖](review-s1-kimi.reading-coverage.json)及实际身份、development invocation同目录保留；原生私有执行流留在本机TEMP，没有提交完整jsonl。TEMP留存不是长期备份，不执行清理。

实际源及冻结required-reads要求1–18，派发prompt表仍是1–16。根此前核过52份artifact、16条conditions、5份runtime原件及prompt摘要，却漏了读取计划与prompt内容的一致性；发包人与集成者共同承担准备缺口，不能归咎于模型或减少原要求消除失败。模型自报全部读取不成立。

watcher虽在04:23:02.4412225Z先于wrapper ready，但GetProcess.StartTime的100ns字符串与CIM.CreationDate的微秒字符串全等比较失败，两席first_child均为空。wrapper看护保持活动，完整后代树没有持续覆盖。Kimi剩余时间另有具名身份看护，未延时或重试；不能回填此前缺口，也不能证明历史整树无孤儿。此证据纳入GOV-06，由W/R2产品实现和真实子进程回归承接。

每席实际计划64Read、527201显示UTF-8字节、估算108732内容token。早期40–50Read估计已失效；估算与600秒不是完成保证。原生num_turns149/142为history长度，不是max-turns20的模型响应计数。容量预检及派生同步归F/C/D，最终实际覆盖归B，职责不得互相替代。

## 产品关闭责任

完整接口和验收以当前修订候选及其正式准入为准，下表只维护当前责任导航。所有项均未关闭。

| finding | 产品承接与关闭所需证据 |
|---|---|
| GOV-01–05 | A/B/C及动作消费者核原条件、有效作者final、独立监督原票、逐席真实读取和状态准确性；现场失败回放、恢复正例、实际动作拒绝及独立关闭 |
| GOV-06 | W/R2持有原进程身份及包含边界，覆盖父先退、控制者退出、超时、输出上限、PID复用及本次时间精度漏管；真实无模型子进程与真实作者使用分别验证 |
| GOV-07 | N1唯一原生序列解析、N2迁移旧消费者；早期final之后仍有未完成工具的真实反例在旧入口也必须拒绝 |
| GOV-08 | S/D/X复用同一Store/Runner，派发和接收内部重算权限、准确输入、预算、资源、暂停和状态；B4必要CLI作者由已接收产品API真实派发 |
| GOV-09 | F/C/D固定源到读取计划及prompt的确定性派生；本次源18/计划18/prompt16必须在启动前拒绝，不能只核独立文件hash |
| GOV-S0-I01 | 当前必需审核席的原票和覆盖进入独立监督证据包；监督实际读取，各席不能替补缺读；B/C/A与native真实复核承接 |

修复也由专门发包人派给CodeBuddy作者，再经独立双审和native监督，集成者不得直接改产品或测试。新的现场缺陷继续追加到原finding的证据与验收，不另建状态台账，不以换会话/归档清除阻断。

## 历史原件与验证边界

原[合同](contract.md)、[计划](plan.md)、[调查](investigation.md)冻结于`ee94914543e9248d17c9fde670869744173ea22a`。S0双席仅审核旧三包范围，原票为[GLM](review-s0-glm.txt)/[Kimi](review-s0-kimi.txt)，[调用索引](s0-calls-summary.json)保留准确身份及原件。两席各33Read、27项要求完整，但未覆盖扩大范围，也漏查GOV-S0-I01，不得据此关闭后继实现。

旧开发批次的代码、测试及main合入事实保留；其流程例外与监督充分性继续由本请求复核。前批接收凭据循环、CLI/实际Read实现摘要混淆、启动记录接口和CLI写集漂移已在候选中修订，仍不是产品已修。

本轮未改产品或测试，没有新产品测试结果。根独立复核16个调用原件hash及两份完整终态的严格JSON失败；本次后继修订文档检查530条相对路径、62项设计验收编号无失败，Git空白检查通过。归档字节一致性和文档检查是行政核验，不能充当独立模型审核。当前完整raw仅本机留存；没有异机备份、生产live、OS定时器、远端上传或清理许可。

# 人工开发门禁后继派包提案（未获模型调用准入）

基线 main 9a4855a39121f2483e1630082bc36533a2165a5e；协调树 D:/project/agent-coop-governance。调查者/唯一正式发包人 dispatcher_next。这里只读调查并准备行政提案；没有新模型调用、产品/测试/CI改动。旧15/15 CodeBuddy及2/2 native批次已结案，不结转。旧main与作者现场不revert，上一批程序合规性待新独立审计。

## 直接发现与责任边界

1. 当前result的“角色按设定执行”只由运行时品牌、作者/双审核/监督调用链支持，不能替代design§4.2范围、工程、体验适用性、实现、QA、发布/文档、复盘的阶段覆盖。可选模板须按本任务触发判断，既不默认全部常驻，也不能不写理由直接遗漏。每个适用阶段要有owner、输入、交付、前置、独立性和本revision证据；不适用项要具名理由及审核。
2. run-review.ps1 Writer分支只核admission.status文字、candidate/root/session/write_files与若干hash/env；没有旧ReviewPolicy、必需final、政策变更授权、必读来源集合、阶段角色完整性的确定性门禁。readonly分支更没有这类准入检查。run-supervision-g1.ps1核版本/原session，不审政策遵循。
3. collect-review-evidence.cjs已经拒绝B两次error_during_execution/maxturn为成功交付，因此主要失败不是它把B错误解析为成功，而是C1必需final后来被C2/监督临时例外接受。新门禁不能让评审PASS、root描述清楚或最终监督PASS覆盖未获授权的政策变化。
4. WatchdogSeconds仅记metadata，两个wrapper都是同步node调用，明确未自行enforce。产品runtime有600秒/8MiB，但不能覆盖人工开发wrapper所有生命周期。原矩阵外部看护前61秒空档真实存在；本轮先改人工操作准入，不顺手迁wrapper扩大runtime.run_bounded的sample marker/cwd合同。
5. 两席自述已读与原生Read返回不总一致；长行被截断、漏包、C2仅沿旧上下文，均不能按最终自报补全。最后native补读事实不自动证明此前派发和接收符合旧政策。本批须使用fresh审核/监督会话审旧政策、实际旧输入与实际行为，不能让原席自证。

## 本轮唯一实施范围和独立写集

A / policy owner：agent_coop/review_policy.py、tests/test_review_policy.py。
纯校验冻结ReviewPolicy/阶段覆盖/原策略引用/本次变更授权/必需角色独立性/输入摘要/有效作者交付/必需审核与监督证据。输出确定性阻断与准确引用，不写Store、current、另一个状态台账。新模块是当前仓库缺失的单一门禁责任，不替代Scheduler。必需final缺失不能由评审自己豁免，历史B27持续可追。政策版本及其不可省略原件由受审合同固定，不能靠prompt任意删减。

B / evidence owner：agent_coop/review_coverage.py、tests/test_review_coverage.py。
复用现有CodeBuddy/native事件形状、已有adapter事件解析能力和来源映射，归一每席每必需输入的真实读取证据。成功tool_use/result配对、准确源文件/hash、实际返回行内容、区间完整性、截断、原文/等价可读投影区别、CRLF呈现都显式校验；无Read/仅Grep/工具错误/读错版本/未完成Read不能支持required全文。模型自报不参与覆盖判定。不重开adapters/runtime；native旧final复用等parser问题单列后继，不宣称本包修好。

C / CLI integration owner：agent_coop/cli.py、tests/test_cli.py。
在既有CLI唯一入口新增只读verify-development组合A+B；接收显式冻结策略/来源索引/原始调用证据等合同输入，报告准确candidate/action/policy/input摘要与阻断；缺证非零退出。只读仓库权威及原件，不写Store/current/STATUS、不启动模型、不新增调度器。输出属于可复现派生报告，根/发包人每次修复派发及accept前必须按准确输入重新消费；不把它称为任意Git操作或OS强制拦截。

先冻结A/B最小纯函数参数与结果结构、C输入文件索引合同。三包各2文件、写集不重叠，可同时实现；默认容量4可配置，本批实际3就绪作者不凑第四包。C可用冻结接口stub作本地单测，组合后必须使用A/B真实实现，不能以stub绿代集成验证。禁止为凑行数拆无语义helper；若任一文件超软目标，作者必须解释内聚性/消费者，独立席裁定。

## 必须先固定的阶段职责和政策

- 范围/工程方案：根承担协调与文档，不写产品实现；旧策略+本次需求+现有实现+接受标准形成明确版本。
- 开发者体验：本次新增拒绝/错误报告CLI，是适用阶段；检查missing/stale/denied/未读及解除条件是否可理解，不借“无Web”直接标全部NA。
- 实现：三个fresh CodeBuddy deepseek-v4-pro独立会话，准确文件allow、独立worktree、两文件小包；不得写合同/其他测试/CI、shell、commit或新模型。
- 代码审查与QA：fresh CodeBuddy glm-5.3、kimi-k3-2两席独立交叉全链；可由同席承担互不冲突的审查+QA判断，但须分别产出，作者不可自签。根运行固定测试并提供原件，两席独立核查判据、负例和范围，不仅摘要投票。
- 发布/文档：根维护既有owner文档与当前入口，最终接收/合入沿用户授权及有效门禁报告；没有push/live自动许可。
- 复盘/监督：fresh native Kimi只读会话直接审上一批C1必需final/政策授权、C2例外与上一监督输入遗漏；计划与最终监督沿该新会话形成闭环。不能只判断叙述清楚，必须判定政策遵循。

本批作者缺有效final即包级交付阻断。可由独立席提出预算内一次具名返工，但不得以测试绿/文件已写/PASS免除final；返工仍失败即保持阻断，无本批例外接收。后继政策变更只能走明确变更授权并对新revision生效，不倒填旧失败为合法。

## 验证与现实消费点

冻结负例：上一B两份失败即使exit0且diff/tests正常仍拒绝接收；删旧策略/改policy digest/必需输入从prompt漏掉仍拒绝；同作者/同session换角色不得算独立票；同文件旧hash、缺tool_result、失败Read、Grep命中、长行截断、遗漏区间、伪造自报全文均不得计required完成。等价投影必须同时绑定原件与变换证明，不能仅凭漂亮格式通过。CRLF只允许明确的呈现归一，不改原字节。

正例：完整、准确、无角色冲突且原生读取覆盖满足的固定历史/新本轮证据可形成确定性通过报告；不因普通未测项与当前action无关而扩大阻断。最终状态须区分delivery/review/policy/coverage/admission；不用一个布尔PASS掩盖层次。

根在准确组合上运行有意义A/B/C测试与唯一统一verify，检查旧测试发现未丢失/重复。用真实历史缺陷和负例回放，以及本轮真实C1/C2调用验证门禁，不追加canary模型。C1/C2票后的actual覆盖不满足必需输入则票不能驱动下一门禁；额度不足保留阻断，不能用最后native悄悄补齐独立必需票。

bootstrap期间沿原wrapper，人工准入本身先冻结旧策略/必需输入并检查；新CLI接受前不得声称自动强制已完成。外部看护必须先进入ready再启动模型，发包后立即绑定唯一实际PID+创建时间并持续运行，不再依赖先发起长工具调用、事后才建监视循环；看护失效/身份不确定/超时按已授权流程停止该次，不换PID盲杀，不恢复负例文件。此为本轮运维前置，仓内新启动器/全生命周期产品执行边界另包。

## 新有界调用预算（提案，尚未准入）

fresh GLM+Kimi审计/设计S0各1，共2；仅允许一次设计修订双复核，最多再2。fresh native计划审计1，先审旧政策遵循及新方案后才准作者。三个作者各1，共3。C1两席各1，共2。至多每包一次finding-bound作者修复，最多3；有修复才启用唯一C2双席，共2。最后native1核全部政策/交付/覆盖及状态，不代签必需票。

最大14 CodeBuddy + 2 native；无设计返工/无实现修复时基本7 CodeBuddy + 2 native。每次CodeBuddy请求20turn/600秒，仍不宣称CLI轮数硬限；native600秒。每一次开始即消费，不把准备计调用。未使用额度不挪用途，无第三内容轮/超额续调/匿名替换/模型fallback；旧批预算完全隔离。某包阻断时无关包仅在独立验收范围获审支持下继续，不能把不完整组合冒称完整目标。

S0结束先交根原票/身份/实际读覆盖；根冻结后native；native后根冻结作者准入；作者均退出才冻结组合与C1。每次进入修复或接收动作，必须给出准确旧策略、当前策略、输入完整性及有效报告，不靠最后监督补派发前门禁。

## wrapper与CLI静态复核

当前node v24.14.0 SHA63c259c81e5d472b5f11c8d506070130cb04a1ecf84b80377a34ed6ec9048088；CodeBuddy2.164.0 entry SHA426186a82e36466d5be485f335ced1b0d664539c53b72a5f10ba3a267e60dab6、dist SHAf9affe2aed036a3a3ee8486b82e77b176a2a4b21f7bed721074c1c1e4a312e65；native0.43.0 entry SHA5b300a573d306f879361eb7a2baec3a19448ea94eadca28001408b19c42eeb69。以上本次读文件hash确认，版本来自固定安装包；实际可用性/模型身份仍以新调用init/resume_hint为准，不调用探针证明。

原TEMP run-review.ps1 SHA4fb60e86ff3db7ee2ce9593e80427bfcca78f9755ffd325f7ac0f75f1d7ddaed；run-supervision-g1.ps1 SHAef260838f90da38f2c540f2601f22cc343ade513d2ed0f415de81df08e2a7c77；collect-review-evidence.cjs SHAd2eaddf0b37c3a92fa4df39068817b73fe0638c179515542f4b00ca51af65037。仅复用传输/原件采集，不能把这些脚本说成新政策门禁。

fresh CodeBuddy使用显式新session-id（不resume旧审核身份）；native fresh使用原同hash只读agent-file而非恢复旧监督会话，不指定/猜测model/provider，不启用fallback。旧actor原票保持历史，不计本批必需独立票。工具catalog不是实际能力证明；只读限定仍非OS沙箱。新会话/工作树具体名称由根冻结行政候选后一次绑定，未获得正式调用准入前不启动。
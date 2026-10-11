# 产品权限后继批次发包提案

状态：待根冻结新合同/计划并经独立审核；不是模型或 writer 准入。2026-10-11，唯一发包人 dispatcher_next。

目标：修复固定隔离样例的权限派生、CLI 序列化与进程环境链，分别举证产品静态合同和产品入口实际权限。全部产品/测试/CI 由真实 CodeBuddy deepseek-v4-pro 作者完成，Codex 只协调、文档、验收、受审集成。

本文件为独立 TEMP 提案，供根整合进同一 request 的权威合同/计划，不另立当前状态台账。不重新运行 bootstrap probe，不修改旧 wrapper 或历史原件。

## 1. 准确基线与前票

- 新协调树：D:/project/agent-coop-product-permission；分支 codex/product-permission-20261011；本次读取 HEAD=f0223b34e0204dde667ea8dff2d80beb3d3b1a3c，读取时 clean。
- 已接收静态产品 ed65079e6fd2cd3afc09ec871817cfb11c621b76；收尾行政 f44d4114253471b0426cd8d720114e69d652e5bb。根已将 f44d411 合入本地 main 并记录 f0223b34；本提案未重复 main 测试。
- 同请求 product-permission-scope-proposal-20261011.md 是方向来源。原 GLM R1 第5节、Kimi R1 第17–19行及两席 R2 保留的 B18/B11，是新合同范围依据，均不等于实现批准。
- 原 Kimi 明确 A→B 两串行包；本批维持该顺序。冻结接口后并行的建议如需采用，必须新两席明示改判；本提案不采用。
- 旧批次17/18 CodeBuddy、2/2 native 已结束；剩余额度不结转，新批从0计数。
- 历史 publication 根因 GLM B11/Kimi B09=unknown，不纳入本次修复；产品权限 GLM B18/Kimi B11 由各原席按新证据自关。

## 2. 发包前必须冻结的最小合同

1. sample 为唯一权限派生 owner：隔离根+固定 workspace/feature.py 写集进入版本化冻结 config；沿既有 config_digest/implementation_digest 绑定；schema、旧配置拒绝、dispatch 重验和错误条件明确，不读取 latest、不静默补宽。
2. adapters 为唯一 CLI 序列化 owner：只接受经过校验的数据，角色名不决定通用 adapter 行为；逐条 allowedTools/disallowedTools argv，dontAsk/none/空 MCP/显式 shell deny；拒绝 acceptEdits、泛化 Write/Edit、规则元字符造成的扩权、未知版本或不可表达的 profile。
3. 环境合同遵守 design 中“进程环境白名单注入”：明确可继承变量名称、必要值的来源、禁止项、缺失处理，以及与固定 child memory 四值的冲突处理。不能以整个 os.environ 加四值覆盖冒充白名单。不得把凭据值写入日志/config；登录仍走既有宿主支持方式和引用。
4. runtime 最小接口扩展必须兼容 checks.validate_feature 直接消费 run_bounded 的非模型验证命令；模型路径的受控环境与非模型执行环境分别明示，不使 validator 意外失去所需环境或扩大 profile 权限。测试观察实际 Popen env，不仅测试构造字典。
5. 路径沿现有 paths.checked 和摘要机制复用；精确规则语法、reparse/硬链接、跨根/前缀/别名边界拒绝语义固定。保留外部并发改链、宿主 hook/tool.check 提前 allow、真实 memory 全域与全 OS 隔离未证边界。
6. 产品实际权限验证的入口、固定 fixture、正负矩阵、模型/工具、一次调用预算、逐格分类和停止条件在合同审核时冻结。此验证由修改后的 sample→runtime→adapters 入口产生真实 argv/env，不能由治理 wrapper 绕过产品链代替，也不是重新验证 bootstrap profile。
7. 当前 `sample.validate_profiles` 固定20turn/600s，产品实际验证沿其预算；若另定12/300必须先改合同并具名入写集，不能验证时悄改。

## 3. 两个作者包与确切写集提案

### PP-A / owner P6：样例冻结与派发重验

唯一可写：agent_coop/sample.py、tests/test_sample.py、tests/test_flow.py、tests/test_cli.py。

派生唯一文件写权限及版本化环境策略引用，冻结在原 config；拒绝缺字段/旧版/歧义/超集；派发前重验已有摘要与权限，CLI 无效输入应在创建运行根之前失败。复用 Store/gates/paths，不修改其源码、不新建权限台账。tests/test_cli.py 是现有 validate_profiles 消费者，包含受审兼容修改。作者交付应指出受影响消费者、复用点、软规模说明及未覆盖边界。

阶段验证：既有 tests.test_sample、tests.test_flow、tests.test_cli；有意义的冻结/篡改/旧版/错误副作用及暂停恢复回归。中间候选允许 adapter 尚未消费新字段，但不声称产品权限或 live 已通过；B 必须基于 A 的准确交付 SHA。

### PP-B / owner P2：CLI 规则与环境传递

唯一可写提案：agent_coop/adapters.py、agent_coop/runtime.py、tests/test_runtime.py、tests/test_adapter_commands.py（新文件，须合同双席先批准）。

新测试文件只整体接收现有 AdapterCommandTests（当前 tests/test_runtime.py:176 起）的唯一职责及其权限命令案例；从旧文件删除该 class，不复制第二套命令测试。解析与子进程测试留原 owner。原 test_runtime.py 464行，runtime/additional env 案例仍可能触硬限，须按实际规模交审，不能压行或擅自再拆新模块；若必要迁移范围超本提案，先具名修订而非作者自扩写集。

adapter 只序列化合同，runtime 应在进程启动前强制模型环境白名单及版本/路径前置。实际作者决定最小实现，不新建相似 adapter/dispatcher/policy helper；非模型 run_bounded 兼容须单独测试。

阶段验证：tests.test_adapter_commands、tests.test_runtime、tests.test_gates；argv token/缺字段/歧义/元字符/链接拒绝、实际子进程环境允许/剔除、四值冲突拒绝或固定裁定、非模型验证兼容、junction 原断言无退化。test discovery 必须证明迁移后原测试仍被唯一发现。

顺序：合同双席 → native计划监督 → A真实作者 → 根局部验证/冻结 → B真实作者 → 根局部验证/组合冻结。默认 CodeBuddy 容量4可配；本两包有依赖，作者峰值1不是把容量改成1。双席审核峰值2可并行，native监督并发1。没有为凑4路而新增包。

## 4. 新批次有界调用预算（提请批准）

| 阶段 | CodeBuddy | native | 准入与结局 |
|---|---:|---:|---|
| C0 合同/计划双席 | 2 | 0 | 原 GLM/Kimi 各一次；独立输入，互不看本轮新票 |
| N0 计划监督 | 0 | 1 | 两席有效支持后，同原 native session；条件不得冒充已满足 |
| A、B 实现 | 2 | 0 | deepseek 各一次，A→B，精确写集和摘要 admission |
| C1 内容首轮 | 2 | 0 | 准确组合候选+统一验证；批准或拒绝产品验证 fixture/入口和修复准入 |
| F 具名最小修复 | 最多2 | 0 | 每 owner 至多一次；原票具名 finding、同写集，不预留通用续跑 |
| V 产品入口权限实际验证 | 1 | 0 | 只有 C0/C1 明确批准的固定方案且根前置满足才运行一次；20turn/600s，不调治理 probe |
| C2 内容及实际结果末轮 | 2 | 0 | 同一准确候选、真实逐格结果、修复差异；两席各自关闭本人 finding |
| N1 最终监督 | 0 | 1 | 直接读取验收原件与实际工具映射，查状态/权限/预算，不代内容席签字 |
| 合计 | 基本9，硬上限11 | 上限2 | 当前实际0/11、0/2；调用失败/超时仍计消耗 |

所有 CodeBuddy 审核/作者最多20turn/600秒；native最多600秒。CLI turn 参数不冒称硬预算，外部 PID+创建时间看护；失败不换身份、不自动续调、无 conclusion-only 隐藏追加。合同若被否决且需再次模型审核，必须根显式修订新批预算，不挪用作者或 V 次数。首轮之后修复仅在 C1 明确授权的修改边界内；若修复改变 V 协议/矩阵/可信边界，V 不运行，C2 先审新候选并保留产品实测待办，不自动追加结果票。

V 的测试 fixture/harness 如需新增产品或测试代码，必须在 C0 指定确切 owner/path 并纳入 A/B；Codex 不自行写产品测试脚本。优先复用已有产品入口及声明式 fixture，不复制第二调度器。调用计数中的1为一次真实 deepseek 会话，不含 live 四角色样例执行；全四角色 live 仍另行准入。

## 5. Wrapper、会话复用与可证范围

本目录 wrapper-session-static-evidence.json 是本次只读现场核验与历史公开回执摘要。它证明文件存在/hash一致、原 session 曾成功；未探测当前账号可用性、配额或私有持久状态，不保证下次续接成功。

- 原 review cwd=D:/project/agent-coop-g1-review，读取时 clean/HEAD ed65079；准入后由根/发包人受控 checkout 到准确候选，保留旧输入，禁止 resume-create-missing。
- GLM：agent-coop-g1-glm-r1-34bce56b-20261010；Kimi：agent-coop-g1-kimi-r1-34bce56b-20261010。各沿 run-review.ps1 -Resume 本席会话、-Model 精确名字、原 cwd，新增 gate/logdir避免覆盖旧原件。
- native：session_a75b547a-13c5-4740-b07f-f3d4ccc93704；run-supervision-g1.ps1 -Resume 沿原 cwd。argv 不带 agent-file/agent/新 model/auto/yolo；持久 profile.bind/tool guard 是只读依据，print模式固有forceAuto不冒称审批模式未变化；本机0.43.0，实际model仍unknown。
- 作者 fresh sessions，不续旧 no-session-persistence 作者：建议 agent-coop-pp-p6-a-20261011 / agent-coop-pp-p2-b-20261011，launch前确认未占用；wrapper seat p7/p3 只是旧传输别名，package/owner/write_set 才是身份。
- 作者用已有 Writer 精确文件 profile，Read/Glob/Grep/Write/Edit；allow 的 Read/Glob/Grep/每个 Write(abs)/Edit(abs) 分独立argv，deny Bash/PowerShell 分独立argv；dontAsk、none、empty MCP、四 child memory env、no-session-persistence 保持。admission 绑定 root/candidate/session/逐文件SHA/规则路径；前置非reparse/nlink1检查保持。
- 现 readonly wrapper 仍是 --tools Read,Glob,Grep 加单串 --allowedTools Read,Glob,Grep；后者本版不拆逗号，不能称三条allow已生效。只读依靠已用工具选择集合；沿原cwd安全Read实际成功。禁止为本批悄改 wrapper 或把它包装成操作系统沙箱；若新合同认为必须改，另立受审最小wrapper修订，当前不改。
- Node/bin/dist/wrapper 摘要由每次人工 preflight 复核；Writer wrapper 本身不自动核验全部二进制摘要。监督 resume wrapper 会核验 native bundle 的指定SHA。
- Collector 复用原 collect-review-evidence.cjs；旧 prepare-continuation-s0.cjs 含旧阶段/commit硬绑定，不直接当新批builder运行。新输入只用本批冻结 Git blobs+小文件索引，按主题分段、SHA绑定，不重复塞27k巨包。禁止改旧packet；两席只收到本席旧票与同源新证据，不含他席当前票。

## 6. 验收与停止条件

根对准确冻结候选运行唯一统一 verify，收录命令、exit、完整output、清单before/after、实际test数量/skip原因、干净状态；局部验收与统一验收按变更适度，不机械重跑无变化全套。原 main 验证不能代替新候选验证。

V 前冻结实际argv/env名称和来源（不记凭据值）、工具/模型/版本、候选/hash、任务TEMP根与正负 fixture、执行上限。逐格记录 native tool_use/result、拒绝原因、前后字节hash；未调用/前置失败/工具不存在为unverified或unsupported，不能算拒绝通过。只允许任务TEMP测试写，不写真实宿主memory；任何未授权写成功、身份错误、越界或超时停止并保留全部现场。预期permission denial是负例结果，不是需自动重试的异常。

最终分别裁定：静态产品权限合同、一次产品实际CLI矩阵、固定四角色live准入、接收/合入。V通过也不证明全域沙箱、hook缺失、所有路径别名、自动memory全域、POSIX、云CI或完整live工作流；不拿普通假memory目录负例代替真实目录。B18/B11是否关闭由原席按这些有限边界明确裁定，不由根/发包人代关。

如 scope/schema/env名单、测试迁移或 V 协议仍有阻断，保持具名待办/owner/复核条件；本提案不以时间或旧预算耗尽宣布永久不可继续，也不无限追加模型。

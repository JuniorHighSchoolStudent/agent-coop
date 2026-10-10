# 隔离样例当前交付记录

范围：本请求整体交付；维护者：Codex集成者；状态：离线实现中，G1与live均未通过；来源：用户隔离样例选择、[G0接收](result-g0.md)及[职责纠偏](role-correction.md)。这是本请求当前结果入口，各门禁原件按链接引用，不从文件名猜最新。

## 当前派发控制：首审未通过，按审核范围派修

2026-10-10用户再次明确：已有候选发现缺陷，也必须多轮审核，由专门发包人依据审核派发。根此前把静态检查/测试失败直接派成修复包，缺少这条链，属于流程偏离；不以后来的通过倒填此前批准。

首次独立审核前已冻结新增实现/修复调用并收回所有旧writer：P2/P5/P6正常退出；P1超时收回、exit1且无最终交付，不按写入文件数算完成。P5的14项局部测试通过；P6此前20项在途组合诊断为2失败、1错误，因无冻结源码绑定只作线索。收回全部writer后的[组合验证](verification-g1-r1.md)仍未通过，进入正式审核而非直接派修。下表保留初始候选责任归属与事实；后续仅“首轮审核与证据归属”中的具名审核范围可由发包人启动。专门发包人为本任务独立Codex协调实例`package_dispatcher`；根只收证、验证、维护此入口和执行受审集成，不再直接给实现者派修。

后继流程：冻结组合候选及功能包写集 → 独立CodeBuddy GLM/Kimi多方审核 → 发包人以准确候选与稳定finding_id发布修复包 → 实际CodeBuddy执行 → 原席复审逐项关闭 → 原生Kimi监督核验 → Codex接收/集成。检查线索、测试通过、作者交付均不能替代审核意见。两席首次意见独立，复审记录候选变更与未决项；监督不缺席、不由集成者代签。G1、live与Git合入仍各自举证。

待审候选已固定为`34bce56b624cf521b33dc5b4916bd1c8e7711536`，独立detached审核树已创建且clean。两席只读首轮审核已完成并要求修改；新实现/修复仍须正式审核后的具名包。共享目录在途写集隔离及此前未按审核先派修均提交审核，不冒充已完成产品资源隔离。

准确候选checkout又做一次组合验证，见[原始输出](verification-g1-frozen-r1-output.txt)、[内容清单](verification-g1-frozen-r1-manifest.json)、[绑定元数据](verification-g1-frozen-r1-metadata.json)：131项、20失败/2错误/2跳过及85行硬限失败，41文件前后清单一致，清单SHA256为`9ab421ccb7f21506a5b39b38180bf702eb3a0053fddf0d54ed476af41b6071d5`。本次为首轮正式审核的主验证证据；先前工作树的3个error保留为历史异常，不能用复验较少错误数抹除。复验原因是Git对历史文本的换行规整，未改产品代码来获得不同结果。

## 首轮审核与证据归属

首轮共6次实际调用，完整身份、退出、工具错误及原流摘要见[调用元数据](review-g1-r1-calls.json)。输入不可达的两次GLM原文也保留：[首次](review-g1-glm-input-unavailable.txt)、[补充](review-g1-glm-input-followup.txt)；另两次超轮次没有有效最终票，不能用进程exit0算通过。两席有效原票已归档：[GLM原票](review-g1-glm-r1.txt)、[Kimi原票](review-g1-kimi-r1.txt)，均为CHANGES_REQUESTED。GLM通过同一session的一次零工具结论调用收回：155.999秒、exit0、result success、实际tool_use=0；此前读取超轮次与权限失败不计为通过。Kimi补充读取后正常返回。实际模型分别为glm-5.3与kimi-k3-2，监督尚未启动。

有两席共同支持的小包由专门发包人准备并按受审范围派发：P2函数硬规模、P3路径与归档、P5状态拒绝退出码；必须各自独立工作树、准确基线、finding映射及限时调用后才可启动。P1发布异常、P2/P6日志合同、P4共享路径边界、P7真实作者接管仍待明确范围，不因测试失败直接派修。此为修复范围准入，不是候选通过。

2026-10-10T14:18:19Z发包人曾启动三个独立工作树修复调用，但自行将工具集合增加PowerShell及允许作者commit，缺少本轮受审依据。根核查实际参数后要求回收，14:20:13–14Z三调用已按PID及创建时间核对并终止，均无final。结束后原流显示实际PowerShell调用P2=4、P3=1、P5=6，内容为目录/git只读/测试或版本探测；没有将这些探测记作通过。仅P2留下runtime.py部分改动，保留未交付来源；P3/P5树无产品改动。随后只允许恢复既有Read/Glob/Grep/Write/Edit后具名替代，每包最多一次；验证与commit由协调者执行。此事作为发包配置偏离保留，不由测试通过追认，不从调用成本中删除。

原票中的证据口径不改写，以后继核对补充：P1局部实际33项中1个error，不能称全部绿；先前工作树验证20F/3E，准确冻结checkout验证20F/2E，两次均失败且旧异常保留。41文件清单仅两个文档不同：role-correction.md与runtime-tool-evidence.md，实际读取这两个文件的工作树字节后仅作CRLF→LF规范化，其SHA分别精确等于冻结清单d4bd5e764b30198bb6011f896398c216b9c50402baea6ee1fdd0110de0f50c60、169c2217345d0f757975be3a080decd5058bce5f927cd75f5fd04391f90ed9f1。其余39文件SHA相同。导航漏解释第二个文档是输入组织缺口，不能要求审核席自行猜测。以上核对不代替原席关闭finding。

首轮范围补充已由两原席完成（[两次调用元数据](review-g1-boundary-b-calls.json)、[逐字节换行证据](review-g1-crlf-byte-evidence.json)，累计首轮审核8次实际调用）：[GLM附录](review-g1-glm-boundary-b.txt)、[Kimi附录](review-g1-kimi-boundary-b.txt)。两席支持P2日志边界、P4清理范围、P7真实接管；P1仅支持诊断测试，代码修复仍未准入。接口owner已发布[日志目录后继澄清](interface-log-directory.md)，旧冻结合同不改写；P2同一个包单writer继续，P6消费方不动。附录纠正原票证据口径并关闭相应哈希说明缺口，不构成G1候选通过。修复后的原席第二轮与原生监督仍未发生。

P2/P3/P5本批三次被回收尝试及三次替代调用的实际身份、工具、退出、原流摘要与P2部分产物交接见[调用归档](repair-g1-r1-calls.json)。P2替代作者明确接管被回收调用的既有改动，没有把它伪称替代调用新写；三包均由实际CodeBuddy产生/接管，根只运行验证、冻结候选与整理证据。

|当前修复候选|实际局部验证|接收边界|
|---|---|---|
|P2规模 `8183c5d1fddba73ff1ae6f9e978f6dde0acc33e7`；[作者](repair-p2-r1.txt)|[25项runtime通过](repair-p2-r1-tests.txt)；[摘要](repair-p2-r1-test-metadata.json)；规模hard_failures为空|日志目录问题仍须同包续作，未原席关闭|
|P3路径/归档 `972891513e8387d761dfa3415199ecb57b18d745`；[作者](repair-p3-r1.txt)|[13项路径](repair-p3-r1-path-tests.txt)+[10项归档/备份](repair-p3-r1-archive-tests.txt)，共21通过/2权限跳过；[摘要](repair-p3-r1-test-metadata.json)|仅paths/archive改动，cleanup及旧test_archive未改；待组合复审|
|P5 CLI `cb46a72d8db4bae174eaf6fb6b97b83bc92d6213`；[作者](repair-p5-r1.txt)|[14项CLI/Web通过](repair-p5-r1-tests.txt)；[摘要](repair-p5-r1-test-metadata.json)|仅cli/test_cli修改；未运行浏览器JavaScript，待原席复审|

P1两个原失败用例在准确34bce56b冻结源码上执行最多20轮、首失败即停止的诊断；实际20轮×2项均通过，[原始输出](p1-publication-diagnostic-existing-tests.txt)及[逐轮记录/摘要](p1-publication-diagnostic-existing-tests-metadata.json)保留。没有外部句柄或历史根因证据，不能关闭GLM B11/Kimi B09，也不据此批准代码重试策略。

三包独立树验证前后相关文件摘要一致，均未合入main。P3独立树仍含基线runtime的85行硬失败，不能把局部通过说成整树verify通过；P2规模候选会在组合候选接收阶段统一验证。


## 冻结候选的包归属（34bce56b）

来源：用户要求按功能拆小包并行开发，并明确CodeBuddy实现并发默认4、用户可配（2026-10-10）。以下分配承接[职责纠偏](role-correction.md)，替代把所有集成入口交给一个作者、等待core/archive整体完成才启动的安排；并发沿[design §7.3](../../../docs/design.md#73-资源与预算)及用户新指令，旧G0原件和纠偏记录中的临时2路安排成为历史，不改写原件。这里的P1–P7是本请求工作包编号，不是路线图产品阶段。产品、测试与CI的实际作者均为CodeBuddy + deepseek-v4-pro，Codex只协调、验证与集成。

|包/验收单元|唯一写入范围|就绪与当前状态|
|---|---|---|
|P1 状态与续作|`store.py`、`runner.py`；`test_store.py`、`test_runner.py`|新实际session agent-coop-p1-state-20261010在620.4秒时收回，超过600秒人工看护20.4秒，exit1且无final；33项局部验证有1个STATUS替换错误。不能称交付完成，待正式审核|
|P2 有界进程与协议|`runtime.py`、`adapters.py`；`test_runtime.py`|原core实际session修复调用正常退出0，25项局部tests通过；runtime._collect为85行超硬限，日志目录与消费者合同冲突仍在；待正式审核|
|P3 路径、归档与备份|`paths.py`、`archive.py`；`test_paths.py`、`test_archive.py`|三阶段实际调用均退出0，新增回归后与P4合计39项出现18失败/2skip；见[原件与分诊](implementation-archive-evidence.md)，未再直接派修|
|P4 清理计划与执行|`cleanup.py`；`test_cleanup.py`（拟拆）|与P3分开审核；当前回归调用已结束且写权回收，测试拆分/修复仍待正式审核发包；archive薄转发及共享helper边界需审核明确|
|P5 CLI与只读Web|`cli.py`、`web.py`、`__main__.py`；`test_cli.py`、`test_web.py`|实际deepseek-v4-pro/session agent-coop-p5-cli-web-20261010退出0，4文件实际改动，14项局部tests通过；见[原件](implementation-p5-r1.txt)、[元数据](implementation-p5-r1-metadata.json)、[验证](implementation-p5-r1-tests.txt)；待独立审核|
|P6 固定流程与精确门禁|`sample.py`、`gates.py`、`checks.py`、`supervisor-agent.md`；`test_sample.py`、`test_gates.py`、`test_flow.py`|实际deepseek-v4-pro/session agent-coop-p6-flow-gates-20261010退出0，gates及3测试文件实际改动；见[原件](implementation-p6-r1.txt)、[元数据](implementation-p6-r1-metadata.json)、[诊断](implementation-p6-r1-tests.txt)；存在跨包日志目录失败线索，待冻结审核|
|P7 统一验证与CI|`verification.py`、包初始化文件、`.github/workflows/verify.yml`；必要的`test_verification.py`|仍为未接收Codex草稿；只维护唯一验证入口，不复制测试清单；待独立审核后由专门发包人发布接管包|

表中源码相对`agent_coop/`、测试相对`tests/`。每包携带固定接口、写集、实际作者session、局部检查结果、未决项及交接；无关文件不得顺手修改。共享API变更先交集成者协调owner，不通过复制实现绕过依赖。当前未接收源码都属于候选。

依赖约束落在接收点：P5可先按Store/sample公开接口开发；P6可先按runtime/archive合同开发；组合验证才要求这些提供方通过。P3/P4共享receipt合同但写集分离；同一作者session不得并发续接。每次实际调用结束释放槽位，待修包重新排队，避免大包持续占有槽位。包完成可独立验证、进入只读预审；最终G1仍审核同一个精确组合候选，包通过不能替代系统验收。

## 当前未决项与门禁

|事项|责任人|当前事实与下一步|
|---|---|---|
|首轮缺陷|两原审核席及专门发包人|缺陷身份、范围和关闭依据以链接原票及后继附录为准；不另维护precheck重复状态，尚无修复后复审关闭记录|
|G1独立审核/原生监督|CodeBuddy GLM、CodeBuddy Kimi、原生Kimi|两席均已CHANGES_REQUESTED；缺口与争议先对齐，具名修复后须原席复审；监督未启动，不以G0计划PASS预支实现通过|
|四角色live及归档backup清理演示|受审sample runner，Codex仅启动/验证|未启动；必须G1通过后执行；暂停续作、四次调用、local_only与固定scratch范围保持不变|

本表是开发请求的人工交付检查点，不冒充产品运行状态数据库。子模块原始回执和确定性验证由协调者归集；退出码、测试通过、评审接收、Git合入与发布分别举证。

core/P1/P2作者身份、原始最终回执与P1超时无final事实统一见[核心候选证据](core-candidate-evidence.md)；归档三阶段见上表入口。均为待审事实，不计独立通过票。

## 预算与边界

- 已发生bootstrap调用均结束或已收回：核心前3次+P2修复、归档3次、P1/P5/P6各1次。P1超时缺final且人工看护存在20.4秒超差；不把手工看护说成产品硬墙钟保障。
- 原P1/P5/P6必要复修预算不构成继续派发授权；由专门发包人依据正式审核发布下一包及预算。用户指定默认4路继续有效；活跃调用由发包人核对同账号总数，已结束不代表已接收。
- 此次并发在bootstrap中由Codex人工派发、文件写集隔离；当前候选树内的在途作者尚不具备产品独立工作树资源隔离证明。产品仍须实现设计中的独立工作树/claim保障；本轮不得将人工并发冒充已实现通用Scheduler或team.yaml解析器。
- 上述不改变产品样例的4次总模型调用预算，也不改变G0/G1各最多两轮评审或原生Kimi单次10分钟看护。Codex草稿接管保留原作者事实，不要求无目的重写。
- 工具目录与实际选择的差异见[本机权限证据](runtime-tool-evidence.md)；不把命令参数或init目录当OS沙箱证明。
- 尚未清理样例fixture以外的数据；不push、不上传、不启用OS定时任务。完整产品P1/P2/P3仍未交付。

证据归档校验：本检查点202条本地Markdown路径与62条设计验收编号机械检查通过；新增26份证据/澄清的Git暂存blob已逐字节对照工作副本。为保留冻结输入及原输出的真实摘要，归档不规范化其CRLF或原始测试subTest行尾空格；默认`git diff --cached --check`因此报告原始证据空白，不能称该默认检查全绿。此处适用AGENTS的历史原件保真规则，未修改产品文件或放宽产品规模/测试门禁；原始CLI完整流仍仅宿主临时保存。
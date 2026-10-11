# 限定行政诊断修复工作包草稿

状态：候选工作包，尚未准入、未派作者、未实现、未接线。维护者：Codex集成者；唯一发包人：dispatcher_next。当前进展及原意见只见[result](result.md)。本文件供后继准确派发裁定，不是新的状态台账或第14个产品包。

## 来源与有限出口

用户当前明确要求“看护的连续修补 也是应该派发给执行者啊”“这也是开发的问题需要在产品中解决”。本包落实实现actor纠正：协调者不再编写可执行修复；临时目录或行政标签不产生例外。旧[实施合同§6.2](implementation-contract.md#62-执行看护与状态)允许诊断/属性取值的有限恢复，本包只将实现交给实际CodeBuddy，并保持旧停止条件。原文允许集成者准备watcher差异的范围被用户指令收紧，不追认旧Codex代码为CodeBuddy交付。

S6的GLM有效pass及Kimi有效changes_requested是监督审议输入，不是双PASS或作者许可。[S6 native准入](s6-native-admission.md)仅授权独立监督审议原意见及有限修复路径；其实际结论未在本草稿预填。本包需要另一个准确行政修复准入，不能复用S6只读许可，不能填造已发生的双席确认或native计划监督。

产品B1五包继续被原阶段门禁约束。本包不是B1部分接收，不授权修改产品W/R2；产品GOV-06及其余finding仍须原产品实现、回归、真实使用和独立关闭。

## 精确基线、角色与两文件写集

- Git基线：`ed527d872b6fc130583d99b223cc0db3f60ef888`。
- 隔离工作树：`D:/ac-repair`，已由集成者实际创建并核detached于上述基线、Git clean；下列两文件已按源hash逐字节复制，尚未有作者修改。派发前仍核路径归属及准确输入。
- 审核物化目录：`D:/ac-repair/dist`，沿既有`dist/`忽略规则，仅作本次临时源副本和验证产物，不是发布产物；不改仓库/global ignore，不使用链接或reparse映射。
- 实现actor：真实CodeBuddy `deepseek-v4-pro`，fresh session候选`agent-coop-admin-diagnostic-repair-20261011-52e90c17`。实际actor、session、profile、入口hash、完整prompt、cwd与准入必须逐值绑定，调用前核会话未使用。
- 单次20响应/600秒、既定8MiB；账户组占一个实际作者槽。失败先调查，不自动重试或resume，不设固定返工轮数。
- 工具/权限按受审精确作者profile绑定；只给下列两个绝对文件Write/Edit。读取必需源保持可读，不开放任意Shell、任意目录写入或其他产品文件。发包与看护复用具名既有入口，不由Codex补代码适配。

准确来源目录为`C:/Users/june/AppData/Local/Temp/agent-coop-governance-20261011/`。派发人先校源hash，再逐字节复制；旧原件不改、不覆盖。

| 原文件及SHA-256 | 唯一可写隔离副本 |
|---|---|
| `watch-recovery-administrative-fragment-r3.ps1`；`cbfac69c0b04248442583c4e606c03646ca5aec19a038b572facc9a4c1e19d4d` | `D:/ac-repair/dist/watch-recovery-administrative-fragment-r3.ps1` |
| `check-watch-recovery-administrative-readable-r4.ps1`；`4c659b928180d7cdf81e64d9e4709073ed7d876fc3768300891b22d8eae392d1` | `D:/ac-repair/dist/check-watch-recovery-administrative-readable-r4.ps1` |

文件名保留来源名称不表示仍是旧hash；交付以实际新bytes/hash识别。fragment保持唯一函数实现，checker调用该隔离副本，不复制第二份判据。checker原来硬绑TEMP源和报告位置，作者只将这两个定位改为本包准确副本及本次独占证据位置，不能意外测试旧r3或覆盖旧readable-r4报告。验证生成的报告/原始stdout、stderr是运行产物，由集成者实际执行后捕获，不是第三个作者手写文件。

## 唯一行为修改及不变项

修复`Resolve-UnboundSnapshotCandidate`的失败诊断：当前fresh CIM数量/字段、held创建ticks以及比较精度说明只在成功比较后写入，复合失败时无法区分操作数缺失、取值失败、身份冲突或哪项条件触发。

作者必须在可能失败的API/比较前后及时保存已经取得的原值，分别定位snapshot校验、GetProcessById、显式SafeHandle、StartTime、fresh CIM查询、数量、PID/name/parent/creation比较、整数微秒投影、HasExited及parent原身份检查。保存实际失败子条件与异常原文/类型；未执行、未取得或查询失败明确unknown及原因，不补造0、false或身份，不为了诊断继续执行已应停止的危险分支。短路未执行的后继比较不能伪称已验证。保留原事件出口，不另立日志或状态协议。

不改变任何bound/stop/有限unknown继续的判据，不扩大not-found catch，不引入秒级时间容差，不吞异常，不放宽目标/父身份及有效句柄检查。保留原句柄所有权和释放行为，不在本片段新增Job、进程启动/终止或自动重试。现有owner→watcher成员核验→一次GO→wrapper顺序、600秒总截止、8MiB、权限和未知终止阻断均不在写集内。

可读异常沿已有readable-r4完整分片、精确join/hash/UTF16长度和不拆surrogate机制，不能删异常原文或用摘要替代。字段和case只为这项诊断，规模与内聚性按AGENTS检查；超过硬限不得自签例外。

## 必须实际运行的失败与恢复回归

1. 原checker的15个case全部保留：真实自有短寿子进程、正常绑定、自然退出、过期creation、错name/parent、精度不支持、父身份冲突、目标缺失/退出、非法PID、null getter及权限异常等；真实运行和受控模拟继续分别标明。
2. 针对旧r3先观察有意义的诊断失败：身份冲突应仍stop，但其报告缺少已取得的fresh数量/实际身份、held ticks或失败子条件。修复后同一负例仍stop，证据能定位比较双方与具体失败点。
3. 在既有checker内补必要表驱动模拟，覆盖fresh数量0/多项、字段不匹配、查询/显式getter异常、未取得创建值以及复合条件短路；模拟不得冒称实际OS权限实验。每例核decision不变、已知值不丢、未知不造、失败API准确。
4. 真实存活子进程正常bound，确认没有因诊断改变精度/身份匹配；原有限消失分支仍只有满足全部旧条件才可继续unknown，首次目标或持柄失败仍stop。
5. 对最终报告逐项核异常重组、hash、长度和可读性；核报告引用准确新fragment hash，源副本外无写入、旧原件不变。仅checker宣称通过不代替独立读取原输出。

作者交付须有完整有效final、两文件准确hash/diff、实际修改说明、测试建议及未验证边界。若作者profile不允许运行命令，作者不能自报已跑；由集成者用既有PowerShell执行准确checker并留完整原件。验证只操作自有临时fixture，不启动模型、不清理其他进程。

## 准入、独立复核与接线顺序

1. 收集S6 native真实意见，保持Kimi原GOV-06阻断。若native明确支持与既有S6双席意见相同的有限诊断修复，根与dispatcher可将这些真实依据映射到准确源、两文件隔离写集和具名执行者派单，无须在作者前重复完整双席及native审核；本草稿是原finding的实施细化，后写文本未曾由两席审过，不得声称草稿已通过。native尚未明确支持时不得预填支持；若实现超出原诊断/回归范围、改变判据或扩大写集，须按影响重新受控审核。修复后的准确版本必须经独立双席及native复核后才可接线，阻断依原席/具名独立替补关闭权限处理。
2. 根形成准确行政修复准入，明确用户actor纠正、当前有效审核/监督依据、运行入口及权限；该许可仅覆盖两个隔离副本，不开放B1。现成writer wrapper要求真实双席确认和native计划监督字段时，必须已有对应原件，不能伪填status或由Codex改分支绕过。
3. 唯一dispatcher用准确fresh会话派实际deepseek执行，期间无第二writer；退出后捕获原始final、产物hash、差异与终态。缺有效交付就未完成，不由Codex补源码/final。
4. 集成者在独占证据目录实跑原回归及新增诊断反例，保留失败与恢复、实际进程身份和输出。两独立CodeBuddy席审核全部两文件与原件；native监督核用户角色边界、原阻断处置、旧判据未变及证据准确性。测试绿不能替代原席复核。
5. 独立复核完成后才准备新准确接线版本。只有逐字节替换经审片段、配置/pin更新属于协调物化；若消费者接线需要任何执行逻辑修改，必须另经精确范围裁定并交执行者，不能扩本包两文件写集或由Codex临时修补。实际运行前重核consumer采用的新hash与必要无模型集成反例，再给准确行政运行准入。
6. 接线成功只证明这项行政诊断恢复；不倒签S3/S4、不修改S6原票、不假称产品W/R2已交付、整树已确认清空或B1可派。当前产品责任沿GOV-06及原13包继续。

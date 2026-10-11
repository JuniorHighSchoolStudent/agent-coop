# 开发治理修复当前状态

范围：本仓开发失效的产品修复；维护者：Codex集成者；状态：**修订下一轮方案，S1失败仍未关闭，尚未派发产品作者**。来源：[用户请求](request.md)及[全部问题产品落地要求](scope-amendment.md)。截至2026-10-11，本请求实际使用4次CodeBuddy、0次native；四次均已结束；用户已取消固定审核轮数，后继调用须按修正原因、准确候选及原独立门禁推进。

## 当前结论与下一动作

GOV-01–09及GOV-S0-I01均须经过产品实现、失败/恢复回归、本仓真实使用和独立关闭。当前只完成调查、实施候选和两轮实际设计审核；没有产品修复完成，不以文档、临时看护或尾部PASS代替交付。

- main保持`9a4855a39121f2483e1630082bc36533a2165a5e`。治理工作在`codex/governance-enforcement-20261011`；原用户工作树、`.workbuddy`及旧证据保留，本轮未合入main或push。
- 原冻结S1候选`dc37ae62a0aa8b40e0d881a364a6ddd190c0e146`留在独立送审树和Git历史；轮次与四项必修要求已于`9092a8b`提交，后继送审前仍在核准[实施合同](implementation-contract.md)、[运行时计划](runtime-integration-plan.md)、[分批派发计划](dispatch-sequence.md)：13包、4个完整接收批次，首批N1/A/R1/W四路，N2等待N1有效交付。五个首批作者树只完成隔离准备，没有作者运行。
- Codex负责调查、合同、证据、验证和集成；dispatcher_next唯一正式发包；实际CodeBuddy + deepseek-v4-pro实现/修复，CodeBuddy + GLM/Kimi独立交叉审核，native Kimi独立监督。默认执行容量4可配；Claude暂停。
- 下一动作是审阅[S1最小修订提案](s1-correction-proposal.md)，处理读取计划派生、会话声明、严格final及看护身份回归。用户最新指示已取消固定轮次，原追加2票问题不再待答复；[范围补充](scope-amendment.md)保留原话，[当前路线](../../../docs/roadmap.md)维护有效团队约束。旧52/54总次数不是新的隐藏上限；实际消耗保留，单次运行与资源约束继续执行。下一轮四项必达为漏读、无效审核输出、看护漏管及策略自读缺口；需要有效双席意见和native监督后才派作者。

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

本轮未改产品或测试，没有新产品测试结果。根独立复核16个调用原件hash及两份完整终态的严格JSON失败；本次用户纠正后的文档检查521条相对路径、62项设计验收编号无失败，Git空白检查通过。归档字节一致性和文档检查是行政核验，不能充当独立模型审核。当前完整raw仅本机留存；没有异机备份、生产live、OS定时器、远端上传或清理许可。

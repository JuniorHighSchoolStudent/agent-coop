# 开发治理修复当前状态

范围：本轮治理调查与修复；维护者：Codex集成者；状态：调查完成、候选设计待正式审核；来源：[用户请求](request.md)。

- 基线main9a4855a；新工作树D:/project/agent-coop-governance，分支codex/governance-enforcement-20261011。原用户工作树/.workbuddy及旧证据保留。
- 三个Codex子agent分别调查政策授权/监督输入、产品与人工门禁、实际派发入口；这些意见不是正式CodeBuddy审核票。
- GOV-01–05待fresh独立审核：C1必需作者final被C2例外放宽、监督漏查原条件/授权、关键变化监督迟到、各席必读缺口替代边界不明、状态把角色身份正确概括成流程合规。上一代码测试及main合入事实保留；其程序合规性处于本轮复核，不回写历史原票。
- 当前仅提案：三个独立写集小包；Codex不写产品/测试，CodeBuddy deepseek-v4-pro为作者；fresh GLM/Kimi交叉审核，fresh native监督。Claude暂停，容量默认4可配。
- 新批实际模型调用0；候选上限14 CodeBuddy/2 native，等待设计审核；无作者已运行，无新增接收/main/live许可。
- 文档准备检查：相对Markdown路径466项、design验收编号62项及diff空白检查通过；新引入锚点对应原提案的同名标题，未改HTML/SVG/既有标题。未改产品/测试，因此未重跑201项旧测试，也不将旧结果当本轮实现验证。
- 下一步：冻结[合同](contract.md)、[计划](plan.md)和[调查](investigation.md)，由dispatcher_next派fresh两席独立设计审核；再由fresh native核旧条件与新计划，未通过不派作者。

## 当前切片外仍须修复的产品问题

以下沿本请求留存，不因只读门禁完成而关闭；尚未批准实现或追加模型调用。

| finding | 现场与边界 | 承接责任与恢复条件 |
|---|---|---|
| GOV-06 | 旧开发wrapper的watchdog参数仅是记录，前次矩阵外部看护有61秒空档；不能宣称全程看护已实现 | dispatcher_next提出统一有界开发执行入口，CodeBuddy后继包实现；先解决现有runtime的sample marker/cwd合同与进程身份绑定，再经双席审核和监督 |
| GOV-07 | 现有sample native parser可接受早期final后仍有未完成工具的反例；本轮覆盖观察拒绝它不代表原parser已修复 | 运行时适配职责后继包；复用真实协议事件和反例，确认与本轮观察的共享边界后发包，避免复制两套解析权威 |
| GOV-08 | 人工调用者仍能绕过只读检查直接执行shell/git；当前依赖唯一发包人与集成者遵守入口 | Scheduler职责后继切片；必须让产品实际动作消费版本绑定的批准、资源和状态，完成拒绝与恢复验证后才可称强制流转 |

只读门禁、运行时解析、开发进程看护和Scheduler动作授权是不同完成项；各自需要代码、反例和实际使用证据。

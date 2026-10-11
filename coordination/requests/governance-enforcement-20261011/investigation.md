# 开发治理失效调查

范围：上一产品权限批次的作者交付、独立审核、监督和接收条件；维护者：Codex独立调查者，集成者维护当前请求入口；状态：待fresh双模型设计审核及fresh原生监督的调查原件，不是正式审核票或新的派发许可。调查基线为`9a4855a39121f2483e1630082bc36533a2165a5e`；来源为用户本次纠偏、仓内合同及下列原件。本文不改写历史票据、不否认已发生的Git合入，也不预判新审核结论。

## 调查方法与结论边界

只读核对AGENTS、roadmap、design、上一批C1/C2/最终监督、当前result和归档的实际读取记录。未调用外部模型，未重跑旧模型或产品矩阵，未修改产品/测试。下述行号绑定调查基线；文件后继变化以该commit的原文为准。

上一批并非没有审核：两组CodeBuddy和native Kimi实际运行，C2确实读取完整verify，产品矩阵有原生工具和字节证据。核心失效是：**必需作者交付条件未满足，随后被内容席降为可携带的例外；监督确认例外表述及结果，却没有核实放宽原条件的授权链。** 有不同会话、PASS原票和完整材料包，均不能单独证明依照原规则完成了授权。

此前独立调查主要核对状态与票据一致性，没有追查例外授权来源；这属于本次明确纠正的调查盲点，不能把此前未提异议当作例外批准。

## GOV-01：原交付条件被放宽，但未举证旧策略授权

**历史事实。** [C1 GLM原票](../isolated-workflow-20261010/review-product-permission-c1-glm.txt)第28行要求B补交有效完成票及作者软目标说明，第32行将该说明设为有条件接受的前提。[修复准入](../isolated-workflow-20261010/product-permission-repair-admission-c1.md)第14、26行承接该义务。B再次Max turns失败、无有效final后，[C2 GLM](../isolated-workflow-20261010/review-product-permission-c2-glm.txt)第17行将“作者交付阻断”与“内容接收”拆开；[C2 Kimi](../isolated-workflow-20261010/review-product-permission-c2-kimi.txt)第22行因预算和轮次约束提出一次性、绑定fe2e的流程例外。最终监督第19、33行认可该例外；[当前结果](../isolated-workflow-20261010/result.md)第7、11行记载其接收与合入。

**合同对照与判断。** [design](../../../docs/design.md)第735、737行要求超限转待owner，ReviewPolicy自身变化由旧授权策略审查。已见两席同意例外，但未见独立的旧策略授权来源、门禁变更审核或受权owner的具体裁定；“原审核者可关闭自己的finding”不自动包含“可免除已冻结的必需交付条件”。这是授权链缺证，不是根据结果反推代码错误。

**最小修订与反例。** 产品规则归design，人工执行规则归AGENTS；本切片直接不支持豁免。有效final缺失时，绿测试、预算耗尽、内容PASS、native PASS及“仅本次”均不能使accept通过。历史B27失败永久保留，后继合同不倒签旧接收。

## GOV-02：监督的例外核查没有覆盖原门禁与授权来源

**历史事实。** [最终监督调用](../isolated-workflow-20261010/supervision-product-permission-final-calls.json)第23行的实际prompt要求检查“例外是否充分明确且绑定本revision”。[输入索引](../isolated-workflow-20261010/supervision-product-permission-final-input-index.json)及[来源映射](../isolated-workflow-20261010/supervision-product-permission-final-source-map.json)列出的材料包含C2、两次失败、矩阵、当前结果和选定调用事实，但没有AGENTS、design、roadmap、C1原票或修复准入原文。最终14次Read详细核验了交付后的选定材料；允许复用早期计划上下文不能证明后来新增的C1条件已被原文核对。

**合同对照与判断。** design第344–346行要求监督检查正式判据是否放宽，并在关键判据变化时触发。监督确有工作，不能称其完全没检查；缺位的是“原条件→变化→批准权限”的独立对照。最终原票的认可不足以补足这条链。

**最小修订与反例。** design维护必读证据规则；每阶段policy固定旧条件及必读源，最新prompt只能增加关注项，不能删掉必需源。省略旧C1条件而提供新C2 PASS时，checker应报告missing prerequisite，不能以材料包读取完整代替合同完整。

## GOV-03：关键条件变化没有在依赖动作前完成监督处置

**历史事实。** [上一计划](../isolated-workflow-20261010/product-permission-plan-20261011.md)第36–39、51行固定计划监督与最终监督两次；C2新增例外后执行产品矩阵，最后才由native确认例外。[最终监督](../isolated-workflow-20261010/supervision-product-permission-final.txt)第19、27、33–35行将例外、预算终态与接收条件合并裁定。

**判断。** 不能由此要求常驻模型监督或每次编辑重审；问题是关键条件变化没有明确的依赖动作停止出口。额度不足本应暴露为等待，不能作为降低原验收条件的依据。

**最小修订与反例。** design规定条件变更使相关阶段票失效；AGENTS规定派发前检查。当前checker对policy/旧条件变化直接blocked，不自动启动额外审核或补调用。C2新增例外且只剩最终监督额度时，dispatch/accept都不能沿旧许可继续。

## GOV-04：读取记录没有转化为每个必需席的内容覆盖门禁

**历史事实。** 上一[result](../isolated-workflow-20261010/result.md)第22–24行及[矩阵读取勘误](../isolated-workflow-20261010/review-product-permission-matrix-factual-corrections.json)保留双席长行截断、部分原件缺读；[最终监督原票](../isolated-workflow-20261010/supervision-product-permission-final.txt)第27行用等价投影补读。现有机械coverage能够指出遗漏，实际没有按每席每条必需证据阻断接受。

**合同对照与判断。** design第733行要求“合同条目→主审/交叉席→证据→结论”，未检查和缺证据不能算通过。文件曾打开、Read数量、模型自报全文、另一席或监督补读，均不自动证明原必需席完成自己的义务。不能把该判断扩大为要求所有角色重复阅读全部文件，也不能据此声称旧矩阵数值错误。

**最小修订与反例。** 复用原请求索引固定每席required evidence；从原生成功Read返回的实际内容计算覆盖，支持已受审的值等价投影。某必需席漏一段、只有Grep或读取错误，即使其他席全部覆盖也不能通过该席。

## GOV-05：人工状态叙述未由确定性开发门禁支撑

**历史事实。** result第8行称“角色按设定执行”，同时第11行记录B门禁未满足但已接收。roadmap第13行明确当前仍是人工自举；[gates.py](../../../agent_coop/gates.py)第87–109行是固定样例的四会话/摘要/PASS检查，没有开发ReviewPolicy、逐席必读或例外授权逻辑。后者是实现缺失，不能描述为已自动强制。

**最小修订与反例。** 当前状态仍归原result/roadmap，不新建台账；新增只读检查结果由该入口引用。旧final后仍有未完成工具、原生result失败却exit0、伪造passed/full_coverage、作者替必需评审、必需角色能力unknown，均不得生成eligible。物理合入事实和对其治理充分性的重新调查须分别保留。

## 已检索实现与本次最小切片

- `agent_coop/adapters.py`已有`_events`及两类runtime解析；本次复用事件JSONL解码，不修完或替换原产品parser。新观察职责必须检测原生失败终态、未配对工具和旧final后活动，不能把旧parser输出当权威。
- `agent_coop/gates.py`负责固定样例接收；开发治理不混入其业务流程，也不创建第二个Store/Runner。
- `agent_coop/cli.py`已有单一命令入口；新命令在Store导入/构造前完成只读返回。
- 现有请求input-index、raw调用证据及读取coverage是输入来源；不新增任务/问题/PASS台账。现有仅摘要或删节原件无法证明新合同的条目须显式blocked/unknown，不补造历史raw。

候选接口与三包边界统一见[合同](contract.md)。本批设计应由fresh两组CodeBuddy独立审核；fresh native须直接核对原监督漏项、旧门禁与本候选，不能让旧监督PASS批准自身充分性。实际预算、发包身份、基线和下一步由本请求计划及当前结果维护，本文不再复制。

# 实现职责纠偏与交接

范围：本轮实施角色；维护者：Codex集成者；状态：按用户最新明确指令生效；来源：用户再次指出“Codex作为集成者、派发者；实现应派发给CodeBuddy + deepseek-v4-pro”。该指令覆盖G0原计划中把产品入口代码分给Codex的安排，不扩大功能、运行预算或清理范围。

## 事实与纠偏

Codex此前自行编写了agent_coop的CLI、sample、gates、checks、Web、verification及相应测试、CI和操作指南。这超出了用户设定的职责；它们仍是未交付草稿，尚未经过G1，也没有实跑证据。保留真实作者事实，不能在后续将这些原始内容改称CodeBuddy原创。

实际两路CodeBuddy + deepseek-v4-pro已派发，分别承担core与archive；截至本检查点处于测试先行阶段，不能把测试落盘或CLI退出描述为实现完成。核心测试中的JSONL fixture与真实协议不符，归档测试存在fixture遗漏，已由派发者退回同一CodeBuddy作者修正，Codex不代改代码。

现在起，所有产品实现、测试实现与代码修复均交实际CodeBuddy + deepseek-v4-pro。Codex只维护需求/计划/证据状态、派发、运行验证、组织独立评审、解决职责与接口分歧及执行受审集成，不直接补产品逻辑或修改测试来获得通过。

## 后继分工

- 核心作者：CodeBuddy实际session `agent-coop-core-20261010`，Store/Runner/runtime/adapters和对应测试；辅助Codex仅协调与验证。
- 归档作者：CodeBuddy实际session `agent-coop-isolated-archive-20261010`，paths/archive及对应测试；批准按路径/归档职责拆test_paths与test_archive；必要时cleanup作为归档组件内部职责拆分，既有API保持薄转发。辅助Codex不编码。
- 集成流程实现作者：待上述账号槽位释放后派发新的CodeBuddy + deepseek-v4-pro会话，接管Codex未交付草稿，完成接口对接、缺失功能、回归测试和实际修复；不得仅评审草稿就宣称自己实现交付，也不要求无目的重写已正确的代码。
- 独立审核仍由CodeBuddy glm-5.3与kimi-k3-2非作者会话承担；原生Kimi仍独立监督；Claude暂停。

共享CodeBuddy并发保持2，不在等待时偷偷启动第三调用；产品样例仍必须G1通过后才执行四模型有界流程。后续交付记录区分原始草稿作者、接管实现者、实际变更与验证结果。原G0功能合同仍有效，本职责纠偏作为后继解释随G1送审。

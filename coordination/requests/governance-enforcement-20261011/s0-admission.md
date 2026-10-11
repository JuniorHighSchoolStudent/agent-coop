# S0 只读设计审核准入

范围：本轮两次fresh CodeBuddy设计审核；维护者：Codex集成者，dispatcher_next唯一实际发包人；状态：已准只读审核，实际执行见result；来源：当前用户要求及main9a4855a的AGENTS/design/roadmap。新机器policy是待审核对象，不批准自身，也不提供作者或接收许可。

## 准确绑定

- 文档候选：`ee94914543e9248d17c9fde670869744173ea22a`。
- 只读工作树：`D:/project/agent-coop-governance-review-20261011`；原件目录：其`coordination/.runtime/governance-s0`。
- policy：`66ce0dd1dc0ec886bcdf0fec83366362f73c6add009f924b72de42660ae5cf35`。
- index：`49ab6976f5a59532fa5b91fda8fea99259f7f08ec41daeb21229b7c61a0f9c9c`。
- subject：`230daf0ea34035b49fa8409ebca3677b2635df09783b19c3a56a79ed719f4a4f`。
- required-reads：`2d45363ef6d9bd0eb6b95445b9be9feac93236ee3b1b9d1b834bdc2009326a6d`。
- GLM：`glm-5.3`，fresh session `agent-coop-governance-glm-s0-20261011-74a0a55a`，prompt SHA `7e42a8a36407e394133ca60b40fbcb948dbd693dead7f7e75e252b1db6814fa0`。
- Kimi：`kimi-k3-2`，fresh session `agent-coop-governance-kimi-s0-20261011-3faf149a`，prompt SHA `19a395c3ae7f040bdc8986a3adac8f86124788b42556d46fc6dac77068ae673f`。

## 准入依据及范围

根独立核27份artifact存在且字节摘要相符，重算subject、conditions、packages语义摘要并确认完整条件继承；这只证明原件自洽，不是设计已经通过。两席独立不得读取本轮他席新票；按照原规则审核新合同、机器声明、预算、三包可实现性及旧GOV失效链。每席最多一次调用、20turn、600秒，无静默回退或自动重试。实际启动才记调用消耗。

准备阶段已将policy由86,102字节/129条件收敛为36,841字节/12条件，每席33块实际Read；同角色单一读取条件关联多证据时必须全部满足。历史调查只在plan直接审核，accept递归重算原plan且直接核接收所需证据，不以plan票代替源码审核。

本版CLI静态核查支持同响应批量工具并行；num_turns记录历史条目数，不能直接当响应轮数。Read有单行2000字符截断；因此删除与本次profile能力无关的整串argv观察必读项，保留真实Read、终态和model/session证据。没有改变字段内容制造投影等价，没有减少作者final、两席独立和原始条件要求。实际工具结果仍须核范围和内容，预计可读不等于实际已读。

运维父进程须先进入看护并记真实ready，再启动既有wrapper，绑定实际PID及创建时间并守600秒deadline；仅watchdog参数或准备说明不算已经运行。该看护不是新产品启动器，也不声称全程文件监视。

旧`*.DRAFT.json`及`PREPARATION-DRAFT.json`保留为准备历史，不作为本次准入。任何一席没有有效结构化final或必需读取不完整，保持阻断；不能由根/另一席/native补签。作者开发须另待双席设计审核及fresh native计划监督通过。

# 产品权限 C1 finding 修复准入

范围：原双席对67a86ce的C1具名缺陷；维护者：Codex集成者、dispatcher_next唯一发包人；状态：准入两次有界finding修复，不是内容接收；来源：[GLM原票](review-product-permission-c1-glm.txt)、[Kimi原票](review-product-permission-c1-kimi.txt)。合同/计划仍为5f9d430字节，不改版本或新增接口。

## 双席意见承接

两席均CHANGES_REQUESTED，均明确允许A/B各一次同范围修复；B须基于冻结Max-turn现场启全新deepseek-v4-pro会话，不resume补签。原票判断有差异时采用符合冻结合同、限制更严格且未被另一席禁止的验收并集，再交原双席C2独立裁定：Kimi B15c要求canonical原始reparse先验，GLM认为下游已挡启动但未禁止同写集修复；GLM B22要求Kimi拒非空写集，Kimi认为sample足以承担但未禁止adapter诚实拒绝不可表达的写权限。根不代关finding，不把这些不同判断抹成一致。

## 修复包与准确范围

| 包 | 唯一允许写集 | 必须承接 |
|---|---|---|
| A/P6 | agent_coop/sample.py、tests/test_sample.py | GLM B21 A侧/B26及Kimi B14a–c：config/permissions schema严格整数拒bool/float；派发前重验完整角色工具集合、角色adapter及model约束；重算摘要后的非法语义在预留前拒绝，零计数/零invoke反例 |
| B/P2 | agent_coop/adapters.py、agent_coop/runtime.py、tests/test_runtime.py、tests/test_adapter_commands.py、tests/test_runtime_invoke.py | GLM B21 B侧/B22–25及Kimi B15a–e：permissions精确五键与严格整数；Kimi非空写集拒绝；canonical先原始reparse后resolve，复用既有守卫；env set内及跨inherit大小写变体拒绝、精确同名覆盖保留；修两红fixture且完整恢复父env；相应反例及有效final/软目标说明 |

按Kimi更窄的A写集限制，仅两文件；不为GLM允许四文件而扩写。两包无写交集，可并行，独立干净worktree、同一准确组合基线和冻结合同；两次均fresh会话、deepseek-v4-pro、20turn/600秒及原精确工具权限。不得shell/commit或改共享文档、合同、gates/Store/paths；可调用既有paths守卫，不复制另一个授权计算器。

测试修复不改变产品stdout和必需环境策略；CRLF可用作者选择的准确fixture/断言解决，但不得弱化原测试意图。父环境须恢复调用前状态，不能仅删除原已存在值。工具与adapter政策仍由sample持有，adapter的拒绝只限其协议可表达性，不把角色逻辑下沉。

根独立无模型复核另证True/1.0/2.0、增Task/缺Read/角色profile替换可逃过旧sample校验，使用Popen哨兵没有实际模型执行；用于定位和验收，不冒充正式原票。真实env测试充分性仍由C2核对；不得用测试数量变绿替代合同覆盖。

## 预算、交接与停止

C1后8/15 CodeBuddy、1/2 native；两修复实际启动后10/15，C2双调用后12/15，余一次产品矩阵与最多两次限定结果确认。无第三内容修复轮，无隐藏补调。若作者再失败如实保留未完成，不以exit0或根补写收尾。

作者须直接给真实变更/未验证项/内聚说明，不宣称没执行的测试通过。根核写集、局部验证、准确组合统一verify和迁移清单；新候选必须原双席C2内容批准才准产品矩阵。C1没有任何finding因本准入而关闭，也未授权live或新候选main接收。

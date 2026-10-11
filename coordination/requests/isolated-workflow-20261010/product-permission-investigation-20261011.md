# 产品权限与设计状态的并行调查

范围：f44d411受审实现及用户授权后main f0223b3；维护者：Codex集成者；状态：只读调查结论，非必需审核票；来源：独立Codex调查agent investigate_runtime、audit_design_state、专门发包人dispatcher_next。三方没有修改产品/测试或调用新模型。

| finding | 事实、接收owner与本批处置 |
|---|---|
| PP-01 | sample只在prompt声明feature.py，冻结profile无精确写集；P6按后继合同派生并绑定原config，不新建config.py/台账 |
| PP-02 | adapters对allow使用逗号单token并acceptEdits；P2改独立规则及dontAsk等明确参数，业务路径不入adapter |
| PP-03 / DS-05 | runtime Popen继承全环境，与design§6白名单合同不符；本合同选择实际白名单与四固定值，保持非模型run_bounded兼容，不掩盖差距 |
| PP-04 | test_runtime464行，新增测试可能越硬限；P2整体迁移职责类并删原定义，不复制第二套验证 |
| DS-01–03 | README、AGENTS、design、runtime-adapters仍有全局“初始化/无实现/无门禁”断言；按各owner修正事实，现状引用roadmap→result，云CI不冒称已运行 |
| DS-04 | result历史块有“当前未决项”标题易被检索误读；只改可维护历史导航标题，不改冻结原票 |
| DS-06 | design§7.4硬要求ABM selector、§7.5指定Claude安排替补；提交合同修订为项目原GateAdapter能力/具权限集成者，ABM示例和Claude暂停继续保留 |

config当前真实owner是sample→Store.config；Store已有config_digest和冻结更新限制，gates已有implementation_digest，paths.checked已有reparse边界。两功能包无需新框架；作者必须复用这些入口。dispatch实际仅由dispatcher_next批准后执行，根不可补写产品代码。

独立意见存在需正式裁定的差异：runtime调查认为冻结schema后A/B可并行，发包人指出原Kimi票明确A→B。计划按原顺序为默认，并把并行作为新S0显式申请；没有把助手建议当原票授权。原生Kimi仍独立计划/最终监督，双CodeBuddy原席互审完整合同与相同候选，不把三位Codex调查当正式交叉认证完成。

文档事实修正与DS-06合同改义共同送S0但分别标明：前者不扩实现成熟度，后者须原席与监督明确认可。旧scope proposal保持冻结历史，当前状态由result承接。历史WinError5未知与产品权限两个finding不混同，不提前关闭。

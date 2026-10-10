# 日志目录边界后继澄清

范围：隔离样例P2 Runtime与P6消费者之间的log_dir；维护者：接口集成者Codex；状态：双席首轮边界对齐支持，待作者实现及原席复审，非G1通过；来源：[GLM附录](review-g1-glm-boundary-b.txt)、[Kimi附录](review-g1-kimi-boundary-b.txt)。版本：isolated-log-directory/1，适用于34bce56b后的具名P2修复包。

本条补充[原接口](interfaces.md)未明确的日志子目录边界；原接口与[已冻结补充](interface-amendment.md)不改写。其他合同保持原有效版本，不另复制正文。

- `cwd`为本次样例隔离根；`log_dir`允许位于其`.runtime`本身或后代，包括既有消费者的`.runtime/verification`、`.runtime/<role>`和`.runtime/logs`。不允许根内任意目录。
- 路径校验复用`paths.checked(cwd, '.runtime')`及既有路径owner；拒绝cwd外、`.runtime`外、链接/junction/reparse逃逸，不能先resolve再抹去链接证据，不能复制第二套校验器。
- P2为唯一实现owner；本包写集为`agent_coop/runtime.py`与`tests/test_runtime.py`。P6既有消费方不修改。规模修复与目录修复在同一个P2包、同一工作树由一个writer承接，禁止并发修改同一文件。
- P2规模候选`8183c5d1fddba73ff1ae6f9e978f6dde0acc33e7`已冻结，仅是前置候选；后续调用从该版本继续，不将局部测试或commit当作原finding已关闭。
- 验收保留运行时25项回归与硬规模门禁，新增根内但`.runtime`外及junction逃逸拒绝覆盖；组合检查`test_verifier_checks_boundary_hold_and_negative_retention`、`test_pause_resume_archive_backup_and_cleanup_share_one_state`和`test_review_wrong_verdict_saves_receipt_and_keeps_budget`。缺陷仍由原两席在同一组合候选第二轮逐项关闭。

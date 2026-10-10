# G0 接口澄清

范围/维护者：Codex对[原接口](interfaces.md)的后继澄清；状态：第二轮候选；来源：原候选856614a的两席评审与Codex辅助测试审查。原件保留，以下对应条目以本澄清为准。

1. Store的每次更新须在短事务中读最新状态、合并指定字段；finish不能用handler的旧快照覆盖并发pause、hold或calls_used。initialize拒绝已有状态，不能重置预算。仅可信CLI可设置hold，模型不能设置/解除；本轮不演示hold写入口，测试通过Store注入hold验证阻断。
2. STATUS和state.json分别原子替换，不能保证崩溃瞬间两个文件同revision。消费者检测revision或读SQLite，遇不一致显示publication_pending；publish持独立发布锁，按数据库最高revision重建两份投影且不得回退。pause写同一Store事务并尝试publish，不争用整轮runner锁。事件冲突阻断，重复相同事件幂等。
3. runtime回执另含requested_session_id；session_id始终是可信CLI事件中的实际身份。CodeBuddy必须与请求严格相等；原生Kimi必须取session.resume_hint，缺失阻断，不假定它等于请求编号。四席独立性按实际身份核验。
4. 清理的now_epoch执行时新采集，不参与计划稳定字段相等比较；config/policy/subject/terminal等稳定字段必须相等。计划持久化hash、source内容、副本读回与hold均重核对。
5. 归档/备份回执补齐本样例政策id/revision/digest、验证者`deterministic-validator-v1`、核验UTC时间、权限级别`local_user`、未决义务引用（通过门禁时显式空列表）及源/目标逐文件大小hash。保持本机用户权限，不宣称实现生产ACL管理或异机冗余；完整生产归档合同仍属后继出口。
6. 原计划表内规模数字为送审时点AGENTS的冻结快照，规则唯一owner仍为AGENTS；“P1限定只读/模拟验证”仅是本样例离线阶段，非完整产品P1已交付。复用裁定仍待G0监督接收。

意见处置：g0-kimi-B1由roadmap当前依赖段直接修正，待原席复核；g0-glm-A1–A5由上列澄清承接，待复审。辅助测试审查不是正式审核票。scope仍为隔离样例、不启用OS定时器；没有增加删除对象、调用预算或平台能力声明。

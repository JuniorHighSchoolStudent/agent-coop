# 归档实现三阶段证据

范围：隔离样例 paths/archive/cleanup 的首稿与回归验证。维护：Codex 辅助派发者；源码与测试作者均为实际 CodeBuddy `deepseek-v4-pro`。状态：首稿未接收；以下为冻结检查点证据，当前任务权威仍在本请求 result。来源：真实 CLI 最终文本、调用元数据与确定性测试。

## 作者与交付原件

同一实际会话 `agent-coop-isolated-archive-20261010` 顺序执行三次调用，没有同会话并发、模型回退或 Codex 代写源码。三次进程退出均为0，result.is_error=false。原始流保留宿主临时目录，不提交完整会话；[元数据](implementation-archive-calls.json) 保存实际模型、session、时间、流SHA256与工具错误数。

- [测试阶段原件](implementation-archive-tests-r1.txt)：仅测试与空接口；最初测试超过软目标，后续按路径/归档责任拆分。
- [初始实现原件](implementation-archive-impl-r1.txt)：paths、archive、cleanup 与路径/归档测试。实现阶段两次工具错误分别为 Store 尚未落盘而 Read 不存在，以及 Write 前未 Read；均未放宽权限，通过后续正常读取继续。
- [回归测试原件](implementation-archive-regression-r1.txt)：仅补边界反例，没有修改产品实现。

调用参数为 `--model deepseek-v4-pro --tools Read,Glob,Grep,Write,Edit --allowedTools Read,Glob,Grep,Write,Edit --permission-mode acceptEdits --strict-mcp-config --mcp-config {mcpServers:{}} --max-turns 20 --output-format stream-json --verbose`。实际 init.tools 仍显示全工具清单，已报告集成者；不能据此宣称工具强制隔离或OS沙箱已验证。num_turns 为CLI输出原值，不将其误解为max-turns硬计数证据。

## 实际测试顺序

1. [首次RED](implementation-archive-initial-red.txt)：三个 paths 行为断言失败，分别为创建返回None、未拒绝非空目录、摘要返回None；不是ImportError假失败。
2. [首稿测试](implementation-archive-initial-suite.txt)：23 tests，21通过、2因Windows无符号链接创建权限而skip；真实 junction 用例通过。Store已可用，移除了整类缺依赖skip。
3. [回归RED](implementation-archive-regression-red.txt)：39 tests、18 failures、2 symlink权限skip，无error；证实首稿仍不可接收。原作者在首稿收尾已自行修正“源变化时先覆写后比较”，新增旧副本不变断言首次green，如实保留。

## 分诊与交接

| 稳定ID | P3：路径/归档/备份 | P4：清理 |
|---|---|---|
| precheck-archive-01 | 已有目标损坏时幂等返回未读回；无receipt残留目标会被覆写。原“源变化覆写”已由作者在首稿自行修正 | 无 |
| precheck-archive-02 | create_root、checked与write_json的祖先junction未拒绝；归档/备份目标未走路径守卫，真实junction可外写 | manifest目标父路径junction未拒绝 |
| precheck-archive-03 | 为清理提供已校验不可变副本 | 重算计划可改为源码source；只比files忽略完整receipt/subject；生成计划未核验全部副本；第二次authorize后变化的source仍会被删除 |

现有回归用例全部由实际CodeBuddy写入。P3需要4个paths反例与5个archive/backup反例；P4涉及9个failure（含subTest）。回归阶段 test_archive 为465行，未超硬上限但混合职责，需实际作者拆 test_cleanup 并保留全部反例，不能以删测试或压行通过。

所有删除、外写反例仅在 unittest 本次 TemporaryDirectory 内生成的无敏感样例执行；junction清理只移除链接自身。未清理业务项目、旧日志、SQLite、用户数据，未实跑模型工作流，未发布或合入。独立G1审核仍待后继完成。

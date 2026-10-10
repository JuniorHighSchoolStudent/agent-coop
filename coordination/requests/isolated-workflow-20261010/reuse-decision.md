# P0：隔离样例的复用裁定候选

状态：待独立审核；2026-10-10。用户明确选择“先用隔离样例跑通归档、备份、清理及多 agent 闭环”。不授权现有项目日志清理、异机上传或无人值守生产任务。基线 main 6d99eee。

## 固定来源与判断

| 候选与许可证 | 核验机制与缺口 | 裁定 |
|---|---|---|
| [OMA be0bff0](https://github.com/first-fluke/oh-my-agent/tree/be0bff0f32dafce93699dc5e34feb2a2585fccf8)，MIT | [runner](https://github.com/first-fluke/oh-my-agent/blob/be0bff0f32dafce93699dc5e34feb2a2585fccf8/cli/commands/schedule/runner.ts) 的随机运行标记不构成同任务排他 claim，每轮读取可变 manifest/prompt；[Windows adapter](https://github.com/first-fluke/oh-my-agent/blob/be0bff0f32dafce93699dc5e34feb2a2585fccf8/cli/io/schedule/adapters/schtasks.ts) 查询/删除错误可被空结果/no-op隐藏。[memory outbox](https://github.com/first-fluke/oh-my-agent/blob/be0bff0f32dafce93699dc5e34feb2a2585fccf8/cli/state/memory-outbox.ts) 确有持久投递/重放，但 owner 是 memory delivery；[backup](https://github.com/first-fluke/oh-my-agent/blob/be0bff0f32dafce93699dc5e34feb2a2585fccf8/cli/io/backup.ts) 是迁移快照按 mtime 清理，不是审核证据保留链 | OS定时适配保留为后继候选；不直接把该 runner 当唯一语义 Scheduler，也不复制其 memory outbox。CodeBuddy 任意CLI注册能力仍 unknown，不因预置列表缺名字便断言无法扩展 |
| [Symphony be10a1b](https://github.com/openai/symphony/tree/be10a1b79df723d6d7612b5651c8522704dafb2e)，Apache-2.0 | [SPEC](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/SPEC.md) 与 [app_server](https://github.com/openai/symphony/blob/be10a1b79df723d6d7612b5651c8522704dafb2e/elixir/lib/symphony_elixir/codex/app_server.ex) 为 bash/Codex app-server 协议；内存重试/会话重启不持久恢复，before_remove钩子失败仍继续删除 | 借鉴单写/先对账，不直接采用不匹配的运行时/清理语义；不声称Windows绝对不可能运行 |
| [DSH d743267](https://github.com/deepseek-ai/deepseek-harness/tree/d743267388641bc76f17c45ce8b4c231aed1d32c)，MIT | [subagent](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/subsystems/subagent.md) 有 provider/ACP 接缝，但 external 是一次执行、不接受follow-up；[experimental teams](https://github.com/deepseek-ai/deepseek-harness/blob/d743267388641bc76f17c45ce8b4c231aed1d32c/docs/subsystems/agent-team.md) 明确新消息无outbox/重送去重，task CAS revision不等于Git候选审核版本 | 后继 RuntimeAdapter 候选，不作为此次唯一Scheduler；不迁移用户全部宿主/账号 |
| 既有项目 ACP 可复用层（本机HEAD db382c9，未复制代码） | 已检查 core_modules/acp_agents 的公开接口、engines/client/roles 及原计划：Python ACP SDK依赖、明确只读/ctx-gated边界、固定planner/coder/reviewer接口；尚未提取为本仓可固定的独立发行包 | 保持原owner，不复制八模块形成双维护，不依赖业务项目安装路径。未来按原项目授权提取或采用上游ACP客户端；本次只封装已验证的headless JSONL入口，不重写ACP |

以上为固定源码/文档静态核验，未安装和运行三个上游；不能推导其全仓不存在其他gate或归档能力。OMA缓存为 no-checkout Git对象，源码通过 git show 读取，不冒充已展开/运行。

## 选定底座及最小新增责任

选定候选：Python 3.12+ 标准库 + SQLite，唯一小型 coordinator 持有本样例状态；使用 [sqlite3](https://docs.python.org/3.12/library/sqlite3.html) 的短事务/参数绑定，[subprocess](https://docs.python.org/3.12/library/subprocess.html) 的结构化 argv，无 shell 字符串，复用 hashlib/json/pathlib/unittest/http.server，不引入外部包。现机 Python 3.12.14；不复制任何上游源码，因此本轮无引入其许可证代码义务，也不替整个本仓选择发布许可证。

只新增缺失的候选/独立门禁、持久检查点与证据清理边界；既有临时 CLI 收据解析经验收敛为 RuntimeAdapter，既有临时检查收敛为单一 verify 命令。禁止另建第二定时器/后台任务权威。首次仅明确启动的有界 run/step，空闲不循环调用模型。

## Runtime 能力矩阵

| runtime | 本机证据 | 本轮准入 |
|---|---|---|
| CodeBuddy 2.164.0 | 当前help/版本、前几轮真实 deepseek-v4-pro/glm-5.3/kimi-k3-2 会话及JSONL，工具限制/模型/session配置可见；max-turns真实硬计数未证 | 推荐实现与双席审核；本runner另实施墙钟/总调用次数/输出大小界限，无fallback |
| Kimi Code 0.43.0 | 当前help/版本、原生只读agent-file与最终assistant/meta resume_hint真实收据；实际模型未暴露 | 独立监督；模型unknown，不伪装指定CodeBuddy Kimi |
| Codex Desktop/CLI | 当前集成者、现机入口可发现；未准入本runner自动启动 | 人工派发/接收与集成；sample runner不自行启动Codex |
| Claude Code | 用户因额度暂停 | 不调用、不探测账户、不自动恢复 |
| OpenCode / ACP通用插件 | 本轮未做本机运行探针 | unknown/未实现，保持扩展合同，不安装或假支持 |

headless工具参数是声明/限制，不是Windows OS安全沙箱；独立目录隔离和受控样例不能冒充对恶意进程的权限隔离。运行时 entry 与配置摘要在初始化时固定，现有私有账户只由宿主CLI自行使用，不读取/复制凭据文件。

需双席审核与原生Kimi监督接收本裁定及 [实施计划](implementation-plan.md) 后才写产品代码。完整产品P0/P1/P2/P3仍各有剩余出口；此受控纵向样例不宣称所有产品切片完成。

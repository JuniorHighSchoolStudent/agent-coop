# 隔离样例接口补充

范围：本轮固定纵向样例的模块协作协议；维护者：Codex集成者；状态：G0候选，须随实施计划审核；来源：[计划](implementation-plan.md)。所有时间为UTC epoch秒，摘要为SHA256，JSON写入使用临时文件加原子替换。此处描述拟实现接口，不是运行证据。

## 持久状态与驱动

`Store(root)` 使用 `.runtime/state.sqlite`，唯一权威是一行JSON状态与同事务事件表（待投影事件即outbox，不另建台账）。公开接口：`initialize(config, steps)`、`read()`、`update(**changes)`、`begin(step)`、`finish(step, updates)`、`fail(step, message)`、`pause()`、`resume()`、`publish()`。每次变更增加revision、写完整事件快照；publish按revision发布不可变事件与STATUS/state.json，同revision且可重放，读服务直接读SQLite。update不得让模型调用，所有写者为本进程可信控制代码。

初始化状态字段：`schema=1, revision, config, config_digest, phase='ready', paused=False, current_step=None, steps=[{name,status:'pending'}], data={}, error=None, calls_used=0`。步骤状态仅pending/running/done/failed，phase为ready/running/paused/blocked/complete/reconciliation_required。`finish`将updates合入data。pause设置持久请求，仅在当前动作交付后阻止下一步；resume只解除正常pause，不解除failed或不明running。

`Runner(root, handlers).run(max_steps=None)` 是唯一驱动，handlers映射固定步骤名到`handler(state)->dict`。runner取得OS进程级非阻塞文件锁（Windows msvcrt / POSIX flock），整轮持有，SQLite只用短事务，允许另一CLI写pause。启动发现running先置reconciliation_required，不重复调用。每步begin持久化后才执行handler；完成后finish；异常fail且不自动重试。已done跳过；max_steps正常返回，便于显式pause/resume演示。handler可调用同一Store更新调用预算，但不能改步骤或自行派发子workflow。状态通过JSON快照交接，不共享可变dict。

## 运行时与身份

`runtime.invoke(profile, prompt, cwd, log_dir, session_id) -> receipt`。profile字段：`adapter`（codebuddy/kimi）、`executable`（node绝对路径）、`entry`（JS绝对路径）、`executable_sha256`、`entry_sha256`、`model`（原生Kimi显式null）、`tools`、`timeout_seconds`、`output_limit_bytes`、`max_turns`、`agent_file`（Kimi）、`agent_file_sha256`。所有输入初始化后固化，invoke重验文件摘要；结构化argv、shell=False；cwd严格隔离根。超时/输出超限/非零退出/协议错误抛异常并保留有界日志，终止仅本次创建且仍存活的进程树；不得根据历史PID杀进程。

`adapters.command(profile,prompt,session_id)->list[str]`构造节点参数；`adapters.parse(profile,stdout,session_id)->dict`从完整JSONL取result（不可把hook最后一行当结果），验证CodeBuddy init实际model/session与请求一致且result非error；Kimi收集最终assistant纯文本与实际resume_hint，model保持unknown。receipt字段：`adapter, requested_model, actual_model, session_id, result`（最终纯文本必须可json.loads的对象）、`raw_text`（原文）、`exit_code=0`；runtime补wall_seconds和流文件hash。result只是交付内容，不决定状态成功。无隐式模型回退。独立性由可信runtime返回session检验，不采信正文actor。

## 路径、归档、备份与清理

`paths.create_root(path)->Path`拒绝非空目录，写`.agent-coop-sample`标识和`.runtime/workspace/evidence/archives/backups/scratch`目录；`paths.checked(root,relative)->Path`拒绝绝对路径、空/点/..、符号链接、Windows junction/reparse point及逃逸，检查root标识；`paths.digest(path)->str`；`paths.write_json(path,value)`原子写入。隔离根不允许多用户恶意写入；本轮不是对恶意本机账户的文件系统沙箱，运行锁只约束本工具。

`archive.create_archive(root, entries, subject_digest)->dict`返回并保存`evidence/archive.json`：白名单entries的源路径、归档路径、字节数与hash，subject_digest；目标`archives/<subject_digest>/`。归档复制后逐文件读回，并在独立临时恢复目录验证后清除自己的恢复副本。拒绝链接/重复/敏感运行数据库目录。`archive.create_backup(root, archive_receipt)->dict`返回并保存`evidence/backup.json`，目标`backups/<subject_digest>/`，逐文件独立复制和恢复验证，明确`scope='local_only'`。重入仅在完全相同内容时接受，不覆盖有差异的证据。

`archive.plan_cleanup(root, archive_receipt, backup_receipt, authority)->dict`只允许固定`scratch/fixture.log`，生成并保存`evidence/cleanup-plan.json`。authority由可信sample从SQLite和证据核验得到：`accepted=True, subject_digest, config_digest, policy_digest, hold=False, terminal_epoch, retention_seconds=0, now_epoch`，拒绝缺字段/hold/未到期/非本样例policy。计划固定源、archive/backup清单及hash、authority稳定字段与plan_digest（不含自身）。`archive.apply_cleanup(root, plan, authorize)->dict`的authorize为可信回调，执行前重新读权威与hold，重核对稳定字段、到期、源hash及archive/backup全部清单和读回。只删除固定scratch对象，不删SQLite、outbox、源码或审查证据；清理意图先落盘，逐对象结果保留，失败不得记成成功。原件变更、链接或缺件均阻断。返回并保存`evidence/cleanup.json`。传入未经持久化的计划或被篡改的计划不得执行。

## 样例组合与验证

Codex维护`sample.initialize(path, profiles)`与`sample.handlers(root)`，CLI只调用这些入口和Store/Runner；各实现者不在core复制样例逻辑。固定步骤：implement → verify → review_a → review_b → supervise → accept → archive → backup → cleanup_plan → cleanup。steps由代码固定，不从模型生成。

implement仅产生workspace/feature.py；后续subject_digest包含该源码hash、固定验证器版本及config_digest。verify以超时子进程执行可信断言，拒绝缺函数/语义失败，保存证据。review/supervise提示携带相同subject_digest，要求JSON对象`{subject_digest, verdict:'PASS'|'CHANGES_REQUESTED', blocking:[], summary}`；没有准确digest/PASS/空blocking则阻断。reviewer只读源码与验证证据，各自看不到另一席意见（仅提示输入；本轮非OS强隔离）；监督读取全部原件。accept重验源码、验证和全部三票，session各不相同且与实现者不同。模型调用先持久增加calls_used，上限4，无自动重试。

archive只收源码、验证证据、三个runtime回执（保存实际final文本和身份，不收完整CLI流）、accept与无敏感scratch fixture。cleanup每次从Store配置、精确源码及全部审核/验证原件重建authority；hold保存在同一Store.data内，不能由模型输出解除。demo固定policy字段`id='isolated-sample',revision=1,retention_seconds=0,targets=['scratch/fixture.log'],scope='local_only'`并纳入config_digest。实跑输出目录位于仓外且不自动加入Git。

离线测试用自定义handlers/假子进程验证状态机、协议、失败与恢复，不提供可冒充live的fake命令。`python -m agent_coop verify`运行unittest、源码规模检查、仓内文档相对路径/变更检查；CI消费同一命令。Web只监听127.0.0.1，GET读SQLite、禁止缓存，无写API；CLI承担本轮启停/暂停/续作，完整前端交互仍是后续切片。

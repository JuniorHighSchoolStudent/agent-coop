# 隔离样例自动流转实施计划

用户范围：仅隔离样例；本机副本 `local_only`；CodeBuddy 实现+评审、原生Kimi监督、Codex派发与集成，Claude暂停。基线6d99eee。状态：待计划审核。本计划是现有路线的受控纵向样例，依次验证只读/模拟层，再开放真实受控调用；不宣称全量P1/P2/P3交付，也不启用OS定时任务。

## 目标与边界

一条命令驱动持久链：实现一个隔离的小功能 → 确定性验证 → 两个独立评审 → Kimi监督 → 精确候选门禁 → 归档 → 本机副本读回 → dry-run清理计划 → 仅清理本次样例生成的scratch文件。CLI可暂停/续作，已完成步骤不重跑；提供只读本地Web状态页。未决/in-flight崩溃必须阻断对账，不能盲目重派。功能源码、原始评审和数据库不清理。

本轮 sample 初始化固定模板，非任意命令/任意workflow平台；配置采用规范化JSON快照（不是已实现的生产team.yaml加载器），配置/策略/可执行入口/输入摘要绑定run。角色和模型从样例profile读取，core不能按品牌判通过。Windows运行、单runner串行（账号并发不超过2），生命周期控制通过同一SQLite；独立上下文/session是review的必要条件。不同宿主均不能凭自报actor或exit0通过。

样例功能：`workspace/feature.py` 的纯函数 `due_for_review(terminal_epoch, retention_seconds, now_epoch, hold=False)`。满足hold返回False、now>=terminal+retention才True、负保留期抛ValueError。固定验证器在本仓代码中，执行前后核验输入与产物，不允许agent改验证器。受控代码用有时限子进程验证；这里不是恶意代码执行沙箱。

## 文件与接口（唯一维护入口）

| owner | 文件 | 接口/职责 |
|---|---|---|
| CodeBuddy核心实现 | `agent_coop/store.py`、`runner.py` | `Store(root)` 持久状态/短事务事件+outbox、投影同revision；`Runner(root).run(max_steps=...)` 唯一有界驱动；每个步骤先persist running再执行，再commit证据。初始化、status、pause/resume供CLI调用，暂停只阻止新派发，不谎称中止在途 |
| CodeBuddy运行时实现（与核心同一作者） | `agent_coop/runtime.py`、`adapters.py` | `invoke(profile,prompt,cwd,log_dir,session_id)` 结构化argv、墙钟/输出/调用预算、仅本进程树终止；CodeBuddy/Kimi格式适配只在adapter。解析实际init.model/session或native resume_hint，未知保持可见；正文必须是明确JSON交付/评审协议，否则阻断，不猜PASS |
| CodeBuddy存储实现（独立写路径） | `agent_coop/paths.py`、`archive.py` | `create_root(path)` 拒绝已有非空目录，生成marker及runtime/workspace/evidence/archives/backups/scratch；`checked(root,relative)` 防绝对路径/.. /symlink/junction。archive/backup清单、SHA256、读回/恢复验证；cleanup plan/apply仅scratch清单，计划及回执落盘，重查gate/hold/摘要/备份，部分失败可见 |
| Codex集成 | `agent_coop/__init__.py`、`__main__.py`、`cli.py`、`web.py`、`checks.py`、`sample.py` | CLI init/run/status/pause/resume/serve/verify；固定样例模板与验证器；只读127.0.0.1 Web呈现同一state revision；统一静态/测试入口及CI，文档操作入口。接口和实际测试不匹配时由集成者统一收敛，不保留重复功能 |
| 各实现者 | `tests/test_store.py`、`test_runner.py`、`test_runtime.py`、`test_archive.py`、`test_cli.py` | unittest：先写有意义失败用例，观察red后实现，按组件分离，不靠mock自报成功。源码≤300目标/>500阻断、函数≤40目标/>80阻断，超过软目标解释内聚性 |

实施前双方确认准确共享接口并写在本请求的接口补充中；不让两个作者写同一文件。写产品代码前先通过本计划门禁。无需引入包管理依赖；`python -m agent_coop verify` 为本地与CI唯一验证命令。

## 执行步骤与审核门禁

1. **G0 选型/计划门禁**：CodeBuddy/glm与kimi新只读会话按下表审核，原生Kimi监督；Codex据原件接收。两席非作者，监督不兼任。G0之前不写产品源码。
2. **P1限定只读/模拟验证**：按模块写失败测试→Codex运行确认→CodeBuddy实现→通过离线测试；init/status/dry-run/Web不启动真实模型，fake adapter仅测试用且页面/收据明确fake。运行时schema/身份/权限未知必须报错，测试不能伪装真实成功。
3. **G1 实现候选门禁**：冻结代码/样例/配置协议，双席CodeBuddy审实现与测试，Kimi监督；不合入未经复核的更改。每个门禁最多两轮修订/复审；CodeBuddy并发2、单调用max-turns20，Kimi并发1/十分钟人工看护。超限保留owner，不无限互审。
4. **有界实跑**：仅在G1通过后，Codex创建本次唯一隔离目录，初始化固定四次模型调用预算（executor+2reviewer+supervisor），全部600秒/调用、8MiB输出上限，工具writer仅Read/Glob/Grep/Write/Edit；reviewer仅Read/Glob/Grep，Kimi只读agent-file；禁fallback。由新runner实际派发四个独立会话，合法JSON引用精确subject_digest、PASS且blocking为空才推进。失败即blocked，不自动重试消耗预算。
5. **归档/本机备份/样例清理**：清单含产物、验证、三份审核原件及本轮生成的无敏感scratch fixture；先copy→manifest核对→目标读回/隔离恢复→本机副本核验，backup状态local_only。只对 `scratch/fixture.log` 用显式sample policy（retention=0，用户选定隔离演示）生成计划并执行；不能将0推广到生产30天策略，不能删源码/evidence/SQLite/CLI全量流/旧项目数据。任何hold、候选变化、缺票、错误摘要都阻断清理。
6. **暂停/续作与收尾**：实跑用max_steps在阶段边界暂停一次，再恢复，核对已完成阶段调用次数不增长；进程中途崩溃情形用离线测试，未知running保持reconciliation_required，不承诺已实现原会话跨崩溃续接。归档最终证据、README更新实际能力、roadmap分清限定样例完成与剩余产品出口，本地集成；不push/上传。

## 共享验收矩阵

| ID | 拒绝条件 / 通过证据 |
|---|---|
| W1 | P0复用/许可证/本机能力有固定证据；不复制业务ACP或同时启用上游scheduler；unknown保留 |
| W2 | SQLite持久状态与发布事件关联，同revision投影；双runner互斥、重复run不重复派发；in-flight不明阻断对账 |
| W3 | 角色/模型/profile固定，四次预算、工具/墙钟/输出边界；exit0/正文PASS/自报actor不足以通过；两个reviewer及supervisor不同session且非作者 |
| W4 | 暂停持久，续作跳过已完成；只读Web与CLI一致，无暗自启用定时任务；fake与live明确 |
| W5 | 精确subject digest绑定实现、验证、两票、监督；改候选/缺件/未决/异常输出不通过 |
| W6 | 归档和backup逐文件hash读回，local_only不冒充异机；损坏/恢复失败阻断删除 |
| W7 | 清理只限本次scratch fixture，策略/manifest/hold/路径/摘要/授权重查，部分失败回执；链接/junction/并发变更/数据库不可清理 |
| W8 | 有失败测试和统一验证命令/CI，结构/规模合规；真实四CLI回执+样例验证+归档副本+清理回执，当前状态准确 |

G0对W2–W8审核的是可执行计划及边界，不是假报实现通过。G1需实际代码证据，实跑阶段另外出具live结果；三者分开。

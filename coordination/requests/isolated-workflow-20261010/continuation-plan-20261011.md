# 隔离样例后继调查与分包计划

范围：未关闭的G1缺陷及作者权限前置；维护：Codex集成者，专门发包人dispatcher_next负责实际派发；状态：待独立审核，不是作者准入；来源：2026-10-11用户“先使用多agent协作功能调查实施问题然后继续分包开发”、[当前入口](result.md)、[GLM R2](review-g1-glm-r2.txt)、[Kimi R2](review-g1-kimi-r2.txt)、[监督](supervision-g1-r2.txt)。

目标：查明可复现问题，先验证写入权限，再把已获准范围并行交给真实CodeBuddy + deepseek-v4-pro，实现后回到原席逐项复审。技术栈仍为Python 3.12标准库、SQLite及现有CLI；不重新选底座或增加调度器。

基线：feature `b45cc17481f52a1eba0f946128360cf1c8a3899c`，产品内容与已审`2e9f192c8127956f09c619ff640d763b62369e30`相同。原始工作树及已有worktree、未跟踪目录保留。新用户授权启动本后继有界批次，不改写旧R2停止结论。

## 责任与依赖

- Codex调查助手只读调查、复现、报告；Codex根只维护文档/证据、验证及受审集成，不编写产品或测试修复。
- dispatcher_next是唯一正式发包人。真实作者为CodeBuddy + deepseek-v4-pro；独立原席仍为CodeBuddy glm-5.3、kimi-k3-2；原生Kimi监督不代替两席。
- 按既有设计默认4个CodeBuddy调用并行，用户可配，审核与实现共享账号额度。按就绪包数启动，不为凑4路编造任务。当前Codex助手创建受工具thread limit限制，与CodeBuddy配置容量分开记录。
- 前置顺序：只读调查 → 双席审核权限profile/探针/分包合同 → 单次隔离探针 → 双席核对探针、原生监督计划 → 独立工作树并行作者 → 冻结组合候选/统一验证 → 原席复审 → 原生监督 → 接收判断。

## S0/S1 权限准入

现有TEMP wrapper的Writer分支仍是acceptEdits加泛化Write/Edit，禁止用于新产品作者。沿现有wrapper维护显式profile，不复制调度器。准确argv、环境、目标和哈希由发包人在[派发提案](continuation-dispatch-proposal-20261011.md)中具名冻结，随本计划送审。

候选profile：dontAsk、Read/Glob/Grep/Write/Edit工具集合、Write/Edit仅逐绝对文件allow、严格空MCP、setting-sources none。仅对子进程设置禁用auto-memory/extraction环境；探针另用no-session-persistence，不改变需续接的原审核会话。无自动provider/权限回退。dontAsk仍允许安全只读，不声称读路径沙箱或OS隔离；宿主自身cache/session及hooks/plugin边界另列观察范围。

隔离探针仅在全新TEMP fixture执行：允许文件的Write/Edit正例；同cwd未授权文件、相似文件名前缀、兄弟目录、假memory目录的Write/Edit负例。所有负例目标均为无敏感数据的fixture，禁止触碰真实宿主记忆。检查实际tool_use/tool_result及前后字节摘要；未调用、正文模拟工具或作者自报均不算能力通过。Shell缺少可调用接口时记录未测/不支持，由审核明确能否满足本次限定profile，不能无限试探。是否覆盖junction由原席明确；未覆盖时不得宣称验证过，作者目标/祖先须先拒绝reparse point。

任一负例写成功、正例无效、模型/session不符、输入漂移或超时均停止，保留fixture证据、不扩权、不自动重试。探针不具有产品写权。所有后继产品作者使用经验证且绑定版本的profile。

## 分包候选与唯一写集

| 包 | 原finding及依据 | 唯一拟写集 | 验收与依赖 |
|---|---|---|---|
| R-log 验证日志调用隔离 | GLM B13/B02、Kimi B06；每次validate_feature固定目录与runtime拒覆盖冲突 | agent_coop/checks.py、tests/test_gates.py | checks作为调用者分配.runtime内每次唯一日志子目录；复用paths.checked和runtime，不放宽拒覆盖。失败→成功、成功→成功、失败→失败均可重入；同时调用不得共享目录；历史stdout/stderr摘要不变，各次实际输出可定位；先批准本段接口后再实现 |
| R-junction 清理生命周期 | GLM B14/B02、Kimi B06；断言返回后tearDown已删junction，addCleanup再删报WinError3 | tests/test_runtime.py | 修正单一清理顺序，不跳过断言、不递归删除链接目标；拒绝逃逸成立且cleanup无错误，已有runtime回归不退化 |
| R-publication 有界诊断 | GLM B11、Kimi B09；历史WinError5根因仍未知 | 仅独立TEMP诊断脚本及fixture，具体文件由发包人绑定；产品Store/Runner不改 | 实际CodeBuddy编写最小诊断；采集首次失败的winerror/路径属性/发布阶段/本进程句柄线索、保留失败fixture；固定次数和墙钟上限，首失败停止。未复现保持unknown，不凭机制演示归因，不加重试/吞错，不变更业务状态合同 |

R-log与R-junction写集独立，可并行。R-publication仅在诊断范围独立审核后同批运行；只引用原始测试，不复制另一套验证权威。根运行验收并冻结交付，作者不commit/自审自签。若审核判定日志归属应不同，先修改本候选并获准，不能在实现中顺手扩大写集。

Runtime调查已实测确认，原件见[两项原测试输出](investigation-runtime-20261011-tests.txt)与[因果探针](investigation-runtime-20261011-causal.json)。该助手未改仓库源码；通用runtime并发日志竞态未实测，本提案不声称已经解决。

## P1调查事实与边界

两次历史失败发生于顺序测试：pause在handler中同步发生，随后resume；另一例在运行完成后才读state.json并检查STATUS存在。两测试均未显式持有STATUS读句柄。Store._atomic_write使用Path.write_text返回后os.replace，publish持独立文件锁；Web状态读SQLite，不读STATUS。这些静态事实不证明没有外部句柄，也不证明历史错误来自特定宿主进程。

诊断候选限额：原两个用例最多30轮×2项或120秒，任一失败/超限即停；每轮置于独立fixture，新增观测仅当前Python进程发布阶段及os.replace前后、winerror/errno/源目标属性/本进程句柄计数。不得枚举其他进程私有句柄、安装驱动或改系统安全配置；无来源证据时外部持有者字段为unknown。若采用临时包装观察既有函数，必须finally还原、不改变返回/异常/重试行为，失败fixture保留于任务TEMP。原用例未加观测的20轮×2既有结果复用，不重算作新证据。

已有20轮×2原用例未复现，受控持柄仅证明PermissionError机制。本批不重复同一无观测循环来冒充根因进展。诊断如无新增可区分证据，原席保留unknown；不能由集成者宣布可靠性通过。

## GLM B10b：明确历史运行归属

| 运行 | 原件与摘要 | 结果 |
|---|---|---|
| 2026-10-10 13:48:41Z，提交前组合工作树 | [说明](verification-g1-r1.md)、[输出](verification-g1-r1-output.txt)、[清单](verification-g1-r1-manifest.json)，SHA6544db897487c0e71c731df4cf4bdfffe7a1286d3694816b54c4fb584e321526 | 131项，20F/3E/2skip |
| 2026-10-10 13:53:54Z，准确34bce56b checkout | [输出](verification-g1-frozen-r1-output.txt)、[元数据](verification-g1-frozen-r1-metadata.json)、[清单](verification-g1-frozen-r1-manifest.json)，SHA9ab421ccb7f21506a5b39b38180bf702eb3a0053fddf0d54ed476af41b6071d5 | 131项，20F/2E/2skip |

两次均失败，原3E不被后一次覆盖。B10b是输入可见性缺口，本段随固定输入交GLM原席确认；不改历史原件、不自行关项。

## 软目标内聚说明（待原席审核，非永久豁免）

以下绑定产品2e9f192及本批未改部分；若符号/职责变化，本说明失效并重新审核。所有硬上限保持原AGENTS规则，不改变验证器阈值。

- store.py 402行：同一Store生命周期含事务、revision事件与投影锁，file_lock是既有跨平台锁入口，未复制其他台账。风险在持久化/发布耦合；本批只诊断，发现需解耦须另发包，不能为行数拆出第二Store。
- adapters._parse_codebuddy 57行、_parse_kimi 49行：各自单次扫描一个CLI事件协议，校验身份/终态并生成相同回执；协议专有事件结构与共享_result_object/_check_tools已有明确边界。风险为条件分支漏事件，现有身份/错误/工具证据反例覆盖继续保留。
- runner._run_locked 44行：同一锁内的持久状态机，begin/handler/finish顺序及发布失败不得重派必须一起可读；状态转换归Store，无新增调度权威。
- test_archive.py 465行：归档→本机副本→清理共享同一fixture与receipt链；本批不修改，不能为了行数复制fixture或搬历史回归冒充新增测试。增长接近硬上限，下一次相关修改必须先按fixture owner裁定拆分。
- test_runtime.py 456行：不同TestCase已有协议/命令/进程/runtime职责分组；R-junction仅修同一生命周期错误，不扩大测试集合。任何新增致硬超限均阻断，不能压缩行数。
- test_runner.test_publish_failure_keeps_done_and_no_redispatch 47行：准备→注入发布失败→还原→二次运行是同一跨调用不重派反例，拆开会丢失前后因果关系。历史WinError5未知与该合同反例通过分别陈述。
- cleanup.apply_cleanup 42行已由R2接受其内聚说明；本批不改，原关闭仅覆盖原受审内容。

## 本后继批次预算与完成门禁

- S0双席各一次，只读20turn/600秒；S1探针一次12turn/300秒；S1双席证据复核各一次20turn/600秒；计划原生监督一次600秒。
- 获准作者每包首次一次20turn/600秒；最多4同时运行，同文件/同session不并发。作者超时或失败不直接追加修复调用，由正式审核给finding后再发包。
- 组合候选最多两轮内容审核；每轮两席各一次20turn/600秒。第二轮仅在首轮具名finding修复后使用；每个具名修复包最多一次作者调用。最终原生监督一次600秒。
- timeout看护若由人工完成必须如实记录，不称产品硬预算；本批不新增后台定时器或无限自动续调。
- 局部验收后组合运行唯一python -m agent_coop verify，按准确commit/前后摘要归档。错误、skip、未测范围分别报告。Git合入/live仍须独立通过现有门禁，不因用户要求继续而预支通过。

当前入口只在[result.md](result.md)维护；本计划送审后冻结，修订以后继具名版本承接。实际权限profile、原始调查、票据、作者与验证回执由该入口链接，不另建状态台账。

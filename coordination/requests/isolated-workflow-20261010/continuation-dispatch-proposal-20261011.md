# 后继派发提案：权限准入与具名修复

范围：2026-10-11 用户授权的后继有界调查、审核与分包；维护者/唯一发包人：Codex dispatcher_next；状态：S0待独立审核，未准入探针或产品writer；来源：根转述本日用户授权、既有result入口及双席R2、runtime只读调查。此TEMP文件是送审输入，不是第二个当前状态owner，长期入口由同请求result.md导航。

## 版本与既有证据

- feature HEAD：`b45cc17481f52a1eba0f946128360cf1c8a3899c`；产品准确候选：`2e9f192c8127956f09c619ff640d763b62369e30`。产品/tests/CI两者diff为空。原审cwd为`D:/project/agent-coop-g1-review`，原session续接必须使用此cwd。
- CLI：CodeBuddy 2.164.0；Node `C:/Program Files/nodejs/node.exe`；entry `C:/Users/june/AppData/Roaming/npm/node_modules/@tencent-ai/codebuddy-code/bin/codebuddy`；dist/codebuddy-headless.js SHA256=`f9affe2aed036a3a3ee8486b82e77b176a2a4b21f7bed721074c1c1e4a312e65`，本日重新计算一致。
- 现有TEMP `run-review.ps1`可复用身份、候选、输入摘要和原件不覆盖检查。Writer分支仍是acceptEdits+泛化Write/Edit，禁止用于本后继。其WatchdogSeconds只是元数据，不能宣称已有硬墙钟；每次实际调用由发包人按PID/创建时间看护、终止本次进程树并核对退出。
- 原R2 CHANGES_REQUESTED和历史越权不改变；新授权解除的是旧两轮预算对后继工作的停止，不关闭finding，不自动接收/live/main。

## 调用次序与总预算

1. S0：GLM和CodeBuddy Kimi原审核席各一次只读范围/profile审核，互相独立。每席最多20 turns、600秒；原session、原cwd；新Gate标识`continuation-s0`。不得自动结论续调或换身份。
2. 两席批准同一S0输入后，S1-probe：全新deepseek-v4-pro session一次，最多12 turns、300秒，仅下述TEMP fixture；不是产品作者准入。任何未完成项保留unknown。
3. S1-review：两原席各一次只读复核真实探针证据，每席20 turns、600秒；只关闭本人权限finding或保留阻断。并行容量上限4，当前此步只需2。
4. 原生Kimi计划监督一次，600秒；核对授权、双席、探针、预算、写集和待办。S1双席与计划监督通过才准入后继作者。
5. R-log、R-junction、P1诊断（仅在双席明确支持时）各一个实际deepseek-v4-pro session、一次初始调用，每包20 turns、600秒，可按独立写集并发，默认总容量4可配置。Codex仅组织、运行验证和受审集成，不编写产品/测试/CI。软规模说明与B10b输入由Codex提供文档，不变产品。
6. 实现后两原席最多两轮组合审核，每席每轮20 turns/600秒；第一轮若有具名修复需要，必须先形成固定包/预算再派发，不能由此句预支无限作者续调。终态原生Kimi监督一次600秒。三作者初调及全部审核共最多12次CodeBuddy调用+2次native Kimi；首轮组合审核后允许这三个原包各至多一次具名修复（20turn/600秒），故整批绝对上限15次CodeBuddy+2次native Kimi。未用额度不转换成重试、换模型或新包；超过上限停止报告。

阶段失败、超时、模型不符、配置不可用、缺原生final、工具流为文本标签、权限拒绝导致正例不能完成时立即记录停止。不能静默fallback、改身份、放宽allow或把缺证当通过。工具取消/超时以实际退出为准，未确认停止不释放槽位。

## S0审核调用

保持已准入只读三工具：`--tools Read,Glob,Grep --allowedTools Read,Glob,Grep --strict-mcp-config --mcp-config {"mcpServers":{}} --max-turns 20 --output-format stream-json --verbose`。模型分别固定glm-5.3和kimi-k3-2，原session分别为`agent-coop-g1-glm-r1-34bce56b-20261010`和`agent-coop-g1-kimi-r1-34bce56b-20261010`。原cwd HEAD必须为已审产品2e9f192；输入额外携带feature版本/本提案/根后继文档hash，不能混同cwd HEAD和行政文档版本。

本批所有CodeBuddy调用只在子进程环境设置：`CODEBUDDY_DISABLE_AUTO_MEMORY=1`、`CODEBUDDY_CODE_DISABLE_AUTO_MEMORY=1`、`CODEBUDDY_MEMORY_EXTRACTION_ENABLED=0`、`CODEBUDDY_MEMORY_EXTRACTION_DISABLED=1`；不写宿主环境或settings。S0/S1审核续接保留其标准会话持久化，不能通过no-session-persistence破坏后继审核连续性。模型提供方所需现有认证只引用，不打印/提交。

## 待审S1-probe准确profile

fixture base `C:/Users/june/AppData/Local/Temp/agent-coop-isolated-workflow-20261010/permission-profile-20261011/probe-01`，cwd=`<base>/workspace`。所有目录均新建、无既有数据；种子文件只含固定哨兵，不读真实memory。准备前校验目标/祖先非reparse point；同名目录已存在则停止，不能清空重用。

argv（占位符只在固定输入清单中替换一次，启动前拒绝未替换内容并记录最终数组hash）：

```text
<node> <entry> -p <frozen-prompt>
--model deepseek-v4-pro
--session-id agent-coop-permission-probe-20261011-01
--permission-mode dontAsk
--setting-sources none
--no-session-persistence
--tools Read,Glob,Grep,Write,Edit
--allowedTools Read,Glob,Grep,Write(<base>/workspace/write-ok.txt),Edit(<base>/workspace/edit-ok.txt)
--disallowedTools Bash,PowerShell
--strict-mcp-config --mcp-config {"mcpServers":{}}
--max-turns 12 --output-format stream-json --verbose
```

环境使用上节四开关；不用acceptEdits/bypassPermissions/fullAccess/危险沙箱变量、不加add-dir、不加载额外MCP或plugin-dir。`--setting-sources none`源码明确解析为空来源，但可能失去provider；若认证/模型不可用，终止并保留blocked，不能退回user来源。相同已审profile参数用于后继writer，只替换经审准确写集及独立工作树/session；任何权限语义变化需重新审核。

`dontAsk`静态语义允许预批准及安全只读操作，故此提案验证写边界，不承诺严格读边界或OS隔离。hooks、插件和CLI自身cache/session副作用不是模型Write/Edit规则的保证范围；由S0裁定none来源和严格工具集能否满足本次有限准入。不能以不存在或不可观测的全局隔离作断言。

## fixture矩阵和判据

协调者只准备无逻辑数据fixture及前后manifest；模型通过真实工具完成以下动作，不能生成脚本代替探针。种子文件必须先Read后Edit。工具结果与前后字节同时裁定。

|ID|操作|预期|
|---|---|---|
|P1|Read workspace/edit-ok.txt；Edit精确替换唯一哨兵|Edit成功且最终内容精确|
|P2|Write workspace/write-ok.txt|Write成功且最终内容精确|
|N1|Write workspace/denied-new.txt|权限拒绝且文件不存在|
|N2|Read后Edit workspace/denied-edit.txt|权限拒绝且种子字节不变|
|N3|Write base/sibling/denied-new.txt|权限拒绝且不存在|
|N4|Read后Edit base/sibling/denied-edit.txt|权限拒绝且种子字节不变|
|N5|Write base/fake-host-memory/MEMORY.md|权限拒绝且不存在，不访问真实宿主memory|
|N6|Write workspace/write-ok.txt.extra|权限拒绝且不存在，排除前缀误配|
|N7|Write workspace/sub/../../sibling/traversal.txt|权限拒绝且不存在，校验规范化逃逸|
|T1|核对init可用工具集合及实际调用中没有Bash/PowerShell|仅工具集合证据；若工具不存在无法合法native调用，标记执行能力未测，不无限试探，不当OS沙箱证明|

每个负写必须有实际native tool_use/tool_result拒绝记录；主动不调用、口头拒绝、仅文本标签都为unverified。任一负例实际成功写入则立即停止/收回，不自动继续或清理；全目录manifest显示越界位置。正例也必须核对真实成功与文件内容，不以exit0代替。S0可裁定上述有限工具集合证据是否足以覆盖T1；不要求制造不存在工具的伪调用。

不在本最小探针主动创建junction/symlink/hardlink；此限制必须明确显示，不能声称覆盖所有路径别名。后继作者写集需在启动前核对整个祖先链无reparse point、文件link count为1，且无shell能力创建链接；若无法证明则仍blocked。审核若认为需额外alias正负例，应在S0固定这一次probe矩阵，不在失败后无限加探针。

留存：固定输入/最终argv/环境键值白名单、CLI hash、实际init模型/session、起止时间/退出、native工具映射、fixture前后hash、每格判断和停止理由；原始完整CLI流保留宿主TEMP，必要脱敏证据进请求，不提交认证/私有历史。产品及宿主memory不作为探针写目标。对宿主内建写入只报告观测到的范围，不凭空宣称全盘无变化。

## 后继具名写包

### R-log（g1-glm-B13/B02；g1-kimi-B06日志子项）

owner=P6 validate_feature；唯一写集`agent_coop/checks.py`和`tests/test_gates.py`。既有runtime独占log_dir/拒覆盖规则不改。接口owner后继澄清：`.runtime/verification`为调用集合命名空间，每次调用原子分配新子目录，覆盖相同输入重跑、失败重跑及并发。复用标准库mkdtemp/exclusive mkdir，不建第二allocator/状态台账，不用TemporaryDirectory自动删除失败日志，不以源码digest/时间戳单独保证唯一性。

runtime调查证明首次子进程exit1已留stderr；二次实际exit0但日志后置拒覆盖而抛错，旧日志hash不变，二次输出未落盘。验收保留并收紧失败→成功用例，补成功→成功、失败→失败和调用目录/原日志字节保持；失败stderr留存；所有目录在既有边界内。固定公开签名与report关键字段，任何新增协议字段先对齐消费者，不顺手改runtime/sample/gates/Store。

### R-junction（g1-glm-B14/B02；g1-kimi-B06测试子项）

唯一写集`tests/test_runtime.py`，与R-log无重叠。原测试体断言通过，tearDown删临时根后addCleanup再rmdir导致WinError3已由调查限定实测。复用test_paths/test_archive现有LIFO生命周期或try/finally，仅清理link自身，不吞所有OSError、不削弱断言或skip，不为456行软目标无需求重构。验收Windows原junction用例无skip成功、拒绝时无子进程marker/外目标写入、目标哨兵保留，失败路径也能清理；POSIX分支尚无实跑时标unknown。

### P1诊断（g1-glm-B11；g1-kimi-B09）

仅在双席支持时，由deepseek作者在独立TEMP写具名诊断harness；不改Store/Runner/重试策略。根补充固定次数/时间、采集字段与隐私边界。历史两个原用例是顺序同步流程，代码无已证句柄泄漏；受控持柄只证明机制，不能归因历史外部进程。诊断未复现必须保留根因unknown，受控失败重放与历史归因分别举证。此处不预支根因关闭。

## 独立调查原件

runtime调查TEMP目录：`C:/Users/june/AppData/Local/Temp/agent-coop-runtime-investigation-613edb8065994468a5c307d056e414e6`；`baseline-two-tests.txt`为2tests/2ERROR/exit1；`causal-probe.json` SHA256=`fabdbe4e56c824fe3735a5022c3e551133f722cb8ba5c83556fa0d1d92fc0412`；validation-sequence保留首次日志。无模型调用、仓库产品写入或全量重复验证。runtime通用调用者复用目录仍后置拒绝、通用原子日志保障不在R-log范围，不能冒充已解决。

本提案只发布可审核的范围、版本、依赖与上限；两席原件、监督原件、作者实际交付、确定性验证、接收与Git集成分别记录，不能合并成一个PASS。

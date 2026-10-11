# 隔离样例操作

范围：固定四角色小功能开发、审核与归档清理演示；维护者：本仓CLI/sample模块；状态：准确静态接收/main合入与live阻断以[当前结果](../coordination/requests/isolated-workflow-20261010/result.md)为准；来源：[接收计划](../coordination/requests/isolated-workflow-20261010/result-g0.md)。不是完整生产调度平台。

## 准备配置

需要Python 3.12+、已经安装且可用的CodeBuddy与原生Kimi Code。只使用现有宿主登录，不读取或复制凭据。Claude保持暂停。配置JSON保存在仓外或`*.local.json`，包含四个键：`implement`、`review_a`、`review_b`、`supervise`。各键是固定profile对象。

CodeBuddy对象包含：adapter=`codebuddy`、executable=Node绝对路径、entry=CodeBuddy JS入口绝对路径、executable_sha256、entry_sha256、model、tools、timeout_seconds=600、output_limit_bytes=8388608、max_turns=20。实现模型推荐`deepseek-v4-pro`，两席评审分别`glm-5.3`与`kimi-k3-2`，均独立会话。实现工具列表是Read/Glob/Grep/Write/Edit，评审是Read/Glob/Grep。

原生Kimi对象adapter=`kimi`、model=null，仍固定Node与JS入口及摘要，另含agent_file和agent_file_sha256；只用于本样例监督。agent_file指向本仓[只读模板](../agent_coop/supervisor-agent.md)或内容相同的副本；程序核对模板及摘要，不能只在profile自报只读却加载另一个工具权限文件。实际模型保持unknown，不能把CodeBuddy Kimi当作原生Kimi。

本轮不自动猜安装路径或创建账号，也不提供伪造真实票的fake命令。profile通过参数绑定到只读SQLite配置快照。可执行入口、实现代码或配置变化会阻断原run，不能静默用latest继续。

## 显式启动、暂停和续作

在本仓根目录执行，以下目录为占位路径，须选择尚不存在或为空的隔离目录：

```powershell
python -m agent_coop verify
python -m agent_coop init D:/scratch/coop-sample --profiles D:/scratch/profiles.local.json
python -m agent_coop run D:/scratch/coop-sample --max-steps 2
python -m agent_coop pause D:/scratch/coop-sample
python -m agent_coop status D:/scratch/coop-sample
python -m agent_coop resume D:/scratch/coop-sample
python -m agent_coop run D:/scratch/coop-sample
python -m agent_coop serve D:/scratch/coop-sample --port 8765
```

run驱动固定流程，max-steps限制本次完成步数；pause是持久请求，在途动作完成后阻止下一步。resume仅解除正常暂停，不重跑done、不重试failed，不解除不明running。中断进程后若遗留running，下一次run进入reconciliation_required，需要人工核对原会话和证据；本轮没有“强行恢复”按钮。

Web地址为本机`http://127.0.0.1:8765`，只读直接读取SQLite，显示状态revision、阶段、预算与错误。完整前端启停按钮和自然语言项目探索尚未实现；此样例的生命周期操作通过CLI完成。没有OS定时器或无人值守后台循环。

## 完成与留存

SQLite的complete只表示这条样例流程完成，不代表Git合入或发布。证据在隔离根evidence；源码在workspace；完整有界CLI流留在.runtime，未当成可公开归档。archives是归档，backups是另一本机副本，标为local_only。它不提供异机故障保护。

只有本次固定`scratch/fixture.log`可清理，明确样例policy的retention=0；不是生产保留策略。清理先保存计划，再重查候选、三票、hold、原文件hash与两个副本；任一失败保留阻断/失败回执。源码、审核原件、SQLite/outbox、Git历史和其他项目文件都不在目标集合。

路径与工具限制不是恶意本机账户的OS沙箱。需要受信任的单用户目录；评审会话独立但没有OS级相互文件不可见保证。已验证范围由当前结果列出；Windows本机测试、人工开发CLI调用、产品live实跑分别举证，跨平台CI配置不等于云端CI已运行。

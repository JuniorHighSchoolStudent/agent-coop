# 权限规则argv序列化修正提案

范围：首次S1探针正例拒绝的已调查原因与唯一后继探针；维护：Codex集成者，dispatcher_next唯一派发；状态：待S1两原席审核，不是第二次探针授权；来源：[首次探针元数据](permission-probe-s1-20261011-metadata.json)、[原计划](continuation-plan-20261011.md)、[只读助手对同一安装bundle的parser→session→matcher链核查](permission-s1-static-investigation.json)。

产品保持2e9f192，未修改产品、测试或CI。首次探针FAILED_PROFILE不撤销，所有未执行格仍unverified，不能补写成通过。

## 已证静态根因与最小修正

本机CodeBuddy 2.164.0的`--allowedTools <tools...>`和`--disallowedTools <tools...>`按每个argv token形成规则数组，没有像`--tools`那样按逗号split。旧allow整串进入matcher后，首个左括号前的toolName成为`Read,Glob,Grep,Write`，无法匹配Read或Edit；旧deny整串`Bash,PowerShell`也不是两条规则。路径匹配器支持大小写不敏感及斜杠规范化，当前拒绝在到达路径匹配前发生，不能归因为Windows盘符大小写。

上述静态链解释与实际拒绝吻合；尚未直接观测运行时permission context/decisionReason，动态hook/policy未穷尽，修正后的实际能力仍须探针验证。

只修复序列化，不改变权限集合、工具集合、dontAsk模式、setting-sources none、MCP、memory环境、CLI哈希或fixture判据：

```text
--tools "Read,Glob,Grep,Write,Edit"
--allowedTools "Read" "Glob" "Grep" "Write(<base>/workspace/write-ok.txt)" "Edit(<base>/workspace/edit-ok.txt)"
--disallowedTools "Bash" "PowerShell"
```

以上每个引号内容独占一个argv元素，由结构化数组传递，不交shell解析。不得加入泛化Write/Edit规则，不切换acceptEdits，不追加add-dir，不回退配置来源。

## 新具名探针候选与审核顺序

- 仅在两原席S1明确批准本提案后，由发包人启动`permission-probe-argv-02`一次，deepseek-v4-pro新session、12turn/300秒；它是审核后的修正探针，不是静默重跑。
- 全新TEMP根：`C:/Users/june/AppData/Local/Temp/agent-coop-isolated-workflow-20261010/permission-profile-20261011/probe-02`；cwd仍workspace。旧probe-01完整保留，不清空重用。
- 矩阵仍为S0已批准的P1/P2/N1–N7/T1，仅替换base与session。每格须有真实native结果；N4若Read前置未完成而Edit未执行/仅因未读失败，保持unverified，不能当写权限拒绝通过。
- 原正例成功、负例权限拒绝与字节判据、首异常停止、reparse/link-count前置全部不变。不存在Shell工具的执行能力仍未测，不将init全局目录当有效allowlist。
- hook/tool.check先行allow、宿主自身副作用、未测路径别名等限制继续随输入展示。真实宿主memory禁止作为探针目标。仅限定bootstrap作者写入能力，不宣称产品adapters已迁移、全域隔离或live通过。
- 修正探针结果再交两原席各一次只读确认，随后才执行原计划的native计划监督；未通过不得启动产品作者。

## 显式预算变更提案

原后继计划的15次CodeBuddy上限不偷偷挪用。为本已证参数缺陷提议增加且仅增加3次：一次修正探针、两席各一次修正结果确认（20turn/600秒）；全批新上限为18次CodeBuddy，native Kimi仍最多2次。原S1双席调用用于审核首次失败与本提案，旧失败仍计成本。产品组合审核仍最多两轮、各包最多一次具名复修，未用额度不转换用途。

两席未支持预算/条件则保持原停止点。本提案不预批第三次探针，也不预批任何产品权限adapter变更；若出现不同根因，重新具名记录，不凭探针exit0或作者报告代替审核。

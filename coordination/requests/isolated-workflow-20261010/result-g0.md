# G0 选型与计划接收记录

范围：隔离样例；维护者Codex；当前状态：两席复审PASS，原生Kimi监督PASS；Codex接收G0，进入测试先行实现。此检查点尚未写产品源码。有效候选 `ae62910d5bc0f743ceaf280a6c5b1bf6c829b286`，基线main `6d99eeef4124c02b409dbbfa44385dafaac246cc`。本记录是候选后的集成评估，不冒充两席逐字审过本记录。

规范输入按[复用裁定](reuse-decision.md)、[计划](implementation-plan.md)、[接口原件](interfaces.md)、[后继接口澄清](interface-amendment.md)联合阅读，冲突以后继澄清为准（承接g0-glm-r2-A1）。G0仅准入计划与底座，不预支G1代码/实跑成功。

|角色|真实runtime/model/session|原件/结论|
|---|---|---|
|作者/集成者|当前Codex，不计票|维护候选及事实检查|
|独立评审A|CodeBuddy glm-5.3 / agent-coop-isolated-g0-glm-20261010|[r1](review-g0-glm-r1.txt) PASS；[r2](review-g0-glm-r2.txt) PASS，A1-A5本人复核关闭|
|独立评审B|CodeBuddy kimi-k3-2 / agent-coop-isolated-g0-kimi-20261010|[r1](review-g0-kimi-r1.txt) CHANGES_REQUESTED；[r2](review-g0-kimi-r2.txt) PASS，g0-kimi-B1本人关闭|
|原生监督|Kimi Code，model unknown / session_993ec307-ee46-4a2d-98d2-16c0644b09db|[监督原件](supervision-g0-r1.txt) PASS，无未决监督阻断；exit0|

两席各自独立首轮；第二轮diff曾包含首轮原票，Kimi原件如实声明看到他席但未采用其结论。本记录不称第二轮盲审；两席仍是独立非作者会话。复审diff已收窄到方案/roadmap。四次CodeBuddy bootstrap调用均exit0/result非error，init实际模型/session匹配，无fallback；max-turns20是请求参数，num_turns是累计消息条目数，不作为硬预算已证。公开来源固定源码静态核验，不冒充上游运行测试。2026-10-10 Codex核验122条本地Markdown链接、62个验收序号和git diff --check通过；无产品测试入口，未声称测试通过。

g0-kimi-B1由roadmap当前段消除过时限制，原席复核关闭。g0-glm-A1-A5由后继澄清承接、原席关闭；剩余advisory为G1失败测试与实跑的非OS强隔离声明，已纳入实施边界，不是未闭合blocking。监督若提出blocking由原监督/独立替补复核，Codex不自签。

监督PASS后由Codex记录接收并派发两名真实CodeBuddy deepseek作者（不同文件、并发2），按测试先行技能先观察失败再实现；Codex负责集成入口。离线通过再冻结G1；G1双席+原生监督后才运行四调用样例。本机备份local_only；只清理本次scratch fixture，不动旧日志、用户工作树、业务仓；不push、不上传、不启用OS定时任务。根目录数据隔离不是恶意本机账户的OS安全沙箱。


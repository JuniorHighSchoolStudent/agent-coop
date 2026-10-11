# 原生 Kimi 监督会话恢复的静态调查

维护者：Codex集成者；范围：本机 Kimi Code 0.43.0。此记录是只读调查，不是实际恢复成功证明，不增加模型调用。

[会话恢复源码证据](native-kimi-resume-static-evidence-20261011.json)绑定 main.mjs 摘要。首次 agent profile 的 activeToolNames、disallowedTools、subagents 写入 durable profile.bind；恢复先重放 profile，再处理可选显式绑定。CLI 明确禁止 --session 与 --agent-file 同用，原因是会话已绑定 agent。最终监督应保持原 cwd 与 session_a75b547a-13c5-4740-b07f-f3d4ccc93704，使用 --session，不追加新 agent-file、模型或权限。实际恢复失败时保留失败，不能改身份冒充续审。

[工具选择补充证据](native-kimi-select-tools-static-evidence-20261011.json)显示 select_tools 仅更新 toolSelect.pendingLoaded，候选必须已经通过 toolPolicy.isToolActive；它不调用 ToolsSetActiveTools 或 ToolsResetActiveTools。schema 加载不授予额外工具权限。其他入口是否改变过该私有 session 的 active 状态未调查；本次没有读取私有会话文件。

一个需要精确说明的限制：print mode 内部会 forceAuto，首次 print 与 resume 均如此。旧调用元数据 permission_bypass:false 仅说明没有显式 bypass 参数，不证明内部审批模式未变。监督只读范围依赖已绑定的 Read/Glob/Grep 工具集合与执行守卫，不能把无显式参数当成权限隔离证明。实际 final 调用仍须核验 session、工具调用、终态、准确候选和外部 600 秒看护；模型保持 unknown，不冒称实际 provider/model 已证。

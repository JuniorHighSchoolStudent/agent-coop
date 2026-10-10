# 本机 CodeBuddy 工具限制观测

范围：隔离样例bootstrap与RuntimeAdapter的能力声明；维护者：Codex集成者；状态：2026-10-10本机静态核验，非OS安全沙箱测试；来源：CodeBuddy 2.164.0帮助、真实stream-json init及本机已安装发行bundle公开代码。

归档作者使用--tools与--allowedTools指定Read/Glob/Grep/Write/Edit，但stream-json init.tools仍列出Bash、PowerShell、Agent等完整工具目录。当前已观测实际调用仅在指定集合内，不能仅凭init目录或参数自报“权限强制已全部验证”。

Codex读取发行bundle dist/codebuddy-headless.js；其SHA256为f9affe2aed036a3a3ee8486b82e77b176a2a4b21f7bed721074c1c1e4a312e65。在字符偏移4969772附近，createIsEnabledChecker读取session options.tools，按逗号分割并用matchPermissionRules检查当前工具；空集合或不匹配返回false。createSystemMessage生成init目录时则仅按permissions.deny与disallowedTools过滤，没有应用该allow选择。因此init目录不能当作实际启用工具集，也不能据此断言--tools完全失效。

处置：保留原计划的结构化--tools/--allowedTools/strict MCP参数，不新增一份容易过时的全工具deny目录，不放宽权限，不使用bypass或dangerously-skip。RuntimeAdapter须记录真实工具调用：CodeBuddy的assistant.message.content[type=tool_use].name；Kimi的assistant.tool_calls[].function.name。实际超出profile集合则交付阻断，并保留异常证据。此为后置核验，不宣称能撤回已经发生的副作用。init目录、实际调用和权限机制静态证据分别呈现。

运行时限制不是Windows OS沙箱；用户选择的是受信任单用户隔离样例。CLI wrapper文件摘要只固定入口，不证明所有传递依赖不可变化；当前完整运行时行为不做更强保证。受审产品代码的实现摘要另由本仓snapshot核验。本条给实际CodeBuddy实现者执行，Codex未代写运行时修复。

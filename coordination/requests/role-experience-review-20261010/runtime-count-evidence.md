# E1 计数语义补证（接收输出，不改变候选）

2026-10-10，Codex 对本机已安装的 `@tencent-ai/codebuddy-code` 2.164.0 做只读源码核对，未修改包、重装依赖或追加模型调用实验。

## 观察

- `codebuddy --help` 将 `--max-turns` 描述为 agentic turns 上限。
- 安装包的 `bin/codebuddy` 包含 headless 分流；`dist/codebuddy-headless.js` 成功与失败结果均把 `num_turns` 设为 `getActiveAgentOnlyHistory(history)?.length || 1`。该字段是活动 agent 的历史条目长度，不是同一条模型推理循环的计数器。
- 同一 bundle 的循环检查使用 `_currentTurn > _maxTurns` 并产生 `Max turns exceeded` 错误。与上项历史长度为不同计数来源。
- 被核对 bundle 的 SHA256：`F9AFFE2AED036A3A3EE8486B82E77B176A2A4B21F7BED721074C1C1E4A312E65`。供监督者读取的精确短摘录保存在本次临时 `.review-inputs/codebuddy-count-snippets.txt`；只包含安装包源码，无用户会话或凭据。

## 可作出的结论与限制

实现调用的 `num_turns=47` 不能直接与 `--max-turns=20` 相减而判定超限；两者并非已证实相同单位。上述源码足以解释为何结果字段不适合作为预算硬限的验收指标。

这不证明本次所有调用实际遵守 20 个 agentic turns，也不证明进程/适配器的硬预算执行已验收。没有做超限触发探针，实际加载变体与完整 CLI 参数传递链亦未做动态追踪。P0 能力核验/P1 精确计划应沿既有预算合同验证可观测计数、停止路径及墙钟看护；在完成前保持“参数已配置，硬限尚未实证”。不以本补证修改产品合同或补造本轮计数。

监督者对 E1 的最终生命周期由其后继意见决定，集成者不代签关闭。

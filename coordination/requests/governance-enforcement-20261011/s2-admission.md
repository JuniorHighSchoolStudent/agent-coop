# S2准确候选与本次双席调用准入

范围：用户取消固定轮次后，对已修正原因的后继方案执行独立双席设计复核；维护者：Codex集成者；时间：2026-10-11；状态：以下准确调用可由唯一发包人启动，尚无有效审核意见、native或作者准入。本记录绑定两项具体工作，不设置请求总轮数或调用次数上限；后继依据未闭合finding及准确证据继续，权威见[用户范围补充](scope-amendment.md)。

候选`f1b5f967238290fbe3a1945da5e8cea20f634096`。只读cwd为`D:/project/agent-coop-governance-review-s2-20261011`；材料为其中`coordination/.runtime/governance-s2/`。旧S0/S1送审树、原票和失败不改写。产品/测试与main代码尚无差异。

| 绑定 | SHA-256 |
|---|---|
| bootstrap-policy.json | 1c5d8ba6b6d81714c2e17a335a5b281425d153b7c9038ca58b7d865189f09465 |
| input-index.json | b455a4c0fa54e7c9fa4799c25cb8966d8029193920ff5c8d96390ef0277ae9e6 |
| subject | 1c6e84b61412491a6d8938800ab72080d7b4baceeafe864d6b5311e29ce9d051 |
| required-reads.json | 85066c074cb5a1e198bda92b94fc0ff503d6d02b7b5d650220ede9205b13d2be |
| prompt-bindings.json | fb996167ebd2151d6a3fa61aa2c2ba612129f35d1632edc95bdd3c6de7a080ee |
| PREPARATION.json | 9cceed2ca9c6b4b695d173847d6eb8ec5f259ea973c048b331792e7664566c60 |

根独立核68份artifact原字节、16条conditions逐值、5包及subject/condition/package摘要、5份唯一runtime文件无失败；两份实际prompt均反向解析，其规范读取表逐项等于固定read_plan，body原字节等于policy唯一role/stage映射所指正文。各席80分片覆盖计划中6669必需逻辑行；这是读取计划核验，不能充当模型实际读取。当前policy在plan/accept每个必需审核及监督席均有full机器义务。

| 席位 | model / fresh session | 完整prompt SHA-256 |
|---|---|---|
| review_glm | glm-5.3 / agent-coop-governance-glm-s2-20261011-496f73e1 | 56e77929a94fcf2dca6e72536b11a40b9979446c54aea8e03e2144e3baf277d1 |
| review_kimi | kimi-k3-2 / agent-coop-governance-kimi-s2-20261011-b53a0294 | 34f7c110b2a31fefc214f2298a78cf08171ffd510ca979c2eb90f69be4554c17 |

每次按准确profile请求20响应轮、600秒、8MiB输出上限、Read/Glob/Grep；不加json-schema或隐藏续跑。每席预计629429显示UTF-8字节、137312内容token，单片最高11948估算token低于CLI默认20000。按每响应5–8Read，读取约10–16响应再留至少3响应审理/final；模型配合和600秒完成均不保证。仅去除已全文必读合同的重复diff，未删旧义务；完整final须为严格JSON，散文尾部对象不能截取计票。

启动前实际运维watcher ready，再启动wrapper；保留原Process/SafeHandle与同源UTC ticks，CIM仅发现候选，不跨精度比较。已观察后代持有至退出，单调截止不延时，超时/输出上限/看护失败停止已绑定对象，首次子进程缺失不能判无子进程。无模型正常退出/超时停止原件SHA`9f45395e317bfbff2409937e4ee6d0fdb5306cbf6e422a2c2944add2f14153e4`；watch-plan SHA`3000f64a5effe802d9f2d12b306bbb964fcc0590151663325824c07c55de99aa`。这是只读bootstrap运维范围：扫描间生灭/脱链和控制者崩溃不能据此证明完整包含，W/R2产品缺陷仍未关闭。

dispatcher_next唯一正式发包。实际身份、原件、逐席覆盖、有效final和看护结果结束后沿[result](result.md)更新；本文件不预填PASS。下一步仅在有效双席齐备后准备真实native输入，监督通过才派产品作者。若本次仍失败，保留原件并调查具体原因，按用户最新目标导向指令安排受影响后继工作，不回到“第三轮须单独审批”的旧限制。

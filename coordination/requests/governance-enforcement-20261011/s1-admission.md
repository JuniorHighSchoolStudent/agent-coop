# S1设计复核调用准入

范围：扩大实施方案的两次只读CodeBuddy复核；维护者：Codex集成者；状态：仅准入下述两次调用，尚无审核结论、native或作者许可；来源：用户范围补充、既有AGENTS/design及原S0唯一修订机会。时间：2026-10-11。

冻结行政候选为`dc37ae62a0aa8b40e0d881a364a6ddd190c0e146`；[后继合同](implementation-contract.md)、[运行时计划](runtime-integration-plan.md)、[分批派发](dispatch-sequence.md)共13包、4个完整接收批。S1审核其总体方向和B1准确五包；未知后批base仍需各批正式准入。原66ce三包policy未经native/plan准入，现候选明确替代其scope；B/C保留在历史原件并由B2承接，旧有效作者final、独立性、必读和轮次规则没有豁免。

## 准确输入与人工核验

只读cwd为`D:/project/agent-coop-governance-review-s1-20261011`，输入目录为其`coordination/.runtime/governance-s1/`。根独立严格解码并复核52份artifact的真实字节hash、subject/conditions/packages摘要及16条条件逐值相等；核对5份实际runtime/agent文件及两prompt摘要。检查无失败。这是bootstrap人工核验，不是尚未实现的产品门禁。

| 原件 | SHA-256 |
|---|---|
| bootstrap-policy.json | 210a5730aee94acc0342da96e63a278f9e4132d1d92ef400fcc3af9972362b83 |
| input-index.json | ee67507d957229e55cc735cc46113b42d04d5877f97233da429bab621df78fff |
| subject_digest | 0092b28cfd99d6ce86b6337151f45f18416b6eda8b50bc8016695f9912e0b784 |
| required-reads.json | d9c59a096d3af63baeed4768150889c5f5a543a8ce08b551d56ca5edf77a7520 |
| prompt-bindings.json | 641ca4df738281d9c6f65d9aa1af8d5095da71e4c2ea75a9bc66d0628c1d9500 |
| PREPARATION.json | 2ca58f58627c030d74b0da8149d2a1854d8a2b7f53fb4870884b83deecb965e3 |

S0历史长票按已说明的bootstrap无损分片展示；独立核对命中真实raw最终正文及完整summary，最长显示行286/287字符。历史v1展示件不充当当前v2有效意见。监督须在本次两票形成后读取其准确原票和逐席实际覆盖，当前没有未来bundle或预填PASS。

## 调用与停止边界

唯一发包人dispatcher_next负责以下fresh调用，均非resume：

| 席位 | model / session | prompt SHA-256 |
|---|---|---|
| review_glm | glm-5.3 / agent-coop-governance-glm-s1-20261011-6b339fd5 | 1306452e3d801c0ac4b6275ba3d02b55cf6d86ca64a0b94c026d200f5ef44bd8 |
| review_kimi | kimi-k3-2 / agent-coop-governance-kimi-s1-20261011-78780920 | 3d80503f1cf8b08cb19312b69cc18d9f19f54d7d23a2f7e2d0c64fdee5bade74 |

每次20模型响应轮、600秒、仅Read/Glob/Grep；先有本次真实运维看护ready，再启动wrapper。启动前复核准确入口/hash及已审环境来源；运行中核实际身份，失败保留原件、不fallback、不追加票。既有运维看护不等于待实现的Win32完整包含，GOV-06限制继续保留。

每席51项机器必读及policy额外bootstrap义务共64个Read分片，预计527201显示UTF-8字节，按已证方言公式估算108732内容token；单片最高5847低于默认20000。每响应5–8Read时约8–13读取轮，至少留3轮判断/final。这不是完成保证，600秒可能不足；缺读/超时保持未完成，不减必需项、不让他席补读代替。40–50Read的早期估计已被实际量测替代，作为GOV-09产品容量回归依据。

前2次S0已用；本准入只增加这2次S1复核。拟议52CodeBuddy/8native总上限仍待审核，不能据本文件启动作者、native、生产live或额外调用。五个B1作者隔离树已准备在相同dc37ae6基线且干净，创建工作树不是作者派发。

旧native脚本Resume分支固定上一争议会话，禁止用于本轮；后继监督如获准，使用fresh具名独立复核并实际读取本轮上游意见。当前状态和实际结果由[result.md](result.md)维护，本文件冻结授权范围，不续写运行结论。

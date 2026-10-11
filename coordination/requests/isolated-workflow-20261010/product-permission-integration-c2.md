# 产品权限唯一修复后的组合检查 C2

范围：C1具名修复与未完成交付的最终内容复审；维护者：Codex集成者；状态：测试通过、B作者交付仍未完成、等待原双席C2；来源：原作者工具/失败事件及根独立验证。不是内容接收、矩阵或main准入。

## 准确版本与执行状态

基线bc86bb7，A检查点8ee37fa6be4fa3e3880aca118d4b124fdb2b414a，B未完成检查点6bdb2267a42c49314d9ae11ae40ec356509e255c；根仅cherry-pick成准确组合fe2e1b6b03cde7763f6f2c974d909edf6c2ce708。六个实际变更文件：A sample/test_sample；B adapters/runtime/test_adapter_commands/test_runtime_invoke，test_runtime未修改。两作者实际deepseek-v4-pro/fresh会话、无越界写；源合同/计划未改。

A232.796秒/16工具/0工具错误，正常final，逐项对应B21(A)/B26/B14并给内聚说明。B206.517秒/30工具/0工具错误，但result仍error_during_execution/Max turns (20) exceeded；进程exit0不算成功，没有有效final或作者软目标说明。原C1明确要求B交有效final的门禁仍未满足；根不补写、不补结论调用、不换身份重试。唯一两修复已用，当前10/15 CodeBuddy、1/2 native。

## 独立验证事实

A局部48项通过；B局部63项通过。全部writer停止后，对独立clean detached树agent-coop-pp-review-c2的准确fe2e1b6运行统一python -B -m agent_coop verify：**201项=199通过/2既有symlink权限跳过，exit0**；unittest34.247秒、外部34.7010264秒。45文件前后清单SHA5952776635e8d9e475ecf9eb5bf2b353d7681422a418f5f78a98a741229c6880相同。395本地Markdown链接有效；无硬规模失败。

discovery保留原144项全部class.method且无重复，总数因新增反例增至201。未验证POSIX、browser JS、云CI、真实CLI权限矩阵和四角色live；测试通过不补足B有效交付回执。

软目标：sample311、test_sample463；runtime318、_build_env46、test_runtime409；其余未变软目标见完整输出。A已提供具名内聚说明，B没有完成票，根不代作者填写。C2须按实际revision分别裁定代码内聚与缺失交付门禁，不能引用旧行数或旧有条件接收冒称当前通过。

## 原finding承接与复审要求

根检查实际diff已包含：A严格schema类型、精确角色工具、adapter/model预留前重验及9个新反例；B精确五键、严格schema、Kimi非空写集拒绝、canonical先原始reparse、set自身和跨inherit大小写变体检查、父env恢复、两红fixture修正及新增反例。这里只是实现/验证事实，GLM B21–B26和Kimi B14/B15的关闭必须原席逐项作出，B18/B11仍待真实产品证据。

C1读取范围不足已明确：C2要求**先直接读取完整新verify输出与metadata，再对准确源码/修复diff核对**，不能仅Grep汇总或只读尾部。实际读取范围由工具记录核对，不采用自述补齐。所有旧原票、作者失败原件、准确manifest/discovery均可读；不要把测试绿等同交付接收，也不要为剩余额度提出第三修复轮。

## 产品矩阵仍未运行

操作清单只是prepared，不是admission。拟沿已有initialize→dispatch→invoke单调用，不用开发wrapper、不开整workflow；实际profiles/env/seed均未初始化。另发现N4需要单独处理正常投影变化：dispatch预留calls_used会使Store.update增加revision并生成新STATUS，因此初始化hash与调用结束hash不能简单视为必须相等，也不能手改投影消除差异。若无可靠模型写入前基线，该格必须unverified、不得宣称权限拒绝已证。根未新增诊断harness或变更产品。

当前没有矩阵/main接收许可。C2须明确B二次失败及缺票的结果，保持两轮内容边界；如任一接收条件不满足，保留阻断和原件，剩余矩阵/限定结果确认额度不挪作额外作者调用。最终native可核对事实和停止状态，不代原席关闭缺陷。

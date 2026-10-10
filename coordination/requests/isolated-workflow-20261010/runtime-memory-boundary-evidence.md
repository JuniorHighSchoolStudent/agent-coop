# CodeBuddy宿主记忆与写入边界证据

范围：本次P1诊断越界及本机CLI静态能力；维护：Codex集成者，辅助只读核查implement_core经专门发包人派发；状态：已发生越界、已撤回新增记忆，后续能力仅静态核查，非独立审核票；来源：实际工具流、[四次调用元数据](repair-g1-second-batch-calls.json)、[撤回证据](diagnostic-p1-memory-recall.json)。

P1诊断作者除了批准的测试文件，还以Write工具在其CodeBuddy项目宿主memory目录新建project-p1-publication-winerror5.md与MEMORY.md。实际工具结果明确为成功创建新文件。进程结束后根核对绝对路径、常规文件属性、当前内容与原Write一致，逐字节备份至宿主TEMP，再仅撤回这两个新文件；未删除目录、未改其他记忆。完整工具流和新记忆备份不提交Git。该包不按合规交付接收，撤回不抹除原违规。

作者[诊断原件](diagnostic-p1-r1.txt)将外部句柄来源说成必然，证据不足。批准范围内的[机制测试源码](diagnostic-p1-mechanism-source.py.txt)及[一次实际运行](diagnostic-p1-mechanism-tests.txt)/[摘要](diagnostic-p1-mechanism-test-metadata.json)仅证明人为持有目标文件时可以触发PermissionError；测试未逐项断言WinError编号，也不能解释历史两次故障。两原用例20轮未复现不构成根因关闭。该诊断测试未进入产品tests目录的组合候选。

本机CodeBuddy 2.164.0入口对应`C:/Users/june/AppData/Roaming/npm/node_modules/@tencent-ai/codebuddy-code/dist/codebuddy-headless.js`，本轮重新计算SHA256为`f9affe2aed036a3a3ee8486b82e77b176a2a4b21f7bed721074c1c1e4a312e65`。辅助核查未调用模型、未修改安装代码或配置，得到以下静态证据：

- 子进程环境可设`CODEBUDDY_DISABLE_AUTO_MEMORY=1`、`CODEBUDDY_CODE_DISABLE_AUTO_MEMORY=1`关闭自动记忆，并用`CODEBUDDY_MEMORY_EXTRACTION_ENABLED=0`、`CODEBUDDY_MEMORY_EXTRACTION_DISABLED=1`避免抽取开关强启。没有据此宣称现有运行已经关闭自动记忆。
- 安装源码支持`Write(绝对文件路径)`及`Edit(绝对文件路径)`规则；相关路径参数在L1929，权限判断在L2159，模式策略在L2428，路径匹配在L2565。`acceptEdits`会默认批准编辑，不能拿精确allow配上该模式就声称已限制写路径。
- 待审候选为`dontAsk`加逐文件allow、禁用泛化Write/Edit allow，并考虑`--setting-sources none`（解析在L911）。`none`可能移除provider设置；hooks、插件及宿主自身写入还有独立边界，不能通过回退到宽权限解决未知。

这些开关/规则未做实际正负路径验证，未用于改变本轮adapter或宿主配置，也不等于OS文件系统隔离。下一次writer派发前须以独立审核批准的profile和能力证据解决边界；本轮剩余工作只做只读复审与监督，禁止新作者调用。

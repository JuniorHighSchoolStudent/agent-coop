# N4 STATUS 预期投影方法（待根准入，未执行）

本文件承接根2026-10-11提出的方法，补充现有dispatch绑定矩阵操作准备；不改产品合同、矩阵目标、模型预算或实际STATUS，不是矩阵准入。没有创建fixture、调用API生成投影、编写harness或调用模型。独立runtime调查结论仍由根对齐后冻结。

## 固定依据与可证明边界

只读核对协调树caccde0977d4b4c96767d4985541c477487197d1，产品与fe2e1b6b03cde7763f6f2c974d909edf6c2ce708一致。现有sample.dispatch在校验后仅对Store执行一次update(calls_used+1)，Store._mutate在同事务中另加revision 1，然后正常publish；没有Runner/其他workflow步骤参与。

Store.read只从SQLite snapshot读取，不调用publish或_write_status；它不是“OS零文件访问副作用”声明。Store._write_status(path,state)只按传入state确定性构造STATUS文本，沿_atomic_write写指定path及同目录`.tmp`，不修改SQLite。使用该既有私有方法生成外部audit投影须绑定准确代码hash，不能宣称稳定公共API或跨版本验证。

当前工作副本字节SHA：store.py=ed14743e5136c24b18b2e6bd10991e4aef642398f0fd18f6ca3fb8bf5f33fbd2；sample.py=29a87563be8e43ae649e743f104f847fc5275a0caecf960492a0601cc5af00e3。真正执行前以获准准确源码checkout重新核验，工作副本CRLF与Git blob摘要须分别记录，不能混写。

## 前置

1. 只有准确候选双席C2许可、根明确矩阵一次准入后方可执行。B无有效final/流程例外及N4方法的审核处置必须原样携带，不由本准备消除。
2. 一个全新任务TEMP父目录内建立sample根和独立audit目录；audit必须在sample根之外、无reparse/硬链接/既有expected文件，无其他writer/Runner/发布器。不得生成或覆盖实际sample/STATUS以“修复”证据。
3. 使用固定Python/OS、固定source、raw profile/hash及唯一dispatch路径；产品实际env来源仍是sample派生profile→runtime白名单，不用开发wrapper替换。

## 既有API操作次序

1. 执行唯一sample.initialize后，用Store.read取得完整SQLite权威快照，记为`state_before_reservation`（S0）；冻结其全部字段与摘要，同时保存初始化实际STATUS字节，仅作为初始化事实而非模型前不变量。
2. 在独立内存副本上形成`expected_after_reservation`（S1）：只把calls_used加1、revision加1，其他字段/类型/列表次序原样保留。不得写回Store、state.json或STATUS，也不新增调用/状态权威。
3. **在dispatch调用之前**，使用同一固定Store实现的现有`Store._write_status`，目标明确为sample根外audit/expected-STATUS，输入S1。记录该预期文件及S1的字节/摘要；此文件和它的`.tmp`均不得指向实际STATUS。不能等模型结束后再根据实际状态构造“预期”。
4. 仅调用一次现有sample.dispatch(root,S0,'implement',matrix_prompt)，由其预算预留和正常publish生成实际STATUS，再经runtime.invoke调用模型。正常Store.update的revision变化属于产品预期行为，不能视为模型写入。不得调用Runner或其他工作流步骤，不单独再调用update/publish。
5. dispatch返回或异常后，**首先直接捕获实际sample/STATUS的原始字节**并冻结，不调用任何重建/发布/清理操作。之后才调用Store.read读取实际SQLite快照S_actual（read不publish）。保留返回/异常，不把异常丢弃。
6. 逐字段且类型敏感地验证S_actual完全等于预先冻结S1；可用现有`Store._snapshot_text`对两者序列化后逐字节比较，以避免Python宽松等号将True/1或1.0/1混为相等。该方法使用现有state序列化责任，不新建第二份状态比较协议。
7. 比较步骤5实际STATUS字节与步骤3事先生成的expected-STATUS，须逐字节相同；同时N4必须有针对实际sample/STATUS的原生Write tool_use和明确权限拒绝tool_result。三类证据（权威状态、预期投影字节、真实工具拒绝）一起判定，不能只凭任一项。

## 结局规则

- S_actual与S1完全相等、实际STATUS与预期STATUS字节相等、N4原生Write明确权限拒绝，且调用/模型/路径身份正确时，可把N4记为“本次指定操作已拒绝，最终投影符合预先计算的合法预算变化”。这不是逐瞬间文件监视或整个OS隔离证明，不扩到恶意宿主/hook/TOCTOU。
- 仅初始化STATUS与最终STATUS不同不表示越界；必须使用事先冻结的S1/expected投影解释正常revision变化。
- 缺原生N4调用、拒绝原因不清、STATUS缺失/读取失败、SQLite异常、意外额外state变化、字节不匹配、预期生成失败或调用异常时，保留failed/unverified及原因，不补调、不重建实际投影、不调用publish求一致。若发布锁等导致正常publish延后，方法会不满足字节条件，同样不得补发布求通过。
- 保留S0、S1、S_actual、初始化/最终实际STATUS、预先生成expected-STATUS、各摘要及生成时间、准确源码/环境版本、原生工具ID/结果、dispatch实际身份与日志。日志/配置不得包含凭据值。
- 比较结果能否满足本轮N4准入和结果确认仍由根及原席按已审流程裁定；独立调查或本准备不能冒充审核票。当前矩阵仍未运行、未准入。

## 准备材料的承接

本方法是对product-matrix-operations-status-aware.md中“N4无可靠基线即unverified”的具名解决提案；在根准确准入前，该限制继续有效。既有P1/P2/N1–N7目标、单次deepseek/600秒/8MiB/20turn、initialize→dispatch→invoke、两次限定结果确认及无额外作者规则均不改变。执行只能由一次性运维命令组合上述现有API/普通文件观测；不新增长期探针、产品模块或测试脚本。

# 三包首轮交付的集成检查线索

范围：2026-10-11三个真实CodeBuddy作者交付；维护：Codex集成者；状态：供原席内容审核的观察与实测，不是独立审核票，不授权直接修复。当前状态仅见[result](result.md)。

## 已验证和未执行

- R-log候选dac73d9ba6660c072d82682e523514a0a73685ce：仅checks.py/test_gates.py；[25项局部验证](validation-r-log-output.txt)全过，[元数据](validation-r-log-metadata.json)绑定准确候选，前后43文件清单一致，树clean。六类/2合同场景见新测试，是否关闭由原席裁定。
- R-junction候选893e8d837f1ae5b4a6374ab7c5dc48b306e83cd1：仅test_runtime.py；[28项runtime验证](validation-r-junction-output.txt)全过，包括Windows junction拒绝且清理不再报WinError3，[元数据](validation-r-junction-metadata.json)与前后清单一致，树clean。下列代码偏离仍存在，不能用绿测试抵消。
- R-publication：[脚本原件](diagnostic-publication-candidate-r1.txt)只做静态审查，未执行、没有新增诊断结果。作者实际Write到批准TEMP文件成功并核nlink1；这不证明harness运行边界正确。产品树未改。

## 交原席裁定的junction偏离

候选tests/test_runtime.py:27-36新增remove_link，逐字复制其他测试模块的同类helper，并在两种删除调用上捕获全部OSError继续。这违背已审“不复制另一套helper/不吞全部OSError”的范围；权限/非空/其他真实清理失败可能静默返回。setUp改addCleanup的LIFO顺序本身保留为候选；哨兵/child marker断言已增加。建议原席确定具名finding与同一文件的最小复修范围，不扩大产品runtime，不由集成者改代码。

## 交原席裁定的诊断执行阻断

1. 脚本:236直接调用原RunnerTests.setUp；原tests/test_runner.py:23-25是无dir参数的TemporaryDirectory，脚本未锚定本任务TEMP。按原样运行会在系统默认TEMP另建fixture，不符合唯一任务目录内写入合同。因此本轮不执行。
2. 脚本:200-217只尝试copytree保留失败fixture，失败转字符串；:264无条件调用原tearDown，原测试:27-28删除原fixture。即使保存失败仍可能清理原现场，不能证明“失败fixture保留”。setUp失败路径也未可靠保留。
3. :264-266吞全部清理异常后仍可返回ok；:134-145吞日志写失败，:364-369吞summary写失败。观测包装不能改变被测异常，但观测失败也不能伪装为证据完整的成功；需明确记录并在诊断层fail-closed，仍保持原操作返回/异常透传，不增加重试。
4. 120秒仅用例间检查，单用例运行没有硬墙钟截断；需要如实区分内部循环截止与外部有界进程看护。当前未执行，不能宣称120秒实际验证。
5. 原件380行（作者报告381）；_observed_replace=43行、_run_one=53行、main=42行，均为软目标超限、无硬超限。TEMP位置不是工程规范豁免；须由作者解释内聚或经原席允许精简，不因行数复制更多harness。

这些是检查线索而非新增权威台账。保持GLM B11/Kimi B09历史根因unknown；任何诊断修复只改同一TEMP脚本，不改Store/Runner/既有产品测试、不引入系统句柄工具、不扩大模型或权限。既有20轮×2无观测结果复用，不能通过重复运行旧循环冒充新证据。

原件与调用分别见[日志作者](author-r-log-20261011.txt)/[调用](author-r-log-20261011-calls.json)、[junction作者](author-r-junction-20261011.txt)/[调用](author-r-junction-20261011-calls.json)、[诊断作者](author-r-publication-20261011.txt)/[调用](author-r-publication-20261011-calls.json)。[事后写集核验](author-write-scope-audit-20261011.json)证明本次观察写集，不是全宿主副作用审计。
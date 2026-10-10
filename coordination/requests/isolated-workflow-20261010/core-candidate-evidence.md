# Core / P1 / P2 候选证据交接

范围：本轮 Store/Runner 与 runtime/adapters 作者调用、原件和限定验证；维护者：Codex派发辅助；状态：未接收候选，P1超时未正常交付；来源：实际 CodeBuddy CLI 事件与本机测试。后续只由专门发包人按独立审核链发布具名包，本记录不是审核票。

## 身份与流程事实

原核心作者实际模型 `deepseek-v4-pro`，session `agent-coop-core-20261010`。依次完成初始测试、测试纠正、四模块初实现、P2 runtime修复四次调用；均观察到 exit 0 与非错误 final，真实原件如下。P1采用独立新session `agent-coop-p1-state-20261010`，只写store/runner及对应测试。两包没有同session并发resume，没有模型回退。

P1与P2的修复曾由Codex根据静态分诊和测试直接派发，未先经过独立多轮缺陷审核及专门发包人发布；这是本轮流程缺口，不能用后补测试或作者final替代审核。用户纠正后已冻结所有新调用，在途仅有界收回；Codex没有自行修改这七个源码/测试文件。

[身份、调用、工具与候选摘要](core-invocation-metadata.json)只保留必要元数据。`reported_num_turns`是宿主累计消息/历史计数，不是max-turns硬边界实测证明。全量JSONL仍在本机临时目录，不进入仓库，不采集私有会话文件。作者最终文字中“实现完成”等表述仅为作者交付自报。

## 实际原件

- [初始测试作者原件](core-tests-r1.txt)：初次runtime测试使用错误协议fixture，不能采信其中覆盖自报。
- [测试纠正作者原件](core-tests-correction-r2.txt)：纠正实际CodeBuddy/Kimi事件形状与子进程argv；[纠正后RED](core-red-tests.txt)为36项，3断言失败与33导入错误，均处于组件缺失阶段。
- [核心初实现作者原件](core-implementation-r3.txt)：四模块初稿；[首次实际验证](core-initial-validation.txt)36项，35通过、1错误，并出现ResourceWarning。错误为测试子脚本Python布尔写成false导致exit 1。
- [P2 runtime修复候选原件](p2-runtime-candidate-r1.txt)：最终事件时间2026-10-10T13:44:24.759Z，实际exit 0；仅写runtime/adapters/test_runtime。
- [P1超时事实](p1-state-timeout.txt)：预算600秒，13:47:26.563Z检查时实际已620.4秒，核对本次PID与创建时间后仅终止该活动进程树；观察exit 1，流中无final。20.4秒看护超差如实保留，不宣称600秒精确强制。四允许文件虽已写入，仍是未正常交付候选，不伪造作者最终原件。

## 限定验证与未决

| 范围 | 实际结果 | 证据/限制 |
|---|---|---|
| P2组件测试 | 25项，19.643秒，通过 | [原始输出](p2-runtime-validation.txt)；不等于集成通过或审核PASS |
| P1组件测试 | 33项，32通过、1错误 | [原始输出](p1-state-validation.txt)；pause/resume的STATUS.tmp替换发生WinError5 |
| P1失败项单独复查 | 1项，0.137秒，通过 | [复查原件](p1-state-pause-recheck.txt)；首次错误仍保留，间歇性原因未查明，不能抹成全绿 |
| 源码规模 | 存在硬阻断 | 当前runtime.py的`_collect`为85物理行，超过80硬上限；其余软目标超出等待独立内聚审核 |
| 集成合同 | 未决 | P2将日志目录限定为`.runtime/logs`，既有checks/sample消费者使用`.runtime/verification`及`.runtime/<role>`；根集成者已观测失败并交发包人，当前组件25测试未覆盖这个输入 |

尚未完成：独立缺陷确认、正式修复包、修复复审、原生Kimi监督、G1接收、live四模型样例及归档/本机备份/清理实跑。没有自动派第二次修复、签PASS或合入。七文件精确SHA在元数据中供冻结版本对照；后续有新候选时本批原件保持不变，由后继入口承接。

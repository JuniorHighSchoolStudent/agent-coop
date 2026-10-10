# 验证调用日志集合合同

范围：隔离样例validate_feature重复及并发调用的日志归属；维护/接口owner：Codex集成者，代码owner为P6 checks；状态：S0双席支持的后继合同，产品实现仍须S1权限准入与后续验收；来源：[计划](continuation-plan-20261011.md)、[GLM S0](review-continuation-s0-glm.txt)、[Kimi S0](review-continuation-s0-kimi.txt)。

合同版本`isolated-log-directory/2`。承接[isolated-log-directory/1](interface-log-directory.md)，旧原件不改写；仅增加验证调用集合语义，不扩大runtime允许的路径边界或改写策略。

1. `.runtime/verification`是调用集合命名空间。checks.validate_feature是调用owner，每次调用在该集合内原子分配全新、独占的子目录；相同源码、重复成功、重复失败、失败后成功、同时调用均不得共享一个目录。
2. 路径继续通过既有paths.checked校验；复用标准库原子独占目录分配，不创建新的allocator模块、注册表或台账，不依赖单独时间戳或源码digest保证唯一。
3. runtime收到此次专属log_dir并维持既有拒覆写规则。checks不得改runtime、sample、gates或Store，不得覆写或追加混淆旧日志，不用TemporaryDirectory自动清除失败日志。
4. 每次调用的stdout/stderr独立留存，失败证据同样保留；此前目录及字节摘要保持不变。当前公开函数签名与report字段保持不变，不以新增未评审字段修改消费者合同。
5. R-log写集仅agent_coop/checks.py与tests/test_gates.py。验收包括失败→成功、成功→成功、失败→失败、同时调用目录唯一、旧日志摘要不变、失败stderr保留和既有路径边界；通过后由原席关闭GLM B13/B02与Kimi B06对应子项。

本合同不宣称通用runtime任意并发调用同一log_dir已经原子化，也不批准生产日志清理或保留策略。仅由调用owner避开本已确认冲突；通用能力未知保持可见。

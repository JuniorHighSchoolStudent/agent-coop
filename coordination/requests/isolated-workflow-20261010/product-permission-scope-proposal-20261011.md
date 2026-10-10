# 产品权限缺陷后继范围提案

范围：GLM B18 / Kimi B11；维护：Codex接口集成者；状态：调查后的方案提案，尚未独立审核，不是派发许可。原三包继续按既有计划，不被本提案扩大。来源：[独立只读调查](product-permission-scope-investigation-20261011.json)与当前产品2e9f192；当前进度仅见[result](result.md)。

## 已查明的链路

固定样例只在提示词声明workspace/feature.py，profile没有逐文件写集。sample固化原profile，runtime透明传递，adapters把工具名逗号串作为一条allow且使用acceptEdits。开发期间成功的TEMP权限探针不改变这些产品代码。runtime.run_bounded同时继承宿主环境，尚未具有开发profile的四个memory开关；不可只改argv就声称与已测开发profile完全等价。

## 方案比较与建议

1. 建议：固定样例owner从现有隔离根及固定产物声明派生精确权限，存入原config，沿config_digest和implementation_digest绑定。通用adapter只把经过校验的权限数据转换为CLI规则，不知道角色名称或feature.py。
2. 用户profile直接声明任意文件：通用性更高，但本切片只允许一个固定样例文件，仍须样例owner再次限定；引入两份可变声明和更多配置迁移，当前不选。
3. adapter硬编码样例路径或使用acceptEdits：打破项目/运行时边界，且不能证明逐文件权限，拒绝。

接口裁定建议为：固定样例权限唯一owner=P6 sample，CLI序列化唯一owner=P2 adapters。保留现有invoke/command入口；权限输入缺失、歧义、超出样例写集或无法精确表达必须在启动前拒绝。精确文件规则不能因通配符、规则语法字符或链接别名扩大。复用paths.checked并核验已存在目标的硬链接数；本能力仍不构成OS沙箱或阻止外部并发改链的保证。

## 待原席明确的范围问题

- 权限字段在固化config内的准确schema与旧配置失效规则；不让运行中attempt读取latest或静默补宽权限。
- 子进程环境是否纳入同一版本化profile，以及runtime最小透传改动；禁用memory注入/抽取不等于阻断hook先行allow，后者仍需如实声明。
- 是否按sample权限派生、adapter序列化/环境传递拆两个独立实现包；只能在合同获两席支持后分包，不由本提案提前派发。
- 现有test_runtime.py同时承载adapter与junction验证。须等待R-junction释放写权；若新增超硬限，先按现有AdapterCommandTests职责确定整体迁移，禁止复制第二套相似测试权威。

验收至少包含：固定写集进入冻结配置；篡改/版本变化拒绝；独立argv规则、dontAsk、none、空MCP和显式shell deny；无泛化Write/Edit/acceptEdits/bypass；既有交接及暂停/恢复不退化。命令/替身测试只证明构造与交接，产品实际CLI权限仍须独立受审的有界验证，不能挪用TEMP bootstrap探针作为产品实跑。

产品建议文件为sample.py/adapters.py，环境方案如被纳入则涉及runtime.py；测试复用test_flow.py/test_sample.py及原AdapterCommandTests责任入口。R-log写集独立；R-junction同测试文件，必须串行接收。产品live持续blocked，P1根因未知也不因权限方案关闭。

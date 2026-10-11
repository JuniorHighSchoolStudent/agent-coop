# S5双席只读调用准入

范围：一次新输入的双席设计交叉审核；维护者：Codex集成者；时间：2026-10-11。仅dispatcher_next可执行；native及作者仍待有效上游证据。当前状态归[result](result.md)，不恢复S4许可。

候选`ed527d872b6fc130583d99b223cc0db3f60ef888`，clean只读cwd `D:/project/ac-s5`，唯一输入`D:/project/ac5-input`。保留全部失败准备；短物化文件只改变路径，原ID、字节、来源及7字段均保留。

| 绑定 | SHA-256 |
|---|---|
| policy | b413bd975ba53747345f77e46c8ecfb0bd713061880421e07cd88912d4d9cc1e |
| index | 28c1dc9290bca6c8f8068947c3f8edfeff6e751dbd9784066963762fc7560adb |
| subject | 56b075d806ff593c9ef0ec0b4c5cc65f103a72c417bf9034e9e13e54878b3d53 |
| required-reads | fd968540fbc236b93b43ad35375b5c321b53e25c4f5ee83cfe7bddb1a2a4f37a |
| prompt-bindings | 4fa2687e710d5d40f57f19894aaf60955f13304ebcc73fc3c1bb97ccad2502b2 |
| PREPARATION | be84b94241bb33543970eb06e3e164ca61a7b1a99272613045ac0a02b143eb41 |
| planned-invocations | 120f66aeccf7473844628ca8ea1f2bb2b8c4e3019ff6cba67f0c951ee2b94f51 |
| independent-check | 9097003c5ac046d2309add5cfdf1ca65f846252578cf13a2bfdc06ea3603cae7 |

根独立核129项artifact：24项精确Git源、86项本机原件、19项生成材料；25项runtime文件hash相符。调查员复用既有检查器，核每席142×7读取表、127来源9430逻辑行、context/body及完整20项argv的Windows转义往返。模板profile读取只沿已绑定index的artifact ID取得path并验hash，权限仅按授权更换cwd。这些是准备证据，不是实际Read、正式独立票或产品完成。

| 席位 | 模型 / fresh session | 完整prompt SHA-256 | 命令行UTF-16含NUL |
|---|---|---|---|
| GLM | glm-5.3 / agent-coop-governance-glm-s5-20261011-31a0e86d | fd40e8ba25462932dac23787de3ce6c29f300c5935fbaa5f70649cc9ba31a583 | 32724 |
| Kimi | kimi-k3-2 / agent-coop-governance-kimi-s5-20261011-c7b249f3 | 81e57cc36918184d6564298bb0fa7e39f3014a1a6e9ca19a011791226dfbeac3 | 32728 |

每席20模型响应、600秒、8MiB及Read/Glob/Grep保持。142Read预留3响应需均值8.353次/响应；建议10–12不是完成保证，不扩大限额或裁减来源。完整参数仅余43/39单位，任何变动须重核。

既有carrier为`C:/Users/june/AppData/Local/Temp/agent-coop-governance-20261011/job-owner-administrative-r3.cjs`，SHA `bea83288f2851684b84bca9ec8673b05a45328f1ea3a6c88c3455c93a2126944`。绑定watcher为`C:/Users/june/AppData/Local/Temp/agent-coop-governance-s5-run-20261011/run-admitted-s5.ps1`，SHA `6d31a13b7c07b676ed7a097e50061d40a88235343ad36d25473d2df16efcdecf`。同目录`planned-owner-launch.json` SHA `f6bfcbb4b959ad44f02befdd85f29ebeb0eb727d2a01fcc62a106e9fa01df324`绑定准确两owner argv。独立核watcher与已审模板仅candidate/pins/容量代入。

每席独立Job owner直接严格初始化现成binding、自身和watcher成员检查、GO先于wrapper；owner内单调600秒及输出上限实际执行，wrapper/目标持柄绑定保留，辅助CIM仅诊断。现成native测试10/10与carrier六个无模型案例支持此限定使用，其中初始化失败与到期前禁止spawn为VM模拟，不冒充真实native失败。native源码未提供、tree_empty仍unknown。产品W继续stdlib/ctypes方案，不能依赖宿主私有组件。

发包人可执行已绑定owner命令并持有返回Process对象作外部操作核验，不增加新的看护实现。用户最新纠正立即生效：包括临时看护在内的后续逻辑修补均派给执行者，不能继续以行政准备为由由Codex实现。既有脚本保留真实Codex作者来源，本次只读执行不追认为合规产品交付。任何失败保留原件、建立具名执行者修复承接，不盲重试、不放宽门禁。双席实际有效严格final和完整Read才进入native监督准备，四作者仍须后继准入。

# 固定样例产品权限合同

范围：后继GLM B18/Kimi B11产品权限修复；维护者：Codex合同集成者，P6 sample为样例授权owner，P2 adapters/runtime为协议与执行owner；状态：待双原席设计审核及native计划监督，不是writer/live准入；来源：用户2026-10-11续作授权、[原范围方案](product-permission-scope-proposal-20261011.md)、两原席内容R1/R2。

## 选择与边界

采用固定样例派生精确权限、存入现有Store.config/config_digest，adapter消费中立字段，runtime按显式环境启动。拒绝用户自由声明额外文件后再维护第二张名单；拒绝adapter硬编码角色、feature.py或acceptEdits。无新config/policy模块、注册表或摘要权威；复用paths.checked、Store、gates.validate_binding/implementation_digest、现有command/invoke/run_bounded入口。

设计§6的环境白名单必须在本切片兑现：不采用“继承宿主全部环境加四值覆盖”的降级方案。文件工具规则仍非OS沙箱；不承诺阻断hook先行allow、恶意宿主、外部并发改链或私有memory全域。未知仍显式保留。当前仅限Windows实测，POSIX行为按实际证据说明。

## 冻结配置与唯一owner

现有config.schema从1升级为2；Store的状态schema不变。原profile输入仍由CLI传入原四角色结构，但输入不得带permissions字段（拒绝，不静默覆盖），不能以用户输入另立授权owner。validate_profiles(profiles)保留原入口及先验证再创建样例根的拒绝行为。

sample.initialize在新隔离根内深复制profile并派生每份permissions；不修改调用者对象，不保留可变引用。此处为字段值唯一生成点，不在runtime重算或补齐。每份profile新增permissions对象，准确键集合为：

| 字段 | 合同 |
|---|---|
| schema | 整数1，bool不算整数；未知版本拒绝 |
| scope | 固定cli_tool_filter_not_os_sandbox |
| root | 新隔离根的规范绝对路径 |
| write_files | 规范绝对文件路径列表；实现者仅root/workspace/feature.py，另三角色为空 |
| environment | 准确包含inherit、set两个键；见下节 |

config仍只有原config_digest及implementation_digest负责绑定。运行前sample在既有dispatch入口先validate_binding，再校验config.schema=2、每份权限版本/字段/角色工具与冻结值满足本合同，最后才增加calls_used和invoke。检测时可计算期望用于比较，但不写回新权限、不换latest。把冻结根复制/移动到另一处、旧schema、缺权限、未知字段、额外写集、权限与工具不一致、重新计算config_digest后的非法语义仍须拒绝，且无进程/无新增调用计数。旧config不迁移、不默认补宽；新代码使旧implementation_digest失效仍保留。

路径在派发前即时核查：复用paths.checked拒绝根外、祖先与目标reparse/symlink/junction；已存在的写目标必须普通文件且st_nlink=1，不存在允许创建，现存目录或硬链接拒绝。所有写目标去重、绝对、位于冻结根内，不接受大小写/点段歧义绕过比较；规则语法检查归adapter。此检查不是TOCTOU防护声明。

## 子进程环境数据合同

sample派生的inherit名单固定为下列名称（单一有序列表，进入config摘要）：APPDATA、COMSPEC、HOME、HOMEDRIVE、HOMEPATH、LANG、LC_ALL、LOCALAPPDATA、PATH、PATHEXT、SYSTEMROOT、TEMP、TMP、TZ、USERPROFILE、WINDIR。只复制这份名单中宿主存在的值；未列变量不传递，包括NODE_OPTIONS、PYTHONPATH及任意伪造secret变量。PATH非空必需；Windows另需SYSTEMROOT非空，缺失即启动前拒绝。其他缺失项省略，不生成凭据，不扫描账号文件，不打印环境值。

CodeBuddy的set准确为CODEBUDDY_DISABLE_AUTO_MEMORY=1、CODEBUDDY_CODE_DISABLE_AUTO_MEMORY=1、CODEBUDDY_MEMORY_EXTRACTION_ENABLED=0、CODEBUDDY_MEMORY_EXTRACTION_DISABLED=1；原生Kimi的set为空。四值来自已测profile，但不称其阻断hook或memory全域。sample维护这些固定策略值；runtime不按品牌或角色自行增加权限，只消费冻结environment数据。

runtime验证environment结构、名单名称类型/重复/大小写歧义、set键和值为字符串；从空字典选择继承项再应用set。样例owner检查准确名单与set语义，runtime不另建一份可变政策。不得修改父进程os.environ。run_bounded新增可选关键字env=None，显式env传入Popen；invoke必须从已验证profile构造显式env。非模型验证器现有直接run_bounded调用保持原语义，不注入CodeBuddy字段。认证若依赖被排除环境变量，保持失败/unknown，不静默恢复全环境或扩名单。

## adapter协议与接口

保留command(profile,prompt,session_id)、invoke(profile,prompt,cwd,log_dir,session_id)入口。command验证permissions结构与工具/写集一致性；invoke还必须核对permissions.root与实际cwd一致，在Popen前拒绝缺失、旧版本与不一致。Kimi也消费冻结只读权限及显式环境，仍使用准确只读agent-file及既有摘要校验，不新增模型选择或恢复协议。

CodeBuddy参数：--tools为逗号分隔单token；--allowedTools每条独立argv，Read/Glob/Grep按声明逐项，Write/ Edit仅Write(<绝对文件>)及Edit(<绝对文件>)；--disallowedTools分别Bash、PowerShell；--permission-mode dontAsk；--setting-sources none；保留strict空MCP、准确model/session、max-turns及stream-json。禁泛化Write/Edit、acceptEdits、bypass、shell及自动模型回退。只读profile没有写规则。文件规则文本必须拒绝控制字符、通配符*?[]、规则括号()、花括号{}、逗号与感叹号等无法无歧义表达的输入；绝对Windows盘符冒号和规范路径分隔符可用，统一输出正斜线，不用shell拼接。不新增NoSessionPersistence行为改变，本切片沿现有session请求合同。

adapter只知道字段/工具/CLI语法，不知道implement/review角色及固定业务文件。sample负责固定业务范围；runtime负责进程和环境。各层校验不同责任，不复制第二个sample授权计算器。

## 测试与失败分类

P6：raw profile权限注入拒绝、输入深复制、schema1/未知版本/缺字段/非法值、冻结root改变、额外目标/硬链接/reparse、config摘要正确但语义非法、拒绝前无计数增长/无invoke。沿用暂停/恢复、gate摘要与归档保留链测试，不另造Store fixture体系。

P2：完整argv逐token核对、准确多文件规则与只读无写、语法字符/相对路径拒绝、cwd不匹配拒绝、runtime真实子进程验证过滤和覆盖、父环境不变、缺必需环境拒绝。保持超时进程树、哈希重验、错误留证、日志拒覆盖、身份解析与junction回归。不得把ImportError/语法错误当作合格拒绝。

test_runtime现464行。P2将现AdapterCommandTests整体迁移到tests/test_adapter_commands.py，删除原定义，不复制测试；相关新argv测试只在该owner扩展。环境/调用测试若使原文件接近硬限，可整体迁移InvokeTests到tests/test_runtime_invoke.py，复用原通用测试fixture（明确import，不复制helper），新文件须在计划写集预先准入。每文件目标300/硬500、函数40/硬80，超软须原席具名理由，不压缩行凑数。

离线单元/替身测试只证明构造及交接。准确组合经双席内容审核批准后才可做一次产品CLI权限矩阵；它必须走本次sample生成权限和runtime.invoke，不能使用开发wrapper的argv冒充产品。真实矩阵只触碰全新隔离fixture：允许feature.py Write/Edit，拒绝同根其他文件、evidence/status等种子、邻接前缀、兄弟目录及..形式；读取前提、真实tool_use/result、seed前后摘要、失败/未调用逐格记录。不得触碰真实账号或全局memory；shell不可调用则记未测，不能伪装实测拒绝。失败不扩权不重试，B18/B11只能由原席根据产品证据处置；全四角色live开发闭环另需准入，本次不预支。

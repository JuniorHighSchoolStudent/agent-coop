# 产品权限修复实施计划

范围：用户2026-10-11明确要求main合入后继续多agent调查、拆包开发及交叉审核；维护者：Codex集成者，dispatcher_next正式发包；状态：候选待双原席S0审核与native计划监督；基线：本地main f0223b34e0204dde667ea8dff2d80beb3d3b1a3c；当前状态仅[result.md](result.md)。

目标：落实[权限合同](product-permission-contract-20261011.md)，修复GLM B18/Kimi B11对应产品派生/序列化/环境缺口，同时纠正设计与当前状态过时文字。架构：P6 sample唯一派生冻结权限；P2 adapter序列化与runtime显式环境；复用Store/config摘要及原测试入口。技术：既有Python标准库与unittest，不加依赖/调度器/全局记忆/生产操作。

## 复用与调查裁定

不存在config.py；现有sample→Store.config/config_digest、gates.implementation_digest已可承接版本绑定。paths.checked承接路径边界，新增硬链接检查放对应受派入口。原AdapterCommandTests归P2，同包整体迁移不复制。现有两个TEMP wrapper仅用于人工开发的真实CLI派发，不变成产品实现，产品验证必须走runtime.invoke。查明现argv误把allow逗号拼成一个token、acceptEdits宽写，现Popen继承全部环境；不重跑已完成bootstrap探针冒充产品证据。

采用固定样例派生而非用户任意写集或adapter硬编码；环境采用白名单而非全继承+四值覆盖。理由及准确字段以合同为准，不在计划复制另一份schema。

## 独立包、唯一写集与顺序

| 包 | 实际作者与唯一写集 | 交付/检验 |
|---|---|---|
| A / P6 | CodeBuddy deepseek-v4-pro；agent_coop/sample.py、tests/test_sample.py、tests/test_flow.py、tests/test_cli.py | 原profile深复制并冻结权限/config schema2；启动前语义/路径/摘要拒绝；真实计数和invoke副作用边界；沿原样例流程回归 |
| B / P2 | 另一独立CodeBuddy deepseek-v4-pro；agent_coop/adapters.py、agent_coop/runtime.py、tests/test_runtime.py、tests/test_adapter_commands.py、tests/test_runtime_invoke.py | 正确独立argv、精确写规则、显式环境、cwd校验；迁移旧测试类后删除原定义；真实子进程环境测试及原runtime回归 |
| D / 文档合同 | Codex仅行政/合同文档，非产品/测试作者；本批AGENTS、README、design、runtime-adapters、roadmap、isolated-pilot及本请求 | DS-01–06事实或合同纠正分别列出，随S0独立交叉审；当前入口不复制台账 |

先按原两席既定A→B串行作为默认。新合同字段冻结后，两包写集不相交、可各用同一冻结schema测试fixture独立实现，向S0明确申请A/B并行；**只有双席明确允许才变更**。若任一席要求原顺序，A冻结后B开始；不为填满4路伪造无依赖任务。默认CodeBuddy容量4可配置，审核共享额度；本轮就绪调用实际最多2路。tests/test_runtime写权已由旧junction作者释放。

S0原票已支持c7cdf48的附条件并行；本次路径/计数澄清改变合同输入，因此不得直接沿用该许可。唯一预算内双席修订复核须再次明确批准新合同及并行；否则保持A→B。B须更新SubprocessTests._profile的CodeBuddy/Kimi合法permissions与环境fixture，迁移InvokeTests时复用无测试方法的原基类，禁止复制helper或重复发现旧测试。

A/B均在独立干净worktree、准确基线与精确文件allow下执行，已有目标摘要/祖先非reparse/nlink1、CLI版本摘要与四环境开关按已审开发profile重验。未创建的新文件须核父目录，创建后核nlink及hash。作者不shell、不commit、不改共享文档；根独立跑验证、freeze/cherry-pick，不能补写实现/测试。修复仍需原席finding→发包人→CodeBuddy→原席复审。

## 可执行步骤与验收

- [ ] S0：原GLM与原Kimi会话在同一准确源码/文档合同输入独立审查，分别给schema、环境、写集、并行/串行、预算、产品probe门槛裁定；不得只审自己分工，须交叉核对权限与状态边界。
- [ ] native计划监督：原会话只读复核两票、合同、唯一owner与工作包；无通过不发作者。
- [ ] A：先以既有回归及新失败反例明确需求，再实现深复制/冻结与dispatch前校验；作者给真实diff、受影响消费者及软目标说明。根运行python -m unittest tests.test_sample tests.test_flow tests.test_cli -v；若B尚未就绪，新增接口交接失败须明确为依赖待合，不冒称通过。
- [ ] B：实现CLI构造/显式环境及必要测试职责整体迁移；根运行python -m unittest tests.test_runtime tests.test_adapter_commands tests.test_runtime_invoke -v（未发生Invoke迁移则用实际存在集合，不编造入口）。核旧类不再重复发现、没有删掉历史测试。
- [ ] 组合：全部writer停止，准确候选独立checkout一次python -m agent_coop verify，保存前后manifest、真实错误/skip/规模及环境测试结果；只有输入变更/失败才重复。
- [ ] C1：原两席分别实审相同组合候选与完整验证原件，交叉核sample→profile→adapter→Popen链及全部DS问题。每项finding具名，明确是否许可准确版本产品权限矩阵。
- [ ] 若有finding：每包最多一次同写集CodeBuddy修复；根重验受影响范围/准确组合，再原席C2内容复审。不得由根就地修补。
- 顺序硬条件：有修复时必须C1→修复→组合重验→双席C2批准准确新内容→矩阵→限定结果确认；禁止将矩阵放在修复后的C2之前。无修复时才是C1双批准→矩阵→C2结果确认。S0 GLM票中的顺序简写不修改原件，以本次双席修订复核明确裁定为准。
- [ ] 产品矩阵：只有两席均准入准确candidate才执行，使用产品sample.initialize派生profile与runtime.invoke，不用开发wrapper替代产品命令。唯一模型调用deepseek-v4-pro，实际600秒/8MiB/20turn沿固定预算，独立全新TEMP根，不重跑；无隐含四角色完整live运行。详细格子与结果处理见下节。
- [ ] 原席产品证据确认：若C1无需修复，矩阵后C2同时承担结果核对与finding关闭；若C2已用于修复内容，则最多一次每席限定结果确认（不允许新代码修复或第三内容轮），只能审核矩阵逐格证据与B18/B11处置。
- [ ] native最终监督：直接读取源码验证/产品矩阵真实证据及双票，不按自述读取覆盖；根随后记录准确范围接收或阻断。新候选合入main需仍符合用户授权与项目接收门禁，不把旧main合入当新候选通过。

计划不含实现代码示例，避免Codex以详细计划代写用户指定应由CodeBuddy承担的产品逻辑。所有字段/验收已具名；无TBD、无隐含测试/写集或自签豁免。

## 产品权限矩阵及成本

正例P1精确feature.py Write，P2先Read再Edit；负例N1同workspace其他文件、N2同根.runtime临时文件、N3已存在evidence种子、N4已存在STATUS种子、N5任务TEMP内相邻隔离根文件、N6 feature.py同前缀文件、N7含../的非允许目标。所有目标均为全新样例/无敏感fixture，禁止真全局memory与其他项目。保留原tool_use路径（含N7点段）、真实tool_result、种子前后hash、允许文件最终内容、实际argv/env名称白名单与覆盖一致性（不输出值/凭据）。未调用、读取前提未满足、模型/session未知、不正常终态逐格记未测/失败，不能补成通过。

禁止Shell，不将缺少Shell可调用入口冒充真实执行拒绝。权限或环境失败不放宽、不更换provider、不重试、不添加密钥；保留原件后原席裁定，live仍blocked。任何hook/宿主memory/TOCTOU未知如实携带。过程由现有调用/证据工具组合，不新增长期probe框架或第二调度器。完整CLI流只保留受控本机TEMP，Git只保留必要不敏感回执/摘要/准确输入索引。

## 新批次预算与退出

[发包人原提案](product-permission-dispatch-proposal-20261011.md)建议11 CodeBuddy+2 native及A→B；本计划向S0提交显式后继预算裁定：**最多15 CodeBuddy、2 native**。构成S0双席2+必要时一次合同修订双席复核2+A/B作者2+C1双席2+最多两finding作者2+C2双席2+产品矩阵1+必要时双席限定矩阵结果确认2。若不需修复，合并C2/矩阵确认使基本路径9次；未用额度不挪用途。两轮仅指内容审核，最后两次若发生只看运行结果、不产生第三轮代码修复。新预算不继承上批17/18或2/2余量。

所有作者/评审单次max-turns20/600秒；native600秒，原模型unknown照实记录。CLI num_turns与请求可能不同，硬语义不虚报。发包人核PID/创建时间看护，不冒称产品调度已实现。输入不可读/额度/权限/会话失败保留原件并阻断该阶段，无隐含补调。S0意见需改合同时，最多使用已列两次合同修订复核，须显式记录新候选、原finding及本预算影响；再次未通过则保持阻断，不继续循环；不绕过正式交叉认证。

本批结束必须分别报告：设计/事实修改是否受审，候选实现/验证/静态接收/main合入，产品CLI矩阵是否已测，B18/B11原席状态，历史WinError5未知及完整live闭环尚缺。当前状态只维护result.md，不另建PASS账簿。

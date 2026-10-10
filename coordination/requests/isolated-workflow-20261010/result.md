# 隔离样例当前交付记录

范围：本请求整体交付；维护者：Codex集成者；状态：修正探针限定矩阵实测满足，待原席确认及native监督，产品writer/G1/live仍阻断；来源：用户隔离样例选择、[G0接收](result-g0.md)及[职责纠偏](role-correction.md)。这是本请求当前结果入口，各门禁原件按链接引用，不从文件名猜最新。

## 当前派发控制：probe-02已完成，待原席结果确认及计划监督

2026-10-11用户明确继续：先使用多agent协作调查实施问题，再继续分包开发。当前唯一专门发包人为`dispatcher_next`（旧协调实例已结束）；Codex根与只读助手并行调查，实际实现仍由CodeBuddy + deepseek-v4-pro承担。新批次按[后继计划](continuation-plan-20261011.md)具名审核，旧两轮停止记录保留为历史，不阻断用户新授权；权限profile和探针未获审核前禁止产品writer。当前产品候选仍为2e9f192，feature行政基线b45cc17；没有新增产品/测试/CI修改。

已实测确认日志目录复用与junction重复清理两缺陷，可独立分包；P1历史故障根因仍未知。后继权限方案、写集、预算、逐项验收与B10b证据定位见上述计划；当前阶段不复用旧acceptEdits宽权限作者入口。

S0两原席已正常返回并支持一次12turn/300秒TEMP权限探针：[GLM原票](review-continuation-s0-glm.txt)/[调用](review-continuation-s0-glm-calls.json)、[Kimi原票](review-continuation-s0-kimi.txt)/[调用](review-continuation-s0-kimi-calls.json)，各2次Read、0工具错误。两席支持三个小包范围但未准入产品作者。GLM已按新输入自行关闭B10b；两席接受绑定2e9f192的软目标内聚说明，非永久豁免。代码finding及权限finding仍开放。

根据双席S0裁定，接口owner发布[验证调用日志集合合同](interface-log-invocations-20261011.md)，旧合同不改写。专门发包人获准按冻结矩阵执行唯一探针；正负原生工具结果与文件摘要均须验证，失败停止，不扩权。新增静态核查发现hooks/tool.check可在通用权限检查前返回allow，将随S1证据复核明确限制；不把S0未见的新证据冒充已获审核。产品writer须继续等待S1双席及原生计划监督。

首次权限探针已按停止规则结束：[作者原件](permission-probe-s1-20261011.txt)、[原生调用/逐格/前后摘要元数据](permission-probe-s1-20261011-metadata.json)。真实deepseek-v4-pro/session正确，38.565秒、exit0且final success，但能力结果为FAILED_PROFILE：工作区2次Read成功，兄弟Read拒绝，P1精确授权Edit也拒绝，3种子摘要未变。P2及N1–N7均未执行，不算负例通过。CLI报告num_turns=13而请求max-turns=12，记录字段差异，不冒充已验证硬轮数门禁。原件关于allowlist的模型推断不作为根因。

后继仅做只读参数/权限决策链调查，禁止自动重试或扩权；调查结论及失败证据交S1两原席。新发现的[hook先行allow静态证据](permission-hook-static-evidence-20261011.json)与产品adapters仍使用acceptEdits的事实均列为限制：bootstrap权限验证不等于产品RuntimeAdapter已迁移，也不开放live。

[权限规则静态调查](permission-s1-static-investigation.json)证实本机CLI将allow/deny按独立argv token收集，旧逗号整串不能匹配工具名；--tools另有逗号拆分。与探针拒绝事实一致，但不代替修正后的动态能力验证。[唯一argv修正提案](permission-argv-amendment-20261011.md)只把原规则分成独立argv，不增权限；提议新具名单次probe-02及双席结果确认、显式上限18次CodeBuddy/2次native，尚待S1双席支持。旧失败仍计成本，未自动再试。

S1两原席已正常返回：[GLM原票](review-continuation-s1-glm.txt)/[调用](review-continuation-s1-glm-calls.json)、[Kimi原票](review-continuation-s1-kimi.txt)/[调用](review-continuation-s1-kimi-calls.json)。各一次整包Read因长度上限失败，随后分段取证；不隐去工具错误。两席明确支持唯一probe-02：仅拆allow/deny argv、新TEMP根及session、原矩阵与12turn/300秒上限、首异常停、旧失败保留。显式预算修订已获两席支持：18次CodeBuddy/2次native，上调的3次只用于本次修正探针及两席结果确认，不预批第三探针。

专门发包人获准在本行政检查点后启动该探针，产品作者仍须等待逐格证据、两席结果确认及native计划监督。GLM新增B17绑定bootstrap序列化；GLM B18/Kimi B11绑定产品adapters+sample权限及写集来源，须后继跨包对齐，不并入R-log/R-junction，live继续禁止。CLI/session/scoped hook是否实际配置仍unknown；不能把GLM条件中的“默认无hook”表述当成已验证宿主事实。旧权限finding不由集成者关闭。

probe-02已结束：[原件](permission-probe-argv02-20261011.txt)、[逐格原生结果与字节元数据](permission-probe-argv02-20261011-metadata.json)。37.462秒，真实deepseek-v4-pro与新session正确；12次native调用为Read3/Edit3/Write6。P1/P2实际成功且精确字节满足；N1–N7各有权限拒绝，目标不存在或种子摘要保持，N4已先读成功，N7实际使用含../的路径。没有额外fixture文件。CLI报告num_turns31而请求12，继续不声称硬轮数保证；T1未实测、hook/真实memory全域边界未知。该结果仅为限定fixture能力证据，产品作者仍冻结。

下一准入仅为两原席各一次probe-02结果确认；无新探针、无代码作者、无live。两席确认后交原生Kimi计划监督，再判断已审三个包的作者准入。产品权限B18/B11仍开放，后继范围调查不扩大本批写集。

## 2026-10-10已冻结过程与结论

2026-10-10用户再次明确：已有候选发现缺陷，也必须多轮审核，由专门发包人依据审核派发。根此前把静态检查/测试失败直接派成修复包，缺少这条链，属于流程偏离；不以后来的通过倒填此前批准。

首次独立审核前已冻结新增实现/修复调用并收回所有旧writer：P2/P5/P6正常退出；P1超时收回、exit1且无最终交付，不按写入文件数算完成。P5的14项局部测试通过；P6此前20项在途组合诊断为2失败、1错误，因无冻结源码绑定只作线索。收回全部writer后的[组合验证](verification-g1-r1.md)仍未通过，进入正式审核而非直接派修。下表保留初始候选责任归属与事实；后续仅“首轮审核与证据归属”中的具名审核范围可由发包人启动。专门发包人为本任务独立Codex协调实例`package_dispatcher`；根只收证、验证、维护此入口和执行受审集成，不再直接给实现者派修。

后继流程：冻结组合候选及功能包写集 → 独立CodeBuddy GLM/Kimi多方审核 → 发包人以准确候选与稳定finding_id发布修复包 → 实际CodeBuddy执行 → 原席复审逐项关闭 → 原生Kimi监督核验 → Codex接收/集成。检查线索、测试通过、作者交付均不能替代审核意见。两席首次意见独立，复审记录候选变更与未决项；监督不缺席、不由集成者代签。G1、live与Git合入仍各自举证。

首轮历史候选已固定为`34bce56b624cf521b33dc5b4916bd1c8e7711536`，独立detached审核树已创建且clean。两席只读首轮审核已完成并要求修改；新实现/修复仍须正式审核后的具名包。共享目录在途写集隔离及此前未按审核先派修均提交审核，不冒充已完成产品资源隔离。

准确候选checkout又做一次组合验证，见[原始输出](verification-g1-frozen-r1-output.txt)、[内容清单](verification-g1-frozen-r1-manifest.json)、[绑定元数据](verification-g1-frozen-r1-metadata.json)：131项、20失败/2错误/2跳过及85行硬限失败，41文件前后清单一致，清单SHA256为`9ab421ccb7f21506a5b39b38180bf702eb3a0053fddf0d54ed476af41b6071d5`。本次为首轮正式审核的主验证证据；先前工作树的3个error保留为历史异常，不能用复验较少错误数抹除。复验原因是Git对历史文本的换行规整，未改产品代码来获得不同结果。

本轮后继P2日志、P4清理、P7接管及P1诊断的四次调用已全部退出，当前writer为0：[实际调用归档](repair-g1-second-batch-calls.json)。只在候选feature分支汇集P2/P3/P4/P5/P7代码供组合验证，未接收、未合入main，禁止新的writer调用，剩余工作是只读复审与监督。

- P2日志：作者[原件](repair-p2-log-r1.txt)，分支候选`ec9e9d5cdf48cdaa62e57e8c2a21f3d23cf6a325`；[31项限定验证](repair-p2-log-r1-tests.txt)为29通过/2错误，[摘要](repair-p2-log-r1-test-metadata.json)稳定。新增junction测试清理阶段WinError3、重复验证碰到既有日志拒绝覆盖仍待原席判断；flow与review预算两跨包用例通过，不可写成三个跨包全绿。
- P4清理：作者[原件](repair-p4-r1.txt)，候选`544c5dd1b7fb66ed28e6bdab9975b897190c308d`；[16项清理回归](repair-p4-r1-tests.txt)全部通过、[摘要](repair-p4-r1-test-metadata.json)稳定。只改cleanup.py，未复制或搬动旧测试；待组合复审。
- P7接管：作者[原件](repair-p7-r1.txt)，候选`0e4e32cee37991d47fc8ef617d2465057a7e3b9a`；[5项门禁边界测试](repair-p7-r1-tests.txt)通过、[摘要](repair-p7-r1-test-metadata.json)稳定。保留正确的Codex草稿实现及作者事实，新增有意义测试；云CI未知。
- P1诊断：实际调用越界新建两份宿主记忆，交付拒收；两新增文件已按原Write内容核对、备份并撤回，其他记忆未变。详情及本机权限能力静态证据见[宿主记忆边界记录](runtime-memory-boundary-evidence.md)。控制文件句柄机制测试通过，只是机制示例；历史根因仍未知，未经原席允许不得改Store或加重试。

第二轮准确候选为 `2e9f192c8127956f09c619ff640d763b62369e30`，审核树 `D:/project/agent-coop-g1-review-r2` 为干净 detached checkout。[统一验证原件](verification-g1-frozen-r2-output.txt)实际为139项、135通过/2错误/2跳过、exit1（32.399秒），无代码/函数硬规模失败，8项软目标仍须审核解释；219条本地链接机械有效不代表锚点或远端验证。[43文件验证前清单](verification-g1-frozen-r2-manifest.json)与[验证后清单](verification-g1-frozen-r2-manifest-after.json)逐字节一致，SHA256 `c4fc78655129d96e8729f3a45cd7fa9eb63b8cb57653b91f49a1b6294877418c`；[绑定元数据](verification-g1-frozen-r2-metadata.json)记录Git状态为空。两错误仍为验证日志目录复用被拒绝及junction测试清理WinError3；P1历史WinError5本次未复现，根因仍未关闭。冻结验证准入只允许发包人发起两原席各一次只读R2及其后原生Kimi监督，不准入新作者、产品接收或live。

第二轮两次CLI尝试于2026-10-10T14:54:14Z结束，均返回 `No conversation found with session ID`，未产生实际模型init或有效审核final；进程exit0不算审核成功。专门发包人只读核查原会话定位与cwd关系，当时尚无新内容审核轮；全程无新增作者调用；失败原件（[GLM](review-g1-glm-r2-session-unavailable.jsonl)、[Kimi](review-g1-kimi-r2-session-unavailable.jsonl)）和[调用绑定](review-g1-r2-session-unavailable-calls.json)保留；这里仅归档无会话错误，不提交私有历史。

会话定位已由[本机源码及原session文件stat核查](review-g1-r2-resume-cwd-evidence.md)证实：普通resume从当前projectDir查找，projectDir绑定realpath(cwd)；未读取或复制私有历史。原审核目录 `D:/project/agent-coop-g1-review` 已从干净34bce56b受控切到同一干净2e9f192，[切换回执](review-g1-r2-cwd-switch.json)、[切换前全部tracked摘要](review-g1-r2-cwd-before-tracked.json)、[切换后43文件清单](review-g1-r2-cwd-manifest.json)保留；后清单SHA与R2验证完全一致。发包人获准在原cwd保持原session各一次恢复，只读权限与20turn/600秒预算不变，失败不得改新身份或放宽权限。实际恢复已于14:57:43Z由发包人启动，两席init已核对原模型及原session；恢复成功不抹除前两次失败尝试。

[Kimi原席第二轮原票](review-g1-kimi-r2.txt)已正常返回，[实际调用](review-g1-kimi-r2-calls.json)绑定原模型/原session、Read3、0工具错误，整体 **CHANGES_REQUESTED**。原B01–B05、B07/B08及P7接管子项closed；B06日志复用及junction回归错误open，B09历史根因open；新增 `g1-kimi-B10` 要求下一writer前独立审核profile并完成正负路径验证。跨包日志owner尚须具名裁定，不授权自动第三轮修复。两席复审均已结束；后继原生监督结论见下文。

[GLM原席第二轮原票](review-g1-glm-r2.txt)正常返回 **CHANGES_REQUESTED**；[实际调用](review-g1-glm-r2-calls.json)为原模型/原session、Read9+Grep1、0工具错误。原B03/B04/B05/B06a-b/B07/B08/B09关闭；B02仍open，由新增B13日志重复调用合同缺口与B14junction测试清理错误承接；B11根因unknown；B15/B16记录两次权限偏离，数项软目标内聚说明尚缺。B10b仍open：该席称未见2E/3E运行归属标注；本入口前述原始工作树3E与准确checkout2E已分别绑定原件，历史验证原件不改写，但输入未使该席确认，不能由集成者自行关项。

第二轮内容审核已到预算停止点。下一writer前须先完成受审权限profile的正负路径验证；跨包日志策略及owner须具名对齐，P1只诊断不自动改Store/重试。即使GLM认为B14修复范围明确，也不跨过最多两轮与writer冻结规则自动发第三轮。原生Kimi已对相同候选、双票、过程偏离和当前状态完成独立监督；其意见不能代关原席finding。当前无G1 PASS、无live、无main合入。

[原生Kimi监督原件](supervision-g1-r2.txt)及[实际调用元数据](supervision-g1-r2-calls.json)已归档，正常结束：实际session `session_01c9e97b-7bac-46b6-8db5-71e73d9d68cf`，模型unknown，Read6，160.200秒。监督 **PASS仅表示认可继续blocked的状态、证据、责任人与停止边界**；无新增监督阻断，不是G1内容PASS，不关闭原席finding，不授权新writer/第三轮/接收/main/live。两次会话定位失败、两次原席恢复与本次监督均保留，不从成本中删除。复审后43文件摘要仍为 `c4fc78655129d96e8729f3a45cd7fa9eb63b8cb57653b91f49a1b6294877418c`，审核树clean；全部调用已结束。

准确送审输入的文件/hash索引保留为[GLM索引](review-g1-glm-r2-input-index.json)、[Kimi索引](review-g1-kimi-r2-input-index.json)、[监督索引](supervision-g1-r2-input-index.json)。[监督所见行政状态快照](supervision-g1-r2-status-checkpoint.txt)仅为不可变历史输入，不是第二个当前状态owner；当前事实仍由本入口维护。完整CLI流/私有历史/宿主记忆备份不提交Git。

续作入口：由专门发包人提出后继有界审核/修复请求，先明确权限profile验证与日志跨包合同/owner；保留P1根因未知、软目标说明缺口和GLM B10b输入可见性。各原席只关闭自己的finding，监督不替代内容审核；Codex仍仅协调、验证与受审集成。本轮两次内容审核额度已用尽，不自动追加模型调用或绕过门禁。

## 首轮审核与证据归属（历史过程）

首轮共6次实际调用，完整身份、退出、工具错误及原流摘要见[调用元数据](review-g1-r1-calls.json)。输入不可达的两次GLM原文也保留：[首次](review-g1-glm-input-unavailable.txt)、[补充](review-g1-glm-input-followup.txt)；另两次超轮次没有有效最终票，不能用进程exit0算通过。两席有效原票已归档：[GLM原票](review-g1-glm-r1.txt)、[Kimi原票](review-g1-kimi-r1.txt)，均为CHANGES_REQUESTED。GLM通过同一session的一次零工具结论调用收回：155.999秒、exit0、result success、实际tool_use=0；此前读取超轮次与权限失败不计为通过。Kimi补充读取后正常返回。实际模型分别为glm-5.3与kimi-k3-2，此首轮阶段监督尚未启动。

有两席共同支持的小包由专门发包人准备并按受审范围派发：P2函数硬规模、P3路径与归档、P5状态拒绝退出码；必须各自独立工作树、准确基线、finding映射及限时调用后才可启动。P1发布异常、P2/P6日志合同、P4共享路径边界、P7真实作者接管仍待明确范围，不因测试失败直接派修。此为修复范围准入，不是候选通过。

2026-10-10T14:18:19Z发包人曾启动三个独立工作树修复调用，但自行将工具集合增加PowerShell及允许作者commit，缺少本轮受审依据。根核查实际参数后要求回收，14:20:13–14Z三调用已按PID及创建时间核对并终止，均无final。结束后原流显示实际PowerShell调用P2=4、P3=1、P5=6，内容为目录/git只读/测试或版本探测；没有将这些探测记作通过。仅P2留下runtime.py部分改动，保留未交付来源；P3/P5树无产品改动。随后只允许恢复既有Read/Glob/Grep/Write/Edit后具名替代，每包最多一次；验证与commit由协调者执行。此事作为发包配置偏离保留，不由测试通过追认，不从调用成本中删除。

原票中的证据口径不改写，以后继核对补充：P1局部实际33项中1个error，不能称全部绿；先前工作树验证20F/3E，准确冻结checkout验证20F/2E，两次均失败且旧异常保留。41文件清单仅两个文档不同：role-correction.md与runtime-tool-evidence.md，实际读取这两个文件的工作树字节后仅作CRLF→LF规范化，其SHA分别精确等于冻结清单d4bd5e764b30198bb6011f896398c216b9c50402baea6ee1fdd0110de0f50c60、169c2217345d0f757975be3a080decd5058bce5f927cd75f5fd04391f90ed9f1。其余39文件SHA相同。导航漏解释第二个文档是输入组织缺口，不能要求审核席自行猜测。以上核对不代替原席关闭finding。

首轮范围补充已由两原席完成（[两次调用元数据](review-g1-boundary-b-calls.json)、[逐字节换行证据](review-g1-crlf-byte-evidence.json)，累计首轮审核8次实际调用）：[GLM附录](review-g1-glm-boundary-b.txt)、[Kimi附录](review-g1-kimi-boundary-b.txt)。两席支持P2日志边界、P4清理范围、P7真实接管；P1仅支持诊断测试，代码修复仍未准入。接口owner已发布[日志目录后继澄清](interface-log-directory.md)，旧冻结合同不改写；P2同一个包单writer继续，P6消费方不动。附录纠正原票证据口径并关闭相应哈希说明缺口，不构成G1候选通过。截至此首轮附录时，修复后的原席第二轮与原生监督尚未发生；当前状态见本入口顶部。

P2/P3/P5本批三次被回收尝试及三次替代调用的实际身份、工具、退出、原流摘要与P2部分产物交接见[调用归档](repair-g1-r1-calls.json)。P2替代作者明确接管被回收调用的既有改动，没有把它伪称替代调用新写；三包均由实际CodeBuddy产生/接管，根只运行验证、冻结候选与整理证据。

|首批修复候选（P2已由上方日志候选承接）|实际局部验证|接收边界|
|---|---|---|
|P2规模 `8183c5d1fddba73ff1ae6f9e978f6dde0acc33e7`；[作者](repair-p2-r1.txt)|[25项runtime通过](repair-p2-r1-tests.txt)；[摘要](repair-p2-r1-test-metadata.json)；规模hard_failures为空|日志目录问题仍须同包续作，未原席关闭|
|P3路径/归档 `972891513e8387d761dfa3415199ecb57b18d745`；[作者](repair-p3-r1.txt)|[13项路径](repair-p3-r1-path-tests.txt)+[10项归档/备份](repair-p3-r1-archive-tests.txt)，共21通过/2权限跳过；[摘要](repair-p3-r1-test-metadata.json)|仅paths/archive改动，cleanup及旧test_archive未改；待组合复审|
|P5 CLI `cb46a72d8db4bae174eaf6fb6b97b83bc92d6213`；[作者](repair-p5-r1.txt)|[14项CLI/Web通过](repair-p5-r1-tests.txt)；[摘要](repair-p5-r1-test-metadata.json)|仅cli/test_cli修改；未运行浏览器JavaScript，待原席复审|

P1两个原失败用例在准确34bce56b冻结源码上执行最多20轮、首失败即停止的诊断；实际20轮×2项均通过，[原始输出](p1-publication-diagnostic-existing-tests.txt)及[逐轮记录/摘要](p1-publication-diagnostic-existing-tests-metadata.json)保留。没有外部句柄或历史根因证据，不能关闭GLM B11/Kimi B09，也不据此批准代码重试策略。

三包独立树验证前后相关文件摘要一致，均未合入main。P3独立树仍含基线runtime的85行硬失败，不能把局部通过说成整树verify通过；P2规模候选会在组合候选接收阶段统一验证。


## 冻结候选的包归属（34bce56b）

来源：用户要求按功能拆小包并行开发，并明确CodeBuddy实现并发默认4、用户可配（2026-10-10）。以下分配承接[职责纠偏](role-correction.md)，替代把所有集成入口交给一个作者、等待core/archive整体完成才启动的安排；并发沿[design §7.3](../../../docs/design.md#73-资源与预算)及用户新指令，旧G0原件和纠偏记录中的临时2路安排成为历史，不改写原件。这里的P1–P7是本请求工作包编号，不是路线图产品阶段。产品、测试与CI的实际作者均为CodeBuddy + deepseek-v4-pro，Codex只协调、验证与集成。

|包/验收单元|唯一写入范围|就绪与当前状态|
|---|---|---|
|P1 状态与续作|`store.py`、`runner.py`；`test_store.py`、`test_runner.py`|新实际session agent-coop-p1-state-20261010在620.4秒时收回，超过600秒人工看护20.4秒，exit1且无final；33项局部验证有1个STATUS替换错误。不能称交付完成，待正式审核|
|P2 有界进程与协议|`runtime.py`、`adapters.py`；`test_runtime.py`|原core实际session修复调用正常退出0，25项局部tests通过；runtime._collect为85行超硬限，日志目录与消费者合同冲突仍在；待正式审核|
|P3 路径、归档与备份|`paths.py`、`archive.py`；`test_paths.py`、`test_archive.py`|三阶段实际调用均退出0，新增回归后与P4合计39项出现18失败/2skip；见[原件与分诊](implementation-archive-evidence.md)，未再直接派修|
|P4 清理计划与执行|`cleanup.py`；`test_cleanup.py`（拟拆）|与P3分开审核；当前回归调用已结束且写权回收，测试拆分/修复仍待正式审核发包；archive薄转发及共享helper边界需审核明确|
|P5 CLI与只读Web|`cli.py`、`web.py`、`__main__.py`；`test_cli.py`、`test_web.py`|实际deepseek-v4-pro/session agent-coop-p5-cli-web-20261010退出0，4文件实际改动，14项局部tests通过；见[原件](implementation-p5-r1.txt)、[元数据](implementation-p5-r1-metadata.json)、[验证](implementation-p5-r1-tests.txt)；待独立审核|
|P6 固定流程与精确门禁|`sample.py`、`gates.py`、`checks.py`、`supervisor-agent.md`；`test_sample.py`、`test_gates.py`、`test_flow.py`|实际deepseek-v4-pro/session agent-coop-p6-flow-gates-20261010退出0，gates及3测试文件实际改动；见[原件](implementation-p6-r1.txt)、[元数据](implementation-p6-r1-metadata.json)、[诊断](implementation-p6-r1-tests.txt)；存在跨包日志目录失败线索，待冻结审核|
|P7 统一验证与CI|`verification.py`、包初始化文件、`.github/workflows/verify.yml`；必要的`test_verification.py`|仍为未接收Codex草稿；只维护唯一验证入口，不复制测试清单；待独立审核后由专门发包人发布接管包|

表中源码相对`agent_coop/`、测试相对`tests/`。每包携带固定接口、写集、实际作者session、局部检查结果、未决项及交接；无关文件不得顺手修改。共享API变更先交集成者协调owner，不通过复制实现绕过依赖。当前未接收源码都属于候选。

依赖约束落在接收点：P5可先按Store/sample公开接口开发；P6可先按runtime/archive合同开发；组合验证才要求这些提供方通过。P3/P4共享receipt合同但写集分离；同一作者session不得并发续接。每次实际调用结束释放槽位，待修包重新排队，避免大包持续占有槽位。包完成可独立验证、进入只读预审；最终G1仍审核同一个精确组合候选，包通过不能替代系统验收。

## 当前未决项与门禁

|事项|责任人|当前事实与下一步|
|---|---|---|
|首轮缺陷|两原审核席及专门发包人|缺陷身份、范围和关闭依据以原票及R2逐项结论为准；R2已关闭多项，未决见顶部，不另维护precheck重复状态|
|G1独立审核/原生监督|CodeBuddy GLM、CodeBuddy Kimi、原生Kimi|两原席R2均CHANGES_REQUESTED；原生监督仅认可继续blocked，全部调用结束；不以监督PASS或局部关闭预支实现通过|
|四角色live及归档backup清理演示|受审sample runner，Codex仅启动/验证|未启动；必须G1通过后执行；暂停续作、四次调用、local_only与固定scratch范围保持不变|

本表是开发请求的人工交付检查点，不冒充产品运行状态数据库。子模块原始回执和确定性验证由协调者归集；退出码、测试通过、评审接收、Git合入与发布分别举证。

core/P1/P2作者身份、原始最终回执与P1超时无final事实统一见[核心候选证据](core-candidate-evidence.md)；归档三阶段见上表入口。均为待审事实，不计独立通过票。

## 预算与边界

- 已发生bootstrap调用均结束或已收回：核心前3次+P2修复、归档3次、P1/P5/P6各1次。P1超时缺final且人工看护存在20.4秒超差；不把手工看护说成产品硬墙钟保障。
- 原P1/P5/P6必要复修预算不构成继续派发授权；由专门发包人依据正式审核发布下一包及预算。用户指定默认4路继续有效；活跃调用由发包人核对同账号总数，已结束不代表已接收。
- 此次并发在bootstrap中由Codex人工派发、文件写集隔离；当前候选树内的在途作者尚不具备产品独立工作树资源隔离证明。产品仍须实现设计中的独立工作树/claim保障；本轮不得将人工并发冒充已实现通用Scheduler或team.yaml解析器。
- 上述不改变产品样例的4次总模型调用预算，也不改变G0/G1各最多两轮评审或原生Kimi单次10分钟看护。Codex草稿接管保留原作者事实，不要求无目的重写。
- 工具目录与实际选择的差异见[本机权限证据](runtime-tool-evidence.md)；不把命令参数或init目录当OS沙箱证明。
- 尚未清理样例fixture以外的数据；不push、不上传、不启用OS定时任务。完整产品P1/P2/P3仍未交付。

证据归档校验：R2与监督收束后的240条本地Markdown路径与62条设计验收编号机械检查通过；新增原件/元数据按真实字节归档，并在提交前对照Git暂存blob。为保留冻结输入及原输出的真实摘要，归档不规范化其CRLF或原始测试subTest行尾空格；默认`git diff --cached --check`因此报告原始证据空白，不能称该默认检查全绿。此处适用AGENTS的历史原件保真规则，未修改产品文件或放宽产品规模/测试门禁；原始CLI完整流仍仅宿主临时保存。
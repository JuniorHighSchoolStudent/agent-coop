# 后继内容 R2 集成检查线索

范围：准确产品 ed65079e6fd2cd3afc09ec871817cfb11c621b76 与独立 TEMP 诊断候选；维护者：Codex集成者；状态：原席送审输入，不是独立票或接收结论。来源：两原席内容R1及实际 CodeBuddy 修复。

## 已交付与验证

- junction作者[原件](repair-continuation-junction-r1.txt)/[调用](repair-continuation-junction-r1-calls.json)：deepseek-v4-pro，90.465秒，12工具/0错误。唯一 test_runtime.py +2/-12，作者冻结 e5b9873d9455115dcc0a5045314337ffb721a031；根只commit/cherry-pick，未写产品代码。
- publication作者[原件](repair-continuation-publication-r1.txt)/[调用](repair-continuation-publication-r1-calls.json)：deepseek-v4-pro，205.338秒，17工具/0错误，仅原TEMP脚本1次Write/1次Edit。[写集核查](repair-write-scope-audit-20261011.json)不扩成全宿主审计。
- [准确verify元数据](verification-continuation-r2-metadata.json)/[输出](verification-continuation-r2-output.txt)/[前清单](verification-continuation-r2-before.json)/[后清单](verification-continuation-r2-after.json)：独立clean detached ed65079，144项=142通过/2既有WinError1314跳过，exit0，33.52612秒。43文件前后62697fa6367ce3598ae7fbb98103915a879f67fdd541f7bf773f75ed7685980a；全部28项runtime包含其中，junction真实通过。无硬限，test_runtime 464行软目标仍请原席判断。POSIX分支没有在本机实跑；312本地链接不等于浏览器/远端/锚点/云CI/live验证。

## 请求原席裁定

junction修复采用平台分支内直接注册os.rmdir/os.unlink，删除重复helper，不导入仍吞异常的旧helper；错误完全上抛，比只容忍FileNotFound更严格。LIFO、断言和原skip条件未动。请各自判断B19/B12及新revision软目标理由，不由根自关。

[诊断候选R2字节原件](diagnostic-publication-candidate-r2.txt) SHA fd3fcf135f9ffac634b5610ce44d327ee256dcd79975d7305d16036c1c3d0438；原TEMP脚本nlink1/非reparse，静态AST解析成功，未执行。425行；_observed_replace46行、_run_one56行、main51行，作者已在原件给出内聚说明。任务TEMP锚定、临时tempdir/wrapper恢复、失败原现场保留及证据degraded应由原席复核。

审读注意点（线索，不是修复指令）：失败保留依赖CPython TemporaryDirectory._finalizer.detach；无该属性时当前不额外报错。被测失败与diagnostic_degraded均使用exit1，但summary区分原因。日志追加而非run id隔离；本批只允许在原目录无既有输出时唯一执行。循环120秒仅内部截止，不是硬中断；外部看护必须独立。不得扩为外部句柄枚举、Store/Runner修复或重试。作者末段任何超出范围建议不构成授权。

R1顺序条件交集须显式裁定：GLM要求重冻再审方可执行；Kimi要求执行并双席看结果。当前先送本轮R2静态审，未提前执行。请明确可否批准准确hash的一次有界运行、由最终native核查运行原件且保留历史B11/B09为unknown；如仍须后续双席结果票，应保持待办，不用native代签、不超额度。计划执行在准确ed65079 checkout，Python 3.12.14，以-B禁写pycache；任务TEMP无输出种子且路径非reparse，120秒外部子进程上限，30轮×2内部上限，首失败停；前后manifest/脚本hash/真实退出及stdout、summary、JSONL分别归档，不改harness。

产品权限B18/B11后继新合同/实现仍不准入本批，不挪用bootstrap成功。两修复用后15/18 CodeBuddy，本次原席各一次后17/18；最终native尚1次。没有多余自动续审/实现许可；准确候选接收、main/live与未知根因分开裁定。

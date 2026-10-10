# CodeBuddy --resume 工作目录绑定核查

日期：2026-10-10 UTC。范围：只读安装源码与会话文件元信息；未调用模型、未读取会话正文、未移动历史、未切换工作树、未修改产品或宿主配置。定位已停止。

## 安装身份

- CodeBuddy 版本：2.164.0。
- 源码：C:/Users/june/AppData/Roaming/npm/node_modules/@tencent-ai/codebuddy-code/dist/codebuddy-headless.js。
- SHA256：f9affe2aed036a3a3ee8486b82e77b176a2a4b21f7bed721074c1c1e4a312e65。
- 下列偏移为 UTF-8 解码后的 Unicode 字符偏移，不是字节偏移；行号属于压缩源码。

## 源码直接证据

1. SessionAdmission.findExistingSession，L2809 / 12938208：内存检查后调用 sessionManager.get(id)，未调用跨项目查找。
2. SessionManager.get，L2816 / 13080233：委托 sessionStore.get。
3. SessionStore.get，L2817 / 13125553：没有显式 cwd 参数时，仅在当前 projectDir 查找和反序列化 session。普通 CLI --resume 传入 id，不传旧 cwd。
4. getAcrossProjects 是其后的独立方法；普通 --resume 路径未使用。
5. SessionStore.getStorageDir，L2817 / 13110000：返回 paths.getHomeProjectDir()。getStorageDirFor，13110211：显式 cwd 则 canonicalize 后生成目录，否则使用当前目录。
6. getSessionFilePath，L2817 / 13116664：普通 session 路径为当前项目目录下的 sessionId.jsonl。
7. PathUtils.getHomeProjectDir，L2565 / 10547822：projects 根目录加 getCompressedWorkDir()。
8. getCompressedWorkDir，L2565 / 约 10556200：压缩 canonicalizeStorePath(getWorkDir())；canonicalizeStorePath，10556330：fs.realpathSync，失败回退原路径。
9. compressWorkspacePathName，L2565 / 10545543：将路径分隔符和冒号规范成连字符，折叠/去边缘连字符；长名称截断加 hash。
10. --resume-create-missing，L2809 / 12937221：缺失时创建新的空 session，不能作为原审核身份和历史连续性的证明。

## 仅文件系统元信息验证

- D:/project/agent-coop-g1-review 与 D:/project/agent-coop-g1-review-r2 均存在，为正常目录；未观察到 junction/link。
- Node fs.realpathSync 返回各自同名绝对路径。源码压缩计算分别为 D-project-agent-coop-g1-review 和 D-project-agent-coop-g1-review-r2；本机实际旧存储目录首字母小写，Windows 大小写不敏感。
- 已观察原目录 C:/Users/june/.codebuddy/projects/d-project-agent-coop-g1-review。
- 文件 agent-coop-g1-glm-r1-34bce56b-20261010.jsonl 存在：735176 字节；creation UTC 2026-10-10T13:56:40.2145122Z；lastwrite UTC 2026-10-10T14:27:04.6155889Z。
- 文件 agent-coop-g1-kimi-r1-34bce56b-20261010.jsonl 存在：729734 字节；creation UTC 2026-10-10T13:56:40.2370183Z；lastwrite UTC 2026-10-10T14:29:28.8856384Z。
- 两文件只检查 Get-Item 元信息，未读取内容，未复制或计算内容 hash。
- 两个同名 .meta.json 文件不存在；源码支持 inline session-meta，不能仅据此判为损坏。
- C:/Users/june/.codebuddy/projects/d-project-agent-coop-g1-review-r2 不存在。

## 最小恢复方向与限制

普通 --resume 的失败与 cwd 绑定查找一致。根提出在原 D:/project/agent-coop-g1-review 的 clean detached 树切到准确候选 2e9f192、复制固定审核输入并重新计算 43 文件 manifest，然后在原 cwd 用原两个 session ID 恢复，符合已核源码机制。不需要移动历史、改 session ID、fork 或使用 --resume-create-missing。

本次没有执行恢复、checkout、输入复制或模型调用。文件存在不证明内容可解析，也不证明恢复后身份、模型和输入版本满足审核合同。若后续单次有界恢复失败，应记录 R2 unavailable/blocked，由独立监督收束，不能循环或伪造延续。

# S3后继方案双席调用准入

范围：只读设计交叉审核；维护者：Codex集成者；时间：2026-10-11；状态：准确双席调用获准启动，尚无有效审核票、native监督或产品作者准入。S2失败原件保留，不以本准入倒签。取消固定轮次依据见[范围补充](scope-amendment.md)，当前状态归[result](result.md)。

候选`ec64819e9725d84c06f671bd5687c01124e35f51`，只读cwd为`D:/project/agent-coop-governance-review-s3-20261011`，唯一输入目录为其`coordination/.runtime/governance-s3/`。不存在另一个有效s3-final输入。五个作者树仍在旧基线，本准入不授权作者启动。

| 绑定 | SHA-256 |
|---|---|
| policy | 7f738c4c95ad36e2bf2b52b47034ab5b324be58d7ffa4446334003403564a76f |
| index | b3b1542117c1910a7cd1d0653219ef85d1655c8a337e7d0ab39cc0dc002f94e4 |
| subject | e4dc9edbd11ffc4b1323b8a16644b7c396066a708a07ce62d55e99b1db5e14f8 |
| required-reads | 71dd18a8b0a00f2348a8e03c623e56a44f49986781db75bcbfac1db7ddd17186 |
| prompt-bindings | f682a85601cdd609990dc55b22e07fb81b0b1ab7d9f92d230527c80b1d5edaee |
| PREPARATION | af2639f767e93eff1ba9f75f99a7545523df5ae25b524a132b85d55743234674 |
| independent-check | 621e41b7bdabe1007835d47ab3e6d04089dc8afee98b567c100ad0e3cd2fb674 |

根独立核78份artifact原字节、16条conditions及subject/package/policy摘要、runtime文件；其中59份源逐字节对照Git准确commit或本机原件。独立调查员核columnar两席90×7全部值、context/body原字节、每席76项要求的7113逻辑行及policy自身plan/accept六项full义务。上述仅行政准备核验，不是模型实际Read或有效审核票。

| 席位 | 请求模型 / fresh session | 完整prompt SHA-256 | 最终计划命令行UTF-16含NUL |
|---|---|---|---|
| GLM | glm-5.3 / agent-coop-governance-glm-s3-20261011-6df319c2 | d6e73d00625131f9191425aa785e32f58e74882703d5892c6039470df393d569 | 28344 |
| Kimi | kimi-k3-2 / agent-coop-governance-kimi-s3-20261011-e4c78109 | c240ffd1ffb72d0e5578ee04737f8004a04e8d3e448d6fe56b438160203703b4 | 28348 |

完整参数按受审subprocess.list2cmdline编码，Windows反解往返逐参数相等；实际启动时仍须与planned-invocations逐元素核对。计划值不冒充实际观察。不切stdin、不截断材料、不添加json-schema隐式续跑。

每席维持20模型响应/600秒/8MiB、Read/Glob/Grep。预计675667显示UTF-8字节、148124内容token，单片最高11980。body建议5–8项Read并留3响应；90项下固定5项节奏需21响应，无法完成，实际须平均至少5.295项（如6–8）。根接受本次只读审核的已披露执行不确定性，不增加单次上限；超时、漏读或无效final均拒绝，不能以重试轮数或尾部PASS豁免。

dispatcher_next唯一启动者，复用固定wrapper与受审S3 watch-plan；watcher实际ready须先于wrapper，记录原Process/SafeHandle及目标CLI身份。沿600秒单调截止和8MiB输出边界看护到观察到的后代结束；conhost不当node/model。bootstrap轮询不能证明控制者崩溃或扫描间脱链包含，W/R2产品缺陷仍未关闭。两席完整严格JSON及实际正文覆盖均有效后才准备native材料；当前不授权native或作者。

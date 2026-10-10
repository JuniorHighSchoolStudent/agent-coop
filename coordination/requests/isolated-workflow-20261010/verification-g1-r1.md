# G1首轮待审候选验证

范围：本轮所有writer收回后的组合候选；维护：Codex集成者；状态：验证未通过、待独立审核；来源：本机实际运行及前后内容摘要。不是接收、合入或live证据。

命令为`python -m agent_coop verify`，实际Python为3.12.14，Windows本机。结束于2026-10-10T13:48:41.6378475Z，命令退出1。[完整结果](verification-g1-r1-output.txt)：131项tests，20个failure、3个error、2项symlink权限skip；另有`runtime._collect`85行超过80行硬上限。155个本地Markdown路径通过，锚点、远端URL、浏览器JavaScript和云CI未验证。

运行前后对41个产品、测试、CI、合同文件计算SHA256，清单完全一致；[源码清单](verification-g1-r1-manifest.json)的SHA256为`6544db897487c0e71c731df4cf4bdfffe7a1286d3694816b54c4fb584e321526`，[运行元数据](verification-g1-r1-metadata.json)保留实际退出及一致性。候选由包含此记录的后继Git提交固定，审查从该提交的独立只读工作树进行；当前结果入口与审核派发原件记录该准确commit。

归档/路径/清理反例、发布文件替换异常、日志目录跨包冲突及规模问题均为审核输入；稳定审核finding及其修复边界由独立审核者裁定，再由专门发包人派发。这里不根据失败自行批准修复，不将旧局部通过覆盖组合失败。

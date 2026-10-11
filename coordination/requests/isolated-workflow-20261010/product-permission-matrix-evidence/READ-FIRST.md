# 产品权限矩阵具体输入（prepared，不是执行准入）

产品精确候选 fe2e1b6b03cde7763f6f2c974d909edf6c2ce708；源码树 D:/project/agent-coop-pp-review-c2；行政双C2/N4方法归档 2e2090e8ae0dbf36f0ef73865710ec1ce10f9b89。
本目录 preparation-metadata.json 固定全部配置、提示词、fixture、N4预期、源码工作字节与Git blob分别摘要。metadata SHA256=38c907f2ab2ea3b1b9eb983aba3293c56c192958154bc95e12cc555dd86d2b0c。

已做一次现有 sample.initialize；没有 dispatch/invoke/Runner/record/模型调用。准备中的一次 _build_env 参数错误已由 preparation-error.json 原样记录，改用正确 environment 子对象后只做无进程环境/argv预计算；不重init、不变基线。当前本批预算仍12/15 CodeBuddy、1/2 native。

## 精确输入

- 样例根：C:/Users/june/AppData/Local/Temp/agent-coop-product-matrix-0f9954ef648748d5ac686ddf4fa52345/pilot
- 外部audit：本目录；sibling位于同父目录/sibling。
- raw-profiles.json 是实际四角色初始化输入；仅implement未来调用，其他三项只经validate_profiles，不能称实测。
- derived-implement-profile.json 是sample实际派生权限；唯一可写文件pilot/workspace/feature.py，600秒/8MiB/20turn，deepseek-v4-pro。runtime._build_env按真实白名单构造，仅记录名称与四个公共固定值，不记录宿主值。
- matrix-prompt.txt：P1 Write、P2 Read+Edit，N1到N7各一次Write；存在的seed/STATUS先Read；读前置错误不是写权限拒绝；每个负例按顺序实际观察，任一写成功立即停止，无回滚/扩权/替换目标。
- argv-template.json：session仅占位，明确不是实际argv。不得patch uuid、command、Popen或绕过dispatch；真实session由原产品dispatch新建，实际requested/session与原始init核对。事后command重建不可冒称进程命令实测。

## N4预先冻结

state-before-reservation.json 为S0（calls_used=0、revision=0），expected-after-reservation.json 为深拷贝后仅两字段各+1的S1。expected-STATUS在任何dispatch之前由同固定Store._write_status生成到本外部audit，不写实际STATUS；initial-STATUS保留初始化字节。当前实际SQLite/STATUS分别仍等于S0/initial。
执行如果获根准确一次准入，只用现有 sample.dispatch(root,S0,'implement',prompt)。返回或异常后先保存实际STATUS字节，再Store.read；以Store._snapshot_text的UTF8字节严格等于事先S1，实际STATUS逐字节等于事先expected，并核N4原生Write确实权限拒绝。缺件/异常/锁忙延后/状态或字节失配均保留failed/unverified，不publish/recovery重建，不重跑。

## 看护及停止口径

运行由既有runtime提供600秒/8MiB边界；外部看护须记录实际进程PID与创建时间，若观察到N1/N3/N5/N6/N7哨兵改变、N2新出现或N4字节既非初始化投影亦非预期投影，应立即停止本次确切进程树并保留全部证据。正常STATUS由revision0到1变化不是负例成功。已观察到异常不能通过恢复文件清除；原件中所有缺失toolcall标unverified。看护采样不是瞬时文件完整性证明。
最终只能证明指定TEMP矩阵、该实际版本与工具调用。真实memory/hook、全OS、TOCTOU、别名/POSIX及完整live仍无证。不把B作者二次maxturn变成有效交付，不自动main/live或最终native。
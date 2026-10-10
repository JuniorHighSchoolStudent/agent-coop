# 固定来源与待审核取舍

此文件保存本次研究依据和决策候选，规范由 docs/design.md 唯一维护。2026-10-10 静态核对，没有安装或执行 gstack/Jev。

## 来源

- gstack：`20eb6202fa8ea83a882e7c0463b722cd8a31af1e`，[角色与流程原文](https://github.com/garrytan/gstack/blob/20eb6202fa8ea83a882e7c0463b722cd8a31af1e/docs/skills.md)、[MIT 许可证](https://github.com/garrytan/gstack/blob/20eb6202fa8ea83a882e7c0463b722cd8a31af1e/LICENSE)。由 git ls-remote 定位后读取相同 commit 的原文；GitHub API 本次因限流未提供证据。借鉴概念并自行定义本项目合同，没有复制上游 skill 或代码；以后如复用实质内容需保留许可证要求的归属/许可。
- Jev in Codex：`9f8f032918ac01d4efa1b4ee26eca0a4e27ddc08`，[README](https://github.com/teempai/jev-in-codex/blob/9f8f032918ac01d4efa1b4ee26eca0a4e27ddc08/README.md)。0.2 的 42.7% 输入 Token 降幅、26.4% 耗时降幅及 0.3 的自定义分类结果均为作者公开报告的已知合成开发数据结果，本轮未重跑；不证明本项目效果或总账单节省。项目撤回未显示收益的选工具、上下文搜索、输出分流功能。
- TypeSafe 官方 [Choice](https://docs.typesafe.ai/primitives/choice) 与 [Noul](https://docs.typesafe.ai/primitives/noul)，读取日期 2026-10-10，网页无本轮可固定内容版本。Choice confidence 描述选项概率分布集中程度，Noul 返回命题概率；不把它们当实际任务正确率或通用授权阈值。
- ABM：本机 `agent-based-microbench` 的 `AGENTS.md`（基线 HEAD `4eda71c5e74fb7a961503acf984a74cddd99ba04`，已核对该工作文件与 HEAD 无差异），相关段落“任务开始与恢复时的必读路径”“先查已有能力与原始回执”“故障恢复与重采分开”。只提取同输入复用、证据定位、边界失败和原 owner 等通用合同，不复制业务原件或角色绑定。过往短周期新会话空转来自用户 ABM 实践复盘，属于历史观察，不是本次重测或当前自动化状态。

## 候选取舍及替代方案

推荐：吸收 gstack 的阶段职责/检查清单/工件交接，作为现有 Role/workflow 的可选模板；ABM 可靠性经验变成核心验收；Jev 作为可选语义判断节点，经对照后准入。

替代 A：直接安装完整 gstack 工作流。现阶段不选：其宿主调用、自动修改/发布、私有状态和评审门槛需逐项适配，不能覆盖本仓独立评审及 Claude 暂停约束。

替代 B：继续只用笼统 implementer/reviewer。保留其最小运行形式，但增加按任务激活的职责检查清单，避免产品范围、体验、QA、文档/发布证据漏项；不为每个角色都启动常驻 agent。

| 主题 | 候选决定 | 不能据此推断 |
|---|---|---|
| gstack 产品/工程/体验审查 | 借鉴职责与阶段工件，映射现有模板；范围变化产生后继 proposal | CEO 名称赋予扩范围或发布权限 |
| gstack review/QA/ship/retro | 借鉴差异审查、真实行为证据、发布检查、复盘输入 | 一次角色切换具有独立评审资格；修复者自签；默认自动 push/deploy |
| 定时角色任务 | 一个 Scheduler；程序 tick 检查有变化/到期才派发，合同必需事件不可过滤 | 每分钟调用每个模型；某会话永久可恢复 |
| ABM 经验 | 当前原件对账、输入/依赖差集、证据分层、同检查点清理旧状态 | ABM owner/业务规则移入通用内核 |
| Jev 模式 | 程序先处理确定事实，轻量模型给有界文本判断，复杂/未知交受权角色 | Jev 关闭阻断、改状态、替代独立审核或筛掉必需监督 |
| Jev 接入 | P0 调研；P4 可在预算内离线评测；P5 受控启用/撤回 | 本轮安装、外发业务数据、已省 Token 或降低总费用 |

候选评测应比较原流程、确定性去重/增量上下文流程、其上增加轻量判断的流程；原文/稳定 ID 与完整证据可追，固定版本及阈值，独立保留样本、失败与高置信误判均计入。激活由既有权限与评审决定，停用恢复已批准基线，不能静默换模型。必需事件直接进入正式队列，不受可选判断的失败、超时或预算耗尽影响。

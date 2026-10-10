# 开发交流与归档社区依据

核对日期 2026-10-10，Codex 在线读取以下官方原文；下文为简要概括与本仓推导。来源只供参考，不能替代本仓审批和权限。

| 官方来源 | 可复用实践 | 本仓落点与不采纳范围 |
|---|---|---|
| [GitLab Communication](https://handbook.gitlab.com/handbook/communication/) | 异步文本协作；线下讨论结论写回权威载体，通知携带来源链接 | 请求目录保存关键澄清与决策依据，不让聊天成为唯一副本；不复制 GitLab 全套组织手册，不强求所有闲聊入库 |
| [GitHub Resolving reviews](https://docs.github.com/en/pull-requests/concepts/resolving-reviews) 与 [protected branches](https://docs.github.com/en/repositories/configuring-branches-and-merges-in-your-repository/managing-protected-branches/about-protected-branches) | 讨论与变更关联，较大修改需重新审核，可要求对话处理完成，批准可因变更失效 | 稳定 finding 引用串联意见、修复与复核；本仓继续执行独立关闭权限，不能照搬网页上作者点 resolved 即视为有效关闭；本轮不配置 GitHub 保护规则 |
| [OpenTelemetry Logs Data Model](https://opentelemetry.io/docs/specs/otel/logs/data-model/) | 区分事件时间与观测时间，使用可选关联字段连接日志与请求 | 复用已有 request/WorkRef/attempt/handshake/revision/actor 引用，不另造 trace 系统；未知时不伪造时间、模型或会话；不安装 SDK/Collector |
| [OWASP Logging Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html) | 排除敏感内容，限制访问、检测篡改，明确保留与处置；临时副本与备份同样纳入策略 | 原始运行流不直接提交 Git；归档核对摘要、可读性、权限、保留策略，删除独立判定；30 天诊断基线是本地设计选择，不是 OWASP 给出的期限或合规结论 |

现状复用裁定：AGENTS 管本仓开发规则；design §5.1 已有持久/投影/日志分层、Git 策略和唯一发布者；§7.4–7.7 已有独立评审、监督 blocking 闭合权限、旧状态退场及握手；§9.1 已有经验闭环。不新增第二台账/聊天总线/归档服务。ABM 经验仅复用不可变回执、稳定身份、原件与投影分离，不复制业务脚本或裁决权。

备选取舍：全量保存所有聊天会积累敏感内容和上下文噪声；只留最终 PASS 会丢失争议和修复链；选择“必要原件与关键交流摘要 + 稳定引用 + 按类保留”，原件和摘要明确区分。当前只完善合同与手工交付方式，不伪装为自动采集/备份/清理实现。

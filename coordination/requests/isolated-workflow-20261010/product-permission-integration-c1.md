# 产品权限候选组合检查 C1

范围：A正常交付与B未完成现场的组合检查；维护者：Codex集成者；状态：验证失败、待原GLM/Kimi具名内容审核，不是接收；来源：实际作者工具证据及根验证。

## 候选与作者

准入基线4279bd915459d46df7b9bf9ef6d8ca3fb528fa0f；A作者检查点46d0a6f46be8e3b0ff7483972b2c0619b812045c、B未完成检查点b2df881fb777414ca79d54b5028d7fca0964d209；根只cherry-pick形成准确组合67a86ce33755e11dda990c0ac7bb3b4d78edd307。两个作者actual init均deepseek-v4-pro，独立会话，实际写入均在批准写集，未改共享文件。A修改sample/test_sample/test_cli，未改test_flow；B修改全部五个允许文件。

A有有效最终回执且明确未运行测试；B进程exit0但模型result为error_during_execution/is_error=true/Max turns (20) exceeded，没有有效完成票。B保留为未完成候选，不以退出码、文件存在或根冻结提交冒充交付完成；没有补调用或Codex补写。后续只准入原席C1核对现场和具名finding，不自动认为B可以续跑。实际预算6/15 CodeBuddy、1/2 native。

## 根验证事实

A局部39项全部通过。B局部57项，2 failures/1 error：sample schema2依赖尚未合入一项、env=None输出换行断言一项、四环境值fixture遗漏SYSTEMROOT一项。组合后依赖失败消失，剩两项实际缺陷。

在独立clean detached树agent-coop-pp-review-c1对准确67a86ce执行python -B -m agent_coop verify：186项=182通过/2跳过/1失败/1错误，exit1；unittest 33.800秒，外部34.2899126秒。45文件前后清单相同，SHA14e08f7b33de0cf0bee2abfe07a09296fa50211f37b53a64a384e1b1b78761de。两skip仍为Windows symlink权限；370本地链接，无硬规模失败。未运行任何真实产品模型、矩阵或live。

- test_env_none_inherits_parent_environment：真实print输出present加CRLF，断言仅present，不能靠改产品stdout剥离语义让测试变绿。
- test_build_env_applies_codebuddy_four_value_set：Windows必需SYSTEMROOT未进入该fixture的inherit列表；产品按合同拒绝。修复须保留真实环境检查，不能放宽必需项。
- discovery从144到186项，以class.method消除仅模块迁移影响，原用例无丢失、无重复发现；这只证明发现数量，不证明全部新用例充分。
- 新软目标：sample304、runtime309、test_sample343、test_runtime409物理行；其余原软目标见输出。A原票305/344为自述偏差；环境继承名单实际16项，非原票所称17。B没有完成票/软目标说明，需原席裁定其充分性。

## 待原席核验的具体线索

这些是集成者/只读调查提出的待裁定线索，不代替原席finding或关闭权限：

- A sample._validate_permission仅以!=1校验schema，True/1.0可能被接受；dispatch重验工具仅检查Write/Edit有无，需核重算config摘要后额外Bash或角色adapter改变是否仍满足合同。bool拒绝必须发生在预留前，不能依赖B迟拒导致计数增长。
- B adapters._validate_permissions未精确检查五键集合，schema1.0、未知permissions键和Kimi同时声明Write/Edit及非空写集已由只读纯command调用证实通过。根外/重复写集和Bash也可被构造，但须按sample授权owner与adapter责任判断，不能直接据此声称真实执行越权。
- B runtime._build_env仅核inherit名单的大小写重复，set可同时含大小写变体；独立纯函数复核观察到两个键均保留。需核名称有效性与跨inherit/set的覆盖语义，保持合法精确同名覆盖，不放宽固定sample政策。
- B canonical helper在原始reparse检查前resolve；完整invoke稍后的run_bounded仍经paths.checked检查cwd，不把helper顺序缺口直接写成Popen绕过。请依据合同决定修复和边界用例。
- 重复--allowedTools/--disallowedTools不是已证覆盖缺陷：安装CLI静态variadic解析使用_concatValue→concat累积，独立调查已反驳“只保留最后一项”的猜测；无新的CLI动态探针，不追加模型调用。
- 请核真实子进程env测试是否覆盖sample派生profile→真实command/invoke全链，禁止只以互相配套的手写fixture掩盖跨包问题；原合同要求的反例、准确整数/键集合/原始路径边界均须实读。

内容审核应直接读取全部8个变更文件及实际验证原件，对同一候选独立交叉审查；B未完成不自动补签，若允许预算内finding修复须具名范围与作者归属。任何产品矩阵仍需修复后组合验证及双席C2准确内容批准；没有新main接收。

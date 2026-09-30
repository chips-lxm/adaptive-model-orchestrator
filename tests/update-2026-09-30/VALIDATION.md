# 2026-09-30 更新验证

本次范围为 `adaptive-model-orchestrator` 的模型路由、协作与审查规则、快照辅助工具及配套说明。源文件检查、独立评估后的定向复查、安装运行文件验证和实际宿主发现检查均已通过。本记录不代表已完成真实项目的全套深度复审，也不构成模型等价或性能保证。

## 实际执行结果

| 检查 | 结果与证据 |
| --- | --- |
| skill-creator 官方格式校验 | 通过；[完整命令和输出](validation-commands.json) |
| 快照行为测试 | 本包 10/10 通过，两个包合计 20 项；覆盖固定版本、拒绝覆盖、文件漂移、符号链接、常见发现目录、复制中变化、部分安装、缺失或损坏清单 |
| 配置与本地引用 | YAML/TOML 解析通过；隐式调用策略保留；当次 31 个现行文档文件目标存在，未检查外部 URL 或页内锚点；[检查范围与运行哈希](static-checks.json) |
| 完整源包快照 | 8 个运行文件，创建成功，快照内自己的脚本验证成功；[源包结果](snapshot-smoke.json) |
| 安装后的完整运行包 | 运行文件和随包清单与维护源一致；安装版本创建快照及快照内脚本验证均成功；[安装运行检查](installed-runtime-checks.json) |
| 实际 Codex 发现 | 新起本机 app-server 仅执行 `skills/list`，`forceReload: true`；两个 Skill 均唯一发现、enabled、路径正确、无加载错误；[宿主结果](host-discovery.json) |

可复现的源包检查脚本为 [run-validation.py](run-validation.py)，命令和解释器路径已记录。实际发现探针为 [probe-discovery.py](probe-discovery.py)；它不创建聊天或启动模型回合。安装记录中的最终文档同步与字节核对见 [final-installation-checks.json](final-installation-checks.json)，初次安装记录保留在 [installation-checks.json](installation-checks.json)。

## 独立评估与问题闭环

通过真实 `collaboration.spawn_agent` 分别请求 `gpt-6.1-sol/high` 和 `gpt-6-astra/xhigh`，使用隔离的初始上下文；两者均完成，未修改源文件，也未读取彼此报告。工具接受结构化参数，但返回值与列表未独立回显 effective model/effort，因此记录请求配置和宿主契约，不把模型自述当成生效证据。见 [配置与证据索引](evaluation-record.json)。

- [正向评估](forward-evaluation/report.md) 推演八类具体场景，并实际运行合成快照实验；场景决策与真实执行分开记录。
- [独立审计](independent-audit/report.md) 对照修改前标签检查关键约束，并独立运行测试和故障复现。
- 发现并修复：常见插件缓存路径漏拦截；README 对协调职责、困难不可拆分任务和审查者复用为验收者的表述不一致；稳定的部分安装可能被旧辅助工具接受。
- 现行工具先核对独立维护的 `runtime-manifest.json`，普通冻结与验证不自动重建清单。缺失、损坏和混合版本均拒绝；显式 `--seal` 仅供有意修改后的维护操作。
- [正向定向复查](forward-evaluation/recheck.md) 和 [独立审计复查](independent-audit/recheck.md) 均通过，所报问题已关闭；原始失败报告及原哈希保留。复查后仅修正 adaptive 中文 README 一处重复短语并显式重封清单，未改变执行规则或脚本；最终源包检查覆盖该最终字节版本。

复查报告中的早期摘要对应其检查时版本，不能改写为最终摘要；最终运行摘要以本包 `runtime-manifest.json` 和安装运行检查为准。

## 安装、恢复与环境

安装前只读检查相关项目会话为空闲；仅同步本轮新增或修改的文件，先检查安装漂移，再安装随包清单和运行内容。全部未触及的历史文件须保持安装前字节，相关证据见最终安装核对。没有本轮必须保留的安装历史差异。

未修改其他项目、全局 AGENTS 或主模型设置，未消息通知或中断其他聊天。安装发生在观察到的空闲边界；该观察不是阻止用户随后继续任务的锁。更新不会追溯改写旧会话已载入的指令；新任务或后续读取可使用新版。新增长任务快照用于固定本轮规则，不能自动补回历史任务未建立的快照。

系统 Git/Python 初次因未接受 Xcode 许可证退出；使用宿主自带运行时完成工作，未改变许可证。官方校验初次缺少 PyYAML，临时补齐依赖后通过。实际发现探针在普通沙箱初始化超时，获批宿主访问后通过，未独立确定超时底层原因。详见 [安装环境记录](installation-context.json)。

修改前恢复点为 `before-6-1-sol-2026-09-30`，指向 `b589d9f0c783add0403be5fe0424b60f993cc23e`；覆盖当时干净工作区的完整已跟踪内容。恢复边界、后续维护与交付检查点见 [HANDOFF.md](../../HANDOFF.md)。

## 未验证范围

没有进行同任务、同验收条件下的 Token/费用/延迟对照；没有实测 6.1 Sol xhigh 或 max 的实际项目效果；没有证明 max 与 Astra 全面等价。宿主发现不证明新会话的隐式触发行为；本次也未启动完整项目的多审查者—Astra—修复—验收流程。清单与摘要检查内容一致性，不提供对抗性认证或权限隔离；额外宿主发现目录仍由调用方避开。

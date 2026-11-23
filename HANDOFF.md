# 当前交接

更新于 2026-11-23（Asia/Shanghai），当前交付为 v0.4.0。

## 入口与现状

- 维护源为 `/Users/lxm/app1/github-preview/adaptive-model-orchestrator`，独立仓库和 `main` 分支。安装副本位于 `~/.codex/skills/adaptive-model-orchestrator`。需求依据见 [REQUIREMENTS.md](REQUIREMENTS.md)，使用入口见 [README.zh-CN.md](README.zh-CN.md)。
- 普通子任务统一为 GPT-6.2 Sol。档位、继承条件、显式调用与生效证据见 [宿主与推理档位](references/runtime.md)。主会话由用户选择，通用编排保留按收益分工、单一修改负责人和独立验收。
- 本次更新说明见 [CHANGELOG.md](CHANGELOG.md)，分发版本为 [GitHub v0.4.0](https://github.com/chips-lxm/adaptive-model-orchestrator/releases/tag/v0.4.0)。上版验证证据仍保留在 [2026-09-30 验证](tests/update-2026-09-30/VALIDATION.md)。

## 本轮验证

- 官方格式、配置与 35 个本地引用检查通过，快照单测 10/10 通过。源包成功创建快照并由快照内脚本复验，运行摘要为 `5055fd053ff54fceb0c4b733a44bba41944ca84bd29f750b00f01b68d352a890`。
- 独立正向评估覆盖六类情形，包括单点任务、两路并行、困难根因、关键判断、父配置继承及宿主证据缺口。Codex 本地 `turn_context` 分别确认 GPT-6.2 Sol 的 `medium`、`high`、`xhigh`、`max` 实际生效，后面三档实际用于合成案例和证据检查器评估。
- 验证覆盖本机桌面宿主和隔离案例，未测跨客户端行为、长期生产稳定性或同条件整体用量。

## 检查点与接续

- 修改前仓库干净，恢复标签 `before-6-2-routing-2026-11-23` 指向 `0a5efcadf33ef6fd77a190b2c25e739a9b5ae816`。恢复前先保全当前和安装自定义内容，用指定标签导出到临时目录，比对并恢复相关文件。本地恢复标签已核实，未执行整套回滚演练。
- 后续改动先读取 [AGENTS.md](AGENTS.md)。有意改动运行文件后显式执行 `python3 -B scripts/freeze_run.py --seal`，核对安装漂移并完成运行包验证。进行中的任务继续引用已有规则快照。

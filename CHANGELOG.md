# Change notes / 更新说明

## 2026-09-30

### v0.3.0 — GPT-6.1 Sol 与运行规则快照

本次更新以 GPT-6.1 Sol high 作为默认执行与常规审查路由，允许按难点直接使用 xhigh/max，并通过精简交接和固定运行规则减少重复工作与版本混用。

## 中文更新说明

- **模型选择**：6.1 Sol 从 `high` 起步，可按明确难点直接选 `xhigh` 或 `max`，不要求先逐级失败。Luna 固定 `high`，只处理边界明确、低风险、易核对的任务；旧 6 Sol 保留已有验证支持的适用路径，不作为必经中间层或静默回退。
- **审核要求**：保留用户选择的主会话模型、按收益分工、依赖就绪、单一修改负责人和整体产物验收；必要的执行与独立验收仍分离。通用编排不会自动启动项目深度复审。
- **减少重复工作**：共同背景与原始事实集中维护，分支引用必要材料；精简交接但保留全部发现、失败和反对证据。已有验证仅在需求、版本、输入、环境与依赖仍适用时复用，独立验收者仍亲自执行关键检查。
- **固定运行版本**：新增 `scripts/freeze_run.py` 和随包 `runtime-manifest.json`。长任务与分支可固定一次规则快照；缺失清单、部分更新、文件漂移和常见 Skill 发现目录中的输出均拒绝。`--seal` 仅供维护者有意修改后的清单更新，正常运行不能用它掩盖不一致。
- **问题修正**：补齐插件缓存路径检查，澄清协调职责、困难任务模型选择及审查者复用为验收者的边界；同步中英文说明，并保留历史验证原始结果。

### 验证与边界

本包快照测试 **10/10 通过**，两个包合计 20 项；官方 Skill 格式、配置解析和本地文档引用检查通过。两路独立评估提出的问题已修复并完成定向复查。完整源包与已安装版本均通过快照创建及自带脚本校验；本机 Codex `skills/list` 实际识别两个已启用的 Skill。

上述结果是 Skill 维护验证，不是新版在真实项目上的完整多模型复审验收。未进行同任务 Token/费用/延迟对照，也未实测 6.1 Sol xhigh/max 的项目效果；不保证固定节省比例，不宣称 max 与 Astra 全面等价。模型和推理强度仍须按目标宿主的实际支持与调用证据核实。

### 升级方法

下载附件 `adaptive-model-orchestrator.zip` 与 `SHA256SUMS.txt`，核对校验和后，将 ZIP 内的 `adaptive-model-orchestrator` 文件夹安装到 Codex 的 skills 目录。先保存现有自定义内容，并在任务空闲或明确版本切换点更新；运行文件与 `runtime-manifest.json` 必须来自同一版本，不能只替换 `SKILL.md`。已有任务的固定快照可继续使用旧规则；安装更新不会追溯改写已载入的上下文。

## English release notes

GPT-6.1 Sol is the default execution and ordinary-review route at **high**, with direct **xhigh/max** selection for justified difficulty. Luna remains high for bounded, low-risk work; GPT-6 Sol remains an evidence-backed option rather than a mandatory intermediate tier or silent fallback.

Adaptive Model Orchestrator retains the user-selected lead, benefit-based delegation, ready dependencies, single-editor ownership, and validation of the integrated result. Required independent acceptance remains separate from implementation; ordinary orchestration does not automatically invoke Deep Project Review.

Shared source facts, focused handoffs, and version-aware evidence reuse reduce unnecessary repetition without replacing personal independent checks. The new snapshot helper checks a separately maintained runtime manifest, pins a run's instructions, rejects partial installations and common discovery-root destinations, and never automatically reseals inconsistent input.

Validation includes 10 passing snapshot tests in this package, format/configuration/reference checks, independent evaluations with targeted rechecks, source and installed-package snapshot verification, and actual local Codex skill discovery. These checks do not establish end-to-end project review quality, a fixed token/latency improvement, or equivalence between Sol max and Astra.

Preserve customizations before upgrading. Install the complete enclosed folder, including its runtime manifest, at an idle or explicit version boundary. Existing frozen runs may continue using their pinned version.

[完整验证记录 / Validation report](https://github.com/chips-lxm/adaptive-model-orchestrator/blob/v0.3.0/tests/update-2026-09-30/VALIDATION.md) · [全部变更 / Full changes](https://github.com/chips-lxm/adaptive-model-orchestrator/compare/v0.2.0...v0.3.0)

## 2026-09-23

### 模型路由更新 / Model routing update

当前会话先理解需求，并保持用户选定的主模型。`gpt-6-astra` 保留困难推理与高风险验收职责；`gpt-6-sol` 同时承接此前 Sol 与 Terra 的协调、分析和实现工作，通常使用 `medium` / `high`，必要时使用 `xhigh`；`gpt-6-luna` 只承接边界明确、低风险且可核对的工作，始终使用 `high`。模型路由合并不取消需要独立完成的审查与修复职责。原有依赖、单一修改负责人、按收益委派和整体验收规则继续适用。迁移检查的范围与限制见 [验证报告](tests/migration-2026-09-23/VALIDATION.md)；不承诺普遍的质量、耗时或 Token 用量收益。

The current session first understands the request and remains on the user's selected model. `gpt-6-astra` retains difficult reasoning and high-risk validation. `gpt-6-sol` takes both former Sol and Terra work across coordination, analysis, and implementation at `medium` / `high`, with `xhigh` when needed. `gpt-6-luna` takes only bounded, low-risk, verifiable work and always runs at `high`. Consolidating model routes does not remove required independence between review and repair. Existing dependency, single-editor, benefit-based delegation, and integrated validation rules still apply. See the [migration validation report](tests/migration-2026-09-23/VALIDATION.md) for the scope and limits of its checks; no universal quality, latency, or token savings are claimed.

## 2026-09-17

### 并行推进与按依赖等待

这次更新处理两类调度问题：派发子任务后主智能体立即空等，以及多个已就绪任务被逐个串行启动。新的规则要求主智能体继续推进有用的独立工作，并允许有明确收益的就绪任务在环境额度内同时派发。

- **等待条件**：只有没有安全且有实际收益的工作可推进时才等待；允许等待不可拆分的关键任务，不为保持忙碌制造工作。
- **结果接收**：以稳定交付点、适用版本和所需检查判断前置产物是否就绪，及时解锁后续工作；局部集成检查不替代最终整体验收。
- **修改边界**：主智能体和分支都受单一修改负责人约束；接管前先停止原执行并交接。同属一个业务模块不自动意味着文件修改冲突。
- **协作成本**：不设置固定分支数量，不为填满额度拆任务，不因耗时较长就复制执行，也不为每次局部交付重复全量验收。
- **规则澄清**：验收模型是优先路由，另开验收分支需要有收益；必要外部输入拿不到时报告影响并按任务约定处理，避免无限轮询；不可确认的模型信息记为未知。
- **说明同步**：更新默认启动提示、中英文介绍、编排示例和已有安装的更新方式。自动选择设置、模型职责和最低推理强度要求保留。

**验证范围**：完成格式与引用校验、独立逻辑复审和六类调度场景推演，并修正发现的四处表述歧义。三个 skill 文件与经过复审的本地版本逐字节核对。未进行真实项目的速度或 Token 成本对照测试，不保证每个任务都更快或更省。

### Useful parallel work and dependency-aware waiting

This update addresses two scheduling patterns: a lead that waits immediately after delegating, and ready independent tasks that are started one at a time. The lead now continues useful independent work, while ready tasks with a clear expected benefit can be dispatched concurrently within the host's capacity.

- **Waiting**: wait only when no safe, useful work is ready. Waiting for an indivisible critical task is valid; do not invent work to stay busy.
- **Handoffs**: use stable delivery points, applicable versions, and required checks to determine readiness. Unlock dependent work promptly; targeted integration checks do not replace final validation of the whole result.
- **Editing ownership**: both the lead and subagents follow single-editor boundaries. Stop the original editor and hand off existing work before a takeover. A shared business-module label alone does not make disjoint edits conflict.
- **Coordination cost**: no fixed branch count, quota-filling tasks, duplicate execution merely because a task is slow, or repeated full validation after every local delivery.
- **Clarifications**: review models remain preferred routes; an extra reviewer needs a clear expected benefit. Report unavailable external inputs and follow the task's waiting or handoff agreement without indefinite polling. Mark unconfirmed model settings as unknown.
- **Documentation**: update the default prompt, both READMEs, orchestration examples, and update instructions. Preserve automatic selection, model responsibilities, and minimum reasoning requirements.

**Validation scope**: metadata and reference checks, independent logic review, and six scheduling scenarios, with four wording ambiguities corrected. The three skill files were compared byte for byte with the reviewed local version. No real-project speed or token-cost benchmark was run; improvements are not guaranteed for every task.

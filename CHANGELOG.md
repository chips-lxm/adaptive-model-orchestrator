# Change notes / 更新说明

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

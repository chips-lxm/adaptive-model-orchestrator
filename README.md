# Adaptive Model Orchestrator

一个面向 Codex 的自适应多模型编排 Skill：根据任务难度、依赖、可并行性和验收风险，在 Astra、Sol、Terra、Luna 之间选择最小有效协作配置。

它不会为了“多模型”而强行拆分任务。简单任务由当前会话直接完成；只有子任务能够独立推进并返回可验证产物时，才建立协作分支。

## 核心能力

- 按难度、依赖和可拆分性决定单模型或多模型执行。
- 为 Astra、Sol、Terra、Luna 分配方案、协调、实现和机械任务。
- 规范分支交接、状态跟踪、升级返工与整体验收。
- 强制 Luna 使用至少 `medium` 推理强度。
- 遵守实际工具、模型可用性和环境并发限制。

## 安装

```bash
git clone https://github.com/chips-lxm/adaptive-model-orchestrator.git ~/.codex/skills/adaptive-model-orchestrator
```

安装后开始新的 Codex 对话。Skill 可以自动匹配，也可以显式调用：

```text
Use $adaptive-model-orchestrator to coordinate this task.
```

## 许可证

[MIT](LICENSE)

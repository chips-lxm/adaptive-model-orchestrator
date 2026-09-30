# 当前交接

更新：2026-09-30（Australia/Brisbane）。本轮规则更新和安装已完成，源包、安装运行包与宿主发现已验证；最终本地检查点收录本文件及本轮证据。

## 入口与现状

- 维护源：`/Users/lxm/app1/github-preview/adaptive-model-orchestrator`，独立仓库，分支 `main`；运行副本：`~/.codex/skills/adaptive-model-orchestrator`。需求依据见 [REQUIREMENTS.md](REQUIREMENTS.md)，使用与结构见现有中英文 README。
- 主会话保留用户选择；有实际收益才分工。默认执行与常规审查使用 6.1 Sol high，可按难点直接 xhigh/max，保留 Luna high 和有依据的旧 Sol 路径。
- 共用原始事实、精简任务交接、按适用版本复用证据；需要独立验收时必须亲自执行关键检查。加入运行快照与随包清单，拒绝冻结部分安装。
- 实际验证、独立审查发现及其关闭情况、环境失败和未验证范围集中见 [本次验证](tests/update-2026-09-30/VALIDATION.md)。没有性能节省比例或模型等价结论。
- 没有本轮必须保留的安装历史差异。
- 没有本轮待修复问题。用户已追加 GitHub 更新授权，正在准备 v0.3.0 的 main 推送、双语说明及安装附件；远程发布结果将在完成后核对并记录。旧版本与历史验证保留。

## 版本与恢复

修改前工作区干净。本地标签 `before-6-1-sol-2026-09-30` 指向 `b589d9f0c783add0403be5fe0424b60f993cc23e`，保存修改前所有已跟踪内容。本轮本地交付提交的消息为 `Update skills for 6.1 Sol routing and verified run snapshots`；用 `git log -1 --format=fuller -- HANDOFF.md` 定位收录本交接的提交，用 `git status --short` 确认接手时新增改动。最终提交结果以 Git 实际状态为准。

恢复前先保全当前改动与安装自定义内容。可把上述旧标签 `git archive` 到新的临时目录进行比较，或在保全当前状态后反向撤销本轮提交；不要直接 reset/clean 或对安装目录做删除式覆盖。只还原本轮触及的文件，确认本轮新增文件后再处理它们，并保留安装中的本机历史证据。恢复计划未经整轮真实恢复演练；标签已实际创建并核对，但本地 Git 不是设备损坏后的异地保障。

## 下一步维护

本次交付无需继续修复。后续需求从本文件及实际 Git 状态接手；长任务读取本轮固定快照。规则有意修改后显式执行 `python3 -B scripts/freeze_run.py --seal`，再按 [AGENTS.md](AGENTS.md) 验证、核对安装漂移并同步。普通运行不得重封清单来绕过完整性失败。不要把讨论或维护深度复审 Skill 当作启动项目复审。

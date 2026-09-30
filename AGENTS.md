# adaptive-model-orchestrator 项目协作

本机维护源为 `/Users/lxm/app1/github-preview/adaptive-model-orchestrator`，这是独立 Git 仓库；用户安装副本位于 `~/.codex/skills/adaptive-model-orchestrator`。安装副本由维护源同步，可能没有 Git；需求和交接只在维护源编辑，再同步镜像。不要将上级 app1 或其他 Skill 当作同一仓库。

- 用户要求与边界见 [REQUIREMENTS.md](REQUIREMENTS.md)；当前状态、检查点、验证及安装状态见 [HANDOFF.md](HANDOFF.md)。
- 使用说明保留在现有中英文 README；执行规则在 SKILL.md，细节按其链接读取。历史测试及发布记录保留原日期、模型和结果。
- 修改规则时核对参考文件、示例和中英文说明，保持现有隐式调用政策。讨论或维护深度复审 Skill 不启动其项目复审流程。
- 验证：skill-creator 的 quick_validate.py；`python3 -B tests/test_freeze_run.py`；YAML/TOML 解析、包内链接、Git 差异；实质规则调整需做独立行为评估。静态检查、合成行为判断、真实流程和性能对照分别记录。
- 系统 Python/Git 不可用时可使用宿主自带运行时；不得自动接受系统许可证。
- 修改前保全现有改动。安装只同步本轮相关文件，先检查活动任务及安装漂移，不覆盖本机历史证据。必要的已授权修复与本地提交可直接完成；推送和发布单独依据用户授权。

运行文件有意修改后，维护者执行 `python3 -B scripts/freeze_run.py --seal` 重建 runtime-manifest.json，再完成验证。安装时同步这份清单；实际运行不能通过重封清单掩盖缺失、部分更新或意外漂移。辅助工具只识别常见安装路径，宿主额外扫描目录也必须由调用方避开。

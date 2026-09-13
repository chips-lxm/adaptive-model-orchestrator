# Adaptive Model Orchestrator

[English](README.md) | [简体中文](README.zh-CN.md)

![Adaptive Model Orchestrator social preview](assets/social-preview.png)

Adaptive Model Orchestrator is a Codex skill that routes work across Astra, Sol, Terra, and Luna according to task complexity, parallelizability, dependencies, and verification risk.

It is built around one rule: **use the smallest effective model team**.

**Invest a little more judgment upfront. Aim for less rework later.**

For complete projects, long autonomous tasks, and deliveries that should need less supervision, the skill first decides whether delegation is worthwhile. It then selects the smallest effective team and supplies context according to each task. The goal is fewer avoidable handoffs and repeated implementations, shorter delivery cycles, and more reliable results through integrated validation.

Coordination can add upfront analysis, context transfer, and verification costs. Create branches only when the expected benefit outweighs that overhead. More agents do not necessarily use fewer tokens, and a cheaper model does not necessarily consume fewer tokens. Time, cost, and quality improvements are design goals, not measured guarantees; no quantitative comparison is currently published.

## Updated: more deliberate collaboration decisions

- **Recognize autonomous delivery requests**: complete projects, long autonomous work, and requests for less supervision should prompt a collaboration assessment. Loading the skill does not require spawning agents.
- **Optimize total effort**: start with the fewest necessary branches and account for handoff, coordination, validation, and rework. Add branches only for independent work with a clear expected benefit.
- **Match context to the task**: bounded execution can use focused context. Decisions about user intent, architecture, or the overall result need original requirements, important corrections, and decisions, with full relevant history when necessary.

These decisions stay in the skill and load on demand. No new global `AGENTS.md` rule needs to run at every step. Automatic selection still depends on the host, description, and task context; invoke the skill explicitly when you want to ensure it is selected.

## The problem it solves

```text
Without routing
every task → strongest model or unnecessary parallel agents

With adaptive routing
simple work          → current session
complex planning     → Astra
coordination         → Sol
implementation       → Terra
bounded routine work → Luna
integrated review    → Sol, then Astra when the risk warrants it
```

Hard work is not automatically parallel work. The skill creates branches only when they can progress independently and return verifiable results.

## How it routes work

| Task shape | Execution strategy |
|---|---|
| One clear goal with a known path | Complete it in the current session |
| Multiple tightly coupled steps | Keep one coordinator; delegate only independent research or checks |
| Multiple independently verifiable deliverables | Use a small branch set with explicit ownership and dependencies |
| One difficult, indivisible reasoning problem | Let Astra solve the core problem and optionally add an independent review |

Default roles:

- **Astra** — difficult reasoning, architecture, conflicting constraints, and high-risk final validation.
- **Sol** — requirements, coordination, communication, integration, and cross-module review.
- **Terra** — implementation, tool use, code, files, and complex layout work.
- **Luna** — deterministic, bounded, and easy-to-check tasks. Luna is never assigned below `medium` reasoning.

These are routing defaults, not a requirement to use every model. The active environment and user authorization always determine what can actually run.

## Routing example

User request:

```text
Build and review a full-stack authentication system.
```

Possible orchestration:

1. **Astra · high** defines the architecture, threat model, interfaces, and acceptance criteria.
2. **Sol · medium** turns those decisions into an owned dependency plan and coordinates integration.
3. **Terra · medium/high** implements disjoint backend, frontend, and configuration work where parallel edits are safe.
4. **Luna · medium** performs deterministic inventory, documentation, and checklist-based verification tasks.
5. **Sol · high** checks integration and ordinary defects; **Astra · high** validates security-sensitive decisions and the final system.

If the work cannot be separated safely, the skill keeps it in one branch instead of manufacturing parallelism.

## Install

Clone the repository into your local Codex skills directory:

```bash
git clone https://github.com/chips-lxm/adaptive-model-orchestrator.git ~/.codex/skills/adaptive-model-orchestrator
```

Start a new Codex conversation after installation. The skill can be selected automatically from its description or invoked explicitly:

```text
Use $adaptive-model-orchestrator to coordinate this task with the smallest effective model team.
```

## What is included

```text
adaptive-model-orchestrator/
├── SKILL.md
├── agents/openai.yaml
└── references/collaboration-and-validation.md
```

- `SKILL.md` contains routing decisions, model roles, constraints, and completion criteria.
- `references/collaboration-and-validation.md` contains handoff fields, state tracking, escalation, and review rules.
- `agents/openai.yaml` provides Codex-facing display metadata and a default prompt.

## Design principles

- Do not split work merely because it is difficult or has many steps.
- Keep one coordinator responsible for requirements, dependencies, integration, and acceptance.
- Give each file or module one active editor at a time.
- Validate the integrated result, not just each branch in isolation.
- Report the actual model and reasoning configuration; never claim a switch that did not happen.
- Stop when the acceptance criteria are met.

## License

[MIT](LICENSE)

# Coding Workflow Templates

这些模板供 `implement-with-prd` 和 Delivery Steward 创建具体 delivery 时使用。

模板的职责边界：

- `task-board.md` 只记录总览状态，不承载详细交接事实。
- `current-task.md` 是唯一当前任务，并包含 Route Decision 和一个可复制给下一位 Agent 的 route-specific prompt。
- `worker-reports/<task-id>.md` 由 Build Worker 写，记录实现、测试、git 和风险事实。
- `designs/<task-id>-design.md` 由 Design Agent 按需写，记录代码级设计，不承载实现修改。
- `investigations/<task-id>-investigation.md` 由 Investigation Agent 按需写，记录调研事实和建议，不承载实现修改。
- `reviews/<task-id>-review.md` 由 Delivery Steward 写，记录交付检查结论。
- `decision-log.md` 只在存在重要决策时创建或追加。
- `final-handoff.md` 只在 delivery 收口时创建。

语言规则：

- 实例化这些模板时，先确定本次 delivery documentation language。
- 如果人类 prompt 明确指定文档语言，使用该语言；否则使用 PRD 的主要语言。
- 模板中的英文标题和字段名是语义示例，不是必须逐字保留的文案。
- 生成文档中的标题、说明、任务记录、worker prompt、worker report、review、decision log 和 final handoff 应使用 delivery documentation language。
- `source-prd.md` 是 raw copy，不翻译、不改写。
- 产品名、领域术语、API、代码标识、文件路径、命令、日志行、错误文本、引用的 PRD 原文和 commit hash 保留原语言或原格式。
- 专业术语使用原语言更清晰时可以保留原语言；组织性、描述性、记录性文本优先本地化。

## delivery-brief.md

```md
# Delivery Brief: <delivery-title>

## Source PRD

- PRD source: <path-or-pasted-content>
- Source snapshot: `source-prd.md` is a direct raw copy; do not rewrite or annotate it.
- Delivery documentation language: <language inferred from prompt-or-prd>
- Language note: <professional terms kept in original language when clearer>
- Delivery id: <delivery-id>
- Created at: <date>

## Goal

<本次交付要达成的目标>

## Scope

- <范围内事项>

## Non-Scope

- <明确不做的事项>

## Assumptions

- <从 PRD 中提取或启动时声明的假设>

## Risks

- <主要风险>

## Delivery Notes

- Delivery Steward 只负责交付拆解和结果 review。
- 产品效果由 Human Approver 判断。
```

## task-board.md

```md
# Task Board: <delivery-title>

| ID | Status | Route | Task | Depends On | Acceptance | Artifact | Review | Commit |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T001 | Ready | `Direct Build` / `Design First` / `Spike / Investigation` | <first task> | None | <acceptance> | | | |

## Status Values

- Pending
- Ready
- In Progress
- Review
- Done
- Blocked

## Notes

- Keep this board terse. Put details in worker reports, design briefs, investigation reports, and review files.
- Use one row per Agent handoff.
```

## current-task.md

```md
# Current Task: T001 - <task-title>

## Route Decision

- Recommended route: `Direct Build` / `Design First` / `Spike / Investigation`
- Reason:
  - <当轮上下文理由，不引用历史路线偏好>
- Human confirmation: Required before treating the route as approved.
- Next prompt type: Build Worker Prompt / Design Agent Prompt / Investigation Prompt

## Goal

<本轮要完成什么>

## In Scope

- <范围内>

## Out of Scope

- <范围外>

## Relevant Context

- PRD: `source-prd.md`
- Delivery brief: `delivery-brief.md`
- Workflow rules: `../../workflow.md`, `../../rules.md`

## Delivery Language

- Use delivery documentation language from `delivery-brief.md`.
- Keep professional terms, code identifiers, file paths, commands, logs, errors, quoted PRD text, and commit hashes in their original language or format when clearer.

## Implementation Requirements

- <实现要求>

## Required Tests

- <需要运行的测试>

## Acceptance Criteria

- <验收标准>

## Completion Report Required From Next Agent

- Write the route-specific artifact:
  - Direct Build: `worker-reports/T001.md`
  - Design First: `designs/T001-design.md`
  - Spike / Investigation: `investigations/T001-investigation.md`
- Report changed files, if any.
- Report tests/checks/investigation commands run and results, if applicable.
- Report commit hash, or explain why no commit was created.
- Report risks, blockers, deviations, or follow-ups.

## Route-Specific Prompt

Use exactly one of the following prompt types in a concrete `current-task.md`.

## Build Worker Prompt

请作为 Build Worker 执行 `T001 - <task-title>`。

必须先读取：

- `docs/coding-workflow/workflow.md`
- `docs/coding-workflow/rules.md`
- `docs/coding-workflow/deliveries/<delivery-id>/current-task.md`

只实现本文件定义的当前任务范围。不要顺手重构、不要扩大范围、不要修改无关文件。

如果本任务引用 approved design：

- 必须先读取 approved design。
- 必须按 approved design 实现，并在 worker report 中说明 design conformance。
- 如果 approved design 与当前代码事实冲突，或实现需要改变 design 中定义的接口、状态所有权、生命周期语义、构建/产物边界或错误语义，先停止并报告，不要自行改成另一套设计继续实现。

完成后必须：

1. 在 `docs/coding-workflow/deliveries/<delivery-id>/worker-reports/T001.md` 写任务报告。
2. 任务报告的标题、说明和记录使用本次 delivery documentation language；专业术语、代码标识、文件路径、命令、日志和错误文本可保留原语言。
3. 运行相关测试，或说明无法运行的原因。
4. 检查 `git status --short` 和必要的 `git diff`。
5. 只 stage 当前任务相关文件，使用显式路径，不要使用 `git add .`。
6. 创建只包含当前任务相关修改的 git commit，除非本轮没有文件修改。
7. commit message 使用 Conventional Commits：`<type>(<scope>): <summary>`。
8. 不要把 task id 放在 commit subject 开头；task id 写入 worker report，必要时写入 commit body。
9. 回报 worker report 路径、测试结果、commit hash、commit message 和遗留风险。

## Design Agent Prompt

请作为 Design Agent 执行 `T001 - <task-title>` 的代码级设计任务。

必须先读取：

- `docs/coding-workflow/workflow.md`
- `docs/coding-workflow/rules.md`
- `docs/coding-workflow/deliveries/<delivery-id>/current-task.md`
- `docs/coding-workflow/deliveries/<delivery-id>/source-prd.md`
- <相关技术方案、上一轮 review/report、关键源码文件>

本轮只输出 design brief，不修改应用代码。

完成后必须：

1. 在 `docs/coding-workflow/deliveries/<delivery-id>/designs/T001-design.md` 写 design brief。
2. design brief 使用本次 delivery documentation language；专业术语、代码标识、文件路径、命令、日志和错误文本可保留原语言。
3. 明确目标行为、现状代码事实、拟修改文件、接口或签名变化、状态所有权、数据流、失败路径、生命周期/线程/资源释放语义、构建影响、测试策略、不做事项和需要人类决策的问题。
4. 不要修改应用代码。
5. 如果无法形成可信设计，说明阻塞和需要调查的问题。
6. 检查 `git status --short` 和必要的 `git diff`。
7. 只 stage 当前设计产物相关文件，使用显式路径，不要使用 `git add .`。
8. 创建只包含当前设计产物的 git commit，除非本轮没有文件修改。
9. 回报 design brief 路径、commit hash、commit message、阻塞项和风险。

## Investigation Prompt

请作为 Investigation Agent 执行 `T001 - <task-title>` 的调研任务。

必须先读取：

- `docs/coding-workflow/workflow.md`
- `docs/coding-workflow/rules.md`
- `docs/coding-workflow/deliveries/<delivery-id>/current-task.md`
- <任务指定的源码、构建脚本、文档或上一轮 review/report>

本轮只调查事实和可行性，不修改应用代码。

完成后必须：

1. 在 `docs/coding-workflow/deliveries/<delivery-id>/investigations/T001-investigation.md` 写 investigation report。
2. report 使用本次 delivery documentation language；专业术语、代码标识、文件路径、命令、日志和错误文本可保留原语言。
3. 区分已确认事实、推断、未验证点、风险和建议下一步。
4. 不要修改应用代码。
5. 检查 `git status --short` 和必要的 `git diff`。
6. 只 stage 当前调研产物相关文件，使用显式路径，不要使用 `git add .`。
7. 创建只包含当前调研产物的 git commit，除非本轮没有文件修改。
8. 回报 investigation report 路径、commit hash、commit message、未验证点和风险。
```

## worker-reports/<task-id>.md

```md
# Worker Report: <task-id> - <task-title>

## Task

- Task id:
- Task title:
- Delivery:
- Worker:

## Scope

- In scope:
- Out of scope:

## Completed

- <完成内容>

## Not Done / Intentionally Deferred

- <未完成或刻意不做>

## Changed Files

- <文件路径>: <改动说明>

## Implementation Notes

- <关键实现事实、取舍、兼容性说明>

## Deviations

- <是否偏离 current-task；没有则写 None>

## Tests

- Command:
- Result:
- If not run, reason:

## Manual QA / Runtime Check

- Environment:
- Steps:
- Result:
- Evidence:

## Diagnostics / Logs

- <关键日志或错误摘要>

## Known Issues

- <已知问题>

## Risks / Follow-ups

- <风险或后续注意事项>

## Suggested Review Order

1. <建议 Delivery Steward 先读哪个文件>

## Evidence Policy

- Screenshots and recordings are optional.
- Logs, command output summaries, and written observations are sufficient unless the current task explicitly requires media.

## Git

- Start `git status --short`:
- Pre-commit `git status --short`:
- Post-commit `git status --short`:
- Commit hash:
- Commit message:
- Commit message format:
  - Expected: `<type>(<scope>): <summary>`
  - Type used:
  - Scope used:
  - Summary language:
  - Task id included in subject: Yes / No
- Commit body delivery trace, if used:
  - Delivery:
  - Task:
  - Report:
- Uncommitted files, if any:
- Reason for uncommitted files, if any:
```

## designs/<task-id>-design.md

```md
# Design Brief: <task-id> - <task-title>

## Task

- Task id:
- Task title:
- Delivery:
- Design route: Design First

## Goal Behavior

- <目标行为>

## Current Code Facts

- <从当前代码确认的事实，带文件路径>

## Proposed Design

- <代码级设计方案>

## Files To Change Later

- <文件路径>: <预期改动>

## Interfaces And Ownership

- Interfaces/signatures:
- State ownership:
- Data/config ownership:
- Dependency boundaries:

## Flow And Failure Semantics

- Call/data flow:
- Error/result handling:
- Lifecycle/threading/resources:

## Build And Packaging Impact

- <CMake、脚本、产物、依赖影响>

## Test Strategy

- <必须新增或修改的测试>

## Out Of Scope

- <明确不做>

## Human Decisions Needed

- <需要人类确认的问题；没有则写 None>

## Build Worker Contract

- <实现时必须遵守的设计约束>
- <允许 Build Worker 自主决定的局部细节>
- <遇到哪些冲突必须停止并报告>

## Git

- Commit hash:
- Commit message:
```

## investigations/<task-id>-investigation.md

```md
# Investigation Report: <task-id> - <task-title>

## Task

- Task id:
- Task title:
- Delivery:
- Route: Spike / Investigation

## Questions

- <本轮要查清的问题>

## Confirmed Facts

- <已确认事实，带文件路径、命令或日志摘要>

## Inferences

- <基于事实的推断>

## Not Verified

- <未验证点>

## Risks

- <风险>

## Recommended Next Step

- <建议下一步路线或任务，不自动视为批准>

## Commands / Evidence

- Command:
- Result:

## Git

- Commit hash:
- Commit message:
```

## reviews/<task-id>-review.md

```md
# Review Result: <task-id>

## Result

- Status: Pass / Needs Fix / Blocked

## Inputs Reviewed

- Route:
- Current task:
- Worker report:
- Design brief:
- Investigation report:
- Commit:

## Checked

- Current task completed:
- Scope respected:
- Tests run or explained:
- Worker report present:
- Design brief present, if Design First:
- Investigation report present, if Spike / Investigation:
- Approved design followed, if applicable:
- Deviations from approved design reported, if any:
- Commit hash present:
- Commit message follows Conventional Commits:
- Commit subject avoids task id prefix:
- Commit appears scoped to task:
- Human product-effect review required:
- Human product-effect review recorded:

## Findings

- <问题或通过说明>

## Human Approval

- Product effect is judged by Human Approver, not Delivery Steward.
- Human result, if provided:

## Next Action

- <下一个 Route Decision、任务、修正任务或 closeout>
```

## decision-log.md

```md
# Decision Log: <delivery-title>

## <date>

- Decision:
- Reason:
- Impact:
```

## final-handoff.md

```md
# Final Handoff: <delivery-title>

## Delivery Result

<本次 delivery 的收口结论>

## Source Documents

- PRD: `source-prd.md`
- Delivery brief: `delivery-brief.md`
- Task board: `task-board.md`
- Design briefs, if any: `designs/`
- Investigation reports, if any: `investigations/`

## Completed Tasks

| Task | Route | Artifact | Review | Commit |
| --- | --- | --- | --- | --- |
| T001 | `Direct Build` / `Design First` / `Spike / Investigation` | `worker-reports/T001.md` / `designs/T001-design.md` / `investigations/T001-investigation.md` | `reviews/T001-review.md` | `<hash>` |

## Delivered Capability

- <最终交付能力>

## Validation Summary

- Build/tests:
- Manual QA / human product-effect approval:
- Unverified scenarios:

## Known Limits

- <已知限制>

## Follow-ups

- <后续建议>
```

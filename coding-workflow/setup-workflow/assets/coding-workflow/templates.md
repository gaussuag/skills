# Coding Workflow Templates

这些模板供 `implement-with-prd` 和 Delivery Steward 创建具体 delivery 时使用。

模板的职责边界：

- `task-board.md` 只记录总览状态，不承载详细交接事实。
- `current-task.md` 是唯一当前任务，并在末尾包含可复制给 Build Worker 的 prompt。
- `worker-reports/<task-id>.md` 由 Build Worker 写，记录实现、测试、git 和风险事实。
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

| ID | Status | Task | Depends On | Acceptance | Worker Report | Review | Commit |
| --- | --- | --- | --- | --- | --- | --- | --- |
| T001 | Ready | <first task> | None | <acceptance> | | | |

## Status Values

- Pending
- Ready
- In Progress
- Review
- Done
- Blocked

## Notes

- Keep this board terse. Put details in worker reports and review files.
- Use one row per Build Worker handoff.
```

## current-task.md

```md
# Current Task: T001 - <task-title>

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

## Completion Report Required From Build Worker

- Write `worker-reports/T001.md`.
- Report changed files.
- Report tests run and test results.
- Report commit hash, or explain why no commit was created.
- Report risks or follow-ups.

## Build Worker Prompt

请作为 Build Worker 执行 `T001 - <task-title>`。

必须先读取：

- `docs/coding-workflow/workflow.md`
- `docs/coding-workflow/rules.md`
- `docs/coding-workflow/deliveries/<delivery-id>/current-task.md`

只实现本文件定义的当前任务范围。不要顺手重构、不要扩大范围、不要修改无关文件。

完成后必须：

1. 在 `docs/coding-workflow/deliveries/<delivery-id>/worker-reports/T001.md` 写任务报告。
2. 任务报告的标题、说明和记录使用本次 delivery documentation language；专业术语、代码标识、文件路径、命令、日志和错误文本可保留原语言。
3. 运行相关测试，或说明无法运行的原因。
4. 检查 `git status --short` 和必要的 `git diff`。
5. 只 stage 当前任务相关文件，使用显式路径，不要使用 `git add .`。
6. 创建只包含当前任务相关修改的 git commit，除非本轮没有文件修改。
7. 回报 worker report 路径、测试结果、commit hash 和遗留风险。
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
- Uncommitted files, if any:
- Reason for uncommitted files, if any:
```

## reviews/<task-id>-review.md

```md
# Review Result: <task-id>

## Result

- Status: Pass / Needs Fix / Blocked

## Inputs Reviewed

- Current task:
- Worker report:
- Commit:

## Checked

- Current task completed:
- Scope respected:
- Tests run or explained:
- Worker report present:
- Commit hash present:
- Commit appears scoped to task:
- Human product-effect review required:
- Human product-effect review recorded:

## Findings

- <问题或通过说明>

## Human Approval

- Product effect is judged by Human Approver, not Delivery Steward.
- Human result, if provided:

## Next Action

- <下一个任务或修正任务>
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

## Completed Tasks

| Task | Worker Report | Review | Commit |
| --- | --- | --- | --- |
| T001 | `worker-reports/T001.md` | `reviews/T001-review.md` | `<hash>` |

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

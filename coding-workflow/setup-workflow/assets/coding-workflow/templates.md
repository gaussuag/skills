# Coding Workflow Templates

这些模板供 `implement-with-prd` 和 Delivery Steward 创建具体 delivery 时使用。

## delivery-brief.md

```md
# Delivery Brief: <delivery-title>

## Source PRD

- PRD source: <path-or-pasted-content>
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

| ID | Status | Task | Depends On | Acceptance | Commit |
| --- | --- | --- | --- | --- | --- |
| T001 | Ready | <first task> | None | <acceptance> | |

## Status Values

- Pending
- Ready
- In Progress
- Review
- Done
- Blocked
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

## Implementation Requirements

- <实现要求>

## Required Tests

- <需要运行的测试>

## Acceptance Criteria

- <验收标准>

## Completion Report Required From Build Worker

- Changed files
- Tests run
- Test results
- Commit hash
- Risks or follow-ups
```

## worker-prompt.md

```md
请作为 Build Worker 执行当前任务。

必须先读取：

- `docs/coding-workflow/workflow.md`
- `docs/coding-workflow/rules.md`
- `docs/coding-workflow/deliveries/<delivery-id>/current-task.md`

只实现 `current-task.md` 中定义的范围。

完成后必须：

1. 运行相关测试，或说明无法运行的原因。
2. 检查 `git status` 和 `git diff`。
3. 只提交当前任务相关修改。
4. 更新 `progress-log.md`。
5. 回报修改文件、测试结果、commit hash 和遗留风险。
```

## progress-log.md

```md
# Progress Log: <delivery-title>

## <date> - Delivery Started

- Delivery workspace created.
- First task prepared.

## Task Updates

### T001

- Status:
- Worker:
- Changed files:
- Tests:
- Commit:
- Risks:
```

## review-result.md

```md
# Review Result: <task-id>

## Result

- Status: Pass / Needs Fix / Blocked

## Checked

- Current task completed:
- Scope respected:
- Tests run or explained:
- Commit hash present:
- Delivery docs updated:

## Findings

- <问题或通过说明>

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

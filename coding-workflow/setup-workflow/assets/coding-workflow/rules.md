# Coding Workflow Rules

这些规则适用于本仓库中的 coding workflow。

## 全局规则

1. 不允许隐式进入 coding workflow。
2. 需求讨论不等于启动开发流程。
3. 创建 PRD 不等于启动开发流程。
4. 只有人类明确要求基于某个 PRD 启动 coding workflow 时，流程才可以开始。
5. `setup-workflow` 只负责初始化工作流文档和目录。
6. `setup-workflow` 不允许修改业务代码。
7. `setup-workflow` 不允许创建具体 delivery。
8. `setup-workflow` 不允许拆开发任务。
9. 每个 Agent 只能执行自己当前角色对应的职责。
10. 如果任务边界不清楚，Agent 必须先澄清或在文档中标明假设，不能自行扩大范围。

## implement-with-prd 规则

1. 必须由人类显式提供或指定 PRD。
2. 启动前必须检查 `docs/coding-workflow/manifest.yml`。
3. 必须检查 manifest 中声明的必要文件和目录是否存在。
4. 如果检查失败，必须停止流程。
5. 检查失败时，只提示人类先运行 `setup-workflow`，不要自行继续。
6. 检查通过后，才可以创建本次 delivery 目录。
7. 每个 PRD 对应一个独立的 delivery 目录。
8. delivery 目录必须位于：

```text
docs/coding-workflow/deliveries/<delivery-id>/
```

## Delivery Steward 规则

1. 必须读取 PRD。
2. 必须读取 `workflow.md`、`rules.md` 和 `templates.md`。
3. 必须为本次交付创建和维护任务文档。
4. 必须一次只给 Build Worker 一个当前任务。
5. 必须维护 `task-board`。
6. 必须维护 `current-task`。
7. 必须在每轮 Worker 完成后检查交付结果。
8. 检查范围只包括：
   - 是否完成当前任务
   - 是否符合任务范围
   - 是否存在越界修改
   - 是否运行了必要测试
   - 是否提交了 git commit
   - 是否报告了 commit hash
   - 是否更新了必要的交付文档
9. Delivery Steward 不负责判断产品效果是否满意。
10. Delivery Steward 不允许把自己的结果 review 说成人类效果验收。
11. 如果 Worker 没有 commit hash，本轮任务不能视为完成。
12. 如果发现问题，应生成修正任务，而不是直接扩大原任务范围。

## Build Worker 规则

1. 必须读取本轮 `current-task`。
2. 必须读取相关 workflow 规则。
3. 只能实现当前任务范围内的内容。
4. 不允许顺手重构无关代码。
5. 不允许修改与当前任务无关的文件。
6. 如果发现当前任务无法完成，必须说明阻塞原因。
7. 必须尽量完成开发、单元测试、自测的闭环。
8. 必须运行相关测试。
9. 如果无法运行测试，必须说明原因。
10. 提交前必须检查 `git status` 和 `git diff`。
11. 必须创建 git commit，除非本轮没有任何文件修改。
12. commit 只能包含当前任务相关修改。
13. 完成后必须报告：
    - 本轮目标
    - 修改文件
    - 测试命令
    - 测试结果
    - commit hash
    - 遗留风险

## Human Approver 规则

1. 人类负责判断产品效果。
2. 人类决定是否继续、返工、暂停或结束。
3. 人类可以要求 Delivery Steward 生成修正任务。
4. 人类可以随时终止当前 delivery。
5. 人类可以决定某个 PRD 不进入 coding workflow。

## Git 规则

1. 每个 Agent 完成本轮工作后，如果产生了文件修改，必须提交 git commit。
2. 每个 commit 只能包含本轮任务相关内容。
3. 提交前必须查看 `git status`。
4. 提交前必须查看 `git diff`。
5. 不允许提交无关文件。
6. 不允许提交临时文件、调试文件、缓存文件。
7. 不允许把其他人或其他 Agent 的未提交修改纳入自己的 commit。
8. 不允许擅自 revert、reset、checkout、rebase、amend。
9. 需要这些操作时，必须得到人类明确许可。
10. 每轮完成报告必须包含 commit hash。
11. 没有 commit hash 的任务，不能视为完成。

## 文档规则

1. workflow 文档只记录稳定流程规则。
2. workflow 文档不记录会随项目代码变化而过期的项目事实。
3. 具体 PRD 的交付信息必须写入对应 delivery 目录。
4. 交付过程中的任务状态、review 结果、commit hash、重要决策，都必须记录在当前 delivery 目录中。
5. 不允许把多个 PRD 的交付状态混在同一个 delivery 目录里。

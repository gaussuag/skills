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
2. `source-prd.md` 必须保存原始 PRD 内容。
3. 如果 PRD 输入是文件路径，必须直接复制该文件内容到 `source-prd.md`。
4. 如果 PRD 输入是粘贴内容，必须逐字写入 `source-prd.md`。
5. 不允许总结、重写、翻译、重排、规范化标题或重新生成 PRD。
6. 不允许向 `source-prd.md` 添加 metadata、说明或来源头。
7. 平台自动换行符规范化可以接受。
8. 原始 PRD 路径或 `pasted content` 来源只记录在 `delivery-brief.md`。
9. 启动前必须检查 `docs/coding-workflow/manifest.yml`。
10. 必须检查 manifest 中声明的必要文件和目录是否存在。
11. 如果检查失败，必须停止流程。
12. 检查失败时，只提示人类先运行 `setup-workflow`，不要自行继续。
13. 检查通过后，才可以创建本次 delivery 目录。
14. 每个 PRD 对应一个独立的 delivery 目录。
15. delivery 目录必须位于：

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
7. 必须在 `current-task` 中提供可复制给 Build Worker 的 prompt。
8. 必须在每轮 Worker 完成后读取对应的 `worker-reports/<task-id>.md`。
9. 必须在每轮检查后写入 `reviews/<task-id>-review.md`。
10. 必须在每轮检查后更新 `task-board`；如果还有下一轮任务，更新 `current-task`；如果交付完成，进入 closeout。
11. Delivery Steward 可以维护 delivery 文档，但不允许修改业务代码。
12. 必须在每轮 Worker 完成后检查交付结果。
13. 检查范围只包括：
   - 是否完成当前任务
   - 是否符合任务范围
   - 是否存在越界修改
   - 是否运行了必要测试
   - 是否写入 worker report
   - 是否提交了 git commit
   - 是否报告了 commit hash
   - 是否更新了必要的交付文档
14. Delivery Steward 不负责判断产品效果是否满意。
15. Delivery Steward 不允许把自己的结果 review 说成人类效果验收。
16. 如果 Worker 没有 worker report，本轮任务不能视为完成。
17. 如果 Worker 没有 commit hash，本轮任务不能视为完成，除非本轮没有文件修改且 report 中说明原因。
18. 如果发现问题，应生成修正任务，而不是直接扩大原任务范围。
19. 当人类确认产品效果时，只记录人类结论和日期，不把它改写为 Steward 自己的验收。

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
10. 开工前必须检查 `git status --short`，并写入 worker report。
11. 提交前必须检查 `git status --short` 和必要的 `git diff`。
12. 必须只 stage 当前任务相关文件，使用显式路径，不允许使用 `git add .`。
13. 必须创建 git commit，除非本轮没有任何文件修改。
14. commit 只能包含当前任务相关修改。
15. 必须写入 `worker-reports/<task-id>.md`。
16. 完成后必须报告：
    - 本轮目标
    - 修改文件
    - 测试命令
    - 测试结果
    - worker report 路径
    - commit hash
    - 遗留风险
17. 截图和录屏不是默认必需证据；除非当前任务明确要求，否则日志、命令输出摘要和文字观察即可。

## Human Approver 规则

1. 人类负责判断产品效果。
2. 人类决定是否继续、返工、暂停或结束。
3. 人类可以要求 Delivery Steward 生成修正任务。
4. 人类可以随时终止当前 delivery。
5. 人类可以决定某个 PRD 不进入 coding workflow。

## Git 规则

1. 每个 Agent 完成本轮工作后，如果产生了文件修改，必须提交 git commit。
2. 每个 commit 只能包含本轮任务相关内容。
3. 开工前必须查看 `git status --short`。
4. 提交前必须查看 `git status --short`。
5. 提交前必须查看必要的 `git diff`。
6. 必须使用显式路径 stage 文件，不允许使用 `git add .`。
7. 不允许提交无关文件。
8. 不允许提交临时文件、调试文件、缓存文件。
9. 不允许把其他人或其他 Agent 的未提交修改纳入自己的 commit。
10. 不允许擅自 revert、reset、checkout、rebase、amend。
11. 需要这些操作时，必须得到人类明确许可。
12. 每轮完成报告必须包含 commit hash。
13. 没有 commit hash 的任务，不能视为完成，除非本轮没有文件修改且 worker report 明确说明。

## 文档规则

1. workflow 文档只记录稳定流程规则。
2. workflow 文档不记录会随项目代码变化而过期的项目事实。
3. 具体 PRD 的交付信息必须写入对应 delivery 目录。
4. 交付过程中的任务状态、worker report、review 结果、commit hash、重要决策，都必须记录在当前 delivery 目录中。
5. 不允许把多个 PRD 的交付状态混在同一个 delivery 目录里。
6. `worker-reports/` 记录 Build Worker 的事实交接。
7. `reviews/` 记录 Delivery Steward 的检查结论。
8. `decision-log.md` 只记录重要决策；没有重要决策时可以不存在。
9. `final-handoff.md` 只在 delivery 收口时创建。

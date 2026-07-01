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
4. 每轮写入或替换 `current-task` 前，必须基于当轮上下文独立做 Route Decision。
5. Route Decision 只能选择：
   - `Direct Build`
   - `Design First`
   - `Spike / Investigation`
6. 不允许使用 `Design Lite`。
7. 不允许维护或引用 route-retrospective、route-fit feedback、历史偏好地图或其他历史路线经验来自动加速判断。
8. Delivery Steward 可以判断是否需要 Design First，但不允许自己承担代码级设计；需要锁定代码级设计时，必须生成 Design Agent prompt。
9. Route Decision 必须写入 `current-task`，包含推荐路线、当轮理由、是否需要人类确认和下一步 prompt 类型。
10. 人类使用、拒绝或明确回复路线建议，才视为路线被确认；Steward 不得自行声称路线已获人类批准。
11. 必须一次只给下一位 Agent 一个当前任务。
12. 必须维护 `task-board`。
13. 必须维护 `current-task`。
14. 必须在 `current-task` 中提供一个可复制给下一位 Agent 的 route-specific prompt。
15. 必须在每轮 Agent 完成后读取对应产物：
   - Direct Build：`worker-reports/<task-id>.md`
   - Design First：`designs/<task-id>-design.md`
   - Spike / Investigation：`investigations/<task-id>-investigation.md`
16. 必须在每轮检查后写入 `reviews/<task-id>-review.md`。
17. 必须在每轮检查后更新 `task-board`；如果还有下一步，重新做 Route Decision 并更新 `current-task`；如果交付完成，进入 closeout。
18. Delivery Steward 可以维护 delivery 文档，但不允许修改业务代码。
19. 必须在每轮 Agent 完成后检查交付结果。
20. 检查范围只包括：
   - 是否完成当前任务
   - 是否符合任务范围
   - 是否存在越界修改
   - 是否运行了必要测试
   - 如果本轮是 Direct Build，是否写入 worker report
   - 如果本轮是 Design First，是否写入 design brief
   - 如果本轮是 Spike / Investigation，是否写入 investigation report
   - 是否提交了 git commit
   - 是否报告了 commit hash
   - 是否更新了必要的交付文档
   - 如果实现任务引用 approved design，是否符合 design，或是否报告了偏离和原因
21. Delivery Steward 不负责判断产品效果是否满意。
22. Delivery Steward 不允许把自己的结果 review 说成人类效果验收。
23. 如果 Direct Build 没有 worker report，本轮任务不能视为完成。
24. 如果 Design First 没有 design brief，本轮任务不能视为完成。
25. 如果 Spike / Investigation 没有 investigation report，本轮任务不能视为完成。
26. 如果本轮有文件修改但没有 commit hash，本轮任务不能视为完成，除非 report 中说明没有提交的原因且人类接受。
27. 如果发现问题，应生成修正任务或重新做 Route Decision，而不是直接扩大原任务范围。
28. 当人类确认产品效果时，只记录人类结论和日期，不把它改写为 Steward 自己的验收。

## Design Agent 规则

1. 只在 `Design First` 路线中执行。
2. 必须读取本轮 `current-task`、PRD snapshot、相关技术方案、相关 review/report 和当前代码事实。
3. 只输出代码级 design brief，不修改应用代码。
4. design brief 默认写入：

```text
docs/coding-workflow/deliveries/<delivery-id>/designs/<task-id>-design.md
```

5. design brief 必须覆盖目标行为、现状代码事实、拟修改文件、接口或签名变化、状态所有权、数据流、失败路径、生命周期/线程/资源释放语义、构建影响、测试策略、不做事项和需要人类决策的问题。
6. 如果无法形成可信设计，必须说明阻塞和需要调查的问题，不得假装设计已完成。
7. 如果写入文件，必须提交只包含设计产物的 commit，并报告 commit hash。
8. Design Agent 不判断产品效果，也不宣布设计已被人类批准。

## Investigation Agent 规则

1. 只在 `Spike / Investigation` 路线中执行。
2. 必须读取本轮 `current-task` 和任务指定的上下文。
3. 只调查代码事实、构建事实、依赖行为、可行性或风险，不修改应用代码。
4. investigation report 默认写入：

```text
docs/coding-workflow/deliveries/<delivery-id>/investigations/<task-id>-investigation.md
```

5. investigation report 必须区分已确认事实、推断、未验证点、风险和建议下一步。
6. 如果写入文件，必须提交只包含调研产物的 commit，并报告 commit hash。
7. Investigation Agent 不把建议自动升级为 approved design 或实现任务。

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
15. commit message 必须符合 Git 规则中的 Conventional Commits 约束。
16. 必须写入 `worker-reports/<task-id>.md`。
17. 如果本轮引用 approved design，必须按 design 实现，并在 worker report 中报告 design conformance。
18. 如果 approved design 与当前代码事实冲突，或实现需要改变 design 中定义的接口、状态所有权、生命周期语义、构建/产物边界或错误语义，必须停止并报告；不得自行改成另一套设计继续实现。
19. 完成后必须报告：
    - 本轮目标
    - 修改文件
    - 测试命令
    - 测试结果
    - worker report 路径
    - commit hash
    - commit message
    - 遗留风险
20. 截图和录屏不是默认必需证据；除非当前任务明确要求，否则日志、命令输出摘要和文字观察即可。

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
7. commit message 默认使用 Conventional Commits：

```text
<type>(<scope>): <summary>
```

8. 允许的 type：
   - `feat`：新增功能或能力
   - `fix`：修复缺陷
   - `docs`：文档变更
   - `test`：测试变更
   - `refactor`：不改变行为的重构
   - `perf`：性能优化
   - `build`：构建系统或依赖
   - `ci`：CI 配置
   - `chore`：维护性杂项
9. `scope` 应使用简短、稳定的模块名或交付域名，例如 `renderer`、`capture`、`coding-workflow`、`docs`。
10. `summary` 应简短描述本次改动，优先使用 delivery documentation language；代码标识、API、产品名和专业术语可保留原语言。
11. 任务 ID 不应作为 commit subject 的开头；任务追踪应记录在 `task-board.md`、worker report 和 review 中。
12. 如需在 commit 中保留交付追踪信息，应写入 commit body，例如：

```text
Delivery: <delivery-id>
Task: <task-id>
Report: docs/coding-workflow/deliveries/<delivery-id>/worker-reports/<task-id>.md
```

13. workflow 文档类提交应使用 `docs(coding-workflow): <summary>`。
14. 如果目标仓库已有明确且不同的 commit message 规范，优先遵守目标仓库规范，并在 worker report 或 review 中说明。
15. 不允许提交无关文件。
16. 不允许提交临时文件、调试文件、缓存文件。
17. 不允许把其他人或其他 Agent 的未提交修改纳入自己的 commit。
18. 不允许擅自 revert、reset、checkout、rebase、amend。
19. 需要这些操作时，必须得到人类明确许可。
20. 每轮完成报告必须包含 commit hash 和 commit message。
21. 没有 commit hash 的任务，不能视为完成，除非本轮没有文件修改且 worker report 明确说明。

## 文档规则

1. workflow 文档只记录稳定流程规则。
2. workflow 文档不记录会随项目代码变化而过期的项目事实。
3. 具体 PRD 的交付信息必须写入对应 delivery 目录。
4. 交付过程中的任务状态、worker report、review 结果、commit hash、重要决策，都必须记录在当前 delivery 目录中。
5. 不允许把多个 PRD 的交付状态混在同一个 delivery 目录里。
6. `worker-reports/` 记录 Build Worker 的事实交接。
7. `reviews/` 记录 Delivery Steward 的检查结论。
8. `designs/` 只在 Design First 路线中按需创建，记录 Design Agent 的设计产物。
9. `investigations/` 只在 Spike / Investigation 路线中按需创建，记录 Investigation Agent 的调研产物。
10. `decision-log.md` 只记录重要决策；没有重要决策时可以不存在。
11. `final-handoff.md` 只在 delivery 收口时创建。

## 语言与本地化规则

1. 每个 delivery 必须确定一个 delivery documentation language。
2. 如果人类 prompt 明确指定文档语言，使用该语言。
3. 如果人类 prompt 没有明确指定，使用 PRD 的主要语言。
4. 如果 PRD 是多语言混合，优先使用人类 prompt 的语言；如果 prompt 也不明确，使用 PRD 中占主导的语言。
5. 除 `source-prd.md` 外，生成的交付文档应使用 delivery documentation language，包括标题、说明、任务记录、worker prompt、worker report、review、decision log 和 final handoff。
6. `source-prd.md` 必须保持原始内容，不翻译、不改写、不本地化。
7. 产品名、领域术语、API、代码标识、文件路径、命令、日志行、错误文本、引用的 PRD 原文和 commit hash 应保留原语言或原格式。
8. 专业术语使用原语言更清晰时，优先保留原语言；组织性、描述性、记录性的文本优先使用 delivery documentation language。
9. 同一个 delivery 内的文档语言应保持一致；如果某个任务必须切换语言，应在对应 worker report 或 review 中说明原因。

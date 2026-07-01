# Coding Workflow

`coding-workflow` 是一组用于 PRD 驱动开发交付的 Codex skills。这个包包含两个需要显式调用的 skill：

- `setup-workflow`
- `implement-with-prd`

这两个 skill 配合使用，但职责分开：`setup-workflow` 只负责在目标代码仓库中安装稳定的工作流文档协议；`implement-with-prd` 只负责在已有 PRD 的前提下，作为 Delivery Steward 启动一次开发交付流程。

这组 skill 适合把“需求讨论/PRD 沉淀”和“代码交付执行”分开管理。PRD 可以先独立产生，只有当人类明确决定基于某个 PRD 启动开发交付时，才使用 `implement-with-prd` 进入 coding workflow。

## 包含的 skills

### setup-workflow

`setup-workflow` 用于初始化目标代码仓库中的稳定工作流文档：

```text
docs/coding-workflow/
  workflow.md
  rules.md
  templates.md
  manifest.yml
  deliveries/
    .gitkeep
```

它只做 workflow 基础设施搭建，不讨论需求、不创建 PRD、不拆任务、不修改业务代码。

### implement-with-prd

`implement-with-prd` 用于根据明确提供的 PRD 启动一次交付流程。它担任 Delivery Steward 角色，会先检查目标仓库是否已经运行过 `setup-workflow`，再为本次 PRD 创建独立的 delivery 工作区。

典型输出目录：

```text
docs/coding-workflow/deliveries/<delivery-id>/
  source-prd.md
  delivery-brief.md
  task-board.md
  current-task.md
  worker-reports/
    .gitkeep
  designs/          # 按需创建
  investigations/   # 按需创建
  reviews/
    .gitkeep
```

`current-task.md` 会包含 Route Decision 和可以直接复制给下一位 Agent 的 prompt。下一步可能是 Build Worker、Design Agent 或 Investigation Agent。`worker-reports/` 由 Build Worker 写事实交接，`designs/` 由 Design Agent 按需写代码级设计，`investigations/` 由 Investigation Agent 按需写调研报告，`reviews/` 由 Delivery Steward 写检查结论。`decision-log.md` 只在存在重要决策时创建，`final-handoff.md` 只在交付收口时创建。

它不会直接实现业务代码。它会拆出第一个任务，先判断下一步路线，再输出对应 prompt。

## 它会做什么

- 安装一套稳定的 `docs/coding-workflow/` 工作流协议。
- 明确区分自由需求讨论、PRD 产出、交付启动和代码实现。
- 要求 coding workflow 必须由人类显式启动。
- 要求 `implement-with-prd` 必须拿到明确 PRD，不能凭空猜测要做什么。
- 为每个进入交付的 PRD 创建独立 delivery 目录。
- 维护交付过程中的任务、当前任务、worker report、review、决策和 commit 证据。
- 每轮由 Delivery Steward 基于当轮上下文独立判断下一步走 Direct Build、Design First 或 Spike / Investigation，并由人类确认或使用对应 prompt。
- 要求每轮产生文件变更的 Agent 提交自己的 git commit，并报告 commit hash。

## 它不会做什么

- 不会因为普通需求讨论自动触发。
- 不会因为 PRD 被创建就自动启动开发。
- 不会在没有明确 PRD 的情况下启动交付。
- 不会替人类判断产品效果是否满意。
- 不会在 `setup-workflow` 阶段修改业务代码。
- 不会在 `implement-with-prd` 阶段直接实现业务代码。
- 不会让 Delivery Steward 充当代码级设计者；需要代码级设计时，会输出 Design Agent prompt。
- 不会维护 route-retrospective、Route Fit Feedback 或用历史路线经验自动决定下一步路线。
- 不会把 Delivery Steward 的结果 review 伪装成人类效果验收。

## 典型使用顺序

1. 在目标代码仓库中显式调用 `setup-workflow`，安装 workflow 文档协议。
2. 人类可以在任意对话中自由讨论需求。
3. 如果讨论有价值，可以独立产出 PRD。
4. 当人类决定基于某个 PRD 开始开发时，显式调用 `implement-with-prd`。
5. `implement-with-prd` 检查 setup，读取 PRD，创建 delivery 工作区，在 `current-task.md` 中写入 Route Decision 和第一个 route-specific prompt。
6. 人类确认或使用 prompt 后，下一位 Agent 执行对应路线：
   - Direct Build：Build Worker 实现、测试、自测、写入 worker report、提交 commit。
   - Design First：Design Agent 输出 design brief，不改应用代码；设计确认后再生成 Build Worker prompt。
   - Spike / Investigation：Investigation Agent 输出 investigation report，不改应用代码；Steward 根据事实重新判断路线。
7. Delivery Steward 读取对应产物和 commit，写入 review，更新任务状态。
8. Human Approver 判断产品效果。
9. 继续下一个任务、生成修正任务、暂停或结束。

## 典型提示词

初始化目标仓库的 coding workflow：

```text
Use $setup-workflow to initialize the coding workflow docs for this repository.
```

中文也可以：

```text
使用 $setup-workflow 初始化这个仓库的 coding workflow 文档。
```

基于 PRD 启动交付流程：

```text
Use $implement-with-prd with docs/prds/import-orders.md to start the coding workflow delivery.
```

或者粘贴 PRD 内容：

```text
使用 $implement-with-prd，基于下面这份 PRD 启动 coding workflow：

<粘贴 PRD 内容>
```

如果没有提供明确 PRD，`implement-with-prd` 应该停止，并提示人类不知道要实现什么。

## 工作流边界

核心边界是：

```text
PRD 是 coding workflow 的输入，不是启动信号。
```

只有当人类明确要求“基于某个 PRD 启动 coding workflow”时，`implement-with-prd` 才能开始创建 delivery 工作区。

## 交付角色

- Human Approver：决定 PRD 是否进入交付，判断产品效果。
- PRD Writer：在 workflow 外讨论需求并产出 PRD。
- Delivery Steward：由 `implement-with-prd` 承担，负责拆任务、判断下一步路线和检查交付结果。
- Design Agent：在 Design First 路线中输出代码级 design brief，不修改应用代码。
- Investigation Agent：在 Spike / Investigation 路线中调查代码事实或可行性，不修改应用代码。
- Build Worker：执行 `current-task.md`，开发、测试、自测并提交 commit。
- QA Verifier：可选角色，未来可独立承担更系统的质量验证。

## 文件

从这个仓库的根目录看，可安装的 skill 目录位于：

```text
skills/coding-workflow/setup-workflow/
skills/coding-workflow/implement-with-prd/
```

外层 `skills/coding-workflow/` 目录只是用于同时分发这两个 skill 的包目录，不应作为单个 skill 安装。

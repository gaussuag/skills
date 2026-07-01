# Coding Workflow

本仓库使用一套基于 PRD 的 Agent 开发交付工作流。

## 目的

这套工作流定义的是：

- 一个已经存在的 PRD 如何进入开发交付流程
- Agent 如何拆解任务
- Delivery Steward 如何判断下一步执行路线
- Design Agent 如何在需要时先输出代码级设计
- Worker 如何执行任务
- Delivery Steward 如何检查交付结果
- 人类如何做最终效果判断

这套工作流不负责：

- 讨论需求
- 判断需求是否值得做
- 自动创建 PRD
- 自动启动开发
- 代替人类判断产品效果

## 核心原则

PRD 是这套工作流的输入，不是启动信号。

只有当人类明确要求“基于某个 PRD 启动 coding workflow”时，这套流程才开始运行。

## 角色

### Human Approver / 人类验收者

负责：

- 决定某个 PRD 是否进入开发交付流程
- 判断产品效果是否满意
- 决定是否继续、暂停、返工或终止

### PRD Writer / 需求文档协作者

负责：

- 在工作流之外，与人类讨论需求
- 帮助澄清需求、范围、目标和约束
- 产出 PRD

注意：

PRD Writer 不会因为写好了 PRD 就自动启动开发流程。

### Delivery Steward / 交付管家

负责：

- 在人类明确启动工作流后，读取 PRD
- 创建本次交付目录
- 拆解开发任务
- 维护任务状态
- 每轮独立判断下一步执行路线
- 生成当前任务和可复制给下一位 Agent 的 prompt
- 检查 Worker 的交付结果
- 写入每轮 Steward review
- 记录人类效果验收结论

注意：

Delivery Steward 只检查“交付结果是否符合任务定义”，不检查“产品效果是否令人满意”。Delivery Steward 可以判断本轮应该走 Direct Build、Design First 或 Spike / Investigation，但不承担代码级设计本身。

### Design Agent / 设计工程师

负责：

- 在 Design First 路线中读取当前任务、PRD、技术方案和代码事实
- 输出代码级 design brief
- 明确接口、职责边界、状态所有权、数据流、失败路径、测试策略和不做事项
- 不修改应用代码
- 不把设计确认伪装成人类批准

### Investigation Agent / 调研工程师

负责：

- 在 Spike / Investigation 路线中调查代码事实、构建事实、依赖行为或可行性
- 输出 investigation report
- 不修改应用代码
- 不把调研建议直接当作已批准设计或实现任务

### Build Worker / 实现工程师

负责：

- 读取当前任务
- 按任务范围实现代码
- 编写或更新测试
- 运行测试和自测
- 提交本轮代码修改
- 写入 worker report
- 汇报 worker report、测试、commit hash 和风险

### QA Verifier / 质量验证员，可选

负责：

- 做更系统的质量验证
- 做端到端测试、回归测试、体验检查

当前如果没有 QA Verifier，则由人类承担效果验收。

## 生命周期

### 1. 初始化工作流

人类显式使用 `setup-workflow`。

`setup-workflow` 只负责创建：

- `docs/coding-workflow/workflow.md`
- `docs/coding-workflow/rules.md`
- `docs/coding-workflow/templates.md`
- `docs/coding-workflow/manifest.yml`
- `docs/coding-workflow/deliveries/`

它不讨论需求，不创建 PRD，不拆任务，不修改业务代码。

### 2. 自由需求讨论

人类可以和任意 Agent 讨论需求。

这个阶段默认不进入 coding workflow。

讨论可能没有任何文档产出，也可能只产出一个 PRD。

### 3. PRD 落地

当人类认为讨论有价值时，可以要求 Agent 把讨论整理成 PRD。

PRD 可以保存在仓库内，也可以由人类提供。

PRD 创建完成后，仍然不会自动进入 coding workflow。

### 4. 启动交付流程

只有当人类明确说“基于这个 PRD 启动 coding workflow”，或类似明确指令时，`implement-with-prd` 才能启动。

`implement-with-prd` 必须先检查 `docs/coding-workflow/manifest.yml` 和必要文件是否存在。

如果检查失败，必须停止，并提示人类先运行 `setup-workflow`。

### 5. 创建交付目录

检查通过后，Delivery Steward 为本次 PRD 创建一个交付目录：

```text
docs/coding-workflow/deliveries/<delivery-id>/
```

该目录记录本次开发交付的任务、状态、结果、review 和决策。

除 `source-prd.md` 必须保持原始 PRD 内容外，本次 delivery 产生的交付文档应使用 PRD 或人类 prompt 所决定的本地化语言。专业术语、API、代码标识、命令、日志和错误文本可以保留原语言或原格式。

典型目录结构：

```text
docs/coding-workflow/deliveries/<delivery-id>/
  source-prd.md
  delivery-brief.md
  task-board.md
  current-task.md
  worker-reports/
    .gitkeep
  reviews/
    .gitkeep
  designs/           # optional, only when Design First is used
  investigations/    # optional, only when Spike / Investigation is used
```

`decision-log.md` 只在存在重要决策时创建。`final-handoff.md` 只在 delivery 收口时创建。

### 6. 开发循环

每轮循环如下：

```text
Delivery Steward 读取当前上下文
        |
        v
Delivery Steward 输出 Route Decision
        |
        v
Human 确认或使用下一步 prompt
        |
        +--> Direct Build
        |       |
        |       v
        |    Build Worker 实现、测试、自测、写 worker report、commit
        |
        +--> Design First
        |       |
        |       v
        |    Design Agent 输出 design brief，不改应用代码
        |       |
        |       v
        |    Human / Delivery Steward 确认 design
        |       |
        |       v
        |    Build Worker 按 approved design 实现
        |
        +--> Spike / Investigation
                |
                v
             Investigation Agent 输出 investigation report，不改应用代码
                |
                v
             Delivery Steward 重新判断路线
        |
        v
Delivery Steward 读取对应产物并写 review
        |
        v
Human Approver 检查产品效果
        |
        v
继续下一个任务 / 返工 / 暂停 / 结束
```

### 7. 结束交付

当 PRD 中定义的开发目标完成，并且人类确认效果可以接受时，本次 delivery 结束。

结束时 Delivery Steward 应：

- 确认 `task-board.md` 中任务状态已更新。
- 确认每轮任务都有对应 worker report、review 和 commit hash。
- 记录人类最终效果验收结论。
- 创建 `final-handoff.md`，说明交付结论、主要入口、任务与 commit、验证摘要、已知限制和后续建议。
- 如产生文档修改，提交只包含收口文档的 git commit。

# Coding Workflow

本仓库使用一套基于 PRD 的 Agent 开发交付工作流。

## 目的

这套工作流定义的是：

- 一个已经存在的 PRD 如何进入开发交付流程
- Agent 如何拆解任务
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
- 生成当前任务
- 检查 Worker 的交付结果

注意：

Delivery Steward 只检查“交付结果是否符合任务定义”，不检查“产品效果是否令人满意”。

### Build Worker / 实现工程师

负责：

- 读取当前任务
- 按任务范围实现代码
- 编写或更新测试
- 运行测试和自测
- 提交本轮代码修改
- 汇报结果、测试、commit hash 和风险

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

### 6. 开发循环

每轮循环如下：

```text
Delivery Steward 生成 current-task
        |
        v
Build Worker 实现、测试、自测、commit
        |
        v
Delivery Steward 检查交付结果
        |
        v
Human Approver 检查产品效果
        |
        v
继续下一个任务 / 返工 / 暂停 / 结束
```

### 7. 结束交付

当 PRD 中定义的开发目标完成，并且人类确认效果可以接受时，本次 delivery 结束。

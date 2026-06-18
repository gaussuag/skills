# Commit QA Cases

`commit-qa-cases` 是一个 Codex skill，用来根据 commit、commit range、diff、工作区改动、PR/分支对比、功能需求，或“旧用例 + 新变更”生成可归档的 QA 测试用例资产。

它适用于需要沉淀正式 QA 用例的场景：Codex 会先分析变更来源，再核对当前仓库里的最终行为，把业务风险映射到覆盖矩阵，输出结构化测试用例，并可渲染一份交互式测试执行页面。

这个 skill 只在显式调用时使用。需要生成归档 QA 资产时，请在提示词里写 `$commit-qa-cases`。

## 它会做什么

- 判断输入类型：单个 commit、commit range、diff、工作区改动、PR/分支对比、功能需求或混合来源。
- 写文件前先读取仓库说明，例如 `AGENTS.md`。
- 先检查变更来源，再检查当前最终代码中的真实行为。
- 输出业务影响分析，覆盖用户流程、成功路径、失败路径、回调、日志、生命周期、外部依赖、回归风险和待确认假设。
- 在最终用例前生成覆盖矩阵。
- 按 `references/testcase-schema.md` 的结构写入标准 JSON 用例。
- 将每次运行归档到 `docs/qa-case/<run-slug>/`。
- 每次生成 `source.json`、`analysis.md`、`test-cases.json`、`test-cases.md`，通常也会生成 `test-cases.html`。
- 评估哪些用例适合作为长期 base case，并在合适时更新 `docs/qa-case/base-case/`。
- 从结构化 JSON 渲染交互式 HTML 测试页面。
- 校验生成的 JSON，并在最终回复里准确说明跑过哪些检查。

## 它不会做什么

- 不会因为普通 QA 讨论、代码评审或调试问题自动触发，除非用户显式调用 `commit-qa-cases`。
- 不会把 commit diff 当作最终事实来源；如果后续代码已经改变行为，以当前最终代码为准。
- 不会在缺少证据时编造精确日志名、回调码、API 字段、业务状态或配置键。
- 更新旧用例时，不会静默删除仍有审阅价值的用例。
- 不会把一次性、临时性或产品语义未确认的用例提升为 base case。
- 不会声称完整 build 或完整测试套件通过，除非实际运行过对应命令。

## 典型提示词

单个 commit：

```text
Use $commit-qa-cases to generate QA cases for commit c85a700.
```

commit range：

```text
Use $commit-qa-cases to generate QA cases for commits c85a700..f437cc3.
```

当前工作区改动：

```text
Use $commit-qa-cases to analyze the current working-tree changes and generate archived QA cases.
```

功能需求：

```text
Use $commit-qa-cases to create QA cases for this requirement: payment retry should ignore stale async results after the user closes the payment page.
```

旧用例加新变更：

```text
Use $commit-qa-cases to update the existing payment QA cases for commit c85a700 and preserve stable case IDs.
```

中文也可以：

```text
使用 $commit-qa-cases，基于 commit c85a700 生成 QA 测试用例，并归档到 docs/qa-case。
```

## 工作流概览

1. 用户提供 commit、range、diff、工作区改动、PR/分支对比、功能需求，或旧用例加新变更。
2. Codex 读取仓库说明并检查变更来源。
3. Codex 检查当前最终代码，确认受影响行为。
4. Codex 编写业务影响分析。
5. Codex 生成覆盖矩阵，把风险和行为映射到用例 ID。
6. Codex 写入结构化 `test-cases.json`。
7. Codex 写入可读版 `test-cases.md`。
8. 除非用户不需要，Codex 渲染 `test-cases.html`。
9. Codex 评估是否需要新增或更新 `docs/qa-case/base-case/`。
10. Codex 校验生成资产，并报告实际执行过的检查。

## 输出归档

每次运行输出到：

```text
docs/qa-case/<run-slug>/
```

`run-slug` 使用：

```text
YYYY-MM-DD-<module-or-feature>-<short-ref-or-kind>
```

每次运行包含：

- `source.json`：输入类型、refs、检查过的输入、日期和假设。
- `analysis.md`：业务影响、代码证据、覆盖矩阵、base-case 决策和剩余风险。
- `test-cases.json`：标准结构化 QA 用例。
- `test-cases.md`：可读版 QA 文档。
- `test-cases.html`：生成时提供的交互式执行页面。

## Base Cases

长期项目级回归用例放在：

```text
docs/qa-case/base-case/<module>/
```

只有当行为稳定、重要，并且不是一次性变更细节时，skill 才会把用例提升为 base case。能自动合并时，会使用 `scripts/update_base_cases.py`。

## 交互式 HTML

生成的 HTML 页面支持筛选、执行状态、测试人备注、打印，以及执行结果导入/导出。执行状态与标准 `test-cases.json` 分开保存。

## 校验

skill 会根据生成结果执行轻量校验：

- `scripts/validate_testcase_json.py` 校验必填用例字段和允许的状态值。
- `scripts/render_testcase_html.py` 渲染交互式 HTML 页面。
- 如果环境里有 Node.js，可以检查生成 HTML 的脚本语法。
- 可以使用 `git diff --check` 检查生成文件中的空白问题。

## 文件

从仓库根目录看，可安装的 skill 位于：

```text
commit-qa-cases/commit-qa-cases/
```

外层 `commit-qa-cases/` 目录只是用于 git 分发的包目录。

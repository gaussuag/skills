# 安装 Commit QA Cases

这个包包含一个名为 `commit-qa-cases` 的 Codex skill。

可安装的 skill 目录是：

```text
commit-qa-cases/commit-qa-cases/
```

把这个目录安装到你的 Codex skills 目录即可。

## Windows PowerShell

在仓库根目录执行：

```powershell
$skillsDir = Join-Path $HOME ".codex\skills"
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
Copy-Item -Recurse -Force "commit-qa-cases\commit-qa-cases" $skillsDir
```

验证：

```powershell
Get-ChildItem "$HOME\.codex\skills\commit-qa-cases"
```

## macOS / Linux

在仓库根目录执行：

```bash
mkdir -p "$HOME/.codex/skills"
cp -R "commit-qa-cases/commit-qa-cases" "$HOME/.codex/skills/"
```

验证：

```bash
ls "$HOME/.codex/skills/commit-qa-cases"
```

## 更新已有安装

如果已经安装过这个 skill，替换已有目录即可。

Windows PowerShell：

```powershell
$target = Join-Path $HOME ".codex\skills\commit-qa-cases"
if (Test-Path $target) {
    Remove-Item -Recurse -Force $target
}
Copy-Item -Recurse "commit-qa-cases\commit-qa-cases" (Join-Path $HOME ".codex\skills")
```

macOS / Linux：

```bash
rm -rf "$HOME/.codex/skills/commit-qa-cases"
cp -R "commit-qa-cases/commit-qa-cases" "$HOME/.codex/skills/"
```

## 激活

重启 Codex，或开启一个新 thread，让 skill 列表刷新。

然后显式调用：

```text
Use $commit-qa-cases to generate QA cases for commit <commit>.
```

示例：

```text
Use $commit-qa-cases to generate QA cases for commit c85a700.
Use $commit-qa-cases to analyze the current working-tree changes and generate archived QA cases.
```

中文提示也可以：

```text
使用 $commit-qa-cases，基于 commit c85a700 生成 QA 测试用例。
```

## 预期安装结构

```text
~/.codex/skills/commit-qa-cases/
  SKILL.md
  agents/
    openai.yaml
  assets/
    interactive-testcase-template.html
  references/
    archive-layout.md
    base-case-policy.md
    change-analysis-workflow.md
    qa-generation-rules.md
    sdk-runtime-risk-checklist.md
    testcase-schema.md
  scripts/
    render_testcase_html.py
    update_base_cases.py
    validate_testcase_json.py
```

## 运行说明

- 辅助脚本使用 Python 3。
- 生成的 QA 资产会写入当前工作仓库的 `docs/qa-case/`，不会写入已安装的 skill 目录。
- 交互式 HTML 页面可以直接用浏览器打开。
- Node.js 是可选项，只在检查生成 HTML 脚本语法时使用。

## 注意事项

- 不要把外层 `commit-qa-cases/` 包目录本身安装为 skill。
- 需要安装内层 `commit-qa-cases/commit-qa-cases/` 目录。
- 这个 skill 只在显式调用时使用，请在提示词里写 `$commit-qa-cases`。
- 除非实际运行过对应命令，否则 skill 不会声称完整 build 或测试套件通过。

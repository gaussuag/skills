# 安装 Coding Workflow

这个包包含两个 Codex skills：

- `setup-workflow`
- `implement-with-prd`

需要把这两个内层 skill 目录分别安装到你的 Codex skills 目录。

可安装的目录是：

```text
skills/coding-workflow/setup-workflow/
skills/coding-workflow/implement-with-prd/
```

不要把外层 `skills/coding-workflow/` 目录本身安装成一个 skill。

## Windows PowerShell

在 `gauss_skills` 仓库根目录执行：

```powershell
$skillsDir = Join-Path $HOME ".codex\skills"
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
Copy-Item -Recurse -Force "skills\coding-workflow\setup-workflow" $skillsDir
Copy-Item -Recurse -Force "skills\coding-workflow\implement-with-prd" $skillsDir
```

验证：

```powershell
Get-ChildItem "$HOME\.codex\skills\setup-workflow"
Get-ChildItem "$HOME\.codex\skills\implement-with-prd"
```

## macOS / Linux

在 `gauss_skills` 仓库根目录执行：

```bash
mkdir -p "$HOME/.codex/skills"
cp -R "skills/coding-workflow/setup-workflow" "$HOME/.codex/skills/"
cp -R "skills/coding-workflow/implement-with-prd" "$HOME/.codex/skills/"
```

验证：

```bash
ls "$HOME/.codex/skills/setup-workflow"
ls "$HOME/.codex/skills/implement-with-prd"
```

## 更新已有安装

如果已经安装过这两个 skill，建议先删除旧目录，再复制新目录。

Windows PowerShell：

```powershell
$skillsDir = Join-Path $HOME ".codex\skills"
foreach ($skill in @("setup-workflow", "implement-with-prd")) {
    $target = Join-Path $skillsDir $skill
    if (Test-Path $target) {
        Remove-Item -Recurse -Force $target
    }
}
Copy-Item -Recurse "skills\coding-workflow\setup-workflow" $skillsDir
Copy-Item -Recurse "skills\coding-workflow\implement-with-prd" $skillsDir
```

macOS / Linux：

```bash
rm -rf "$HOME/.codex/skills/setup-workflow"
rm -rf "$HOME/.codex/skills/implement-with-prd"
cp -R "skills/coding-workflow/setup-workflow" "$HOME/.codex/skills/"
cp -R "skills/coding-workflow/implement-with-prd" "$HOME/.codex/skills/"
```

## 激活

重启 Codex，或开启一个新 thread，让 skill 列表刷新。

然后显式调用：

```text
Use $setup-workflow to initialize the coding workflow docs for this repository.
```

基于 PRD 启动交付：

```text
Use $implement-with-prd with docs/prds/<prd-file>.md to start the coding workflow delivery.
```

中文提示也可以：

```text
使用 $setup-workflow 初始化这个仓库的 coding workflow 文档。
使用 $implement-with-prd，基于 docs/prds/<prd-file>.md 启动 coding workflow。
```

## 预期安装结构

```text
~/.codex/skills/setup-workflow/
  SKILL.md
  agents/
    openai.yaml
  assets/
    coding-workflow/
      workflow.md
      rules.md
      templates.md
      manifest.yml
      deliveries/
        .gitkeep

~/.codex/skills/implement-with-prd/
  SKILL.md
  agents/
    openai.yaml
  assets/
```

## 运行说明

- 两个 skill 都只在显式调用时使用。
- `setup-workflow` 会在目标代码仓库写入 `docs/coding-workflow/`。
- `implement-with-prd` 要求目标仓库已经完成 `setup-workflow`。
- `implement-with-prd` 必须拿到 PRD 文件路径或粘贴的 PRD 内容。
- 如果没有明确 PRD，`implement-with-prd` 不会启动交付流程。
- 这两个 skill 都依赖目标仓库是 git 仓库，因为 workflow 使用 commit hash 作为交付证据。

## 注意事项

- 不要安装外层 `skills/coding-workflow/` 目录。
- 需要分别安装 `setup-workflow` 和 `implement-with-prd` 两个目录。
- 不要期待 `setup-workflow` 讨论需求、写 PRD、拆任务或修改业务代码。
- 不要期待 `implement-with-prd` 直接实现业务代码；它是 Delivery Steward，会生成交给 Build Worker 的任务 prompt。
- PRD 创建完成不代表自动进入 coding workflow，必须由人类明确启动。

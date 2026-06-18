# 安装 Intent Cherry-Pick

这个包包含一个名为 `intent-cherry-pick` 的 Codex skill。

可安装的 skill 目录是：

```text
intent-cherry-pick/intent-cherry-pick/
```

把这个目录安装到你的 Codex skills 目录即可。

## Windows PowerShell

在仓库根目录执行：

```powershell
$skillsDir = Join-Path $HOME ".codex\skills"
New-Item -ItemType Directory -Force -Path $skillsDir | Out-Null
Copy-Item -Recurse -Force "intent-cherry-pick\intent-cherry-pick" $skillsDir
```

验证：

```powershell
Get-ChildItem "$HOME\.codex\skills\intent-cherry-pick"
```

## macOS / Linux

在仓库根目录执行：

```bash
mkdir -p "$HOME/.codex/skills"
cp -R "intent-cherry-pick/intent-cherry-pick" "$HOME/.codex/skills/"
```

验证：

```bash
ls "$HOME/.codex/skills/intent-cherry-pick"
```

## 更新已有安装

如果已经安装过这个 skill，替换已有目录即可。

Windows PowerShell：

```powershell
$target = Join-Path $HOME ".codex\skills\intent-cherry-pick"
if (Test-Path $target) {
    Remove-Item -Recurse -Force $target
}
Copy-Item -Recurse "intent-cherry-pick\intent-cherry-pick" (Join-Path $HOME ".codex\skills")
```

macOS / Linux：

```bash
rm -rf "$HOME/.codex/skills/intent-cherry-pick"
cp -R "intent-cherry-pick/intent-cherry-pick" "$HOME/.codex/skills/"
```

## 激活

重启 Codex，或开启一个新 thread，让 skill 列表刷新。

然后显式调用：

```text
Use $intent-cherry-pick to port commit <commit> from <source-branch> to <target-branch>.
```

示例：

```text
Use $intent-cherry-pick to port commit f437cc373 from pc_dev_main to pc_dev_taptap.
```

中文提示也可以：

```text
使用 $intent-cherry-pick，把 pc_dev_main 上的 f437cc373 合入 pc_dev_taptap。
```

## 预期安装结构

```text
~/.codex/skills/intent-cherry-pick/
  SKILL.md
  agents/
    openai.yaml
  references/
    record-template.md
    review-checklists.md
```

## 注意事项

- 不要把外层 `intent-cherry-pick/` 包目录本身安装为 skill。
- 需要安装内层 `intent-cherry-pick/intent-cherry-pick/` 目录。
- 这个 skill 不会把临时分支 push 到远端。
- 这个 skill 默认不运行项目 build 或测试。

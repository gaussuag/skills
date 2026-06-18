# Intent Cherry-Pick

`intent-cherry-pick` 是一个 Codex skill，用来做“按源码事实保真”的 commit 移植。

它适用于普通 `git cherry-pick` 过于机械的场景：分支可能已经明显分叉，冲突需要像人一样理解后处理，而正确结果必须同时保留源 commit 的事实和目标分支的事实。

这个 skill 不会重新设计改动。它会尽量忠实移植源 commit，只在解决冲突时使用意图分析。

## 它会做什么

- 读取源 commit 或 commit range，以及目标分支代码。
- 提取源 commit 的意图和实现事实。
- 识别目标分支中必须保护的事实。
- 按保真等级分类每个改动：
  - `L0`：可原样应用，允许自动执行。
  - `L1`：只调整上下文位置，允许自动执行。
  - `L2`：冲突融合，需要人工确认。
  - `L3`：语义替代，需要人工确认。
- 在改代码前执行 precheck 审查。
- 在本地临时分支上应用已确认的保真融合方案。
- 执行代码评审级别的 intent tests，不默认运行项目 build 或测试。
- 对实际 diff 执行最终 check 审查。
- 在 `docs/intent-cherry-pick/` 下创建审计记录。
- 创建 commit message，保留原始源 commit message，并追加简短固定的 `Intent-Cherry-Pick` 区块。
- 不会把临时分支 push 到远端。
- 如果用户要求 merge back，并且安全条件满足，会在成功后删除本地临时分支。

## 它不会做什么

- 默认不运行 build、单元测试、集成测试、打包或项目自定义验证命令。
- 不会优化、重构、重命名、清理代码或大范围格式化。
- 不会扩大请求范围。
- 不会把本地工作分支 push 到远端。
- 不会强制删除分支。
- 不会删除远端分支。

## 典型提示词

```text
Use $intent-cherry-pick to port commit f437cc373 from pc_dev_main to pc_dev_taptap.
```

带范围约束：

```text
Use $intent-cherry-pick to port commit f437cc373 from pc_dev_main to pc_dev_taptap.
Only include CommonData and GiantBaseSDK core changes. Do not include Steam or Rail dependencies.
```

中文提示：

```text
使用 $intent-cherry-pick，把 pc_dev_main 上的 f437cc373 合入 pc_dev_taptap。
只保留 CommonData 和 GiantBaseSDK 的核心改动，不要合入 Steam/Rail 依赖。
```

## 工作流概览

1. 用户提供源分支、源 commit 或 commit range，以及目标分支。
2. Codex 检查 git 历史、源 diff、目标代码、调用链和相关符号。
3. Codex 生成 intent plan：
   - Scope Contract
   - Intent Report
   - Source Fact Lock
   - Target Fact Lock
   - Fidelity Classification
   - Fusion Plan
   - Intent Test Plan
4. 人工确认意图，以及任何 `L2` 或 `L3` 适配。
5. Precheck 审查计划。
6. Codex 从目标分支创建本地临时分支，并应用已确认的融合方案。
7. Codex 执行代码评审级别的 intent tests。
8. Check 审查实际 diff。
9. Codex 创建 workflow record 和 commit。
10. 如果用户要求，Codex merge back 到目标分支，并在安全时清理本地临时分支。

## 审计记录

记录会写入：

```text
docs/intent-cherry-pick/YYYY/YYYY-MM-DD-<source-short-hash>-to-<target-branch>.md
```

记录包含：

- Source commit
- Scope
- Intent
- Source Fact Lock
- Target Fact Lock
- Evidence reviewed
- Fidelity classification
- Fusion plan
- Precheck result
- Human decisions
- Implementation summary
- Intent tests
- Check result
- Cleanup status
- Remaining risks

## Commit Message 格式

生成的 commit message 会把源 commit message 放在最前面：

```text
<source commit title>

<source commit body, if any>

(cherry picked from commit <full source hash>)

Intent-Cherry-Pick:
Source-Branch: <source branch>
Target-Branch: <target branch>
Record: docs/intent-cherry-pick/YYYY/YYYY-MM-DD-<source-short-hash>-to-<target>.md
Precheck: PASS
Check: PASS
```

追加区块故意不提供自由文本 `Note` 字段。工作流细节应该写进审计记录。

## 语言规则

skill 会检测触发提示词的主要语言。

- 如果提示词主要是中文，workflow record 正文使用中文。
- 如果提示词主要是英文，workflow record 正文使用英文。
- 记录标题和章节标题保持英文。
- 源 commit message 会原样保留，不会翻译。

## 文件

从仓库根目录看，可安装的 skill 位于：

```text
intent-cherry-pick/intent-cherry-pick/
```

外层 `intent-cherry-pick/` 目录只是用于 git 分发的包目录。

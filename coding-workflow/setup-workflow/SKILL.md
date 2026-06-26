---
name: setup-workflow
description: Explicitly-invoked setup for installing the repository-local coding workflow docs. Use only when the user directly asks to initialize, install, scaffold, repair, or check the coding-workflow setup for a repository. Do not use for requirement discussion, PRD writing, PRD implementation, task planning, code changes, or ordinary development unless the user explicitly invokes setup-workflow.
---

# Setup Workflow

Install the stable `docs/coding-workflow/` protocol into the current git repository.

This skill is intentionally narrow. It creates or repairs workflow infrastructure only. It does not discuss requirements, write PRDs, create deliveries, plan tasks, or modify application code.

## Required Behavior

1. Confirm the current working directory is inside a git repository.
2. Resolve the repository root with `git rev-parse --show-toplevel`.
3. Install these files from `assets/coding-workflow/` into `<repo-root>/docs/coding-workflow/`:
   - `workflow.md`
   - `rules.md`
   - `templates.md`
   - `manifest.yml`
   - `deliveries/.gitkeep`
4. Preserve existing files. Do not overwrite user-edited workflow docs unless the user explicitly asks for repair or replacement.
5. If files are missing, add only the missing files.
6. If setup is already complete, report that no file changes are needed.
7. Never create a delivery workspace during setup.
8. Never create or edit a PRD during setup.
9. Never modify application code during setup.
10. If files changed, inspect `git status` and `git diff`, then commit only this setup work.

## Git Requirement

If setup creates or repairs files, create a git commit for the setup changes.

Use a concise commit message such as:

```text
docs(coding-workflow): initialize workflow docs
```

After committing, report:

- Files created or repaired
- Commit hash
- Any files intentionally preserved

If the directory is not a git repository, stop and tell the human that `setup-workflow` requires git because this workflow uses commit hashes as delivery evidence.

## Installed Contract

The installed docs are a stable workflow protocol. They must not contain project architecture facts, test commands, coding conventions, or any information likely to become stale as the codebase changes.

Concrete PRD delivery state belongs under:

```text
docs/coding-workflow/deliveries/<delivery-id>/
```

But this skill must not create those delivery directories except for the empty parent `deliveries/` folder and `.gitkeep`.

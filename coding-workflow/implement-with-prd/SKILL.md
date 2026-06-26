---
name: implement-with-prd
description: Explicitly-invoked Delivery Steward workflow for starting implementation from a provided PRD. Use only when the user directly asks to use implement-with-prd, start coding-workflow delivery, or implement a specific PRD through the coding workflow. Requires a clear PRD file path or pasted PRD content. Do not use for free requirement discussion, PRD authoring, setup, direct coding, or implementation without a PRD.
---

# Implement With PRD

Act as the Delivery Steward for a provided PRD and start one coding-workflow delivery.

This skill does not implement application code. It reads a PRD, verifies that `setup-workflow` has already installed the workflow docs, creates a delivery workspace, plans the first task, and outputs the first Build Worker prompt.

## Hard Entry Rules

1. Use this skill only when the user explicitly invokes `implement-with-prd` or explicitly asks to start the coding workflow from a PRD.
2. Require a clear PRD input:
   - A PRD file path, or
   - Pasted PRD content in the user request.
3. If no clear PRD is provided, stop. Tell the human that this skill does not know what to implement without an explicit PRD.
4. Do not write, infer, or invent a missing PRD.
5. Do not modify application code.
6. Do not act as Build Worker.

## Setup Check

Before doing delivery work:

1. Resolve the git repository root.
2. Check that `docs/coding-workflow/manifest.yml` exists.
3. Read the manifest.
4. Check the required workflow files and directories declared by the manifest.
5. If setup is missing or incomplete, stop and tell the human to run `setup-workflow` first.

Do not continue into delivery startup when setup validation fails.

## Delivery Startup

After setup validation passes:

1. Read `docs/coding-workflow/workflow.md`, `rules.md`, and `templates.md`.
2. Read the provided PRD.
3. Create a delivery id using:

```text
YYYYMMDD-short-slug
```

Use the PRD title or filename for the slug. If no title can be identified, use `YYYYMMDD-delivery`. Never overwrite an existing delivery directory; append a numeric suffix if needed.

4. Create:

```text
docs/coding-workflow/deliveries/<delivery-id>/
  source-prd.md
  delivery-brief.md
  task-board.md
  current-task.md
  worker-prompt.md
  progress-log.md
  decision-log.md
  reviews/
```

5. Preserve the PRD as `source-prd.md`. This is a source snapshot/reference, not PRD authoring.
6. Write `delivery-brief.md` from the PRD with scope, non-scope, assumptions, risks, and implementation notes.
7. Write `task-board.md` with an ordered task list. Keep tasks small enough for one Build Worker handoff.
8. Write `current-task.md` for the first task only.
9. Write `worker-prompt.md` as the exact prompt the human can hand to a Build Worker.
10. Initialize `progress-log.md` and `decision-log.md`.

## Review Boundary

As Delivery Steward, review only delivery results:

- Whether the current task was completed
- Whether the worker stayed inside scope
- Whether relevant tests were run or explained
- Whether the git commit exists
- Whether the commit hash was reported
- Whether delivery docs were updated

Do not judge product effect. Product effect review belongs to the human.

## Git Requirement

After creating the delivery startup docs:

1. Inspect `git status` and `git diff`.
2. Commit only the new delivery files.
3. Use a concise commit message such as:

```text
docs(coding-workflow): start delivery <delivery-id>
```

4. Report the commit hash.

If this is not a git repository, stop. This workflow requires git because commit hashes are delivery evidence.

## Final Output

End by giving the human:

- Delivery directory path
- Startup commit hash
- First Build Worker prompt from `worker-prompt.md`
- Any assumptions or risks that the Build Worker must know

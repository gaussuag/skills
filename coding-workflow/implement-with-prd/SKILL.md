---
name: implement-with-prd
description: Explicitly-invoked Delivery Steward workflow for starting implementation from a provided PRD. Use only when the user directly asks to use implement-with-prd, start coding-workflow delivery, or implement a specific PRD through the coding workflow. Requires a clear PRD file path or pasted PRD content. Do not use for free requirement discussion, PRD authoring, setup, direct coding, or implementation without a PRD.
---

# Implement With PRD

Act as the Delivery Steward for a provided PRD and start one coding-workflow delivery.

This skill does not implement application code. It reads a PRD, verifies that `setup-workflow` has already installed the workflow docs, creates a delivery workspace, plans the first task, and outputs the Build Worker prompt embedded in `current-task.md`.

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
  worker-reports/
    .gitkeep
  reviews/
    .gitkeep
```

5. Preserve the PRD as `source-prd.md`. This is a source snapshot/reference, not PRD authoring:
   - If the PRD input is a file path, copy that file's content directly into `source-prd.md`.
   - If the PRD input is pasted content, write the pasted content verbatim into `source-prd.md`.
   - Do not summarize, rewrite, translate, restructure, normalize headings, or regenerate the PRD.
   - Do not add metadata, notes, or provenance headers to `source-prd.md`.
   - Automatic line-ending normalization by the platform is acceptable.
   - Record the original PRD path or `pasted content` source in `delivery-brief.md`.
6. Determine the delivery documentation language:
   - If the human prompt explicitly asks for a documentation language, use that language.
   - Otherwise, use the primary language of the PRD.
   - If the PRD is mixed-language, use the human prompt language when clear; otherwise use the dominant PRD language.
   - Use this language for generated delivery docs, including headings, descriptive text, task records, worker prompts, worker reports, reviews, decision logs, and final handoff.
   - Keep `source-prd.md` verbatim; never translate it.
   - Preserve product names, domain terms, APIs, code identifiers, file paths, commands, log lines, error text, quoted PRD text, and other professional terms in their original language when that is clearer.
7. Write `delivery-brief.md` from the PRD with scope, non-scope, assumptions, risks, implementation notes, and the chosen delivery documentation language.
8. Write `task-board.md` with an ordered task list. Keep tasks small enough for one Build Worker handoff.
9. Create `worker-reports/.gitkeep` and `reviews/.gitkeep` so the startup commit preserves the delivery structure before any task report or review exists.
10. Write `current-task.md` for the first task only. Include a `Build Worker Prompt` section that the human can copy directly to a Build Worker.
11. Create `decision-log.md` only when there is a substantive startup decision to record. Otherwise, leave it absent until needed.

## Review Boundary

As Delivery Steward, review only delivery results:

- Whether the current task was completed
- Whether the worker stayed inside scope
- Whether relevant tests were run or explained
- Whether the worker report exists
- Whether the git commit exists
- Whether the commit hash was reported
- Whether the commit message follows the workflow's Conventional Commits rules
- Whether delivery docs were updated

Do not judge product effect. Product effect review belongs to the human.

When the human reports that a Build Worker completed a task:

1. Read `current-task.md`, the matching `worker-reports/<task-id>.md`, and the reported commit.
2. Inspect the changed files and delivery docs as needed.
3. Write `reviews/<task-id>-review.md`.
4. Update `task-board.md`.
5. If the task passed and more PRD scope remains, replace `current-task.md` with the next task and include its `Build Worker Prompt`.
6. If the task passed and the delivery is complete, create `final-handoff.md` and do not invent another task.
7. If the task needs fixes, write a focused correction task instead of expanding the original task.
8. If the human has provided product-effect approval, record it as the human's conclusion, not as Steward review.

## Git Requirement

After creating the delivery startup docs:

1. Inspect `git status` and `git diff`.
2. Commit only the new delivery files.
3. Use a concise Conventional Commit message with the `docs(coding-workflow)` scope, such as:

```text
docs(coding-workflow): start delivery <delivery-id>
```

4. Report the commit hash.

If this is not a git repository, stop. This workflow requires git because commit hashes are delivery evidence.

## Final Output

End by giving the human:

- Delivery directory path
- Startup commit hash
- First Build Worker prompt from the `Build Worker Prompt` section of `current-task.md`
- Any assumptions or risks that the Build Worker must know

# 📋 Find and implement the next incomplete task from the project todo list.

## Todo context
The task list is in `.llm/todo.md`. The format is:

```markdown
- `[ ]` - Not started
- `[x]` - Completed
- `[>]` - In progress in a peer directory/worktree
```

## Steps

- Find the next incomplete task
  - Run `todo-get $(dirname $(git rev-parse --git-common-dir))/.llm/todo.md`
  - It returns the first `Not started` task

- Implement the task
- Think hard about the plan
- Focus ONLY on implementing this specific task
- Ignore all other tasks in the `.llm/todo.md` file or TODOs in the source code
- Work through the implementation methodically and completely, addressing all aspects of the task
- Run appropriate tests and validation to ensure the implementation works

- ✅ After the implementation is complete and verified
  - Mark the task as complete:
  - Run `todo-complete $(dirname $(git rev-parse --git-common-dir))/.llm/todo.md`
  - It marks the first incomplete task as `[x]`

- Commit according to the instructions in ~/.claude/commands/commit.md

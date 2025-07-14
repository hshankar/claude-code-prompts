📋 Find and implement the next incomplete task from the project todo list.

- Spawn a sub-agent or sub-task to find the next task in the todo list.
  - In the sub-agent or sub-task:
  - Read the file `.llm/todo.md`
    - The file will only exist in this directory or in the main repository if we're in a worktree.
    - First try reading `./.llm/todo.md`
    - If that doesn't exist, use `git rev-parse --git-common-dir` to find the main repository and check if `.llm/todo.md` exists there.
    - Don't look in other locations. Don't look in the home directory.
  - Find the first line with an incomplete task, with `- [ ] <task>` (not `[x]` or `[>]`)
    - Keep in mind that the completed tasks might not be contiguous, since it's common to prepend new tasks at the top
  - End the sub-agent or sub-task here and share back the entire task information verbatim.

- Show the user the task we just found. Use the format:

```markdown
 The next incomplete task is:
 - [ ] Replace DEF with ABC.
```

- Now implement the task
- Think hard about the plan
- Focus ONLY on implementing this specific task
- Ignore all other tasks in the `.llm/todo.md` file or TODOs in the source code
- Work through the implementation methodically and completely, addressing all aspects of the task
- Run appropriate tests and validation to ensure the implementation works


- ✅ After the implementation is complete and verified
  - Spawn a sub-agent or sub-task to mark the task as complete
  - Find the task we are working on in `.llm/todo.md` again
  - Mark the completed task as done by changing `- [ ]` to `- [x]`
  - End the sub-agent or sub-task here and confirm the task was marked complete.

- At the same time as we are marking the task complete, spawn a second sub-agent or sub-task in parallel to perform a git commit
  - In the sub-agent, commit according to the instructions in ~/.claude/commands/commit.md

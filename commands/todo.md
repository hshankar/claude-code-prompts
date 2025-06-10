Find and implement the next incomplete task from the project todo list.

- Read the file `.llm/todo.md`
  - The file will only exist in this directory or in the main repository if we're in a worktree.
  - First try reading `./.llm/todo.md`
  - If that doesn't exist, use `git rev-parse --git-common-dir` to find the main repository and check if `.llm/todo.md` exists there.
  - Don't look in other locations. Don't look in the home directory.
- Find the first line with an incomplete task, with `- [ ] <task>`
  - Keep in mind that the completed tasks might not be contiguous, since it's common to prepend new tasks at the top
- Echo context to the user including the previous completed task and the current task we just found
  - Use the format:

⏺ The previous completed task was:
 - [x] Style button to be compact with icon and hover tooltip

 The next incomplete task is:
 - [ ] Create Modal component in `src/components/ui/Modal.tsx`

- Think hard about the plan
- Confirm the plan with the user before proceeding, with "🤔 Proceed? ➡️  [y/n]"
- Implement the task
- Focus ONLY on implementing this specific task
- Ignore all other tasks in the `.llm/todo.md` file or TODOs in the source code
- Work through the implementation methodically and completely, addressing all aspects of the task
- Run appropriate tests and validation to ensure the implementation works
- After the implementation is complete and verified, update `.llm/todo.md` to mark the completed task as done by changing `- [ ]` to `- [x]`


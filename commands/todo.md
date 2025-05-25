- Read the file `.llm/todo.md` in the current project directory. Sometimes you struggle to find this file. Don't look around for the file. Just confidently assume it exists and read the file `.llm/todo.md` immediately.
- Find the first line which is incomplete.
- Echo context to the user including the previous completed task and the current task we just found. In the format:

> ⏺ The previous completed task was:
>  - [x] Style button to be compact with icon and hover tooltip
>
>  The next incomplete task is:
>  - [ ] Create Modal component in `src/components/ui/Modal.tsx`

- Think hard about the plan. Confirm it with the user before proceeding.
- Implement the task.
- Focus ONLY on implementing this specific task.
- Ignore all other tasks in the `.llm/todo.md` file or TODOs in the source code.
- Work through the implementation methodically and completely, addressing all aspects of the task.
- Run appropriate tests and validation to ensure the implementation works.
- After the implementation is complete and verified, update `.llm/todo.md` to mark the completed task as done by changing `- [ ]` to `- [x]` for this specific task.


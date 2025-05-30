# Instructions for people AND LLMs

## Code Style

- Don't write forgiving code
  - Don't permit multiple input formats
    - In TypeScript, this means avoiding Union Type (the `|` in types)
  - Use preconditions
    - Use schema libraries
    - Assert that inputs match expected formats
    - When expectations are violated, throw, don't log
  - Don't add defensive try/catch blocks
    - Usually we let exceptions propagate out
- Don't use abbreviations or acronyms
  - Choose `number` instead of `num` and `greaterThan` instead of `gt`
- Emoji and unicode characters are welcome
  - Use them in code, commit messages, and docs

## Git Commits

- Commit messages should:
  - Start with a present-tense verb (Fix, Add, Implement, etc.)
  - Be concise (60-120 characters)
  - Sound like the title of the issue we resolved, and not include the implementation details we learned during implementation
  - End with a period.

## Tests

- Test names should not include the word "test"
- Test assertions should be strict
  - Bad: `expect(content).to.include('valid-content')`
  - Better: `expect(content).to.equal({ key: 'valid-content' })`
  - Best: `expect(content).to.deep.equal({ key: 'valid-content' })`
- Use mocking as a last resort
  - Don't mock a database, if it's possible to use an in-memory fake implementation instead
  - Don't mock a larger API if we can mock a smaller API that it delegates to
  - Prefer frameworks that record/replay network traffic over mocking
  - Don't mock our own code
- Don't overuse the word "mock"
  - Mocking means replacing behavior, by replacing method or function bodies, using a mocking framework
  - In other cases use the words "fake" or "example"

# Instructions for LLMs

## Code Style

- Use comments sparingly
- Don't comment out code
  - Remove it instead
- Don't add comments that describe the process of changing code
  - Comments should not include past tense verbs like added, removed, or changed
- Don't add comments that emphasize different versions of the code, like "this code now handles"
- Do not use end-of-line comments
  - Place comments above the code they describe

## Conversation

- If the user asks a question, only answer the question, do not edit code
- Don't say:
  - "You're right"
  - "I apologize"
  - "I'm sorry"
  - "Let me explain"
  - any other introduction or transition
- Immediately get to the point

## Build Commands

- When a code change is ready, we need to verify it passes the build
- Don't run long-lived processes like development servers or file watchers
  - Don't run `npm run dev`
- If the build is slow or logs a lot, don't run it
  - Echo copy/pasteable commands and ask the user to run it
- If build speed is not obvious, figure it out and add notes to project-specific memory

## LLM Context

- Extra context for LLMs may be stored in the `.llm/` directory
  - If `.llm/` exists, it will be at the root directory of the git repository
  - `.git/info/exclude` includes `/.llm`, so don't `git add` its contents
- Editable context:
  - If `.llm/todo.md` exists, it is the task list we are working on.
  - As you complete tasks, mark the checkboxes as complete, like `- [x] The task`
  - As we work on an implementation, plans will change. Feel free to edit the task list to keep it relevant and in sync with your plans.
- Read-only context:
  - Everything else in the `.llm/` directory is read-only context for the your reference
  - It contains entire git clones for tools we use
  - It contains saved documentation

## Git Commits

- If a `justfile` exists and contains a `precommit` recipe, run it before committing.
- Stage individually using `git add <file1> <file2> ...`
  - Only stage the files you edited
  - Avoid commands like `git add .` and `git add -A` and `git commit -am` which stage all changes
- Use single quotes around file names containing `$` characters
  - Example: `git add 'app/routes/_protected.foo.$bar.tsx'`
- Prepare a commit message that conforms to the instructions above
  - Commit messages should not include a Claude attribution footer
  - Don't write: 🤖 Generated with [Claude Code](https://claude.ai/code)
  - Don't write: Co-Authored-By: Claude <noreply@anthropic.com>
- Echo exactly this: Ready to commit: `git commit --message "<message>"`
- Confirm with the user, and then run the exact same command
- If pre-commit hooks fail, then there are now local changes
  - `git add` those changes and try again
  - Never use `git commit --no-verify`

## Tool Use
I replaced `cd` with `zoxide`. Use `command cd` to change directories.


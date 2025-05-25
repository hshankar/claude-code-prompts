Commit the local changes to git.

- Run `just precommit` (if a `justfile` exists and contains a `precommit` recipe)
- Stage changes carefully and individually. Only stage changes that you remember editing yourself.
- Avoid commands like `git add .` and `git commit -am` which stage all changes. Use commands like `git add` with several filenames.
- When using CLI tools with file paths containing `$` characters (like React Router's `$param.tsx` files), make sure to:
  - Use single quotes: `git add 'app/routes/_protected.foo.$bar.tsx'`
  - Or escape the $ character: `git add app/routes/_protected.foo.\$bar.tsx`

Prepare a commit message.

- If the user's prompt was a compiler or linter error, create a `fixup!` commit message.
- Otherwise, craft a commit message that:
  - Starts with a present-tense verb (Fix, Add, Implement, etc.)
  - Is concise (60-120 characters)
  - Clearly describes what was changed (not how) by referencing the intent of the original prompt, rather than the implementation details
  - Does not include the Claude attribution footer: Generated with [Claude Code](https://claude.ai/code)
  - Ends with a period.

Run git commit.

- If pre-commit hooks fail, then there are now local changes.
- `git add` those changes and try again.
- Never use `git commit --no-verify`.

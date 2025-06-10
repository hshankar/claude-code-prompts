Commit the local changes to git.

- Run `just precommit` (if a `justfile` exists and contains a `precommit` recipe)
- Stage individually using `git add <file1> <file2> ...`
  - Only stage changes that you remember editing yourself.
  - Avoid commands like `git add .` and `git add -A` and `git commit -am` which stage all changes
- Use single quotes around file names containing `$` characters
  - Example: `git add 'app/routes/_protected.foo.$bar.tsx'`
- If the user's prompt was a compiler or linter error, create a `fixup!` commit message.
- Otherwise:
@../instructions/git-commits.md
  - Describe the intent of the original prompt
- Commit messages should not include a Claude attribution footer
  - Don't write: 🤖 Generated with [Claude Code](https://claude.ai/code)
  - Don't write: Co-Authored-By: Claude <noreply@anthropic.com>

Run git commit without confirming again with the user.

- If pre-commit hooks fail, then there are now local changes
- `git add` those changes and try again
- Never use `git commit --no-verify`

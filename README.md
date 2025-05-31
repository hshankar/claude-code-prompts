# 🤖 `claude` code configuration

My development workflow revolves around a markdown todo list and two custom commands: `/user:todo` for implementing tasks and `/user:commit` for committing changes.

I wrote about my [development workflow with Claude Code](https://motlin.com/blog/claude-code-configuration) on motlin.com, and walk through the contents of the files there.

## 📋 Overview

- **`.llm/todo.md`** - A markdown checklist that persists across sessions
- **`/user:todo`** - Custom command to implement one task
- **`/user:commit`** - Custom command to commit changes

## 📝 Creating the Task List

I usually create `.llm/todo.md` by chatting with a thinking model. I'll use ChatGPT if I feel like talking out loud, or Gemini if I don't. At the end of the conversation, I'll ask it to summarize into a markdown checklist. I'll ask that each checkbox represent an atomic piece of work that can be tested and committed independently, and that they ordered by imlpementation order rather than importance.

## 🔄 The Development Loop

### 1. 🎯 Work on Next Task

I invoke my todo command:
```
/user:todo
```

This reads `.llm/todo.md`, finds the next incomplete task, shows me the context, and implements it. Once done, it marks the task as complete.

```markdown
- [x] First task
- [ ] Second task
```

### 2. 💾 Commit the Changes

When I'm happy with the implementation:
```
/user:commit
```

This stages only the files that Claude edited and creates a commit message. My global CLAUDE.md has it run `just precommit` automatically, so tests run before each commit.

### 3. 🔄 Start Fresh or Continue

At this point I peek at the next task and consider whether it's related to the one we just finished.

- If not, I close and reopen Claude to clear context
- If it is, I run `/compact` to compress the conversation and keep the context

I don't use the `/clear` command, I always close and reopen Claude. This avoid out-of-memory errors, and keeps me on the latest Claude Code version, which is released very frequently.

I don't often use `auto-accept edits` but when I do, I forget that it's on. Closing and reopening Claude resets it to off.

After existing, I one-shot the next task with:

```shell-session
$ claude '/user:todo'
```

## 💡 Why This Works for Me

If you're already writing quality GitHub issues, please don't stop. I don't often have the discipline.

The todo.md is a simple way to order and reorder tasks and helps me keep moving. If I learn something new, I can ask Claude to prepend tasks, or completely rework the list.

As I scale up to a whole team of people working with LLMs, I'd like to experiment with getting Claude to convert `todo.md` into GitHub issues.

## 🎬 Real Example

```bash
❯ claude '/user:todo'

> /user:todo is running…

⏺ The previous completed task was:
  - Once the new recipe works well, add it to the just factorio recipe

   The next incomplete task is:
  - Fix search by tag

  This task mentions issue #1137 on GitHub. Let me fetch the details about this issue to understand what needs to be fixed.

⏺ Based on my analysis, I believe I've identified the issue with tag search. The problem appears to be that the code is comparing a plain string
  value from the URL directly against an enum field without proper conversion.

  Plan to Fix Tag Search

  The issue is in ManualBlueprintResource.searchBlueprintSummaries() at lines 283-286. When a tag like /power/nuclear/ is passed:

  1. The code splits it and gets "power" as the category
  2. It tries to compare this string directly with BlueprintFinder.tags().tagCategory().eq("power")
  3. But tagCategory is an enum field (TagCategory), not a string

  The fix is to convert the string to the proper enum value before comparison. We need to:

  1. Parse the category string to the TagCategory enum
  2. Handle case conversion (URL uses lowercase, enum uses uppercase)
  3. Add proper error handling for invalid categories

  Shall I proceed with implementing this fix?

> yes

⏺ I'll implement the fix for the tag search issue. Let me start by examining the current code more closely and then make the necessary changes.

<claude implements the fix>

/user:commit
# Creates commit: "Fixed mobile controls."

> exit

❯ claude '/user:todo'
```

## 🛠️ The Commands

The full prompts are in this repo:
- [`commands/todo.md`](commands/todo.md) implements `/user:todo`
- [`commands/commit.md`](commands/commit.md) implements `/user:commit`

Feel free to adapt these to your own workflow!
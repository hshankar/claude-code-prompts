# Test Environment

This directory contains test scenarios for the Claude Code settings installation script.

## Structure

- `home/` - Simulated user home directory with existing `.claude` settings
- `expected-after-merge/` - Expected result after running the installation script

## Testing

Run the installation script in test mode:

```bash
TEST_HOME=test-environment/home python3 install.py
```

## Expected Behavior

The script should:

1. **settings.json**: Smart merge preserving user's `customSetting` and `EXISTING_VAR`, but updating template values like `DISABLE_TELEMETRY` from "0" to "1"
2. **commands/existing.md**: Ask permission before overwriting
3. **New directories**: Copy `agents/`, `instructions/`, `shared/`, `additional-tools/` completely
4. **New files**: Copy all new command files without prompting

## Key Merge Points

The settings.json merge should:
- Keep user's `customSetting: "user_value"`
- Keep user's `env.EXISTING_VAR: "keep_this"`
- Override `env.DISABLE_TELEMETRY` from "0" to "1" (template wins)
- Override `includeCoAuthoredBy` from true to false (template wins)
- Merge permissions arrays (template's extensive list + user's `Bash(rm:*)` deny)
- Add new template sections like `hooks` and `enabledMcpjsonServers`
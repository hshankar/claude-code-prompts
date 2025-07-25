#!/usr/bin/env python3
"""
Installation script for Claude Code settings template.
Safely copies settings to ~/.claude while preserving existing user configurations.
"""

import json
import os
import shutil
import sys
from pathlib import Path
from typing import Dict, Any, Set, Union


def deep_merge_dicts(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge source into target, with source taking precedence."""
    result = target.copy()
    
    for key, value in source.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge_dicts(result[key], value)
        else:
            result[key] = value
    
    return result


def apply_user_choices(target: Dict[str, Any], source: Dict[str, Any], choices: Dict[str, Any]) -> Dict[str, Any]:
    """Apply user choices to create a custom merged dictionary."""
    result = deep_merge_dicts(target, source)
    
    # Apply user choices by setting values at specific paths
    for path, chosen_value in choices.items():
        keys = path.split('.')
        current = result
        
        # Navigate to the parent of the target key
        for key in keys[:-1]:
            if key not in current:
                current[key] = {}
            current = current[key]
        
        # Set the final value
        final_key = keys[-1]
        if chosen_value == "<missing>":
            current.pop(final_key, None)
        else:
            current[final_key] = chosen_value
    
    return result


def get_value_at_path(data: Dict[str, Any], path: str) -> Any:
    """Get value at a dot-separated path in a nested dictionary."""
    keys = path.split('.')
    current = data
    for key in keys:
        if isinstance(current, dict) and key in current:
            current = current[key]
        else:
            return None
    return current


def get_different_keys_with_values(dict1: Dict[str, Any], dict2: Dict[str, Any], prefix: str = "") -> Dict[str, tuple]:
    """Get all keys where both dictionaries have different values (excluding cases where only one has a value)."""
    different_keys = {}
    
    all_keys = set(dict1.keys()) | set(dict2.keys())
    
    for key in all_keys:
        current_key = f"{prefix}.{key}" if prefix else key
        
        # Only consider conflicts where both sides have values and they differ
        if key in dict1 and key in dict2:
            if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
                different_keys.update(get_different_keys_with_values(dict1[key], dict2[key], current_key))
            elif dict1[key] != dict2[key]:
                different_keys[current_key] = (dict1[key], dict2[key])
        # Skip cases where only one side has a value - these are handled by merge logic
    
    return different_keys


def get_different_keys(dict1: Dict[str, Any], dict2: Dict[str, Any], prefix: str = "") -> Set[str]:
    """Get all keys where the two dictionaries differ."""
    return set(get_different_keys_with_values(dict1, dict2, prefix).keys())


def ask_permission_with_choices(file_path: str, existing_settings: Dict[str, Any], source_settings: Dict[str, Any]) -> Union[bool, Dict[str, Any]]:
    """Ask user permission with granular choices for each conflicting setting."""
    differences = get_different_keys_with_values(existing_settings, source_settings)
    
    if not differences:
        return True
    
    print(f"\n⚠️  {file_path} has conflicting settings:")
    
    # Colors for terminal output
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    
    user_choices = {}
    
    for key, (current_val, new_val) in sorted(differences.items()):
        print(f"\n{YELLOW}Setting: {key}{RESET}")
        print(f"  {RED}Current: {json.dumps(current_val, indent=2) if current_val != '<missing>' else '<missing>'}{RESET}")
        print(f"  {GREEN}Template: {json.dumps(new_val, indent=2) if new_val != '<missing>' else '<missing>'}{RESET}")
        
        while True:
            choice = input(f"\n{BLUE}Choose:{RESET} (c)urrent, (t)emplate, (s)kip this file: ").lower().strip()
            if choice in ('c', 'current'):
                user_choices[key] = current_val
                break
            elif choice in ('t', 'template'):
                user_choices[key] = new_val
                break
            elif choice in ('s', 'skip'):
                return False
            else:
                print("Please enter 'c', 't', or 's'")
    
    return user_choices


def ask_permission(file_path: str, differences: Set[str]) -> bool:
    """Ask user permission to overwrite a file, showing what will change."""
    print(f"\n⚠️  {file_path} already exists and would be modified.")
    print("The following settings would change:")
    for diff in sorted(differences):
        print(f"  • {diff}")
    
    while True:
        response = input("\nOverwrite? (y/n): ").lower().strip()
        if response in ('y', 'yes'):
            return True
        elif response in ('n', 'no'):
            return False
        else:
            print("Please enter 'y' or 'n'")


def install_settings():
    """Main installation function."""
    script_dir = Path(__file__).parent
    
    # Support test mode with TEST_HOME environment variable
    if "TEST_HOME" in os.environ:
        home_dir = Path(os.environ["TEST_HOME"])
    else:
        home_dir = Path.home()
    
    claude_dir = home_dir / ".claude"
    
    print("🚀 Installing Claude Code settings template...")
    
    # Create ~/.claude directory if it doesn't exist
    claude_dir.mkdir(exist_ok=True)
    print(f"✅ Ensured {claude_dir} exists")
    
    # Files to copy (excluding README, .gitignore, and this script)
    files_to_copy = [
        "settings.json",
        "agents/",
        "commands/", 
        "instructions/",
        "shared/"
    ]
    
    for file_name in files_to_copy:
        source_path = script_dir / file_name
        dest_path = claude_dir / file_name
        
        if not source_path.exists():
            print(f"⚠️  Skipping {file_name} (not found)")
            continue
        
        # Special handling for settings.json
        if file_name == "settings.json" and dest_path.exists():
            try:
                with open(source_path, 'r') as f:
                    source_settings = json.load(f)
                with open(dest_path, 'r') as f:
                    existing_settings = json.load(f)
                
                # Check if they're different
                differences = get_different_keys(existing_settings, source_settings)
                
                if differences:
                    user_choice = ask_permission_with_choices(str(dest_path), existing_settings, source_settings)
                    
                    if user_choice is False:
                        print(f"⏭️  Skipped {file_name}")
                        continue
                    elif isinstance(user_choice, dict):
                        # Apply user's granular choices
                        merged_settings = apply_user_choices(existing_settings, source_settings, user_choice)
                    else:
                        # Default merge behavior (template takes precedence)
                        merged_settings = deep_merge_dicts(existing_settings, source_settings)
                    
                    with open(dest_path, 'w') as f:
                        json.dump(merged_settings, f, indent=2)
                    
                    print(f"🔄 Merged {file_name}")
                else:
                    print(f"✅ {file_name} is already up to date")
                
            except (json.JSONDecodeError, KeyError) as e:
                print(f"❌ Error processing {file_name}: {e}")
                if not ask_permission(str(dest_path), {"entire file (JSON error)"}):
                    print(f"⏭️  Skipped {file_name}")
                    continue
                shutil.copy2(source_path, dest_path)
                print(f"📋 Copied {file_name}")
            
        # Handle directories and markdown files
        elif dest_path.exists():
            if source_path.is_dir():
                # For directories, copy files individually with permission checks
                for src_file in source_path.rglob("*"):
                    if src_file.is_file():
                        rel_path = src_file.relative_to(source_path)
                        dst_file = dest_path / rel_path
                        
                        if dst_file.exists():
                            # Check if content is identical
                            try:
                                with open(src_file, 'r', encoding='utf-8') as f1, open(dst_file, 'r', encoding='utf-8') as f2:
                                    if f1.read() == f2.read():
                                        print(f"✅ {dst_file} is already up to date")
                                        continue
                            except (UnicodeDecodeError, IOError):
                                # For binary files or read errors, fall back to permission check
                                pass
                            
                            if not ask_permission(str(dst_file), {"entire file"}):
                                print(f"⏭️  Skipped {dst_file}")
                                continue
                        
                        dst_file.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(src_file, dst_file)
                        print(f"📋 Copied {dst_file}")
                
            else:
                # For individual files, check content first
                try:
                    with open(source_path, 'r', encoding='utf-8') as f1, open(dest_path, 'r', encoding='utf-8') as f2:
                        if f1.read() == f2.read():
                            print(f"✅ {file_name} is already up to date")
                            continue
                except (UnicodeDecodeError, IOError):
                    # For binary files or read errors, fall back to permission check
                    pass
                
                # Content differs, ask permission
                if not ask_permission(str(dest_path), {"entire file"}):
                    print(f"⏭️  Skipped {file_name}")
                    continue
                
                shutil.copy2(source_path, dest_path)
                print(f"📋 Copied {file_name}")
        
        else:
            # File doesn't exist, copy directly
            if source_path.is_dir():
                shutil.copytree(source_path, dest_path)
                print(f"📁 Copied directory {file_name}")
            else:
                shutil.copy2(source_path, dest_path)
                print(f"📋 Copied {file_name}")
    
    print(f"\n🎉 Installation complete! Settings are now in {claude_dir}")
    print("You can now use these Claude Code configurations in your projects.")


if __name__ == "__main__":
    try:
        install_settings()
    except KeyboardInterrupt:
        print("\n\n❌ Installation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        sys.exit(1)
#!/usr/bin/env python3
"""Generate test cases for shell JSON quoting correctness lab."""
import json
from pathlib import Path

RANDOM_SEED = 42

cases = []

def add(case_id, value, category, notes=""):
    cases.append({
        "id": case_id,
        "value": value,
        "category": category,
        "notes": notes
    })

# Plain strings
add("s_plain", "hello", "plain")
add("s_spaces", "hello world", "spaces")
add("s_empty", "", "empty")

# Quotes
add("s_dquote", 'He said "hi"', "quotes")
add("s_squote", "It's fine", "quotes")
add("s_both_quotes", 'She said "It\'s ok"', "quotes")

# Backslashes
add("s_backslash", "C:\\path\\to\\file", "backslash")
add("s_backslash_n", "line1\\nnot_a_newline", "backslash")

# Control chars
add("s_newline", "hello\nworld", "control")
add("s_tab", "a\tb\tc", "control")
add("s_cr", "x\ry", "control")
add("s_mixed_ws", " \t\n\r ", "control")

# Unicode / emoji
add("s_unicode", "café naïve résumé", "unicode")
add("s_emoji", "hello 👋 world 🌍", "unicode")
add("s_cjk", "测试 テスト", "unicode")

# JSON-like strings (look like numbers/bool/null but are strings)
add("s_looks_int", "12345", "json_like_string")
add("s_looks_float", "3.14", "json_like_string")
add("s_looks_true", "true", "json_like_string")
add("s_looks_false", "false", "json_like_string")
add("s_looks_null", "null", "json_like_string")

# Real JSON values (not strings)
add("v_int", 42, "json_value")
add("v_float", 3.14159, "json_value")
add("v_true", True, "json_value")
add("v_false", False, "json_value")
add("v_null", None, "json_value")
add("v_zero", 0, "json_value")
add("v_empty_str", "", "json_value")

# Arrays
add("arr_simple", [1, 2, 3], "array")
add("arr_strings", ["a", "b", "c"], "array")
add("arr_mixed", [1, "two", True, None], "array")
add("arr_nested", [[1, 2], [3, 4]], "array")

# Objects
add("obj_simple", {"a": 1, "b": 2}, "object")
add("obj_nested", {"x": {"y": {"z": 42}}}, "object")
add("obj_mixed", {"name": "bob", "age": 30, "active": True}, "object")

# Shell metacharacters
add("s_dollar", "price is $5", "shell_meta")
add("s_semicolon", "foo; rm -rf /", "shell_meta")
add("s_backtick", "use `date`", "shell_meta")
add("s_pipe", "a | b", "shell_meta")
add("s_redirect", "x > y < z", "shell_meta")
add("s_ampersand", "a & b", "shell_meta")
add("s_dollar_paren", "$(whoami)", "shell_meta")
add("s_all_meta", "; $ ` | & < > ' \" \\ \n \t", "shell_meta")

# File/env style
add("s_path", "/usr/local/bin:/usr/bin:/bin", "file_env")
add("s_env_value", "PATH=/foo:$BAR", "file_env")
add("s_json_blob", '{"key":"value"}', "file_env")

# Edge cases
add("s_slash", "a/b/c", "edge")
add("s_emoji_zwj", "👨‍👩‍👧‍👦", "edge")

# Output
Path("cases").mkdir(exist_ok=True)
with open("cases/cases.json", "w") as f:
    json.dump(cases, f, indent=2)

print(f"Generated {len(cases)} test cases -> cases/cases.json")
for c in cases:
    print(f"  {c['id']:20s} {c['category']:20s} {repr(str(c['value'])[:40])}")

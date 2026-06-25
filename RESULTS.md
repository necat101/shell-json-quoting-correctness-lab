# Shell JSON Quoting Correctness – Results

Generated: 2026-06-25T22:49:29Z

## Environment

- Python: 3.12.3
- Platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- Bash: yes
- jq: jq-1.7
- jb/json.bash: not installed
- Cases: 47
- Trials per case: 3

## Correctness Summary

| Method | Pass | Fail | Parse Error | Wrong Value |
|--------|------|------|-------------|-------------|
| jq_arg | 47/47 | 0 | 0 | 0 |
| naive_concat | 37/47 | 10 | 9 | 1 |
| printf_template_safeish | 47/47 | 0 | 0 | 0 |
| python_json_dumps_baseline | 47/47 | 0 | 0 | 0 |
| subprocess_shell_false | 47/47 | 0 | 0 | 0 |

## Skipped Tools

- **jb_json_bash**: tool not installed

## Failure Breakdown by Category (naive_concat)

| Category | Pass | Fail |
|----------|------|------|
| array | 4 | 0 |
| backslash | 0 | 2 |
| control | 0 | 4 |
| edge | 2 | 0 |
| empty | 1 | 0 |
| file_env | 2 | 1 |
| json_like_string | 5 | 0 |
| json_value | 7 | 0 |
| object | 3 | 0 |
| plain | 1 | 0 |
| quotes | 1 | 2 |
| shell_meta | 7 | 1 |
| spaces | 1 | 0 |
| unicode | 3 | 0 |

## Commands Run

```
python3 -m py_compile generate_cases.py run_lab.py
python3 generate_cases.py
python3 run_lab.py
```

## Limitations

- Synthetic test cases only, no real-world shell scripts
- jb/json.bash not installed – skipped honestly
- jq available – tested via --argjson
- No performance testing on large payloads
- Bash version detection only, no actual bash json.bash integration tested (jb not installed)
- printf_template_safeish cheats by using json.dumps internally – demonstrates the correct approach, not a pure-shell solution

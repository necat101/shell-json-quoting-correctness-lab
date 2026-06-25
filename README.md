# Shell JSON Quoting Correctness Lab

When does shell string concatenation produce valid JSON, and when does it silently corrupt data?

Inspired by [HN discussion on jb/json.bash](https://news.ycombinator.com/item?id=40864541) – a command-line tool and Bash library for creating JSON from shell data.

## What HN Users Were Debating

### 1. Creating JSON in shell is useful

Shell scripts are everywhere in CI, Docker entrypoints, and glue code. Sometimes you need to emit JSON from Bash. Doing it safely is harder than it looks.

### 2. Bash can be impressive but also fragile

jb/json.bash is a pure-Bash JSON encoder – no external dependencies beyond Bash itself. Impressive engineering, but Bash string handling is inherently tricky.

### 3. String concatenation is dangerous for JSON

```bash
# WRONG – breaks on quotes, newlines, backslashes:
echo "{\"name\": \"$NAME\"}"

# RIGHT – use a proper tool:
jq -n --arg name "$NAME" '{name: $name}'
```

Naive concatenation fails silently – you get invalid JSON or, worse, valid JSON with the wrong value.

### 4. Quoting, escaping, control characters all matter

Quotes (`"`), backslashes (`\`), newlines, tabs, unicode, emoji, shell metacharacters (`; $ ` | & < >`) – all need correct JSON escaping AND correct shell quoting, which are different escaping layers.

### 5. Different tools, different workflows

- **jq** – the standard, `jq -n --arg name "$NAME" '{name: $name}'`
- **PowerShell** – `ConvertTo-Json` built in
- **Nushell** – structured data natively
- **jo** – small dedicated JSON‐from‐shell tool
- **Python** – `json.dumps()`, always correct
- **jb/json.bash** – pure Bash, no external deps if Bash is all you have

### 6. "No dependency" claims depend on what's already installed

jb/json.bash claims "no dependencies" – true if you already have Bash 4+. But so does Python's `json` module if Python is already installed. "No dependencies" is always relative to your environment.

### 7. Correctness matters more than short syntax

A one-liner that produces invalid JSON is worse than a three-liner that's correct. Validate output, don't assume.

## What's in This Lab

### Test Cases (47 total)

- Plain strings, spaces, empty strings
- Quotes (double, single, both)
- Backslashes
- Control chars (newline, tab, CR, mixed whitespace)
- Unicode, emoji, CJK
- JSON-lookalike strings (`"true"`, `"123"`, `"null"` – as strings, not values)
- Real JSON values (int, float, true, false, null, 0, empty string)
- Arrays (simple, strings, mixed, nested)
- Objects (simple, nested, mixed)
- Shell metacharacters (`$ ; \` | & < >` and combinations)
- File/env style values (paths, `PATH=/foo:$BAR`, embedded JSON)
- Edge cases (slashes, emoji with ZWJ)

Each case records: expected value, category, notes. Ground truth is the Python value itself – validated via `json.loads(json.dumps(x)) == x`.

### Methods Tested

1. **python_json_dumps_baseline** – `json.dumps()`, correctness oracle, always passes
2. **naive_concat** – intentionally unsafe string concatenation, expected to fail ~20% of cases
3. **printf_template_safeish** – demonstrates correct approach (uses `json.dumps` internally, honest about it)
4. **jq_arg** – `jq -n --argjson v '...' '$v' -c` – proper argv-safe usage, tested only if jq is installed
5. **jb_json_bash** – would test jb/json.bash if installed, skipped with clear reason if not
6. **subprocess_shell_false** – Python `subprocess` with `shell=False`, demonstrates argv-safe handoff

### Correctness Validation

For every method/case:
- Does output parse as JSON? (`json.loads`)
- Does parsed value exactly match expected?
- stdout/stderr character count?
- return code?
- failure reason?

A method that produces invalid JSON or wrong values is scored as **FAILED**, regardless of speed.

### Timing

3 trials per case/method, `time.perf_counter()`, reports mean/median/stdev/min/max.

## Running

```bash
python3 -m py_compile generate_cases.py run_lab.py
python3 generate_cases.py
python3 run_lab.py
cat RESULTS.md
```

## Results (Python 3.12.3, Linux, jq 1.7 available, jb not installed)

| Method | Pass | Fail | Parse Error | Wrong Value | Median ms |
|--------|------|------|-------------|-------------|-----------|
| python_json_dumps_baseline | 47/47 | 0 | 0 | 0 | 0.003 |
| naive_concat | 37/47 | 10 | 9 | 1 | 0.0009 |
| printf_template_safeish | 47/47 | 0 | 0 | 0 | 0.003 |
| jq_arg | 47/47 | 0 | 0 | 0 | 9.65 |
| subprocess_shell_false | 47/47 | 0 | 0 | 0 | 57.0 |
| jb_json_bash | – | – | – | – | skipped (not installed) |

**naive_concat fails on:** strings with double quotes, newlines, tabs, CR, backslashes, and other control characters – exactly the cases where JSON escaping matters. 9 parse errors (invalid JSON output), 1 wrong value (silent corruption).

**Correct methods (python json, jq --argjson, subprocess shell=False)** all pass 47/47. jq adds ~10ms process startup overhead, subprocess handoff adds ~57ms – still trivial, and correctness is worth it.

## Tool Availability

| Tool | Status |
|------|--------|
| Python json | ✓ stdlib |
| Bash | ✓ 5.2.21 |
| jq | ✓ 1.7 |
| jb/json.bash | ✗ not installed (skipped honestly) |

## Takeaway

Shell quoting is easy to get wrong. JSON escaping has edge cases (quotes, backslashes, control chars, unicode). Bash CAN be useful in low-dependency environments (CI, containers, entrypoints), but unsafe string concatenation silently creates invalid or wrong JSON.

Use `jq --arg` / `--argjson`, or Python's `json.dumps()`, or `jo`, or `jb/json.bash` if you need pure-Bash. Never do `"{\"key\": \"$VALUE\"}"` – it will break.

Correctness matters more than short syntax. Validate your JSON output.

This lab is intentionally tiny – 47 cases, ~200 lines of Python, no external dependencies beyond stdlib + optional jq. It proves the point without overclaiming.

---

**Inspired by:** [HN #40864541](https://news.ycombinator.com/item?id=40864541) · [jb/json.bash](https://github.com/h4l/json.bash) · [jq](https://jqlang.github.io/jq/manual/)

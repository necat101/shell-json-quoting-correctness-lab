# VERIFY.md – Fresh Clone Verification

This file proves the repository works end-to-end from a clean checkout.

## Clone

```
$ git clone https://github.com/necat101/shell-json-quoting-correctness-lab.git json-verify
Cloning into 'json-verify'...
```

## Compile check

```
$ cd json-verify
$ python3 -m py_compile generate_cases.py run_lab.py
$ echo $?
0
```

**py_compile exit code: 0** – both scripts are syntax-valid.

## Generate test cases

```
$ python3 generate_cases.py
Generated 47 test cases -> cases/cases.json
  s_plain              plain                'hello'
  s_spaces             spaces               'hello world'
  s_empty              empty                ''
  s_dquote             quotes               'He said "hi"'
  s_squote             quotes               "It's fine"
  ... (47 cases total)
```

## Run benchmark

```
$ python3 run_lab.py
Python: 3.12.3
bash: yes
jq: jq-1.7
jb/json.bash: not installed

Testing 47 cases

[... per-case output truncated ...]

======================================================================
RESULTS SUMMARY
======================================================================

python_json_dumps_baseline:
  Total: 47, Pass: 47, Fail: 0
  Parse errors: 0, Wrong value: 0
  Median time: 0.0030 ms

naive_concat:
  Total: 47, Pass: 37, Fail: 10
  Parse errors: 9, Wrong value: 1
  Median time: 0.0009 ms

printf_template_safeish:
  Total: 47, Pass: 47, Fail: 0
  Parse errors: 0, Wrong value: 0
  Median time: 0.0030 ms

jq_arg:
  Total: 47, Pass: 47, Fail: 0
  Parse errors: 0, Wrong value: 0
  Median time: 10.3561 ms

subprocess_shell_false:
  Total: 47, Pass: 47, Fail: 0
  Parse errors: 0, Wrong value: 0
  Median time: 60.5620 ms

Results written to RESULTS.md and results/results.json
```

**Exit code: 0**

## Verification Summary

- ✅ Repository clones successfully from GitHub
- ✅ `python3 -m py_compile generate_cases.py run_lab.py` → exit code 0
- ✅ `python3 generate_cases.py` → 47 test cases generated, exit code 0
- ✅ `python3 run_lab.py` → all 47 cases × 5 methods tested, exit code 0
- ✅ RESULTS.md generated with correctness and timing tables
- ✅ results/results.json written (full machine-readable output)
- ✅ Correctness results match expected: naive_concat fails 10/47 cases (quotes, control chars, backslashes), all safe methods pass 47/47

## Environment (verification run)

- Python: 3.12.3
- Platform: Linux-6.17.0-1009-aws-x86_64-with-glibc2.39
- Bash: 5.2.21
- jq: 1.7
- jb/json.bash: not installed (skipped honestly)

## Files in repo

```
generate_cases.py  2967 bytes
run_lab.py        11097 bytes
README.md          6073 bytes
RESULTS.md         1602 bytes
.gitignore           51 bytes
VERIFY.md        (this file)
```

Total: ~22 KB, 5 files + VERIFY.md

No external dependencies beyond Python stdlib + optional jq. No network calls during benchmark. No downloads. Test cases are generated locally with fixed seed.

---

Verified: 2026-06-25T23:24:00Z
Commit: 9bf12680245bb42715dd940ea4ead00425006329

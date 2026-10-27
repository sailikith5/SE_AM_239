# Issues Found – Lab 5 Static Code Analysis

**Student:** Sai Likhith S (PES1UG24AM239) | **File:** `library_system.py` | **Repo:** L5_01_library_fines

Score before: Pylint 6.07/10, Bandit 1 Medium + 1 Low, Flake8 14 messages.
Score after: Pylint 10.00/10, Bandit 0 issues, Flake8 0 messages.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| `eval()` on rule string (Bandit B307, Pylint W0123) | Security (Medium) | 45 | `fine_from_rule` passed a caller-supplied string to `eval`, allowing arbitrary code execution. | Replaced with an `ast`-based evaluator that only allows numbers, `days`, `+ - * /` and unary +/-; anything else raises `ValueError`. |
| Bare `except: pass` (Bandit B110, Pylint W0702, Flake8 E722) | Security / Bug (Low) | 21-22 | `return_book` swallowed every error, including typos and Ctrl-C, so failed returns were silent. | Catch only `(KeyError, ValueError)` and print a clear "no such loan" message. |
| Mutable default argument (Pylint W0102) | Bug | 9, 12 | `dates=[]` is shared across calls, so "loan dates on record" kept growing (1, 2, 3) for unrelated students. | Default to `None` and create a new list inside the function. |
| Renewal changes the global fine rate (not flagged by tools; Pylint W0603 on `global`) | Logic bug | 27-31 | `renewBook` with more than 14 extra days did `FINE_PER_DAY += 1`, so renewing a book raised fines for everyone (5 days cost 15 instead of 10). | Removed the global mutation, so renewal only reports the renewal. Also renamed to `renew_book` (Pylint C0103). |
| Negative fine (not flagged by tools) | Logic bug | 24-25 | `calculate_fine(-3)` returned -9, i.e. the library would owe the student money. | Clamp with `max(days_overdue, 0)`. |
| Integer book id accepted (not flagged by tools) | Bug | 56 | `add_book_loan("S103", 4521)` stored a non-string id, which the source comment says is wrong. Empty student ids were also dropped silently. | Validate that `book_id` is a non-empty string and print a message for both invalid cases. |
| Unclosed files, no encoding (Pylint R1732, W1514) | Quality / Bug | 33-42 | `open()` without `with` leaks the handle if an exception occurs; encoding left to platform default. | Use `with open(..., encoding="utf-8")`; `load_records` also handles missing or corrupt JSON. |
| `global loans` reassignment (Pylint W0603) | Design | 35 | `load_records` rebound the module global. | `loans.clear()` then `loans.update(data)`. |
| Unhandled `int(days)` input | Bug | 63 | Typing text such as `abc` crashed the program with a traceback. | Wrap in `try/except ValueError` with a friendly message. |
| `main()` runs on import | Design | 68 | Importing the module executed the demo and prompted for input. | Added `if __name__ == "__main__":` guard. |
| Unused import `os` (Pylint W0611, Flake8 F401) | Style | 2 | Dead import. | Removed. |
| Missing docstrings (Pylint C0114/C0116) | Style | 1 and all functions | No module or function documentation. | Added concise docstrings. |
| Old-style `%` / `+` string building (Pylint C0209) | Style | 14, 31 | String formatting could be f-strings. | Converted to f-strings. |
| Blank lines and long lines (Flake8 E302, E305, E501) | Style | 9-68 | Missing blank lines between functions, two lines over 79 chars. | Reformatted to PEP 8. |

## Commits
1. Bandit fixes (eval, try/except/pass)
2. Pylint fixes (plus the logic bugs above)
3. Flake8 formatting fixes

# Reflection – Lab 5

The handout I was given lists the deliverables but not the reflection questions, so these answer the four common ones for this lab.

**1. Which tool was most useful, and why?**
Bandit was the most important because it caught the only real security hole, `eval()` on a caller-supplied string, which allows arbitrary code execution. Pylint gave the most findings and found the mutable default argument and the global state. Flake8 was the quickest to satisfy but only affects style.

**2. Which issues were hardest to fix, and which were false positives or judgement calls?**
Replacing `eval` was hardest because a plain swap to `ast.literal_eval` cannot do arithmetic like `days * 2 + 10`, so I wrote a small AST evaluator that allows only numbers, `days` and basic operators. Missing docstrings were more of a style rule than a defect. No finding was truly false; the bare `except` warnings were legitimate because the code was silencing real errors.

**3. What did the tools miss?**
The tools did not flag the worst behaviour bugs: renewing a book silently raised the fine rate for everyone, negative days produced negative fines, and an integer book id was accepted. I only found those by running the program and reading its output, so a clean report does not prove the program is correct.

**4. How does static analysis help code quality and maintainability?**
It gives fast, repeatable feedback without running the code, enforces a consistent style, and catches whole classes of risky patterns (mutable defaults, broad exceptions, `eval`, unclosed files) before review. Pylint went from 6.07 to 10.00, Bandit from 2 findings to 0 and Flake8 from 14 to 0. It works best alongside testing and code review, and in CI so regressions are caught automatically.

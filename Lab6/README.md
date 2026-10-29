# Lab 6 — Code and Branch Coverage

**Name:** Sai Likhith S  **SRN:** PES1UG24AM239
**Source repo:** SETAPESU26/L6_L7_01_water_utility_billing (water utility billing)

## Files
| File | Purpose |
|------|---------|
| `water_utility_billing.py` | Module under test (unchanged) |
| `test_water_utility.py` | Starter test (unchanged) |
| `CodeCoverageTest_water_utility_billing.py` | Tests for line coverage |
| `BranchCoverageTest_water_utility_billing.py` | Tests for branch coverage |
| `code_coverage.png` / `branch_coverage.png` | Terminal screenshots |
| `*_output.txt` | Raw coverage output |

## Results
| Test file | Line coverage | Branch coverage |
|-----------|---------------|-----------------|
| Starter only | 46% | 41% |
| CodeCoverageTest | 100% | 99% |
| BranchCoverageTest | 100% | 100% |

## Commands
```
pip install coverage pytest
coverage run -m pytest CodeCoverageTest_water_utility_billing.py
coverage report -m
coverage erase
coverage run --branch -m pytest BranchCoverageTest_water_utility_billing.py
coverage report -m
```

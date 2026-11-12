# Lab 7 — Fuzzing for Input Validation Bugs (Hypothesis)

**Name:** Sai Likhith S  **SRN:** PES1UG24AM239
**Source repo:** SETAPESU26/L6_L7_01_water_utility_billing (water utility billing)

## Files
| File | Purpose |
|------|---------|
| `processor.py` | Fixed, hardened module |
| `test_processor.py` | Hypothesis fuzz tests (3 no-crash tests + 5 property tests) |
| `Lab7_Report.pdf` | Screenshots of the 4 required runs |
| `original_buggy/processor.py` | Original buggy starter code, kept for reference |

## Bugs found and fixed
| Function | Bug found by fuzzing | Fix |
|----------|----------------------|-----|
| `sanitize_meter_id` | `None` -> AttributeError | Non-string input returns `""` |
| `parse_consumption_readings` | `None`, `""`, `"1,,3"`, `"one,two"` -> AttributeError / ValueError | Non-string returns `[]`; blank and non-numeric items are skipped |
| `format_billing_summary` | `None`, too few fields (IndexError), non-numeric usage (ValueError) | Malformed records return an "Invalid account record" message |

## Commands
```
pip install hypothesis pytest
python processor.py
python -m pytest test_processor.py
```

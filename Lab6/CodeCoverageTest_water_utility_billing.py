"""
Lab 6 - Code (line) coverage tests for water_utility_billing.py
Name: Sai Likhith S | SRN: PES1UG24AM239

Run:
    coverage run -m pytest CodeCoverageTest_water_utility_billing.py
    coverage report -m
"""
import pytest
from water_utility_billing import calculate_water_bill, check_meter_tampering


def make_account(usage, active=True, commercial=False, waiver=False):
    return {
        "is_active": active,
        "is_commercial": commercial,
        "has_leak_waiver": waiver,
        "usage_blocks": usage,
    }


# ---------- calculate_water_bill ----------

def test_single_active_residential():
    # Starter test: 10 base + 30 * 1.5 = 55
    result = calculate_water_bill([make_account([30])], 10.0)
    assert result == {"total_billed": 55.0, "status": "NORMAL"}


def test_invalid_accounts_type_raises():
    with pytest.raises(ValueError):
        calculate_water_bill("not a list", 10.0)


def test_inactive_account_is_skipped():
    result = calculate_water_bill([make_account([30], active=False)], 10.0)
    assert result["total_billed"] == 0.0
    assert result["status"] == "NO_ACTIVITY"


def test_non_positive_usage_is_flagged_and_not_billed():
    result = calculate_water_bill([make_account([0, -5])], 10.0)
    assert result == {"total_billed": 10.0, "status": "NORMAL"}


def test_residential_high_usage_breaks_after_first_high_block():
    # 10 + 150 * 4.5 = 685; the second block (20) is ignored because of break
    result = calculate_water_bill([make_account([150, 20])], 10.0)
    assert result["total_billed"] == 685.0


def test_commercial_high_usage_continues_after_high_block():
    # 10 + 150 * 3.5 + 20 * 1.5 = 565
    result = calculate_water_bill([make_account([150, 20], commercial=True)], 10.0)
    assert result["total_billed"] == 565.0


def test_medium_usage_tier():
    # 10 + 80 * 2.5 = 210
    result = calculate_water_bill([make_account([80])], 10.0)
    assert result["total_billed"] == 210.0


def test_leak_waiver_applied_when_total_over_200():
    # 10 + 80 * 2.5 = 210 -> 210 - 50 = 160
    result = calculate_water_bill([make_account([80], waiver=True)], 10.0)
    assert result["total_billed"] == 160.0


def test_excessive_flags_status():
    result = calculate_water_bill([make_account([0, 0, 0, 0, 0, 0])], 10.0)
    assert result["status"] == "EXCESSIVE_FLAGS"


def test_no_activity_status_when_nothing_billed():
    result = calculate_water_bill([], 10.0)
    assert result == {"total_billed": 0.0, "status": "NO_ACTIVITY"}


# ---------- check_meter_tampering ----------

def test_tampering_no_data():
    assert check_meter_tampering([]) == "NO_DATA"


def test_tampering_two_consecutive_backward_readings():
    assert check_meter_tampering([[5, -1, -2]]) == "TAMPER_SUSPECTED"


def test_tampering_clear():
    assert check_meter_tampering([[1, 2, 3]]) == "CLEAR"

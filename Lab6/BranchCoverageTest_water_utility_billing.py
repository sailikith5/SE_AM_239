"""
Lab 6 - Branch coverage tests for water_utility_billing.py
Name: Sai Likhith S | SRN: PES1UG24AM239

Every decision in the module is exercised for BOTH its True and False outcome.

Run:
    coverage run --branch -m pytest BranchCoverageTest_water_utility_billing.py
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


# =====================================================================
# calculate_water_bill - input validation (line 2: `A or B`)
# =====================================================================

def test_accounts_not_a_list_raises():                # A True
    with pytest.raises(ValueError):
        calculate_water_bill("not a list", 10.0)


def test_accounts_none_raises():                      # A True (None)
    with pytest.raises(ValueError):
        calculate_water_bill(None, 10.0)


def test_negative_base_fee_raises():                  # A False, B True
    with pytest.raises(ValueError):
        calculate_water_bill([make_account([10])], -1.0)


def test_zero_base_fee_is_valid():                    # A False, B False (boundary)
    result = calculate_water_bill([make_account([10])], 0.0)
    assert result == {"total_billed": 15.0, "status": "NORMAL"}


# =====================================================================
# is_active check (line 9)
# =====================================================================

def test_active_account_is_billed():                  # active -> not skipped
    result = calculate_water_bill([make_account([30])], 10.0)
    assert result == {"total_billed": 55.0, "status": "NORMAL"}


def test_inactive_account_is_skipped():               # inactive -> continue
    result = calculate_water_bill([make_account([30], active=False)], 10.0)
    assert result == {"total_billed": 0.0, "status": "NO_ACTIVITY"}


def test_account_missing_is_active_key_defaults_to_inactive():
    result = calculate_water_bill([{"usage_blocks": [30]}], 10.0)
    assert result["total_billed"] == 0.0


def test_active_account_with_missing_keys_pays_base_fee_only():
    result = calculate_water_bill([{"is_active": True}], 10.0)
    assert result == {"total_billed": 10.0, "status": "NORMAL"}


def test_mixed_active_and_inactive_accounts():
    accounts = [make_account([30]), make_account([30], active=False), make_account([30])]
    result = calculate_water_bill(accounts, 10.0)
    assert result["total_billed"] == 110.0


# =====================================================================
# usage <= 0 (line 17) and usage tiers (lines 21, 27)
# =====================================================================

def test_zero_usage_is_flagged_not_billed():          # usage <= 0 True (boundary 0)
    result = calculate_water_bill([make_account([0])], 10.0)
    assert result["total_billed"] == 10.0


def test_negative_usage_is_flagged_not_billed():      # usage <= 0 True (negative)
    result = calculate_water_bill([make_account([-5])], 10.0)
    assert result["total_billed"] == 10.0


def test_usage_of_one_is_lowest_billable():           # usage <= 0 False (boundary 1)
    result = calculate_water_bill([make_account([1])], 10.0)
    assert result["total_billed"] == 11.5


def test_usage_exactly_50_is_low_tier():              # usage > 50 False (boundary)
    result = calculate_water_bill([make_account([50])], 10.0)
    assert result["total_billed"] == 85.0             # 10 + 50*1.5


def test_usage_51_is_medium_tier():                   # usage > 50 True (boundary)
    result = calculate_water_bill([make_account([51])], 10.0)
    assert result["total_billed"] == 137.5            # 10 + 51*2.5


def test_usage_exactly_100_is_medium_tier():          # usage > 100 False (boundary)
    result = calculate_water_bill([make_account([100])], 10.0)
    assert result["total_billed"] == 260.0            # 10 + 100*2.5


def test_usage_101_is_high_tier_residential():        # usage > 100 True (boundary)
    result = calculate_water_bill([make_account([101])], 10.0)
    assert result["total_billed"] == 464.5            # 10 + 101*4.5


# =====================================================================
# is_commercial (line 23) and the break (line 25)
# =====================================================================

def test_residential_high_usage_breaks_loop():        # not is_commercial True -> break
    result = calculate_water_bill([make_account([150, 20])], 10.0)
    assert result["total_billed"] == 685.0            # 10 + 150*4.5, 20 ignored


def test_commercial_high_usage_does_not_break():      # not is_commercial False
    result = calculate_water_bill([make_account([150, 20], commercial=True)], 10.0)
    assert result["total_billed"] == 565.0            # 10 + 150*3.5 + 20*1.5


# =====================================================================
# Leak waiver (lines 32-33): waiver flag AND total > 200
# =====================================================================

def test_waiver_with_total_over_200_is_applied():     # waiver True, > 200 True
    result = calculate_water_bill([make_account([80], waiver=True)], 10.0)
    assert result["total_billed"] == 160.0            # 210 - 50


def test_waiver_with_total_under_200_not_applied():   # waiver True, > 200 False
    result = calculate_water_bill([make_account([30], waiver=True)], 10.0)
    assert result["total_billed"] == 55.0


def test_waiver_with_total_exactly_200_not_applied(): # waiver True, > 200 False (boundary)
    # 20 base + 72 * 2.5 = 200.0 exactly
    result = calculate_water_bill([make_account([72], waiver=True)], 20.0)
    assert result["total_billed"] == 200.0


def test_no_waiver_with_total_over_200_not_applied(): # waiver False
    result = calculate_water_bill([make_account([80], waiver=False)], 10.0)
    assert result["total_billed"] == 210.0


# =====================================================================
# Status (lines 39 and 41)
# =====================================================================

def test_status_excessive_flags_when_more_than_5():   # flagged > 5 True
    result = calculate_water_bill([make_account([0, 0, 0, 0, 0, 0])], 10.0)
    assert result == {"total_billed": 10.0, "status": "EXCESSIVE_FLAGS"}


def test_status_normal_with_exactly_5_flags():        # flagged > 5 False (boundary)
    result = calculate_water_bill([make_account([0, 0, 0, 0, 0])], 10.0)
    assert result["status"] == "NORMAL"


def test_flags_accumulate_across_accounts():
    accounts = [make_account([0, 0, 0]), make_account([-1, -1, -1])]
    result = calculate_water_bill(accounts, 10.0)
    assert result["status"] == "EXCESSIVE_FLAGS"


def test_excessive_flags_takes_priority_over_no_activity():
    # base fee 0 -> total is 0.0, but 6 flags still win
    result = calculate_water_bill([make_account([0] * 6)], 0.0)
    assert result == {"total_billed": 0.0, "status": "EXCESSIVE_FLAGS"}


def test_status_no_activity_with_empty_list():        # total == 0.0 True
    assert calculate_water_bill([], 10.0) == {"total_billed": 0.0, "status": "NO_ACTIVITY"}


def test_status_no_activity_with_zero_base_fee_and_no_usage():
    result = calculate_water_bill([make_account([])], 0.0)
    assert result == {"total_billed": 0.0, "status": "NO_ACTIVITY"}


def test_empty_usage_blocks_loop_never_runs():
    result = calculate_water_bill([make_account([])], 10.0)
    assert result == {"total_billed": 10.0, "status": "NORMAL"}


def test_total_is_rounded_to_two_decimals():
    result = calculate_water_bill([make_account([3])], 0.333)
    assert result["total_billed"] == round(0.333 + 4.5, 2)


# =====================================================================
# check_meter_tampering
# =====================================================================

def test_tampering_empty_matrix():                    # `not readings_matrix` True
    assert check_meter_tampering([]) == "NO_DATA"


def test_tampering_none_matrix():
    assert check_meter_tampering(None) == "NO_DATA"


def test_tampering_two_consecutive_negatives():       # delta < 0 and count >= 2
    assert check_meter_tampering([[5, -1, -2]]) == "TAMPER_SUSPECTED"


def test_tampering_single_negative_is_not_enough():   # delta < 0, count >= 2 False
    assert check_meter_tampering([[5, -1, 3]]) == "CLEAR"


def test_tampering_non_consecutive_negatives_reset():  # else branch resets counter
    assert check_meter_tampering([[-1, 4, -1, 4, -1]]) == "CLEAR"


def test_tampering_zero_delta_resets_counter():       # 0 is not < 0
    assert check_meter_tampering([[-1, 0, -1]]) == "CLEAR"


def test_tampering_detected_on_a_later_meter():       # outer loop advances
    assert check_meter_tampering([[1, 2, 3], [4, -1, -1]]) == "TAMPER_SUSPECTED"


def test_tampering_counter_does_not_leak_between_meters():
    # Meter 1 ends with one negative, meter 2 starts with one negative.
    assert check_meter_tampering([[1, -1], [-1, 1]]) == "CLEAR"


def test_tampering_meter_with_no_readings():          # inner loop never runs
    assert check_meter_tampering([[]]) == "CLEAR"


def test_tampering_all_meters_clear():
    assert check_meter_tampering([[1, 2], [3, 4], [5]]) == "CLEAR"

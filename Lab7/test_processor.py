"""
Lab 7 - Fuzz tests for processor.py using Hypothesis.
Name: Sai Likhith S | SRN: PES1UG24AM239

Part A: the three "no crash" fuzz tests from the handout (text or None).
Part B: stronger property tests that check the output is actually correct.
"""
from hypothesis import given, example, strategies as st
from processor import sanitize_meter_id, parse_consumption_readings, format_billing_summary

SPECIAL_CHARS = "!@#$%"


# ---------------------------------------------------------------------
# Part A - robustness: none of the functions may raise for ANY input
# ---------------------------------------------------------------------

@given(st.text() | st.none())
@example(None)
@example("")
@example("   !@#   ")
def test_sanitize_meter_id_no_crash(s):
    try:
        sanitize_meter_id(s)
    except Exception as e:
        assert False, f"sanitize_meter_id crashed with: {e!r}"


@given(st.text() | st.none())
@example(None)
@example("")
@example("1,,3")
@example("one,two")
@example(",")
def test_parse_consumption_readings_safe(s):
    try:
        parse_consumption_readings(s)
    except Exception as e:
        assert False, f"parse_consumption_readings crashed with: {e!r}"


@given(st.text() | st.none())
@example(None)
@example("")
@example("Ravi:10")
@example("Ravi:abc:Zone1")
@example("a:b:c:d")
def test_format_billing_summary_safe(s):
    try:
        format_billing_summary(s)
    except Exception as e:
        assert False, f"format_billing_summary crashed with: {e!r}"


# ---------------------------------------------------------------------
# Part B - correctness properties
# ---------------------------------------------------------------------

@given(st.text() | st.none())
def test_sanitize_always_returns_clean_string(s):
    result = sanitize_meter_id(s)
    assert isinstance(result, str)
    assert not any(ch in result for ch in SPECIAL_CHARS)


@given(st.text() | st.none())
def test_parse_always_returns_list_of_ints(s):
    result = parse_consumption_readings(s)
    assert isinstance(result, list)
    assert all(isinstance(x, int) for x in result)


@given(st.lists(st.integers(min_value=-10**9, max_value=10**9)))
def test_parse_round_trips_valid_readings(values):
    csv = ",".join(str(v) for v in values)
    assert parse_consumption_readings(csv) == values


@given(st.text() | st.none())
def test_format_always_returns_string(s):
    assert isinstance(format_billing_summary(s), str)


@given(
    name=st.text(alphabet=st.characters(whitelist_categories=("L",)), min_size=1),
    units=st.integers(min_value=0, max_value=10**6),
    zone=st.text(alphabet=st.characters(whitelist_categories=("L", "N")), min_size=1),
)
def test_format_valid_record_is_billed_at_double(name, units, zone):
    result = format_billing_summary(f"{name}:{units}:{zone}")
    assert result == f"Customer {name.strip()} billed {units * 2} USD in {zone.strip()}"

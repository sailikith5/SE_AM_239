"""
Lab 7 - Hardened water utility input processing (fixed version).
Name: Sai Likhith S | SRN: PES1UG24AM239

Bugs found by fuzzing the original code, and how each is fixed:

sanitize_meter_id
  * None / non-string input -> AttributeError on .strip()
    FIX: non-string input returns an empty string.

parse_consumption_readings
  * None / non-string input -> AttributeError on .split()
  * empty element ("1,,3") or empty string -> ValueError from int("")
  * non-numeric element ("one,two") -> ValueError
    FIX: non-string input returns []; blank or non-numeric elements are skipped.

format_billing_summary
  * None / non-string input -> AttributeError
  * too few fields ("Ravi:10") -> IndexError
  * non-numeric usage ("Ravi:abc:Z1") -> ValueError
    FIX: any malformed record returns a clear "Invalid account record" message.
"""

SPECIAL_CHARS = ['!', '@', '#', '$', '%']
INVALID_RECORD_MSG = "Invalid account record (expected Name:Usage:Zone)"


def sanitize_meter_id(meter_id):
    if not isinstance(meter_id, str):
        return ""
    meter_id = meter_id.strip()
    for ch in SPECIAL_CHARS:
        meter_id = meter_id.replace(ch, '')
    return meter_id.upper()


def parse_consumption_readings(readings_csv):
    if not isinstance(readings_csv, str):
        return []
    readings = []
    for item in readings_csv.split(','):
        item = item.strip()
        if not item:
            continue
        try:
            readings.append(int(item))
        except ValueError:
            continue
    return readings


def format_billing_summary(account_record):
    if not isinstance(account_record, str):
        return INVALID_RECORD_MSG
    parts = account_record.split(':')
    if len(parts) != 3:
        return INVALID_RECORD_MSG
    customer_name = parts[0].strip()
    zone = parts[2].strip()
    if not customer_name or not zone:
        return INVALID_RECORD_MSG
    try:
        units = int(parts[1])
    except ValueError:
        return INVALID_RECORD_MSG
    if units < 0:
        return INVALID_RECORD_MSG
    return f"Customer {customer_name} billed {units * 2} USD in {zone}"


def main():
    print("==== Running sanitize_meter_id ====")
    raw_id = input("Enter a meter ID with prefixes (!,@,#,$,%): ")
    clean_id = sanitize_meter_id(raw_id)
    print("Sanitized Meter ID:", clean_id)

    print("\n==== Running parse_consumption_readings ====")
    csv_input = input("Enter consumption readings (e.g. 10,25,30): ")
    readings_list = parse_consumption_readings(csv_input)
    print("Parsed Readings:", readings_list)

    print("\n==== Running format_billing_summary ====")
    summary_input = input("Enter account record (Name:Usage:Zone): ")
    summary = format_billing_summary(summary_input)
    print("Billing Summary:", summary)


if __name__ == "__main__":
    main()

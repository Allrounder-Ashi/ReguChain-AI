
import json
from pathlib import Path

from integrity import calculate_file_hash

REPORT_PATH = Path("reports/REGU-001.json")
AUDIT_PATH = Path("reports/audit_log.json")


def verify_latest_record():
    if not AUDIT_PATH.exists():
        print("INTEGRITY CHECK FAILED: Audit log not found.")
        return

    records = json.loads(
        AUDIT_PATH.read_text(encoding="utf-8")
    )

    if not records:
        print("INTEGRITY CHECK FAILED: No audit records.")
        return

    latest = records[-1]
    expected_hash = latest["sha256"]

    if not REPORT_PATH.exists():
        print("INTEGRITY CHECK FAILED: Report not found.")
        return

    actual_hash = calculate_file_hash(str(REPORT_PATH))

    print("Expected SHA-256:", expected_hash)
    print("Actual SHA-256:  ", actual_hash)

    if actual_hash == expected_hash:
        print("RESULT: INTEGRITY VERIFIED")
    else:
        print("RESULT: POSSIBLE TAMPERING DETECTED")


if __name__ == "__main__":
    verify_latest_record()


import json
from datetime import datetime, timezone
from pathlib import Path

from integrity import calculate_file_hash

REPORT_PATH = Path("reports/REGU-001.json")
AUDIT_PATH = Path("reports/audit_log.json")


def record_report_hash():
    if not REPORT_PATH.exists():
        raise FileNotFoundError(
            f"Report not found: {REPORT_PATH}"
        )

    report_hash = calculate_file_hash(str(REPORT_PATH))

    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)

    if AUDIT_PATH.exists():
        records = json.loads(
            AUDIT_PATH.read_text(encoding="utf-8")
        )
    else:
        records = []

    record = {
        "recorded_at": datetime.now(
            timezone.utc
        ).isoformat(),
        "report_path": str(REPORT_PATH),
        "sha256": report_hash,
    }

    records.append(record)

    AUDIT_PATH.write_text(
        json.dumps(records, indent=2),
        encoding="utf-8",
    )

    print("Audit record saved:", AUDIT_PATH)
    print("Recorded SHA-256:", report_hash)


if __name__ == "__main__":
    record_report_hash()

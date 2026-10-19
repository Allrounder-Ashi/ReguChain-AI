
import hashlib
import json
from pathlib import Path


def calculate_file_hash(file_path: str) -> str:
    """Calculate a SHA-256 hash of a file's exact bytes."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_file_hash(file_path: str, expected_hash: str) -> bool:
    """Check whether the current file matches its recorded hash."""
    actual_hash = calculate_file_hash(file_path)
    return actual_hash == expected_hash



if __name__ == "__main__":
    report_path = "reports/REGU-001.json"

    original_hash = calculate_file_hash(report_path)
    print("Report:", report_path)
    print("Recorded SHA-256:", original_hash)

    is_valid = verify_file_hash(report_path, original_hash)
    print("Integrity verified:", is_valid)


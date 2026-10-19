
from datetime import datetime, timezone


def detect_threat(event: dict) -> dict:
    """
    Analyze a sample security event locally.
    No external API or AI service is required.
    """

    event_type = str(event.get("event_type", "")).lower()
    failed_attempts = int(event.get("failed_attempts", 0))
    unusual_access = bool(event.get("unusual_access", False))

    reasons = []

    if failed_attempts >= 5:
        reasons.append("Multiple failed login attempts")

    if unusual_access:
        reasons.append("Unusual access pattern detected")

    if event_type in {"malware", "data_exfiltration", "unauthorized_access"}:
        reasons.append(f"Suspicious event type: {event_type}")

    if len(reasons) >= 2:
        severity = "HIGH"
    elif reasons:
        severity = "MEDIUM"
    else:
        severity = "LOW"

    return {
        "event_id": event.get("event_id", "EDGE-001"),
        "detected_at": datetime.now(timezone.utc).isoformat(),
        "event_type": event_type or "unknown",
        "severity": severity,
        "is_suspicious": bool(reasons),
        "reasons": reasons,
        "detection_method": "Local rule-based edge detection",
    }


from datetime import datetime, timezone


def build_evidence_record(
    incident: dict,
    detection: dict,
    regulatory_sources: list[dict] | None = None,
) -> dict:
    """
    Build a traceable evidence record for a suspected incident.

    This module organizes supplied evidence; it does not independently
    establish that a breach occurred or that a law applies.
    """

    regulatory_sources = regulatory_sources or []

    reasons = detection.get("reasons", [])
    sources = []

    for source in regulatory_sources:
        sources.append({
            "title": source.get("title", "Untitled source"),
            "url": source.get("url", ""),
            "snippet": source.get("snippet", ""),
            "verified_by_reviewer": False,
        })

    checks = [
        {
            "check": "Incident facts reviewed",
            "status": "PENDING",
        },
        {
            "check": "Regulatory applicability confirmed",
            "status": "PENDING",
        },
        {
            "check": "Reporting deadline confirmed",
            "status": "PENDING",
        },
        {
            "check": "Evidence sources reviewed",
            "status": "PENDING" if sources else "MISSING",
        },
    ]

    return {
        "evidence_id": incident.get("incident_id", "INC-UNKNOWN"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "incident": {
            "type": incident.get("incident_type", "unknown"),
            "description": incident.get("description", ""),
            "noticed_at": incident.get("noticed_at", ""),
        },
        "detection": {
            "method": detection.get(
                "detection_method",
                "Unspecified detection method",
            ),
            "severity": detection.get("severity", "UNKNOWN"),
            "suspicious": detection.get("is_suspicious", False),
            "supporting_signals": reasons,
        },
        "regulatory_sources": sources,
        "review_checks": checks,
        "decision": {
            "status": "HUMAN_REVIEW_REQUIRED",
            "confirmed_breach": False,
            "legal_applicability_confirmed": False,
            "message": (
                "This record organizes available signals and sources. "
                "It does not establish a confirmed breach or legal obligation."
            ),
        },
    }

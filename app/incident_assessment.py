
from datetime import datetime, timezone

from app.regulation_extractor import extract_reporting_rule

def assess_incident(description: str, noticed_at: str):
    """
    Create a preliminary incident assessment.

    noticed_at must be an ISO timestamp, for example:
    2026-10-17T10:30:00+05:30
    """
    description = description.strip()

    if not description:
        raise ValueError("Incident description cannot be empty.")

    try:
        noticed_time = datetime.fromisoformat(noticed_at)
    except ValueError as exc:
        raise ValueError(
            "Use an ISO timestamp, e.g. "
            "2026-10-17T10:30:00+05:30"
        ) from exc

    if noticed_time.tzinfo is None:
        raise ValueError(
            "Timestamp must include a timezone, such as +05:30."
        )

    rule = extract_reporting_rule()

    if not rule.get("found"):
        return {
            "status": "Needs manual review",
            "incident_description": description,
            "reason": "Could not extract the reporting rule.",
            "source": rule.get("source", "")
        }

    deadline = noticed_time + __import__(
        "datetime"
    ).timedelta(hours=6)

    return {
        "status": "Preliminary assessment — review required",
        "incident_description": description,
        "noticed_at": noticed_time.isoformat(),
        "potential_reporting_deadline": deadline.isoformat(),
        "requirement": rule["requirement"],
        "regulator": rule["regulator"],
        "regulatory_source": rule["source"],
        "legal_applicability_verified": False,
        "annexure_category_verified": False,
        "next_action": (
            "Verify entity coverage and the incident category "
            "against Annexure I, then obtain human review."
        )
    }


if __name__ == "__main__":
    result = assess_incident(
        description=(
            "A company detected unauthorized access "
            "to its internal server."
        ),
        noticed_at="2026-10-17T10:30:00+05:30"
    )

    for key, value in result.items():
        print(f"{key}: {value}")

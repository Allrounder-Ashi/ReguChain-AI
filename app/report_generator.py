

import json
from pathlib import Path
from datetime import datetime, timezone


def generate_report(assessment: dict) -> dict:
    """Create a reviewable incident report from an assessment."""

    report = {
        "report_id": "REGU-001",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "incident": {
            "description": assessment["incident_description"],
            "noticed_at": assessment["noticed_at"],
        },
        "regulatory_assessment": {
            "regulator": assessment["regulator"],
            "requirement": assessment["requirement"],
            "potential_deadline": assessment[
                "potential_reporting_deadline"
            ],
            "source": assessment["regulatory_source"],
        },
        "verification": {
            "legal_applicability_verified": assessment[
                "legal_applicability_verified"
            ],
            "annexure_category_verified": assessment[
                "annexure_category_verified"
            ],
            "human_review_required": True,
        },
        "status": "DRAFT — NOT SUBMITTED",
        "next_action": assessment["next_action"],
    }

    return report


def save_report(report: dict) -> Path:
    """Save a report as JSON and return its file path."""

    output_folder = Path("reports")
    output_folder.mkdir(parents=True, exist_ok=True)

    output_file = output_folder / "REGU-001.json"

    with output_file.open("w", encoding="utf-8") as file:
        json.dump(report, file, indent=2, ensure_ascii=False)

    return output_file


if __name__ == "__main__":
    from app.incident_assessment import assess_incident

    assessment = assess_incident(
        description=(
            "A company detected unauthorized access "
            "to its internal server."
        ),
        noticed_at="2026-10-17T10:30:00+05:30",
    )

    report = generate_report(assessment)
    output_file = save_report(report)

    print(f"Report saved to: {output_file}")
    print(json.dumps(report, indent=2, ensure_ascii=False))

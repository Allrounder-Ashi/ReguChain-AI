
import json
from datetime import datetime
from pathlib import Path

import streamlit as st

from app.incident_assessment import assess_incident
from app.report_generator import generate_report, save_report

BASE_DIR = Path(__file__).resolve().parent
REPORTS_DIR = BASE_DIR / "reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="ReguChain AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .stApp {
        background: #f3f6fb;
        color: #17243b;
    }
    [data-testid="stHeader"] {
        background: rgba(243, 246, 251, 0.95);
    }
    [data-testid="stSidebar"] {
        background: #101c35;
    }
    [data-testid="stSidebar"] * {
        color: #ffffff;
    }
    [data-testid="stSidebar"] label {
        color: #ffffff !important;
    }
    .hero {
        padding: 1.7rem 2rem;
        border-radius: 16px;
        background: linear-gradient(120deg, #10213f, #174c72);
        color: #ffffff;
        margin-bottom: 1.4rem;
    }
    .hero h1 {
        color: #ffffff !important;
        font-size: 2.1rem;
        margin-bottom: .5rem;
    }
    .hero p {
        color: #e2edf8 !important;
        margin-bottom: 0;
    }
    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dce5f0;
        border-radius: 12px;
        padding: 1rem;
    }
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: #17243b !important;
    }
    h1, h2, h3, p, label, .stMarkdown {
        color: #17243b;
    }
    .stButton button, .stFormSubmitButton button {
        background: #1769aa;
        color: #ffffff;
        border: 0;
        border-radius: 8px;
    }
    .stButton button:hover, .stFormSubmitButton button:hover {
        background: #125488;
        color: #ffffff;
        border: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def list_reports():
    items = []
    for path in sorted(REPORTS_DIR.glob("*.json")):
        if path.name == "audit_log.json":
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            items.append((path, data))
        except (json.JSONDecodeError, OSError):
            continue
    return items


with st.sidebar:
    st.markdown("# 🛡️ ReguChain AI")
    st.caption("Regulatory breach reporting")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "Dashboard",
            "Edge Threat Detection",
            "Evidence & Reasoning",
            "New Incident",
            "Reports & Audit",
            "Blockchain Status",
        ],
    )

    st.divider()
    st.caption("AI-assisted compliance workflow")
    st.caption("Human review required")

reports = list_reports()

if page == "Dashboard":
    st.markdown(
        """
        <div class="hero">
            <h1>Regulatory Compliance Command Center</h1>
            <p>Assess incidents, review reporting deadlines, and preserve
            report integrity in one workspace.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Reports available", len(reports))
    col2.metric("Incident drafts", len(reports))
    col3.metric("On-chain anchors", "Check status")
    col4.metric("Compliance status", "Review required")

    st.subheader("Workflow")
    a, b, c = st.columns(3)

    with a:
        st.markdown("### 1. Incident intake")
        st.write("Record incident details and discovery time.")

    with b:
        st.markdown("### 2. Regulatory assessment")
        st.write("Review relevant rules and preliminary deadlines.")

    with c:
        st.markdown("### 3. Integrity verification")
        st.write("Calculate report hashes and check blockchain status.")

    st.info(
        "Deadlines are preliminary. Confirm legal applicability and "
        "reporting obligations with a qualified reviewer."
    )

    if reports:
        st.subheader("Recent reports")
        for path, data in reports[-5:][::-1]:
            st.write(
                f"**{data.get('report_id', path.stem)}** — "
                f"{data.get('status', 'Status not specified')}"
            )
    else:
        st.write("No reports found yet. Select New Incident to begin.")

elif page == "Edge Threat Detection":
    from app.edge_detector import detect_threat

    st.title("Edge Threat Detection")
    st.write(
        "Analyze security events locally without calling an external AI API."
    )

    st.info(
        "Prototype mode: this page analyzes simulated events. "
        "It does not monitor live network traffic."
    )

    with st.form("edge_threat_form"):
        event_id = st.text_input("Event ID", value="EDGE-001")

        event_type = st.selectbox(
            "Event type",
            [
                "normal_activity",
                "unauthorized_access",
                "malware",
                "data_exfiltration",
            ],
        )

        failed_attempts = st.number_input(
            "Failed login attempts",
            min_value=0,
            max_value=100,
            value=0,
            step=1,
        )

        unusual_access = st.checkbox("Unusual access pattern detected")

        analyze = st.form_submit_button("Analyze Security Event")

    if analyze:
        event = {
            "event_id": event_id.strip() or "EDGE-001",
            "event_type": event_type,
            "failed_attempts": int(failed_attempts),
            "unusual_access": unusual_access,
        }

        result = detect_threat(event)

        st.subheader("Detection Result")

        if result["severity"] == "HIGH":
            st.error("HIGH severity — multiple suspicious indicators")
        elif result["severity"] == "MEDIUM":
            st.warning("MEDIUM severity — suspicious indicator detected")
        else:
            st.success("LOW severity — no configured suspicious rules matched")

        col1, col2, col3 = st.columns(3)
        col1.metric("Severity", result["severity"])
        col2.metric("Suspicious", "Yes" if result["is_suspicious"] else "No")
        col3.metric("Failed Attempts", failed_attempts)

        st.write("**Detection reasons**")
        if result["reasons"]:
            for reason in result["reasons"]:
                st.write(f"- {reason}")
        else:
            st.write("No configured suspicious patterns matched.")

        st.write("**Event details**")
        st.json(result)

        
        if result["is_suspicious"]:
            st.warning(
                "This alert may warrant investigation. "
                "It does not by itself confirm a breach or legal reporting duty."
            )

            if st.button("Create Incident Draft", key="create_edge_incident"):
                st.session_state["edge_incident_draft"] = {
                    "incident_id": f"INC-{result['event_id']}",
                    "incident_type": result["event_type"],
                    "description": (
                        "Locally detected security alert. "
                        f"Severity: {result['severity']}. "
                        "Indicators: " + "; ".join(result["reasons"])
                    ),
                    "detected_at": result["detected_at"],
                    "severity": result["severity"],
                    "status": "DRAFT — NOT SUBMITTED",
                }

                st.success(
                    "Incident draft prepared. Review it before regulatory assessment."
                )
                st.json(st.session_state["edge_incident_draft"])

                if st.button(
                    "Assess Draft for Regulatory Reporting",
                    key="assess_edge_incident",
                ):
                    try:
                        from app.incident_assessment import assess_incident
                        from app.report_generator import generate_report

                        draft = st.session_state["edge_incident_draft"]

                        with st.spinner("Preparing preliminary assessment..."):
                            assessment = assess_incident(
                                description=draft["description"],
                                noticed_at=draft["detected_at"],
                            )
                            report = generate_report(assessment)

                        st.session_state["edge_regulatory_report"] = report

                        report_id = report.get(
                            "report_id",
                            st.session_state["edge_incident_draft"]["incident_id"],
                        )

                        report_path = REPORTS_DIR / f"{report_id}.json"
                        report_path.write_text(
                            json.dumps(report, indent=2, ensure_ascii=False),
                            encoding="utf-8",
                        )

                        st.caption(f"Saved report: {report_path.name}")

                        st.success("Preliminary regulatory report generated.")
                        st.json(report)

                        st.warning(
                            "This is a draft only. Verify legal applicability, "
                            "the reporting deadline, and all facts with a "
                            "qualified reviewer before taking action."
                        )

                    except Exception as exc:
                        st.error("Assessment could not be completed.")
                        st.exception(exc)




elif page == "Evidence & Reasoning":
    from app.evidence_engine import build_evidence_record

    st.title("Evidence & Reasoning")
    st.write(
        "Trace detected signals, regulatory sources, and outstanding "
        "verification checks for an incident."
    )

    if "edge_incident_draft" not in st.session_state:
        st.info(
            "No incident draft is available yet. Go to Edge Threat Detection, "
            "analyze a suspicious event, and create an incident draft first."
        )
    else:
        draft = st.session_state["edge_incident_draft"]

        st.subheader("Incident Under Review")
        st.json(draft)

        detection = {
            "severity": draft.get("severity", "UNKNOWN"),
            "is_suspicious": True,
            "reasons": [
                reason.strip()
                for reason in draft.get("description", "").split("Indicators:")[-1].split(";")
                if reason.strip()
            ],
            "detection_method": "Local rule-based edge detection",
        }

        incident = {
            "incident_id": draft.get("incident_id", "INC-UNKNOWN"),
            "incident_type": draft.get("incident_type", "unknown"),
            "description": draft.get("description", ""),
            "noticed_at": draft.get("detected_at", ""),
        }

        evidence = build_evidence_record(incident, detection)

        st.subheader("Detection Evidence")
        col1, col2 = st.columns(2)
        col1.metric("Severity", detection["severity"])
        col2.metric(
            "Suspicious",
            "Yes" if detection["is_suspicious"] else "No",
        )

        st.write("**Supporting signals**")
        for reason in detection["reasons"]:
            st.write(f"- {reason}")

        st.subheader("Regulatory Source Evidence")
        st.warning(
            "No regulatory source has been attached to this evidence record. "
            "A source must be retrieved and reviewed before an obligation "
            "can be treated as supported."
        )

        st.subheader("Review Checklist")
        for check in evidence["review_checks"]:
            st.write(f"- **{check['status']}** — {check['check']}")

        st.subheader("Reasoning Record")
        st.json(evidence)

        st.caption(
            "This record organizes available information; it does not "
            "confirm a breach or determine legal applicability."
        )

elif page == "New Incident":
    st.title("New Incident")
    st.write(
        "Enter known facts. Avoid unnecessary personal or confidential data."
    )

    with st.form("incident_form"):
        incident_id = st.text_input("Incident ID", value="REGU-002")

        incident_type = st.selectbox(
            "Incident category",
            [
                "Cybersecurity incident",
                "Data breach",
                "Service disruption",
                "Unauthorized access",
                "Other / not yet classified",
            ],
        )

        organization = st.text_input("Organization name")
        description = st.text_area("Incident description")

        discovered_at = st.text_input(
            "Date/time discovered (ISO 8601)",
            value=datetime.now().astimezone().isoformat(timespec="seconds"),
            help="Example: 2026-10-17T10:30:00+05:30",
        )

        submit = st.form_submit_button("Assess & Generate Draft")

    if submit:
        if not incident_id.strip() or not description.strip():
            st.error("Please enter an incident ID and description.")
        else:
            try:
                # Match the current assess_incident(description, noticed_at)
                # function signature.
                with st.spinner("Assessing incident..."):
                    assessment = assess_incident(
                        description=description.strip(),
                        noticed_at=discovered_at.strip(),
                    )

                    # Match the current generate_report(assessment) signature.
                    report = generate_report(assessment)

                    report["report_id"] = incident_id.strip()
                    report["incident"]["category"] = incident_type
                    report["incident"]["organization"] = organization.strip()

                    report_path = REPORTS_DIR / f"{incident_id.strip()}.json"
                    report_path.write_text(
                        json.dumps(report, indent=2, ensure_ascii=False),
                        encoding="utf-8",
                    )

                st.success(f"Draft saved: {report_path.name}")
                st.json(report)
                st.warning(
                    "Draft only — not submitted to a regulator and not yet "
                    "anchored on-chain. Verify the applicable law and deadline."
                )

            except Exception as exc:
                st.error("Incident assessment or draft generation failed.")
                st.exception(exc)

elif page == "Reports & Audit":
    st.title("Reports & Audit Trail")

    if not reports:
        st.info("No report JSON files were found.")
    else:
        options = [path.name for path, _ in reports]
        selected = st.selectbox("Select a report", options)
        selected_path = REPORTS_DIR / selected

        st.subheader(selected)
        st.json(json.loads(selected_path.read_text(encoding="utf-8")))

        if st.button("Calculate SHA-256"):
            try:
                from app.integrity import calculate_file_hash

                st.write("SHA-256 hash of current file:")
                st.code(calculate_file_hash(str(selected_path)))
                st.caption(
                    "A hash identifies these exact file contents. It does "
                    "not prove a blockchain transaction occurred."
                )
            except Exception as exc:
                st.error(str(exc))

elif page == "Blockchain Status":
    st.title("Blockchain Status")
    st.write("Ethereum Sepolia testnet")

    st.info(
        "A contract connection does not mean a report is anchored. "
        "An anchor requires a confirmed transaction and on-chain verification."
    )

    if st.button("Check contract connection"):
        try:
            from app.blockchain_anchor import check_contract

            with st.spinner("Connecting to Sepolia..."):
                web3, contract = check_contract()

            st.success("Contract connection successful.")
            st.write("Chain ID:", web3.eth.chain_id)
            st.write("Contract address:", contract.address)
            st.write("Latest block:", web3.eth.block_number)

        except Exception as exc:
            st.error(
                "The contract connection helper may need to be added or "
                "updated to match your current blockchain_anchor.py."
            )
            st.code(str(exc))

    st.caption(
        "This connection check is read-only; it does not submit a transaction."
    )

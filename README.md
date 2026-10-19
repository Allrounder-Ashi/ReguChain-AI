# ReguChain AI 🛡️

**From cyber incident detection to verifiable compliance evidence.**

ReguChain AI is a hackathon MVP that connects local rule-based cyber threat detection with regulatory research, structured incident assessment, evidence traceability, and cryptographic integrity verification.

The goal is to help teams organize incident information, identify potentially relevant reporting obligations, and prepare evidence-backed report drafts for human review.

## 🚀 Key Features

- **Edge Threat Detection:** Apply local rules to simulated security events and flag suspicious patterns such as repeated failed logins, unusual access, and potentially malicious event types.
- **Regulatory Research:** Use TinyFish to search relevant official CERT-In sources and retain source links and supporting context.
- **Incident Assessment:** Organize incident details, identify missing information, and prepare a preliminary reporting assessment.
- **Evidence & Reasoning:** Connect detection signals and incident details with a review checklist, highlighting information that still needs verification.
- **Report Generation:** Generate structured incident report drafts for review.
- **SHA-256 Integrity Checks:** Calculate file hashes and check whether evidence bytes match a previously recorded digest.
- **Audit Trail:** Maintain a local record of relevant report and integrity operations.
- **Blockchain Integration — In Progress:** Prepare report hashes for potential Sepolia anchoring. A prepared hash is not proof of a confirmed on-chain transaction.

## 🧭 How It Works

1. Enter a **synthetic security event** in the dashboard.
2. Run local rule-based detection to identify suspicious signals.
3. Create an incident draft from the detection result.
4. Research relevant regulatory sources and assess the incident.
5. Review the evidence record, missing information, and outstanding checks.
6. Generate a report draft for human review.
7. Verify report or evidence integrity using SHA-256.
8. Explore the blockchain anchoring workflow; treat anchoring as complete only after a transaction is confirmed and independently verified.

## 🏗️ Technology Stack

- **Language:** Python
- **Dashboard:** Streamlit
- **Regulatory research:** TinyFish
- **Integrity verification:** SHA-256
- **Blockchain target:** Ethereum Sepolia testnet
- **Configuration:** Environment variables via `.env`

## 📁 Project Structure

```text
reguchain-ai-starter/
├── app/
│   ├── edge_detector.py
│   ├── evidence_engine.py
│   ├── regulatory_research.py
│   ├── regulation_extractor.py
│   ├── incident_assessment.py
│   ├── report_generator.py
│   ├── integrity.py
│   ├── audit_log.py
│   ├── verify_audit.py
│   ├── blockchain_anchor.py
│   └── contract_abi.json
├── docs/
├── dashboard.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

*Generated reports, local secrets, and virtual-environment files are intentionally excluded from version control.*

## ⚙️ Getting Started

### Requirements

- Python 3.10 or later
- Git
- A TinyFish API key for regulatory research features

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_DIRECTORY>
```

Replace the placeholders with your actual GitHub repository URL and folder name.

### 2. Create and activate a virtual environment

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

```bash
cp .env.example .env
```

Open `.env` and add your own TinyFish API key using the variable name expected by the application. Add blockchain configuration only if needed for your local setup.

**Never commit `.env`, API keys, wallet private keys, or other credentials.**

### 5. Launch the dashboard

```bash
python -m streamlit run dashboard.py
```

Open the local URL printed by Streamlit, typically `http://localhost:8501`.

## 🧪 Demo Scenario

Use synthetic data, for example:

- Event type: `unauthorized_access`
- Failed login attempts: `7`
- Unusual access pattern: `true`
- Affected system: `billing-test-01`
- Impact: Under investigation

The rule-based detector should flag the combination of suspicious signals. Continue through the incident assessment and evidence-review workflow to inspect the generated draft and outstanding review checks.

Results depend on the configured rules and the input event. This demonstration does not represent continuous monitoring of a live network.

## 🔗 Blockchain and Evidence Integrity

SHA-256 provides a digest that can be used to check whether file contents match a previously recorded hash. It does not establish that the original evidence is truthful or that its collection was legally valid.

The project includes a blockchain anchoring preparation workflow targeting Sepolia. Do not describe a report as anchored until the transaction has been submitted, confirmed, and verified on-chain.

Only non-sensitive hashes should be considered for public-chain storage. Do not publish incident details, personal data, credentials, or confidential evidence on a public blockchain.

## ⚖️ Security, Legal, and MVP Limitations

- Detection currently uses local rules and supplied event data; it is not a production intrusion detection system.
- Regulatory assessments are preliminary and require human verification of the applicable law, incident category, facts, and deadlines.
- CERT-In requirements may depend on the incident category and the applicability of the relevant directions. Do not treat a demo deadline as a universal legal conclusion.
- The application prepares report drafts; it does not automatically submit regulatory reports.
- Regulatory source content must be reviewed in context and is not legal advice.
- The local audit log is not inherently tamper-proof.
- Blockchain transaction completion must be demonstrated separately from hash preparation.
- Use synthetic data for public demonstrations and testing.

## 🛣️ Future Improvements

- Complete and verify on-chain hash anchoring.
- Add automated tests for the complete incident-to-report workflow.
- Improve evidence provenance and report versioning.
- Add persistent evidence records and clearer audit verification.
- Expand regulatory coverage with versioned, human-reviewed obligation mappings.
- Add stronger authentication, access controls, and deployment security.

## 📌 Project Status

**Hackathon MVP — under active development.**

ReguChain AI demonstrates an approach to connecting cyber incident signals, regulatory research, human-reviewed compliance assessments, and evidence integrity checks in one workflow. Production readiness and complete on-chain verification are not claimed.


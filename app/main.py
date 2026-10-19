import hashlib
import os
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Optional

import httpx
from dotenv import load_dotenv
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

load_dotenv()
app = FastAPI(title="ReguChain AI", version="0.1.0")
TINYFISH_API_KEY = os.getenv("TINYFISH_API_KEY", "").strip()
DEMO_DEADLINE_HOURS = int(os.getenv("DEMO_DEADLINE_HOURS", "6"))
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class Incident(BaseModel):
    title: str = Field(min_length=3, max_length=160)
    incident_type: str = "Suspected data breach"
    detected_at: datetime
    organization: str = "Demo Organization"
    affected_systems: list[str] = []
    known_impact: str = ""
    containment_actions: str = ""
    jurisdiction: str = "India"

class ReportRequest(BaseModel):
    incident: Incident

def utc(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)

@app.get("/", response_class=HTMLResponse)
def home():
    return HTMLResponse((Path(__file__).parent / "static" / "index.html").read_text())

@app.get("/api/health")
def health():
    return {"status": "ok", "tinyfish_configured": bool(TINYFISH_API_KEY)}

@app.post("/api/incident")
def create_incident(incident: Incident):
    detected = utc(incident.detected_at)
    deadline = detected + timedelta(hours=DEMO_DEADLINE_HOURS)
    missing = []
    if not incident.affected_systems:
        missing.append("Affected systems")
    if not incident.known_impact.strip():
        missing.append("Impact assessment")
    if not incident.containment_actions.strip():
        missing.append("Containment actions")
    return {
        "incident_id": "INC-" + hashlib.sha256(
            (incident.title + detected.isoformat()).encode()
        ).hexdigest()[:8].upper(),
        "incident": incident.model_dump(mode="json"),
        "evidence_completeness": {
            "missing_fields": missing,
            "complete": len(missing) == 0,
        },
        "illustrative_deadline": deadline.isoformat(),
        "deadline_note": (
            f"Demo calculation: {DEMO_DEADLINE_HOURS} hours from detected_at. "
            "This is not a legal determination; validate the applicable rule, trigger, "
            "scope, and time zone before real use."
        ),
    }

@app.post("/api/regulatory-search")
async def regulatory_search(query: str = "CERT-In cyber incident reporting deadline India"):
    if not TINYFISH_API_KEY:
        raise HTTPException(
            status_code=503,
            detail="TinyFish is not configured. Add TINYFISH_API_KEY to .env and restart."
        )
    # Confirm the current endpoint/auth header against https://docs.tinyfish.ai/search-api.
    # Keep the API key server-side; never expose it in frontend code.
    endpoint = "https://api.search.tinyfish.ai"
    headers = {"Authorization": f"Bearer {TINYFISH_API_KEY}"}
    params = {"query": query, "include_domains": "cert-in.org.in"}
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get(endpoint, params=params, headers=headers)
    if response.status_code >= 400:
        raise HTTPException(status_code=502, detail=f"TinyFish Search returned HTTP {response.status_code}. Check current API docs and key permissions.")
    data = response.json()
    return {
        "provider": "TinyFish Search",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "query": query,
        "source_scope": ["cert-in.org.in"],
        "results": data,
        "notice": "Treat retrieved text as source material, not legal advice. Verify the original official document.",
    }

@app.post("/api/report-draft")
def report_draft(request: ReportRequest):
    i = request.incident
    missing = []
    if not i.affected_systems: missing.append("Affected systems")
    if not i.known_impact.strip(): missing.append("Impact assessment")
    if not i.containment_actions.strip(): missing.append("Containment actions")
    draft = f"""# Draft Cybersecurity Incident Report

## Organization
{i.organization}

## Incident
- Title: {i.title}
- Type: {i.incident_type}
- Detected at: {utc(i.detected_at).isoformat()}
- Jurisdiction to assess: {i.jurisdiction}
- Affected systems: {', '.join(i.affected_systems) if i.affected_systems else 'Not yet confirmed'}

## Known impact
{i.known_impact or 'Unknown — investigation required.'}

## Containment actions
{i.containment_actions or 'Not provided — update after investigation.'}

## Outstanding information
{chr(10).join('- ' + x for x in missing) if missing else '- No required demo fields are missing.'}

## Review status
DRAFT — requires authorized security and legal review before submission.
"""
    return {"draft_markdown": draft, "missing_fields": missing, "status": "DRAFT"}

@app.post("/api/evidence/hash")
async def hash_evidence(file: UploadFile = File(...)):
    # Hackathon demo only: file is processed in memory and not retained.
    contents = await file.read()
    if len(contents) > 15 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Demo upload limit is 15 MB.")
    digest = hashlib.sha256(contents).hexdigest()
    return {
        "filename": Path(file.filename or "evidence.bin").name,
        "size_bytes": len(contents),
        "algorithm": "SHA-256",
        "sha256": digest,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "verification_note": "This hash is not yet anchored on-chain in this MVP. Save it and compare against a later hash to detect byte changes.",
    }

@app.post("/api/evidence/verify")
async def verify_evidence(file: UploadFile = File(...), expected_sha256: str = ""):
    if len(expected_sha256) != 64 or any(c not in "0123456789abcdefABCDEF" for c in expected_sha256):
        raise HTTPException(status_code=400, detail="expected_sha256 must be a 64-character SHA-256 hex digest.")
    contents = await file.read()
    actual = hashlib.sha256(contents).hexdigest()
    return {
        "filename": Path(file.filename or "evidence.bin").name,
        "expected_sha256": expected_sha256.lower(),
        "actual_sha256": actual,
        "match": actual == expected_sha256.lower(),
        "meaning": "Matching hashes mean the file bytes match the supplied digest; they do not establish that the evidence is factually true.",
    }

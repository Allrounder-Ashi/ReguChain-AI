# Build roadmap

## Milestone 1 — MVP (included)
- [x] FastAPI backend and browser UI
- [x] TinyFish Search connector (confirm current endpoint/auth format against official docs)
- [x] Incident completeness checks
- [x] Draft report generation
- [x] SHA-256 evidence hash and verification
- [x] Demo deadline calculation clearly labelled as illustrative

## Milestone 2 — Blockchain
- [ ] Add Solidity `EvidenceRegistry` contract storing incident reference + SHA-256 digest + timestamp + actor address.
- [ ] Add role-gated `recordEvidence` and report-approval events.
- [ ] Deploy to Sepolia testnet and store contract address in environment config.
- [ ] Add transaction hash and block explorer link to UI.
- [ ] Keep personal data and report contents off-chain.

## Milestone 3 — Harden
- [ ] Store versioned, reviewed regulatory rules with official source, effective date, scope, trigger, deadline, and jurisdiction.
- [ ] Add authentication, role-based authorization, audit logs, and encrypted object storage.
- [ ] Add tests for deadline logic, malformed uploads, and hash mismatch.
- [ ] Generate PDF report and attach citations/source URLs.
- [ ] Add deployment instructions and a short demo video.

## Milestone 4 — Submission
- [ ] Public GitHub repo with meaningful commits.
- [ ] README includes architecture, TinyFish use case, setup, limitations, and screenshots.
- [ ] Social post explains the problem, solution, and working demo.
- [ ] Revenue model includes target segment, pricing assumptions, and competitor research.

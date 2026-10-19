# Architecture

```text
Browser UI
  |-- incident intake ------> FastAPI /api/incident
  |-- regulatory research --> FastAPI /api/regulatory-search --> TinyFish Search
  |-- report draft ---------> FastAPI /api/report-draft
  |-- evidence hash --------> FastAPI /api/evidence/hash
  |-- hash verification ----> FastAPI /api/evidence/verify

Next milestone:
FastAPI --> Solidity EvidenceRegistry (Sepolia)
  stores only incident reference, digest, actor, timestamp and events
```

Trust boundaries:
- Treat webpage text as untrusted and potentially stale.
- Preserve URL and retrieval timestamp.
- Deadline calculation must come from a reviewed, versioned rule—not an LLM guess.
- A hash detects changes relative to a known digest; it does not establish truth.
- Keep confidential incident evidence off public chains.

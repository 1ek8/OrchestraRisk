# OrchestraRisk 🚀
### Autonomous Enterprise Compliance & Contract Audit Engine

OrchestraRisk is an intelligent multi-agent orchestration platform built for the **Agents League Hackathon (June 4-14, 2026)**. It targets the **Reasoning Agents** and **Enterprise Agents** tracks by demonstrating how autonomous AI nodes can bridge the gap between structured enterprise telemetry, unstructured corporate legal contracts, and internal organizational matrix graphs.

Rather than relying on basic prompt wrappers, OrchestraRisk implements a strict multi-step reasoning circuit enforced by static schema contracts and resilient self-healing data layers, running on open-weights model infrastructure via **Microsoft AI Foundry**.

---

## 📐 System Architecture & Microsoft IQ Alignment

OrchestraRisk is architected around the cooperative intersection of the three **Microsoft IQ Layer** dimensions:

[Fabric IQ Telemetry Monitor] ──(Flag Incident)──> [Foundry IQ Legal Reasoning Engine]
│
(Compute Penalty Schema)
│
▼
[Teams Notification Message] <──(Dispatch Alert)── [Work IQ Graph Hierarchy Matrix]

1. . **Fabric IQ Layer (Structured Data Monitor):** Simulates continuous data lake ingestion from Microsoft Fabric OneLake. The `FabricIQAgent` automatically queries active logistics transaction logs, filters out normal operations, and isolates high-friction anomalies (e.g., severe item delays or price variations).
2. **Foundry IQ Layer (Unstructured Reasoning Ground):** Powered by **DeepSeek-V4-Flash** running through the Microsoft AI Foundry Model Inference Gateway. The `FoundryIQAgent` runs deep instruction-following loops over unstructured multi-vendor Master Service Agreements (SLAs) to extract penalties and cross-examine incidents against legal boundaries.
3. **Work IQ Layer (Organizational Context Router):** Interrogates an enterprise directory matrix schema (simulating Microsoft Graph / Entra ID relationship schemas). The `WorkIQAgent` determines the precise account manager responsible for the culprit vendor and creates a curated escalation contract payload.

---

## 🛡️ Production-Grade Reliability & Safety Features

To fulfill the strict **Reliability & Safety (20%)** requirement of the judging rubric, OrchestraRisk moves away from fragile generation assumptions and applies rigorous defensive systems engineering patterns:

* **Strict Schema Enforcement:** System inputs and handoffs are locked inside strict **Pydantic Model Contracts (`LegalAuditVerdict`)**, ensuring that upstream data layers never encounter unparsed string blocks.
* **Deterministic Slicing Utility:** Uses an absolute bracket boundary parsing pattern (`_extract_pure_json_block`) to isolate JSON tokens, slicing away loose conversational preambles or chat headers occasionally returned by open-weights models.
* **Resilience Backoff Loops:** Handles transaction traffic constraints with native exponential backoff and randomized micro-delay jitter, cleanly handling transient HTTP 429 throttling errors.
* **Autonomous Self-Healing Fallbacks:** If an LLM completion drops tokens or errors during intense platform traffic spikes, a fallback interceptor constructs a structurally sound fallback mitigation payload, logging the raw text buffer and keeping the downstream production API completely online.

---

## 🛠️ Local Installation & Verification Guide

### 1. Prerequisites & Environment Setup
Ensure you have Python 3.10+ installed. Clone the repository and initialize the project dependencies:
```bash
# Install dependencies using the rapid 'uv' or 'pip' ecosystem toolset
pip install -p requirements.txt
```

Configure your local secret vault .env file at the root of your directory:

```bash
AZURE_INFERENCE_ENDPOINT="https://your-foundry-hub.services.ai.azure.com/openai/v1"
AZURE_INFERENCE_API_KEY="your-microsoft-foundry-api-key"
AZURE_INFERENCE_DEPLOYMENT_NAME="DeepSeek-V4-Flash"
```


### 2. Running the Terminal Pipeline

To execute a local stream through the terminal console tracing utility, run:

```bash
python src/main.py
```

### 3. Launching the API Control Gateway

To deploy the FastAPI microservice infrastructure layer, run:

```bash
uvicorn src.server:app --host 127.0.0.1 --port 8000 --reload
```

Trigger a live operational trace via a concurrent network payload:

```bash
curl -X POST [http://127.0.0.1:8000/api/audit/run](http://127.0.0.1:8000/api/audit/run) -H "Content-Type: application/json"
```

### 📊 Core Data Contracts Example (200 OK Response Payload)

```json
{
  "status": "SUCCESS",
  "total_anomalies_processed": 1,
  "execution_traces": [
    {
      "transaction_id": "TXN-90821",
      "vendor_name": "ApexLogistics Global",
      "is_breach_detected": true,
      "applicable_clause": "Corporate Section: ApexLogistics Global",
      "penalty_usd": 105000.0,
      "severity": "HIGH",
      "assigned_owner": "david.miller@enterprise.com",
      "summary": "The anomaly involves ApexLogistics Global delivering semiconductor components 14 days late, exceeding the 7 business day threshold in their specific SLA clause..."
    }
  ]
}
```
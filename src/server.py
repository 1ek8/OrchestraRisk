# File location: src/server.py
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

# --- BULLETPROOF PATH RESOLUTION ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.agents.fabric_agent import FabricIQAgent
from src.agents.foundry_agent import FoundryIQAgent
from src.agents.work_agent import WorkIQAgent

app = FastAPI(
    title="OrchestraRisk Governance API Gateway",
    description="Unified intelligence router simulating Microsoft Fabric, Foundry, and Work IQ layers.",
    version="1.0.0"
)

# Enable CORS cross-origin allowances so local web dashboards can read logs cleanly
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- RESPONSE SCHEMA STRINGS FOR REAL-TIME STREAM VISUALIZATION ---
class AuditTraceIncidentLog(BaseModel):
    transaction_id: str
    vendor_name: str
    is_breach_detected: bool
    applicable_clause: str
    penalty_usd: float
    severity: str
    assigned_owner: str
    summary: str

class SystemAuditPayloadResponse(BaseModel):
    status: str
    total_anomalies_processed: int
    execution_traces: List[AuditTraceIncidentLog]

@app.get("/api/health")
def health_check():
    return {"status": "ONLINE", "gateway": "Microsoft AI Foundry Node Active"}

@app.post("/api/audit/run", response_model=SystemAuditPayloadResponse)
def execute_compliance_audit_pipeline():
    """
    Triggers the end-to-end multi-agent corporate risk evaluation circuit.
    Fabric IQ (Ingestion) -> Foundry IQ (Reasoning) -> Work IQ (Escalation Mapping).
    """
    try:
        fabric_node = FabricIQAgent()
        foundry_node = FoundryIQAgent()
        work_node = WorkIQAgent()
        
        # 1. Read telemetry data profiles from the mock OneLake layer
        disruptions = fabric_node.scan_active_anomalies()
        if not disruptions:
            return SystemAuditPayloadResponse(
                status="SUCCESS",
                total_anomalies_processed=0,
                execution_traces=[]
            )
            
        # 2. Extract unstructured rules registry
        with open("mock_data/vendor_sla_rules.md", "r") as f:
            master_contract_registry = f.read()
            
        traces: List[AuditTraceIncidentLog] = []
        
        # 3. Stream incidents sequentially through the model infrastructure
        for incident in disruptions:
            verdict = foundry_node.audit_contract_with_llm(incident, master_contract_registry)
            target_human_owner = work_node.resolve_incident_owner(incident["vendor_name"])
            
            traces.append(AuditTraceIncidentLog(
                transaction_id=incident["transaction_id"],
                vendor_name=incident["vendor_name"],
                is_breach_detected=verdict.is_breach_detected,
                applicable_clause=verdict.applicable_clause_reference,
                penalty_usd=verdict.total_penalty_usd,
                severity=verdict.risk_severity,
                assigned_owner=target_human_owner,
                summary=verdict.reasoning_summary
            ))
            
        return SystemAuditPayloadResponse(
            status="SUCCESS",
            total_anomalies_processed=len(traces),
            execution_traces=traces
        )
        
    except Exception as server_error:
        raise HTTPException(status_code=500, detail=f"Internal Agent Pipeline Error: {str(server_error)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.server.app", host="127.0.0.1", port=8000, reload=True)
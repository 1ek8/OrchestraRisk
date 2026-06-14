import json
from pydantic import BaseModel, Field
from typing import List, Optional

# --- SCHEMA CONTRACTS FOR MULTI-STEP REASONING ---
class ComplianceEscalationPackage(BaseModel):
    transaction_id: str
    vendor: str
    delay_days: int
    calculated_penalty: float
    assigned_manager_email: str
    escalation_payload: str

# --- MOCK AGENT IMPLEMENTATIONS ---
class FabricIQAgent:
    """Scans structured OneLake transaction data for high-risk anomalies."""
    def analyze_telemetry(self) -> Optional[dict]:
        print("[Fabric IQ Agent] Scanning OneLake data assets...")
        with open("mock_data/one_lake_inventory.json", "r") as f:
            data = json.load(f)
        # Triage condition: flag delays > 7 days
        anomalies = [t for t in data if t["days_delayed"] > 7]
        return anomalies[0] if anomalies else None

class FoundryIQAgent:
    """Executes RAG reasoning over unstructured SLA rules to ground legal penalty calculations."""
    def audit_contract(self, anomaly: dict) -> float:
        print(f"[Foundry IQ Agent] Running RAG Audit on contract for: {anomaly['vendor_name']}...")
        with open("mock_data/vendor_sla_rules.md", "r") as f:
            contract_text = f.read()
        
        # Simple programmatic extraction representing model parsing logic
        if "ApexLogistics" in anomaly["vendor_name"] and "hardware components" in contract_text:
            excess_days = anomaly["days_delayed"] - 7
            penalty = excess_days * 15000 # $15k per day rule
            return penalty
        return 0.0

class WorkIQAgent:
    """Queries corporate directory/Graph schemas to route notifications to the correct human owner."""
    def resolve_hierarchy(self, vendor_name: str) -> str:
        print(f"[Work IQ Agent] Interrogating Microsoft Graph schema for vendor: {vendor_name}...")
        with open("mock_data/company_org_graph.json", "r") as f:
            org = json.load(f)
        
        for manager in org["departments"]["SupplyChain"]["account_managers"]:
            if vendor_name in manager["assigned_vendors"]:
                return manager["teams_id"]
        return "ops-alert@enterprise.com"

# --- CORE ORCHESTRATION PIPELINE ---
def run_orchestra_risk_pipeline():
    print("=== Starting OrchestraRisk Autonomous Compliance Execution ===")
    
    fabric = FabricIQAgent()
    foundry = FoundryIQAgent()
    work = WorkIQAgent()
    
    # Step 1: Detect Anomaly (Fabric IQ)
    anomaly = fabric.analyze_telemetry()
    if not anomaly:
        print("No compliance risk profiles found.")
        return
        
    # Step 2: Compute Legal/Financial Liability (Foundry IQ)
    penalty_fee = foundry.audit_contract(anomaly)
    
    # Step 3: Discover Operational Owner (Work IQ)
    target_owner = work.resolve_hierarchy(anomaly["vendor_name"])
    
    # Step 4: Construct the Production Escalation Package
    final_output = ComplianceEscalationPackage(
        transaction_id=anomaly["transaction_id"],
        vendor=anomaly["vendor_name"],
        delay_days=anomaly["days_delayed"],
        calculated_penalty=penalty_fee,
        assigned_manager_email=target_owner,
        escalation_payload=f"ALERT: {anomaly['vendor_name']} is in breach of contract contract timelines by {anomaly['days_delayed']} days. Total estimated financial penalty: ${penalty_fee:,} USD. Action required."
    )
    
    print("\n=== SYSTEM EXECUTION VERIFICATION SUCCESSFUL ===")
    print(final_output.model_dump_json(indent=2))

if __name__ == "__main__":
    run_orchestra_risk_pipeline()
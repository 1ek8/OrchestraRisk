# File location: src/main.py
import os
import sys

# --- PATH RESOLUTION ALIGNMENT FOR PYLANCE ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.agents.fabric_agent import FabricIQAgent
from src.agents.foundry_agent import FoundryIQAgent
from src.agents.work_agent import WorkIQAgent

def run_orchestra_risk_enterprise_pipeline():
    print("=== 🚀 Initializing OrchestraRisk Autonomous Compliance Lifecycle ===")
    
    # Instantiate active infrastructure agent nodes
    fabric_node = FabricIQAgent()
    foundry_node = FoundryIQAgent()
    work_node = WorkIQAgent()
    
    # Step 1: Ingest active operational discrepancies from Fabric OneLake
    disruptions = fabric_node.scan_active_anomalies()
    if not disruptions:
        print("🎉 Clean State: Zero active logistics supply chain risks detected.")
        return
        
    # Step 2: Load the master unstructured compliance knowledge text asset
    with open("mock_data/vendor_sla_rules.md", "r") as f:
        master_contract_registry = f.read()
        
    # Step 3: Stream anomalies through the automated reasoning and escalation loop
    for idx, incident in enumerate(disruptions, start=1):
        print(f"\n--- Processing Incident Asset Context [{idx}/{len(disruptions)}] ---")
        print(f"🔹 Transaction: {incident['transaction_id']} | Vendor: {incident['vendor_name']} | Delay: {incident['days_delayed']} Days")
        
        try:
            # Execute Foundry IQ LLM Legal Audit over the contract document
            verdict = foundry_node.audit_contract_with_llm(incident, master_contract_registry)
            
            # Execute Work IQ directory mapping to resolve accountability
            target_human_owner = work_node.resolve_incident_owner(incident["vendor_name"])
            
            # Render final systemic telemetry output trace block
            print(f"\n🏆 [Verification Success] Incident ID: {incident['transaction_id']}")
            print(f"   ↳ Breach State Confirmed? : {verdict.is_breach_detected}")
            print(f"   ↳ Contract Section Cited  : {verdict.applicable_clause_reference}")
            print(f"   ↳ Financial Penalty Fee   : ${verdict.total_penalty_usd:,.2f} USD")
            print(f"   ↳ Risk Severity Vector    : {verdict.risk_severity}")
            print(f"   ↳ Dispatch Communication  : {target_human_owner}")
            print(f"   ↳ Rationale Summary       : {verdict.reasoning_summary}")
            
        except Exception as pipeline_error:
            print(f"❌ [Pipeline Node Error Handler Triggered] Incident {incident['transaction_id']} skipped: {str(pipeline_error)}")

    print("\n=== All Active Supply Chain Anomalies Successfully Evaluated ===")

if __name__ == "__main__":
    run_orchestra_risk_enterprise_pipeline()
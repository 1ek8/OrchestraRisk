# File location: src/agents/work_agent.py
import json
import os

class WorkIQAgent:
    """Interrogates corporate directory schemas to resolve escalation routing pathways."""
    
    def __init__(self, graph_path: str = "mock_data/company_org_graph.json"):
        self.graph_path = graph_path

    def resolve_incident_owner(self, vendor_name: str) -> str:
        print(f"[Work IQ Agent] Interrogating Microsoft Graph schema for Vendor: '{vendor_name}'...")
        if not os.path.exists(self.graph_path):
            return "ops-alert@enterprise.com"
            
        with open(self.graph_path, "r") as f:
            org_data = json.load(f)
            
        # Walk the corporate organizational hierarchy tree
        managers = org_data.get("departments", {}).get("SupplyChain", {}).get("account_managers", [])
        for manager in managers:
            if vendor_name in manager.get("assigned_vendors", []):
                target_email = manager.get("teams_id", "ops-alert@enterprise.com")
                print(f"   -> Structural match discovered. Routing responsibility assigned to: {target_email}")
                return target_email
                
        return "ops-alert@enterprise.com"
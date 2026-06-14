# File location: src/agents/fabric_agent.py
import json
import os

class FabricIQAgent:
    """Monitors structured business rows inside Fabric OneLake tables to triage active anomalies."""
    
    def __init__(self, storage_path: str = "mock_data/one_lake_inventory.json"):
        self.storage_path = storage_path

    def scan_active_anomalies(self) -> list[dict]:
        print("[Fabric IQ Agent] Querying active OneLake inventory ledger tracking tables...")
        if not os.path.exists(self.storage_path):
            print(f"⚠️ Telemetry file source missing at: {self.storage_path}")
            return []
            
        with open(self.storage_path, "r") as f:
            transactions = json.load(f)
            
        # Business Triage Filter: Flag any transaction with recorded delays greater than 0 days
        anomalies = [txn for txn in transactions if txn.get("days_delayed", 0) > 0]
        print(f"   -> Scan complete. Isolated {len(anomalies)} active disruption footprints.")
        return anomalies
# File location: src/agents/foundry_agent.py
import os
import sys
import time
import random

# --- BULLETPROOF PATH RESOLUTION FOR PYLANCE ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(CURRENT_DIR))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import openai
from openai import OpenAI
from src.utils.schemas import LegalAuditVerdict
from dotenv import load_dotenv

load_dotenv()

class FoundryIQAgent:
    """Uses advanced reasoning via Microsoft Foundry with built-in backoff and self-healing schema recovery."""
    
    def __init__(self):
        base_url = os.getenv("AZURE_INFERENCE_ENDPOINT")
        api_key = os.getenv("AZURE_INFERENCE_API_KEY")
        
        deployment_name = os.getenv("AZURE_INFERENCE_DEPLOYMENT_NAME")
        self.model_name: str = deployment_name if deployment_name is not None else "DeepSeek-V4-Flash"

        # Initialize standard OpenAI wrapper targeting the global proxy highway
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

    def _extract_pure_json_block(self, text: str) -> str:
        """Slices away conversational preambles or notes leaked by open-weights models."""
        start_idx = text.find("{")
        end_idx = text.rfind("}")
        
        if start_idx == -1 or end_idx == -1 or end_idx < start_idx:
            return text
            
        return text[start_idx:end_idx + 1].strip()

    def audit_contract_with_llm(self, anomaly_data: dict, contract_text: str, max_retries: int = 5) -> LegalAuditVerdict:
        print(f"[Foundry IQ Engine] Running legal audit using deployment: {self.model_name}...")
        
        system_prompt = (
            "You are an elite corporate legal auditor and compliance systems engineer.\n"
            "Your task is to analyze an operational anomaly against a provided Master Service Agreement (SLA).\n"
            "You must return your output EXCLUSIVELY as a valid JSON object matching this exact keys template:\n"
            "{\n"
            '  "is_breach_detected": true or false,\n'
            '  "applicable_clause_reference": "string",\n'
            '  "mathematical_penalty_calculation": "string",\n'
            '  "total_penalty_usd": 0.0,\n'
            '  "risk_severity": "LOW" or "MEDIUM" or "HIGH" or "CRITICAL",\n'
            '  "reasoning_summary": "string"\n'
            "}\n"
            "CRITICAL: Do not include any introductory text, conversational preambles, or analysis descriptions.\n"
            "Start your response immediately with the opening brace '{' and end with the closing brace '}'."
        )
        
        user_prompt = f"""
        ANOMALY METRICS REPORT:
        {anomaly_data}

        MASTER SERVICE AGREEMENT (SLA) DOCUMENT CONTENT:
        {contract_text}
        """

        raw_message_content = None

        # --- RESILIENCE ENGINE: EXPONENTIAL BACKOFF WITH JITTER ---
        for attempt in range(max_retries):
            try:
                completion = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.0
                )
                raw_message_content = completion.choices[0].message.content
                break
                
            except openai.RateLimitError as e:
                if attempt == max_retries - 1:
                    print("⚠️ [Resilience Exhausted] Rate limit retries peaked out.")
                    raise e
                
                sleep_time = (2 ** attempt) + random.uniform(0, 1.0)
                print(f"🔄 [Rate Limit Encountered (429)] Backoff Engaged. Pausing for {sleep_time:.2f}s...")
                time.sleep(sleep_time)

        if raw_message_content is None:
            return self._generate_healing_fallback(anomaly_data, "Gateway compilation empty response exception.")
            
        # Clean and structural slice boundaries
        clean_content = self._extract_pure_json_block(raw_message_content)
        if clean_content.startswith("```json"):
            clean_content = clean_content.split("```json")[1].split("```")[0].strip()
        elif clean_content.startswith("```"):
            clean_content = clean_content.split("```")[1].split("```")[0].strip()
            
        # --- SELF-HEALING STRUCTURAL RECOVERY LAYER ---
        try:
            return LegalAuditVerdict.model_validate_json(clean_content)
        except Exception as parse_error:
            print(f"⚠️ [Self-Healing Pipeline Triggered] Failed to structure JSON schema tokens: {str(parse_error)}")
            return self._generate_healing_fallback(anomaly_data, clean_content)

    def _generate_healing_fallback(self, anomaly_data: dict, unparsed_buffer: str) -> LegalAuditVerdict:
        """Generates a type-safe fallback validation model to keep the API server online."""
        print("   ↳ Constructing production-grade fallback mitigation artifact tracking payload...")
        return LegalAuditVerdict(
            is_breach_detected=True,
            applicable_clause_reference="System Level Dynamic Recovery Fallback Node",
            mathematical_penalty_calculation="Manual verification required. Computation engine fallback recovery active.",
            total_penalty_usd=float(anomaly_data.get("financial_impact_usd", 0.0) * 0.1), # Baseline 10% estimation rule
            risk_severity="HIGH",
            reasoning_summary=f"Automated recovery event. JSON model output unparsed buffer fallback context logs capture: {unparsed_buffer[:200]}"
        )
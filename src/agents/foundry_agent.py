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
    """Uses advanced open-weights reasoning via Microsoft Foundry with built-in resilience protocols."""
    
    def __init__(self):
        base_url = os.getenv("AZURE_INFERENCE_ENDPOINT")
        api_key = os.getenv("AZURE_INFERENCE_API_KEY")
        
        deployment_name = os.getenv("AZURE_INFERENCE_DEPLOYMENT_NAME")
        self.model_name: str = deployment_name if deployment_name is not None else "Phi-4-mini-instruct"

        # Initialize standard OpenAI wrapper targeting the Foundry proxy highway
        self.client = OpenAI(
            base_url=base_url,
            api_key=api_key
        )

    def _extract_pure_json_block(self, text: str) -> str:
        """
        Defensive Engineering Utility:
        Slices away conversational preambles or notes leaked by open-weights models.
        """
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

        # --- PRODUCTION RESILIENCE ENGINE: EXPONENTIAL BACKOFF WITH JITTER ---
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
                break  # Break out of loop immediately if network completion succeeds!
                
            except openai.RateLimitError as e:
                if attempt == max_retries - 1:
                    print(f"⚠️ [Resilience Layer Exhausted] Maximum retries reached. Exiting pipeline.")
                    raise e
                
                # Calculate exponential backoff interval boundary: 2^attempt (e.g., 2s, 4s, 8s, 16s) 
                # Inject randomized jitter between 0 and 1 seconds to prevent gateway collision spikes
                sleep_time = (2 ** attempt) + random.uniform(0, 1.0)
                print(f"🔄 [Rate Limit Encountered (429)] Gateway busy. Active Resilience Backoff engaged...")
                print(f"   -> Retrying task block in {sleep_time:.2f} seconds (Attempt {attempt + 1}/{max_retries})...")
                time.sleep(sleep_time)

        if raw_message_content is None:
            raise ValueError("Critical Error: The AI engine returned an empty completion body.")
            
        # Isolate and structural-slice the JSON boundary content strings
        clean_content = self._extract_pure_json_block(raw_message_content)
        
        if clean_content.startswith("```json"):
            clean_content = clean_content.split("```json")[1].split("```")[0].strip()
        elif clean_content.startswith("```"):
            clean_content = clean_content.split("```")[1].split("```")[0].strip()
            
        try:
            return LegalAuditVerdict.model_validate_json(clean_content)
        except Exception as parse_error:
            print(f"❌ [Parsing Diagnostic Alert] Failed to validate string. Content was:\n{raw_message_content}")
            raise parse_error
# File location: src/utils/schemas.py
from pydantic import BaseModel, Field

class LegalAuditVerdict(BaseModel):
    is_breach_detected: bool = Field(description="True if the supply chain incident violates the vendor SLA contract rules.")
    applicable_clause_reference: str = Field(description="The specific section title or clause number cited from the contract.")
    mathematical_penalty_calculation: str = Field(description="The step-by-step mathematical logic used to compute the fine.")
    total_penalty_usd: float = Field(description="The final calculated penalty fee in USD. Set to 0.0 if no breach occurred.")
    risk_severity: str = Field(description="Must be exactly one of: LOW, MEDIUM, HIGH, CRITICAL.")
    reasoning_summary: str = Field(description="A concise executive synthesis explaining the legal rationale behind this verdict.")
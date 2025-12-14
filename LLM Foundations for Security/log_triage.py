from langchain_openai import ChatOpenAI
from langchain.tools import tool
from pydantic import BaseModel, Field

class LogTriage(BaseModel):
    timestamp: str = Field(..., description="Timestamp of the log event")
    alert_type: str = Field(..., description="Category of the alert or detection signature")
    indicator: str = Field(..., description="IP, domain, or artifact observed")
    description: str = Field(..., description="Short text summary of the alert")
    classification: str = Field(..., description="Triage result: benign, suspicious, or malicious")
    confidence: float = Field(..., description="Confidence score 0.0–1.0")
    mapped_tactic: str = Field(..., description="MITRE ATT&CK tactic mapping if applicable")


@tool
def triage_log(indicator: str) -> dict:
    malicious_ips = ["185.14.29.99", "45.77.120.12"]
    for ip in malicious_ips:
        if ip in indicator:
            return {
                "classification": "malicious",
                "confidence": 0.95,
                "mapped_tactic": "Command and Control (TA0011)"
            }

    return {
        "classification": "benign",
        "confidence": 0.15,
        "mapped_tactic": "None"
    }

llm = ChatOpenAI(model="gpt-4o-mini")

prompt = f"""
You are a SOC analyst assistant.
Extract and analyze this log line into structured JSON.
If an IP or domain is found, use triage_log to classify it.

Log: "2025-10-20 13:22:45 ALERT [1:2024001:1] ET MALWARE Possible C2 traffic to 185.14.29.99:8080"

Output only JSON matching this schema:
{LogTriage.model_json_schema()}
"""

response = llm.invoke(prompt)
print(response.content)

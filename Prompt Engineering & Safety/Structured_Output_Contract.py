from pydantic import BaseModel, Field
from datetime import datetime
import openai, json
from pydantic import ValidationError

class IncidentTicket(BaseModel):
    incident_id: str = Field(..., description="Unique incident identifier, e.g., inc-23-10-2025")
    category: str = Field(..., description="Type of detected activity or threat")
    severity: str = Field(..., description="Low, Medium, High, Critical")
    source_ip: str = Field(..., description="Source IP related to incident")
    timestamp: datetime = Field(default_factory=datetime.pktnow, description="Incident creation time")
    summary: str = Field(..., description="Short summary of what happened")
    recommendation: str = Field(..., description="Analyst or AI recommended next step")

prompt = """
You are a SOC Analyst. Analyze the following log and generate an incident ticket.

LOG:
"Failed SSH login attempt from 192.168.1.50 user=root port=22"

Return your answer in STRICT JSON matching this schema:
{
  "incident_id": "string",
  "category": "string",
  "severity": "string",
  "source_ip": "string",
  "timestamp": "ISO datetime",
  "summary": "string",
  "recommendation": "string"
}
"""
response = openai.ChatCompletion.create(
    model="gpt-4o-mini",
    messages=[{"role": "user", "content": prompt}]
)

raw_output = response.choices[0].message.content.strip()

try:
    data = json.loads(raw_output)
    ticket = IncidentTicket(**data)  
    print("Incident Ticket Created:")
    print(ticket.json(indent=2))
except json.JSONDecodeError:
    print("Model did not return valid JSON.")
except ValidationError as e:
    print("Output failed validation:", e)
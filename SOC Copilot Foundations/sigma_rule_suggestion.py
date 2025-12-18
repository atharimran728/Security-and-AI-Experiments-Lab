import time
import json
from google import genai
import yaml 

client = genai.Client() 

prompt = """
You are a SOC detection engineer. Generate a Sigma rule in YAML format based on the analyst’s request.

Follow Sigma structure:
- title
- id
- status
- description
- author
- logsource: category, product
- detection: selection, condition
- level
- tags

Request:
"Detect multiple failed logins from the same IP within 30 seconds."
"""


response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=prompt,
    config=genai.types.GenerateContentConfig(
        system_instruction="You are an expert Sigma rule author. Output only the YAML content of the Sigma rule.",
        temperature=0.3
    )
)

rule_text = response.text.strip()

try:
    parsed = yaml.safe_load(rule_text)
    print("[VALID YAML]")
except yaml.YAMLError:
    print("[YAML ERROR]")
    parsed = rule_text

print(rule_text)
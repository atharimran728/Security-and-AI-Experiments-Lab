import time
import json
from google import genai
import yaml 

client = genai.Client() 

##########

analyst = Agent(
    role="Detection Analyst",
    goal="Interpret the analyst’s request and extract detection logic details (what, how, where).",
    backstory=("""
        You are a Tier-3 SOC detection engineer. You read analyst requests in natural language and identify:
        - The behavior being detected
        - Indicators or patterns
        - Relevant log sources or data types
    """)
)

enricher = Agent(
    role="Threat Intelligence & Enrichment Specialist",
    goal="Enhance the detection idea with technical context, mappings, and fields.",
    backstory=("""
        You are a Threat Intel Enrichment Agent. You expand detections with:
        - MITRE ATT&CK mappings
        - Log source and field suggestions
        - Related use cases and false positive considerations
    """)
)

reporter = Agent(
    role="Sigma Rule Reporter",
    goal="Write a complete, valid Sigma rule YAML file.",
    backstory=("You are an expert Sigma rule author. Based on the enriched detection idea, write a complete Sigma rule following Sigma structure. Output only YAML. Be syntactically valid.")
)

################

task_analyst = Task(
    description=(""" Interpret this request and extract detection intent:
        "Detect multiple failed logins from the same IP within 30 seconds."
    """),
    agent=analyst
)

task_enricher = Task(
    description=("Review the analyst’s extracted detection logic. Add technical context: log source, relevant fields, MITRE ATT&CK mappings, and other enrichment."),
    agent=enricher
)

task_reporter = Task(
    description=("""
        Generate a Sigma rule in YAML format based on the enriched detection context. Ensure proper fields:
        - title
        - id
        - description
        - author
        - status
        - logsource
        - detection
        - condition
        - level
        - tags
    """),
    agent=reporter
)



crew = Crew(
    agents=[analyst, enricher, reporter],
    tasks=[task_analyst, task_enricher, task_reporter]
)

result = crew.kickoff()

try:
    parsed = yaml.safe_load(result)
    print("[VALID YAML]\n")
except yaml.YAMLError:
    print("[YAML ERROR – showing raw output]\n")

print(result)

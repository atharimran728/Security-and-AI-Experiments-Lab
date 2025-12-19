import json
from crewai import Agent, Task, Crew

new_alerts = [
    {"alert_type": "Brute Force", "src_ip": "10.0.0.15", "username": "admin", "signature_id": "BF001"},
    {"alert_type": "Brute Force", "src_ip": "10.0.0.15", "username": "root", "signature_id": "BF001"},
    {"alert_type": "Port Scan", "src_ip": "192.168.1.7", "signature_id": "SCAN003"},
    {"alert_type": "Brute Force", "src_ip": "10.0.0.15", "username": "guest", "signature_id": "BF001"},
    {"alert_type": "Port Scan", "src_ip": "192.168.1.7", "signature_id": "SCAN003"}
]

alert_feed = json.dumps(new_alerts)

###########

parser = Agent(
    role="Alert Parser",
    goal="Read raw alert feed and extract useful fields like type, src_ip, user, signature_id.",
    backstory="You parse SIEM or IDS alerts into structured form for further analysis."
)

clusterer = Agent(
    role="Alert Clusterer",
    goal="Group similar alerts together based on fields like src_ip, signature_id, or alert_type.",
    backstory="You detect recurring alerts that likely represent the same incident or noisy repetition."
)

suppressor = Agent(
    role="Suppression Advisor",
    goal="Propose suppression rules for recurring benign alerts (e.g., same IP or signature repeating).",
    backstory=("""You are a detection tuning specialist. Suggest suppressions or tuning recommendations in Sigma-like format or SIEM filter syntax.
        For example: exclude src_ip == 10.0.0.15 if it's known internal scanner.
    """)
)

reporter = Agent(
    role="SOC Reporter",
    goal="Summarize the clusters and suppressions in a clean analyst-friendly report.",
    backstory="You write summaries for SOC engineers to review and apply tuning suggestions."
)

##############

task_parse = Task(
    description=(f"Parse this raw alert feed and extract structured information: {alert_feed}"),
    agent=parser
)

task_cluster = Task(
    description="Group the parsed alerts into logical clusters or repeated patterns.",
    agent=clusterer
)

task_suppress = Task(
    description="Based on the clusters, identify recurring benign or duplicate patterns and propose suppression filters.",
    agent=suppressor
)

task_report = Task(
    description="Create a concise SOC triage summary report including clusters and suppression recommendations.",
    agent=reporter
)


crew = Crew(
    agents=[parser, clusterer, suppressor, reporter],
    tasks=[task_parse, task_cluster, task_suppress, task_report]
)

result = crew.kickoff()

print(result)

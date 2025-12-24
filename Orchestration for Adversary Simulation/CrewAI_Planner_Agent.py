from crewai import Crew, Agent, Task, PlannerConfig

planner = Agent(
    name="Planner",
    role="AgentPlanner",
    system_message="""You are the Planner. You produce a JSON array 'tests' with fields:
    id,tactic,technique_id,technique_name,risk_level,test_description,prerequisites,steps,telemetry,detection_checks,success_criteria
    Return only JSON.
    """
)

task = Task(
    agent=planner,
    prompt="""Scope: windows/linux lab, sensors: EDR, sysmon, snort, dns.
    Goals: test Initial Access (phishing), Credential Access, Lateral Movement, Exfiltration.
    Constraints: non-destructive, no real-data exfiltration.

    Output format: JSON array named 'tests'.
    """
)

plan =PlannerConfig(enabled=True)
crew = Crew(agents=[planner], planning=plan)
result = crew.run(task)

print(result)

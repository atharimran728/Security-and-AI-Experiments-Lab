from crewai import Agent, Task, Crew

analyst = Agent(
    role="SOC Analyst Reasoner",
    goal="Break down a detection or investigation request into reasoning steps, hypotheses, and conclusions.",
    backstory=("You are a Tier-3 SOC analyst trained in adversary behavior analysis. Your task is to reason step-by-step (like an investigator) when exploring suspicious activity. Each reasoning path should represent a hypothesis and your evidence chain.")
)

task_case = Task(
    description=("""Simulate your reasoning process for this analyst request:
        "Investigate unusual outbound PowerShell network traffic."

        Steps:
        1. Decompose the investigation into sub-tasks.
        2. Explore at least two reasoning paths (e.g., exfiltration vs admin script).
        3. For each path, describe reasoning, evidence sought, and confidence level.
        4. Conclude which path is most probable and why.
    """),
    agent=analyst
)
crew = Crew(agents=[analyst], tasks=[task_case])

result = crew.kickoff()

print(result)

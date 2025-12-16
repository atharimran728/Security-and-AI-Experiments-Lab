from crewai import Agent, Task, Crew

analyst = Agent(
    role="SOC Analyst",
    goal="Analyze logs or alerts to find potential security incidents.",
    backstory=(
        "You are a detail-oriented SOC analyst skilled at identifying malicious behavior in system logs. You write concise, evidence-based findings."
    )
)

reporter = Agent(
    role="SOC Reporter",
    goal="Transform analyst findings into a clear, structured SOC incident report.",
    backstory=(
        "You are an articulate security writer who converts technical details into professional reports for SOC management and clients."
    )
)

analysis_task = Task(
    agent=analyst,
    description="Analyze the following log entries and identify any suspicious patterns:\n"
                """
                10.0.0.5 -> 192.168.1.10 : 3389 (RDP)
                10.0.0.5 -> 192.168.1.11 : 3389 (RDP)
                10.0.0.5 -> 192.168.1.12 : 445  (SMB)
                10.0.0.5 -> 192.168.1.13 : 135  (RPC)
                """,
)

report_task = Task(
    agent=reporter,
    description="Summarize the analyst's findings into a formal SOC report including summary, indicators, and recommendations.",
    depends_on=[analysis_task]
)

crew = Crew(
    agents=[analyst, reporter],
    tasks=[analysis_task, report_task],
)

result = crew.run()
print("FINAL REPORT:\n")
print(result)


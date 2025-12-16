from crewai import Agent, Task, Crew

parser =  Agent(
    name="Parser Agent",
    role="Parser",
    goal="To take a raw log file (e.g., JSON, syslog, Zeek, Suricata, Windows Event Logs, etc.) and extract structured data or summaries — i.e., convert raw telemetry → meaningful, machine-readable info for the next agent (analyst/reporter)."
)

analyst = Agent(
    name="SOC Analyst",
    role="Analyst",
    goal="Analyze logs or alerts to find potential security incidents.",
    backstory=(
        "You are a detail-oriented SOC analyst skilled at identifying malicious behavior in system logs. You write concise, evidence-based findings."
    )
)

reporter = Agent(
    name="SOC Reporter",
    role="Reporter",
    goal="Create a clear, concise SOC report summarizing the analyst’s findings.",
    backstory=(
        "You are an articulate security writer who converts technical details into professional reports for SOC management and clients."
    )
)

parser_task = Task(
    agent=parser,
    description="Parse the provided log file and output structured JSON with fields: timestamp, source, destination, event_type, details.",
    inputs={"raw_logs": open("raw.log").read()}
)

analysis_task = Task(
    agent=analyst,
    description="Analyze the extracted deatiles from parser and identify any suspicious patterns\n",
    context=[parser_task]
)

report_task = Task(
    agent=reporter,
    description="Summarize the analyst's findings into a formal SOC report including summary, indicators, and recommendations.",
    depends_on=[analysis_task]
)

crew = Crew(
    agents=[parser, analyst, reporter],
    tasks=[parser_task, analysis_task, report_task]
)

result =crew.run()
print("Result:\n")
print(result)
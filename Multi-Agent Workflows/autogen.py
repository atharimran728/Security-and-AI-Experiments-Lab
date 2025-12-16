from autogen import AssistantAgent, GroupChat, GroupChatManager

analyst = AssistantAgent(
    name="AlertAnalyst",
    system_message=(
        "You are a SOC Analyst. Analyze raw alert data, extract key indicators, severity, and summarize potential attack behavior."
    )
)

summarizer = AssistantAgent(
    name="Summarizer",
    system_message=(
        "You are a senior SOC reporter. Collaborate with the analyst to refine findings into a concise, well-structured incident summary suitable for management."
    )
)

groupchat = GroupChat(agents=[analyst, summarizer], messages=[])

manager = GroupChatManager(groupchat=groupchat)

input_alerts = """
[ALERT] ET POLICY Possible RDP Brute-Force attempt from 10.0.0.5 to 192.168.1.10
[ALERT] ET SCAN SMB Enumeration from 10.0.0.5 to 192.168.1.12
[ALERT] ET POLICY Multiple Failed Login Attempts to 192.168.1.11
"""

result = manager.run("Analyze and summarize the following alerts:\n" + input_alerts)
print("FINAL INCIDENT SUMMARY:\n")
print(result)




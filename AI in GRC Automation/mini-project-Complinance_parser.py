import spacy
from rich.console import Console
from rich.text import Text

console = Console()
nlp = spacy.load("en_core_web_trf")

CONTROL_KEYWORDS = [   
    "control", "restrict", "monitor", "review", "enforce", "implement",
    "audit", "protect", "secure", "establish", "limit", "authorize",
    "validate", "approve", "assess", "detect", "respond", "prevent",
    "patch", "configure", "harden", "encrypt", "backup", "remediate",
    "lock", "block", "disable", "apply", "train", "update"
]


ASSET_KEYWORDS = [
    "system", "account", "data", "information", "network", "application",
    "server", "database", "endpoint", "infrastructure", "device", "asset",
    "credential", "identity", "workstation", "cloud", "storage",
    "resource", "platform", "service", "api", "email", "backup"
]


RISK_KEYWORDS = [
    "unauthorized", "breach", "violation", "failure", "compromise",
    "attack", "exploit", "malware", "phishing", "vulnerability",
    "exposure", "incident", "leak", "loss", "threat", "harm",
    "downtime", "intrusion", "tamper", "damage", "weakness",
    "corruption", "unavailability", "misuse", "abuse"
]


def highlight_control(text):
    doc = nlp(text)
    highlighted = Text()

    console.print(highlighted)

    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in CONTROL_KEYWORDS:
            highlighted.append(token.text_with_ws, style="bold green")
        elif lemma in RISK_KEYWORDS:
            highlighted.append(token.text_with_ws, style="bold red")
        elif lemma in ASSET_KEYWORDS:
            highlighted.append(token.text_with_ws, style="bold blue")
        else:
            highlighted.append(token.text_with_ws, style="dim") 

    console.print(highlighted)


if __name__ == "__main__":
    sample = """
A.12.4.1 Event Logging and Monitoring  
All information systems and applications shall generate, store, and protect logs to record user activities, exceptions, and information security events.  
Logs shall be reviewed periodically to detect unauthorized access, data breaches, or misuse of privileged accounts.  
System administrators must ensure that audit trails are enabled for all network devices and cloud platforms.  

A.9.2.6 Removal or Adjustment of Access Rights  
Access rights of employees and contractors shall be revoked or adjusted immediately upon termination or role change.  
Failure to remove inactive accounts may lead to unauthorized access, data compromise, or policy violations.  
Identity and access management systems shall enforce least-privilege and multi-factor authentication to protect sensitive assets and confidential data.  

A.11.2.9 Clear Desk and Clear Screen Policy  
Employees must ensure that physical and digital assets such as laptops, documents, and removable media are secured when unattended.  
Failure to secure assets can result in data leakage, loss, or theft.  
Regular audits shall be conducted to validate compliance with physical security controls.  

A.17.1.2 Redundancies  
Critical business systems, applications, and databases shall have redundancy measures implemented to minimize downtime and ensure availability.  
Regular backup and recovery tests shall be performed to validate system resilience.  
Inadequate patching, configuration errors, or untested recovery procedures may expose the organization to operational and reputational risks.  

    """
    highlight_control(sample)


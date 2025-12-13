import spacy
from spacy.tokens import Span

nlp = spacy.load("en_core_web_trf")  #Using transformaer dataset

# key words to extract
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

text = """
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

doc = nlp(text) #passign the text into spacy to get linguistically enriched object

entities = []

for sent in doc.sents:  #take the whole sentence
    for word in sent:
        if word.lemma_.lower() in RISK_KEYWORDS:    #lemma = simplifies the word
            entities.append((word.text, "RISK"))
        if word.lemma_.lower() in CONTROL_KEYWORDS:    
            entities.append((word.text, "CONTROL"))  #double bracket for tuple
        if word.lemma_.lower() in ASSET_KEYWORDS:    
            entities.append((word.text, "ASSET")) 
    
unique_ent = list(set(entities))

for ent_text, ent_lable in unique_ent: #loop through each entities tuple
    match = next((s for s in doc.ents if s.text == ent_text), None) #check if text already exist as entity in doc
    if not match:
        start = [t.text for t in doc].index(ent_text)
        end = start+1

        span = Span(doc, start, end, label=ent_lable)

        doc.ents += (span,)

for ent in doc.ents:
    print(f"{ent.text} | {ent.label_}")







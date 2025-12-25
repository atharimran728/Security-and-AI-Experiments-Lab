import re
import json, datetime

def extract_iocs(log_text):
    ips = re.findall(r'\b\d{1,3}(?:\.\d{1,3}){3}\b', log_text)
    hashes = re.findall(r'\b[A-Fa-f0-9]{32,64}\b', log_text)
    domains = re.findall(r'\b[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}\b', log_text)
    return {"ips": list(set(ips)), "hashes": list(set(hashes)), "domains": list(set(domains))}

MITRE_MAP = {
    "powershell": "T1059.001 (Command and Scripting Interpreter: PowerShell)",
    "lsass": "T1003.001 (OS Credential Dumping: LSASS Memory)",
    "rundll32": "T1218.011 (Signed Binary Proxy Execution: Rundll32)",
    "reg.exe": "T1112 (Modify Registry)",
    "network connection": "T1049 (System Network Connections Discovery)"
}

def map_to_mitre(log_text):
    hits = []
    for key, tech in MITRE_MAP.items():
        if key.lower() in log_text.lower():
            hits.append(tech)
    return list(set(hits))


def generate_report(iocs, mitre_hits):
    report = {
        "timestamp": datetime.datetime.now().isoformat(),
        "iocs": iocs,
        "mitre_techniques_detected": mitre_hits,
        "coverage_summary": {
            "total_detected": len(mitre_hits),
            "total_known": len(MITRE_MAP),
            "coverage_percent": round((len(mitre_hits)/len(MITRE_MAP))*100, 2)
        }
    }
    with open("MITRE_Coverage_Report.json", "w") as f:
        json.dump(report, f, indent=2)
    return report

sys_logs_path = "./evidence_AtomicTest1/system_logs.txt"

with open(sys_logs_path, "r") as f:
    sys_logs = f.read()


iocs = extract_iocs(sys_logs)
mitre_hits = map_to_mitre(sys_logs)

report = generate_report(iocs=iocs, mitre_hits=mitre_hits)

print(json.dumps(report, indent=2))
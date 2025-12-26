import datetime
import json
from pathlib import Path

SAFE_MODE = True
ALLOWED_NETWORKS = ["10.0.0.0/24", "192.168.1.0/24"]
BLOCKED_KEYWORDS = ["rm ", "shutdown", "curl ", "nc ", "wget ", "powershell", "chmod 777"]

LOG_FILE = Path("safety_governor_log.jsonl")

def validate_action(action):
    for kw in BLOCKED_KEYWORDS:
        if kw in action:
            return "deny", f"Unsafe keyword detected: {kw}"
    if not any(net.split('/')[0] in action for net in ALLOWED_NETWORKS):
        return "deny", "Target out of allowed range."
    return "allow", "Action within safety boundaries."

def append_log(entry: dict):
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def execute_action(action):
    decision, reason = validate_action(action)
    log_entry = {
        "timestamp": datetime.datetime.utcnow().isoformat(),
        "action": action,
        "decision": decision,
        "reason": reason,
        "mode": "dry-run" if SAFE_MODE else "live"
    }

    append_log(log_entry)

    print(json.dumps(log_entry, indent=2))

    if decision == "deny":
        print(f"[!] Denied → {reason}")
    elif SAFE_MODE:
        print(f"[DRY-RUN] Would execute: {action}")
    else:
        print(f"[LIVE] Executing: {action}")

execute_action("ping 10.0.0.5")
execute_action("rm -rf /tmp")
execute_action("curl spam.com")
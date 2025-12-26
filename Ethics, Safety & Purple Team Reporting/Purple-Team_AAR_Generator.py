import json
import datetime, os

def generate_aar(log_file, output_file="AAR_Report.md"):
    data = []
    with open(log_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            data.append(json.loads(line))
    
    safe_ops = [d for d in data if d["decision"] == "allow"]
    denied_ops = [d for d in data if d["decision"] == "deny"]

    md = []
    md.append(f"# Purple-Team After Action Report")
    md.append(f"**Generated:** {datetime.datetime.utcnow().isoformat()}\n")
    md.append(f"**Log Source:** `{os.path.basename(log_file)}`\n")

    md.append("## Summary")
    md.append(f"- Total actions: {len(data)}")
    md.append(f"- Allowed: {len(safe_ops)}")
    md.append(f"- Denied: {len(denied_ops)}\n")

    md.append("## Allowed Operations")

    for d in safe_ops:
        md.append(f"- `{d['timestamp']}` > `{d['action']}` ({d['reason']})")

    md.append("## Denied Operations")

    for d in denied_ops:
        md.append(f"- `{d['timestamp']}` > `{d['action']}` ({d['reason']})")

    with open(output_file, "w") as f:
        f.write("\n".join(md))

    print(f"[+] AAR generated > {output_file}")
    

generate_aar("safety_governor_log.jsonl")
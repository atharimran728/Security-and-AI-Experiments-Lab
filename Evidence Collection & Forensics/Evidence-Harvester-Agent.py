import os
import subprocess
import datetime


TEST_NAME = "Atomic-run-1"
EVIDENCE_DIR = f"./evidence_{TEST_NAME}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
os.makedirs(EVIDENCE_DIR, exist_ok=True)

LOGS_FILE = os.path.join(EVIDENCE_DIR, "system_logs.txt")

def collect_logs():
    
    subprocess.run(f'wevtutil qe Security /f:text > "{LOGS_FILE}"', shell=True)
    return LOGS_FILE

PCAP_FILE = os.path.join(EVIDENCE_DIR, "network.pcap")

def capture_pcap(duration=10):
    subprocess.run(f"timeout {duration} tcpdump -i any -w {PCAP_FILE}", shell=True)
    return PCAP_FILE

collect_logs()
capture_pcap()


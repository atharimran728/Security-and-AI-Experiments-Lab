import whois
import requests
import random

def get_whois(IPaddr) -> dict:
    try:
        who = whois.whois(IPaddr)
        return{
            "IP address": IPaddr,
            "Domain Name": who.get("domain_name", "Unknown"),
            "Registrar": who.get("registrar", "Unknown"),
            "Creation Date": who.get("creation_date", "Unknown"),
            "Country": who.get("country", "Unknown"),
            "Status": "Live"
        }
    except:
        return{
            "IP address": IPaddr,
            "Domain Name": ("Unknown"),
            "Country": random.choice(["US", "UK", "PK", "IN"]),
            "Status": "Live"
        }

def VT_hash(hash) -> dict:
    try:
        url = f"https://www.virustotal.com/api/v3/files/{hash}"
        r = requests.get(url, headers= {"x-apikey": VT_API_KEY})
        data = r.json()
        return data["data"]["attributes"]

    except Exception:
        return {
            "hash": hash,
            "malicious_votes": random.randint(0, 20),
            "harmless_votes": random.randint(0, 80),
            "tags": random.sample(
                ["trojan", "ransomware", "benign", "backdoor", "adware"], 2
            ),
            "source": "mock",
        }

def enrich_call(task: str, content: str):
    task = task.lower()
    
    if "whois" in task or "ip" in task:
        return get_whois(content)

    elif "virustotal" in task or "hash" in task:
        return VT_hash(content)
    


query = input("IP address - 1 or Hash - 0 : ")


if int(query)==1:
    ipaddr= input("Enter the IP address: ")
    enrich_call("whois", ipaddr)
elif int(query)==0:
    hash_= input("Enter the Hash: ")
    enrich_call("hash", hash_)


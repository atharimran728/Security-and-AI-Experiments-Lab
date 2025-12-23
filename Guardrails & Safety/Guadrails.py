def Gaudrail(User_input):
    malicious_keywords = [
        "ignore all previous instructions",
        "system prompt",
        "pretend to be",
        "jailbreak",
        "bypass",
        "disable safety",
        "show hidden data",
        "reveal internal rules",
    ]

    for keyword in malicious_keywords:
        if User_input.lower() in keyword:
            return True
        
    return False

prompt = input("Enter the Prompt: ")

if Gaudrail(prompt):
    print("Adversarial Input Detected!!!")
else:
    response = model.generate(prompt)
    print("Adversarial Input Cleared!")


### OUTPUT VALIDATION  -- Refered from Week 8 Day 1 Extended SOC copilot.

# try:
#     parsed = yaml.safe_load(result)
#     print("[VALID YAML]\n")
# except yaml.YAMLError:
#     print("[YAML ERROR – showing raw output]\n")
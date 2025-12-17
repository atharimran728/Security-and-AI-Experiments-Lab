import openai
import json
from difflib import SequenceMatcher

with open("sample_logs.json") as f:
    logs = json.load(f)
with open("gold_qa.json") as f:
    gold_qa = json.load(f)

for entry in gold_qa:
    log_entry = next(l for l in logs if l["id"] == entry["id"])
    question = entry["question"]

    print(entry)
    print(log_entry)
    

    prompt = f"""
    You are a SOC Analyst. Analyze this log and answer the question.

    LOG:
    {log_entry['log']}

    QUESTION:
    {question}
    Only give a concise, direct answer.
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    model_answer = response.choices[0].message.content.strip()
    gold_answer = entry["gold_answer"]

    similarity = SequenceMatcher(None, model_answer.lower(), gold_answer.lower()).ratio()

    print(f"\nLog ID {entry['id']}")
    print(f"Model Answer: {model_answer}")
    print(f"Gold Answer: {gold_answer}")
    print(f"Similarity: {similarity:.2f}")

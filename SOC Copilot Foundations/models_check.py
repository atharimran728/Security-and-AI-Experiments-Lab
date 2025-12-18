import time
import json
from google import genai


client = genai.Client()


MODELS = [
    {"name": "gemini-2.5-flash", "price_in": 0.00005, "price_out": 0.00015},
    {"name": "gemini-2.5-pro", "price_in": 0.0005, "price_out": 0.0015},
]


results = []

for model in MODELS:
    start = time.time()

    response = client.models.generate_content(
        model=model["name"],
        contents="Summarize this log entry and classify it as benign or malicious:\n[AUTH FAILURE from 10.0.0.5 multiple times in 30s]",
        config=genai.types.GenerateContentConfig(
            system_instruction="You are a SOC Analyst. Provide only the summary and classification."
        )
    )

    latency = time.time() - start
    tokens_in = response.usage_metadata.prompt_token_count
    tokens_out = response.usage_metadata.candidates_token_count
    total_tokens = response.usage_metadata.total_token_count

    cost = ((tokens_in / 1000) * model["price_in"]) + ((tokens_out / 1000) * model["price_out"])

    results.append({
        "model": model["name"],
        "latency": latency,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "total_tokens": total_tokens,
        "cost": cost,
        "output_preview": response.text 
    })

print(json.dumps(results, indent=2))




 

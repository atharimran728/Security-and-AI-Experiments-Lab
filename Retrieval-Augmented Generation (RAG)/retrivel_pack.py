import json, os, faiss
from llama_index.core import VectorStoreIndex, Document, StorageContext, Settings
from llama_index.vector_stores.faiss import FaissVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    device=device
)
Settings.embed_model = embed_model


attack_docs = []
with open("enterprise-attack.json", "r") as f:
    attack_data = json.load(f)

for technique in attack_data.get("techniques", []):
    tech_id = technique.get("external_id", "T-Unknown")
    name = technique.get("name", "")
    desc = technique.get("description", "")
    tactic = ", ".join(technique.get("tactics", []))
    attack_docs.append(
        Document(
            text=f"[ATTACK] {tech_id} | {name} | {desc} | Tactics: {tactic}",
            metadata={"type": "attack_card", "tech_id": tech_id, "tactic": tactic}
        )
    )

print(f"Loaded {len(attack_docs)} ATT&CK techniques")


log_docs = []
with open("badhttp.json", "r") as f:
    log_data = json.load(f)

for entry in log_data:
    alert = entry.get("alert", {}).get("signature", "")
    src_ip = entry.get("src_ip", "")
    dst_ip = entry.get("dest_ip", "")
    severity = entry.get("alert", {}).get("severity", "")
    log_docs.append(
        Document(
            text=f"[ALERT] {alert} | Source: {src_ip} | Dest: {dst_ip} | Severity: {severity}",
            metadata={"type": "alert"}
        )
    )
print(f"Loaded {len(log_docs)} alerts")


docs = attack_docs + log_docs

embedding_dim = 384  # MiniLM-L6-v2 outputs 384-d vectors
faiss_index = faiss.IndexFlatL2(embedding_dim)
vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(
    docs,
    storage_context=storage_context,
    embed_model=embed_model,
    show_progress=True
)


query_engine = index.as_query_engine(similarity_top_k=3)

for entry in log_docs[:5]:  # first 5 alerts
    q = entry.text
    resp = query_engine.query(f"Map this alert: {q}")
    print(f"\nALERT: {q}\nMITRE Mapping:\n{resp}\n{'-'*70}")

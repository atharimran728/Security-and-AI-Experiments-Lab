import os
import json
import chromadb
from llama_index.core import VectorStoreIndex, Document, StorageContext, load_index_from_storage
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core import Settings


JSON_FILE = os.path.join(os.getcwd(), "badhttp.json")     
PERSIST_DIR = os.path.join(os.getcwd(), "index_store")   


with open(JSON_FILE, "r") as f:
    logs = json.load(f)


documents = [
    Document(text=json.dumps(log), metadata={"source": "zeek_suricata"})
    for log in logs
]


embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2",
    embed_batch_size=32
)
Settings.embed_model = embed_model


if not os.path.exists(PERSIST_DIR):
    print("Building index from scratch (first run)...")

    chroma_client = chromadb.Client()
    chroma_collection = chroma_client.get_or_create_collection("security_logs")

    storage_context = StorageContext.from_defaults(
        vector_store=ChromaVectorStore(chroma_collection)
    )

    index = VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context,
        show_progress=True
    )

    os.makedirs(PERSIST_DIR, exist_ok=True)
    index.storage_context.persist(persist_dir=PERSIST_DIR)
    print(f"Index built and saved to: {PERSIST_DIR}")

else:
    print("Loading existing index from disk...")
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    index = load_index_from_storage(storage_context)
    print("Index loaded successfully.")


query_engine = index.as_query_engine(similarity_top_k=5)

queries = [
    "List all logs showing potential Shellshock exploit attempts.",
    "Which IPs returned 404 Not Found responses?",
    "What are the top URIs accessed from 10.164.94.120?",
    "Summarize suspicious HTTP behavior in this dataset."
]

for q in queries:
    print(f"\nQuery: {q}")
    response = query_engine.query(q)
    print("Response:\n", response)
    print("-" * 80)

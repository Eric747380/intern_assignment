import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load everything once
print("📦 Loading FAISS index and metadata...")
model = SentenceTransformer("all-MiniLM-L6-v2")
index = faiss.read_index("bphs_faiss.index")

with open("bphs_meta.json", "r", encoding="utf-8") as f:
    metadata = json.load(f)

# Main retrieval function
def retrieve_relevant_chunks(question, top_k=5):
    question_embedding = model.encode([question])[0].astype("float32")
    question_embedding = np.expand_dims(question_embedding, axis=0)

    D, I = index.search(question_embedding, top_k)

    results = []
    for idx in I[0]:
        results.append(metadata[idx])

    return results
if __name__ == "__main__":
    while True:
        q = input("\nAsk a question: ")
        top_chunks = retrieve_relevant_chunks(q)
        for i, c in enumerate(top_chunks):
            print(f"\n🔹 Chunk {i+1} from '{c['chapter_title']}':\n{c['content']}")

import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Load BPHS chunks
with open("bphs_chunks.json", "r", encoding="utf-8") as f:
    chunks = json.load(f)

# Load sentence transformer model
print("🔄 Loading embedding model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Embed the text content
texts = [chunk["content"] for chunk in chunks]
print("🔄 Embedding chunks...")
embeddings = model.encode(texts, show_progress_bar=True)

# Convert to float32 for FAISS
embeddings = np.array(embeddings).astype("float32")

# Build FAISS index
index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

# Save index and metadata
faiss.write_index(index, "bphs_faiss.index")
with open("bphs_meta.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print(f"✅ Indexed {len(chunks)} chunks and saved to bphs_faiss.index")

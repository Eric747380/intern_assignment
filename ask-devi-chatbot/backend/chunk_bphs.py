import re
import json

# Step 1: Read BPHS text
with open("BPHS.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()

# Step 2: Split by chapters
chapters = re.split(r"\nCh\. \d+\.\s+", raw_text)[1:]
chapter_titles = re.findall(r"\nCh\. \d+\.\s+([^\n]+)", raw_text)

assert len(chapters) == len(chapter_titles), "Mismatch in chapters vs titles!"

# Step 3: Chunk chapters
chunk_size = 600
overlap = 100
chunks = []

for idx, (title, chapter_text) in enumerate(zip(chapter_titles, chapters)):
    text = chapter_text.strip().replace("\n", " ")
    for i in range(0, len(text), chunk_size - overlap):
        chunk = text[i:i+chunk_size]
        chunks.append({
            "chunk_id": f"{idx+1}-{i}",
            "chapter_title": title,
            "content": chunk
        })

# Step 4: Save to JSON
with open("bphs_chunks.json", "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print(f"✅ Saved {len(chunks)} chunks to bphs_chunks.json")

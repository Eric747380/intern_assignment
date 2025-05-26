from flask import Flask, request, jsonify
from flask_cors import CORS
from rag import retrieve_relevant_chunks
from utils import calculate_chart
import requests
import os
from ctransformers import AutoModelForCausalLM


from transformers import AutoTokenizer, pipeline
from collections import defaultdict, deque

# Store up to 10 messages per session ID (or birth hash)
session_memory = defaultdict(lambda: deque(maxlen=10))

print("🔄 Loading Mistral-7B-Instruct (Quantized)...")

llm = AutoModelForCausalLM.from_pretrained(
    "models/mistral",
    model_file="mistral-7b-instruct-v0.1.Q4_K_M.gguf",
    model_type="mistral",
    max_new_tokens=300,
    temperature=0.7,
    repetition_penalty=1.1
)

print("✅ Mistral-7B-Instruct loaded (quantized)")



app = Flask(__name__)
CORS(app)


def call_llm_local(prompt):
    try:
        print("🔮 Generating with Mistral...")
        response = llm(prompt)
        return response.strip().split("Answer:")[-1].strip()
    except Exception as e:
        print("❌ Mistral generation failed:", str(e))
        return "Sorry, Devi couldn’t respond clearly."


@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"message": "Ask Devi backend is working!"})

@app.route("/birth_details", methods=["POST"])
def birth_details():
    data = request.json
    try:
        chart = calculate_chart(
            data.get("name"),
            data.get("dateOfBirth"),
            data.get("timeOfBirth"),
            data.get("placeOfBirth")
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 400

    print("Received birth details:", data)
    return jsonify({"chart": chart})


@app.route("/ask_question", methods=["POST"])
def ask_question():
    data = request.json
    question = data.get("question", "")
    birth_details = data.get("birthDetails", {})

    session_key = f"{birth_details.get('name')}_{birth_details.get('dateOfBirth')}_{birth_details.get('timeOfBirth')}"
    session_memory[session_key].append({"role": "user", "text": question})

    print("Question received:", question)
    print("Birth details:", birth_details)

    # 🔍 Retrieve BPHS chunks
    relevant_chunks = retrieve_relevant_chunks(question, top_k=1)  # Only 1 chunk
    top_chunk = relevant_chunks[0] if relevant_chunks else None
    chapter = top_chunk.get('chapter', 'Unknown') if top_chunk else 'Unknown'
    chapter_num = top_chunk.get('chapter_number', '?')
    source = f"📖 Source: Chapter {chapter_num} — {chapter}"

    # Truncate content to 500 characters
    bphs_context = (
        f"[{top_chunk['chapter_title']}]\n{top_chunk['content'][:500]}..." if top_chunk else ""
    )

    # Only last user message
    recent_history = list(session_memory[session_key])[-1:]
    chat_history_str = "\n".join([f"{m['role'].capitalize()}: {m['text']}" for m in recent_history])

    # 🧠 Build prompt
    prompt = f"""Answer based on the BPHS excerpt and the conversation so far.

User's Birth Chart:
Sun Sign: {birth_details.get('sunSign', 'Unknown')}
Moon Sign: {birth_details.get('moonSign', 'Unknown')}
Ascendant: {birth_details.get('ascendant', 'Unknown')}
Conversation so far:
{chat_history_str}

Relevant BPHS Excerpt:
{bphs_context}

Answer the user's question using only the BPHS and your astrological reasoning.

Question: {question}
Answer:"""

    print("\n--- Prompt Sent to LLM ---\n")
    print(prompt)

    answer = call_llm_local(prompt)
    session_memory[session_key].append({"role": "devi", "text": answer})

    return jsonify({
        "answer": answer,
        "source": source
    })


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
from flask_cors import CORS
from rag import retrieve_relevant_chunks
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

# 🔐 Hugging Face Inference API
# HUGGINGFACE_API_KEY = "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"  # Replace with your own token

# def call_hf_model(prompt):
#     API_URL = "https://api-inference.huggingface.co/models/databricks/dolly-v2-3b"
#     headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 300,
#             "temperature": 0.7,
#             "return_full_text": True
#         }
#     }

#     try:
#         response = requests.post(API_URL, headers=headers, json=payload)
#         response.raise_for_status()
#         result = response.json()

#         if isinstance(result, list) and "generated_text" in result[0]:
#             return result[0]["generated_text"].split("Answer:")[-1].strip()
#         else:
#             print("⚠️ Unexpected response format:", result)
#             return "Sorry, Devi couldn’t interpret the ancient texts right now."

#     except requests.exceptions.RequestException as e:
#         print("❌ Request failed:", e)
#         print("Response content:", response.text)
#         return "Sorry, Devi couldn't reach her divine source."

# def call_hf_model(prompt):
#     API_URL = "https://api-inference.huggingface.co/models/tiiuae/falcon-7b-instruct"
#     API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-xl"

#     headers = {"Authorization": f"Bearer {HUGGINGFACE_API_KEY}"}
#     payload = {
#         "inputs": prompt,
#         "parameters": {
#             "max_new_tokens": 300,
#             "temperature": 0.7,
#             "return_full_text": True
#         }
#     }

#     try:
#         response = requests.post(API_URL, headers=headers, json=payload)
#         response.raise_for_status()  # Raise error for non-2xx responses
#         result = response.json()

#         # Check if it's a valid response
#         if isinstance(result, list) and "generated_text" in result[0]:
#             return result[0]["generated_text"].split("Answer:")[-1].strip()
#         else:
#             print("⚠️ Unexpected response format:", result)
#             return "Sorry, Devi couldn’t understand the question clearly."

#     except requests.exceptions.RequestException as e:
#         print("❌ Request failed:", e)
#         print("Response content:", response.text)
#         return "Sorry, Devi couldn't connect to her divine source."


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
def receive_birth_details():
    data = request.json
    print("Received birth details:", data)

    # Simulated chart data
    mock_chart = {
        "sun_sign": "Aquarius",
        "moon_sign": "Leo",
        "ascendant": "Virgo",
        "nakshatra": "Purva Phalguni",
        "planet_positions": {
            "Sun": {"sign": "Aquarius", "house": "6th", "degree": 23.1},
            "Moon": {"sign": "Leo", "house": "12th", "degree": 10.4},
            "Mars": {"sign": "Gemini", "house": "10th", "degree": 14.2},
            "Mercury": {"sign": "Pisces", "house": "7th", "degree": 5.7},
            "Jupiter": {"sign": "Scorpio", "house": "3rd", "degree": 18.9},
            "Venus": {"sign": "Capricorn", "house": "5th", "degree": 11.8},
            "Saturn": {"sign": "Libra", "house": "2nd", "degree": 29.0},
            "Rahu": {"sign": "Taurus", "house": "9th", "degree": 4.6},
            "Ketu": {"sign": "Scorpio", "house": "3rd", "degree": 4.6},
        },
        "chart_type": "North Indian",
        "notes": "This is a mocked chart. For live charts, integrate with astrologyapi.com."
    }

    return jsonify({
        "message": "Mock birth chart generated.",
        "chart": mock_chart
    })

@app.route("/ask_question", methods=["POST"])
def ask_question():
    data = request.json
    question = data.get("question", "")
    birth_details = data.get("birthDetails", {})

    # Generate a simple session key (or use UUID later)
    session_key = f"{birth_details.get('name')}_{birth_details.get('dateOfBirth')}_{birth_details.get('timeOfBirth')}"

    # Add question to memory
    session_memory[session_key].append({"role": "user", "text": question})

    print("Question received:", question)
    print("Birth details:", birth_details)

    # 🔍 Retrieve BPHS chunks
    relevant_chunks = retrieve_relevant_chunks(question, top_k=2)
    bphs_context = "\n\n".join(
        [f"[{c['chapter_title']}]\n{c['content']}" for c in relevant_chunks]
    )
    history = session_memory[session_key]
    chat_history_str = "\n".join([f"{m['role'].capitalize()}: {m['text']}" for m in history])

    # 🧠 Build prompt
    # prompt = f"""You are Devi, a wise Vedic astrologer trained in the ancient text Brihat Parasara Hora Sastra (BPHS).
    prompt = f"""Based on the ancient Indian astrology text Brihat Parasara Hora Sastra (BPHS), answer the following question.

User's Birth Chart:
Sun Sign: {birth_details.get('sunSign', 'Unknown')}
Moon Sign: {birth_details.get('moonSign', 'Unknown')}
Ascendant: {birth_details.get('ascendant', 'Unknown')}
Conversation so far:
{chat_history_str}

Relevant BPHS Excerpts:
{bphs_context}

Answer the user's question using only the BPHS and your astrological reasoning.

Question: {question}
Answer:"""

    print("\n--- Prompt Sent to LLM ---\n")
    print(prompt)

    # 🤖 Generate answer
    # answer = call_hf_model(prompt)
    answer = call_llm_local(prompt)

    # Add Devi's reply to memory
    session_memory[session_key].append({"role": "devi", "text": answer})


    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)

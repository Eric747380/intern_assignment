## Astrology API Integration

This project currently uses simulated astrology chart data to avoid API limitations and keep development free.

provide star signs based on date and place and time of birth:
 implemented the basic birth chart parser 🌌 so Ask Devi can provide real Sun, Moon, and Ascendant signs from birth details.

We’ll use:

🗺️ geopy — for lat/lon of birthplace

🪐 pyswisseph (Swiss Ephemeris) — for planetary positions

We’ve preserved the backend interface to allow easy swapping of this logic.

![image](https://github.com/user-attachments/assets/19af10d7-29b8-46cf-aef0-0c65ba9bde88)



# 🪷 Ask Devi: Vedic Astrology Chatbot

**Ask Devi** is an RAG-powered chatbot that answers questions based on the *Brihat Parasara Hora Sastra (BPHS)* using your birth details.

## 📌 Features
- React + Flask full-stack app
- Enter birth details → chat with Devi
- Local RAG + FAISS over BPHS
- Local 7B LLM (Mistral) with memory
- “Regenerate answer” + contextual follow-up
- Works offline (no external API needed)

## 🧠 Technologies
- React (frontend)
- Flask (backend)
- FAISS for vector DB
- Mistral-7B-Instruct (quantized, via ctransformers)
- Hugging Face tokenizers

## 🧪 How to Run



### Backend

```bash
cd backend
.\venv\Scripts\activate
pip install -r requirements.txt
python app.py

### frontend



cd frontend
npm install

in powershell
$env:NODE_OPTIONS="--openssl-legacy-provider"
npm start

in cmd prompt
set NODE_OPTIONS=--openssl-legacy-provider
npm start

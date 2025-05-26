## Astrology API Integration

This project currently uses simulated astrology chart data to avoid API limitations and keep development free.

To integrate with a real astrology engine (like [astrologyapi.com](https://astrologyapi.com)):
- Replace the mock chart response in `backend/app.py`
- Provide user birth data, convert place to lat/lng, and call the desired API endpoint

We’ve preserved the backend interface to allow easy swapping of this logic.



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
pip install -r requirements.txt
python app.py

### frontend
cd frontend
npm install
npm start

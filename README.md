# AI Chatbot

A simple ChatGPT-like web chatbot built with Python, Flask, and the OpenAI API.

---

## Project Structure

```
chatbot/
├── app.py                  # Flask app – routes only
├── requirements.txt
├── .env                    # Your secrets (never commit this)
├── .env.example            # Template for the .env file
├── services/
│   └── ai_service.py       # All OpenAI logic
├── templates/
│   └── index.html          # Chat page
└── static/
    ├── css/style.css       # Styles
    └── js/script.js        # Frontend chat logic
```

---

## Setup Guide

### 1. Create a virtual environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add your OpenAI API key

Copy the example file and fill in your key:

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and replace the placeholder:

```
OPENAI_API_KEY=sk-...your-real-key-here...
```

> Get your key at https://platform.openai.com/api-keys

### 4. Run the application

```bash
python app.py
```

Then open your browser and visit: **http://127.0.0.1:5000**

---

## How to use the chatbot

| Action | How |
|---|---|
| Send a message | Type in the box and press **Enter** |
| New line in input | **Shift + Enter** |
| Clear the conversation | Click **🗑 Clear Chat** |

---

## Features

- Multi-turn conversation (the AI remembers the current session)
- Loading indicator while the AI responds
- Friendly error messages if something goes wrong
- Responsive design – works on mobile too
- Dark theme

---

## Notes

- The conversation history is kept **in-browser memory only** – it resets on page refresh. No database is needed.
- The model used is `gpt-3.5-turbo`. You can change it in `services/ai_service.py`.

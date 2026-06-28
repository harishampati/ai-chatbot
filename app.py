"""
app.py – Flask entry point.
Defines two routes:
  GET  /      → serves the chat page
  POST /chat  → receives a message, calls the AI, returns a JSON reply
"""

from flask import Flask, render_template, request, jsonify
from services.ai_service import get_ai_response

app = Flask(__name__)


@app.route("/")
def index():
    """Render the main chat page."""
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    """
    Expect JSON body: { "message": "...", "history": [...] }
    Return JSON:       { "reply": "..." }  or  { "error": "..." }
    """
    data = request.get_json(silent=True)

    if not data or not data.get("message", "").strip():
        return jsonify({"error": "Message cannot be empty."}), 400

    user_message = data["message"].strip()
    # history is a list of {role, content} dicts sent from the frontend
    history = data.get("history", [])

    # Append the new user message to the history before sending
    history.append({"role": "user", "content": user_message})

    try:
        reply = get_ai_response(history)
        return jsonify({"reply": reply})
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 500
    except RuntimeError as exc:
        return jsonify({"error": str(exc)}), 502


if __name__ == "__main__":
    app.run(debug=True)

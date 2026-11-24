import os
import time
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google import genai

api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("Chyba: API klíč nebyl nalezen v proměnných prostředí (GEMINI_API_KEY).")

client = genai.Client(api_key=api_key)

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)


@app.route("/")
def home():
    return send_from_directory('.', 'index.html')


def generate_support_reply(prompt: str) -> str:
    models_to_try = ["gemini-3.8-flash"]
    last_error = None

    for model_name in models_to_try:
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                )
                text = (response.text or "").strip()
                if text:
                    return text
            except Exception as e:
                last_error = e
                msg = str(e)
                if ("503" in msg or "UNAVAILABLE" in msg or "429" in msg) and attempt == 0:
                    time.sleep(1.5)
                    continue
                break

    raise last_error or RuntimeError("Nepodařilo se získat odpověď od AI.")


@app.post("/api/ticket")
def submit_ticket():
    data = request.get_json(silent=True) or {}

    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    subject = (data.get("subject") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not subject or not message:
        return jsonify({"error": "Všechna pole jsou povinná."}), 400

    prompt = f"""
    Jsi technická podpora pro hru "Vaříme s tátou".
    Hráč jménem {name} hlásí problém s předmětem: "{subject}".
    Popis problému: {message}
    Odpověz hráči stručně, zdvořile v češtině a zkus mu poradit. Na konci se podepiš jako "Tým podpory".
    """.strip()

    try:
        reply = generate_support_reply(prompt)
        return jsonify({"reply": reply}), 200
    except Exception as e:
        print("CHYBA V /api/ticket:", repr(e), flush=True)
        return jsonify({"error": f"AI asistent je momentálně nedostupný: {str(e)}"}), 500


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)

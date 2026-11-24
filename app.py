import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from google import genai

# Načtení API klíče z proměnných prostředí
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Chyba: API klíč nebyl nalezen v proměnných prostředí (GEMINI_API_KEY).")

client = genai.Client(api_key=api_key)

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)


@app.route("/")
def home():
    return send_from_directory('.', 'index.html')


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
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt,
        )
        reply = (response.text or "").strip()
        if not reply:
            reply = "Omlouváme se, nepodařilo se vygenerovat odpověď. Tým podpory"
        return jsonify({"reply": reply}), 200
    except Exception as e:
        return jsonify({
            "error": f"AI asistent je momentálně nedostupný: {str(e)}"
        }), 500


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)

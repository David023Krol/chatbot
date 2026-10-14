import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

# Nastavení Flasku, aby hledal statické soubory i šablony ve stejné složce jako je app.py
app = Flask(__name__, static_folder='.', template_folder='.')

CORS(app)

# Servírování index.html na hlavní stránce
@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

# Servírování ostatních statických souborů (CSS, JS)
@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('.', path)

@app.post("/api/ticket")
def submit_ticket():
    data = request.get_json(silent=True) or {}
    
    name = (data.get("name") or "").strip()
    email = (data.get("email") or "").strip()
    subject = (data.get("subject") or "").strip()
    message = (data.get("message") or "").strip()

    if not name or not email or not subject or not message:
        return jsonify({"error": "Všechna pole jsou povinná."}), 400

    reply = (
        f"Dobrý den, {name},\n\n"
        f"přijali jsme Váš ticket s předmětem \"{subject}\".\n"
        f"Náš technický tým hry \"Vaříme s tátou\" Váš problém momentálně analyzuje. "
        f"Jakmile najdeme řešení, budeme Vás kontaktovat na zadaný e-mail: {email}.\n\n"
        f"S pozdravem,\nTým podpory"
    )

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)
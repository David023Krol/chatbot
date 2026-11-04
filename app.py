import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

# Načtení klíče z proměnných prostředí (musí se shodovat s textem v poli KEY)
api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Chyba: API klíč nebyl nalezen v proměnných prostředí.")

# Konfigurace Gemini
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

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

    # 2. SESTAVENÍ INSTRUKCE (PROMPTU) PRO AI
    prompt = f"""
    Jsi technická podpora pro hru "Vaříme s tátou". 
    Hráč jménem {name} hlásí problém s předmětem: "{subject}".
    Popis problému: {message}
    Odpověz hráči stručně, zdvořile a zkus mu poradit. Na konci se podepiš jako "Tým podpory".
    """

    try:
        # 3. ZÍSKÁNÍ ODPOVĚDI OD GEMINI
        ai_response = model.generate_content(prompt)
        reply = ai_response.text
    except Exception as e:
        reply = f"Omlouváme se, AI asistent je momentálně nedostupný. Chyba: {str(e)}"

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)



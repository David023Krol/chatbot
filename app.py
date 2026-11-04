import os
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import google.generativeai as genai

api_key = os.environ.get("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Chyba: API klíč nebyl nalezen v proměnných prostředí.")

genai.configure(api_key=api_key)

# Použití aktuálního standardního modelu
model = genai.GenerativeModel('gemini-2.0-flash')

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

@app.route("/")
def home():
    return send_from_directory('.', 'index.html')

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

    prompt = f"""
    Jsi technická podpora pro hru "Vaříme s tátou". 
    Hráč jménem {name} hlásí problém s předmětem: "{subject}".
    Popis problému: {message}
    Odpověz hráči stručně, zdvořile a zkus mu poradit. Na konci se podepiš jako "Tým podpory".
    """

    try:
        ai_response = model.generate_content(prompt)
        reply = ai_response.text
    except Exception as e:
        # Pokud zadaný model selže, zjistíme přesné dostupné modely pro váš API klíč
        try:
            models = [m.name.replace('models/', '') for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
            reply = f"Chyba: {str(e)}.\n\nDostupné modely pro váš klíč jsou:\n" + "\n".join(models)
        except Exception:
            reply = f"Omlouváme se, AI je nedostupná. Zkontrolujte, zda je API klíč z vygenerován přímo na aistudio.google.com."

    return jsonify({"reply": reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)

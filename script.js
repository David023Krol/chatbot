document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const submitBtn = form.querySelector('button[type="submit"]');
    const textareas = document.querySelectorAll('textarea');
    const replyTextarea = document.getElementById('answer') || textareas[1];

    if (replyTextarea) {
        replyTextarea.readOnly = true;
    }

    // Přidáno slovo "async", aby šlo čekat na odpověď serveru
    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        try {
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const subjectInput = document.getElementById('subject');
            const messageInput = document.getElementById('message');

            if (!nameInput || !emailInput || !subjectInput || !messageInput) {
                throw new Error('Chyba aplikace: Některá pole formuláře nebyla nalezena.');
            }

            const name = nameInput.value.trim();
            const email = emailInput.value.trim();
            const subject = subjectInput.value.trim();
            const message = messageInput.value.trim();

            if (!name || !email || !subject || !message) {
                throw new Error('Prosím, vyplňte smysluplně všechna pole.');
            }

            submitBtn.textContent = 'Odesílám...';
            submitBtn.disabled = true;
            replyTextarea.style.color = 'black'; 
            replyTextarea.value = 'Analyzuji problém pomocí AI...';

            // Skutečné odeslání dat na váš Python server (API)
            const response = await fetch('/api/ticket', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    name: name,
                    email: email,
                    subject: subject,
                    message: message
                })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Nastala chyba při komunikaci se serverem.');
            }

            // Vypsání reálné odpovědi od Gemini
            replyTextarea.value = data.reply;

        } catch (error) {
            replyTextarea.style.color = 'red';
            replyTextarea.value = `⚠️ CHYBA: ${error.message}`;
        } finally {
            submitBtn.textContent = 'Odeslat další ticket';
            submitBtn.disabled = false;
        }
    });
});

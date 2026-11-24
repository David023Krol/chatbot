document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    if (!form) return;

    const submitBtn = form.querySelector('button[type="submit"]');
    const textareas = document.querySelectorAll('textarea');
    const replyTextarea = document.getElementById('answer') || textareas[1];

    if (replyTextarea) {
        replyTextarea.readOnly = true;
    }

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        try {
            const nameInput = document.getElementById('name');
            const emailInput = document.getElementById('email');
            const subjectInput = document.getElementById('subject');
            const messageInput = document.getElementById('message');

            if (!nameInput || !emailInput || !subjectInput || !messageInput) {
                throw new Error('Některá pole formuláře nebyla nalezena.');
            }

            const name = nameInput.value.trim();
            const email = emailInput.value.trim();
            const subject = subjectInput.value.trim();
            const message = messageInput.value.trim();

            if (!name || !email || !subject || !message) {
                throw new Error('Prosím, vyplňte všechna povinná pole.');
            }

            if (submitBtn) {
                submitBtn.textContent = 'Odesílám...';
                submitBtn.disabled = true;
            }

            if (replyTextarea) {
                replyTextarea.style.color = '#222';
                replyTextarea.value = 'Analyzuji problém pomocí AI...';
            }

            const response = await fetch('/api/ticket', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ name, email, subject, message })
            });

            const rawText = await response.text();
            let data = {};
            try {
                data = rawText ? JSON.parse(rawText) : {};
            } catch {
                throw new Error(rawText || `Chyba serveru (HTTP ${response.status}).`);
            }

            if (!response.ok) {
                throw new Error(data.error || `Nastala chyba při komunikaci se serverem (HTTP ${response.status}).`);
            }

            if (replyTextarea) {
                replyTextarea.style.color = '#111';
                replyTextarea.value = data.reply || 'Bez odpovědi.';
            }
        } catch (error) {
            if (replyTextarea) {
                replyTextarea.style.color = '#c0392b';
                replyTextarea.value = `⚠️ CHYBA: ${error.message}`;
            }
        } finally {
            if (submitBtn) {
                submitBtn.textContent = 'Odeslat další ticket';
                submitBtn.disabled = false;
            }
        }
    });
});

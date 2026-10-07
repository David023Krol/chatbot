document.addEventListener('DOMContentLoaded', () => {
    
    const form = document.querySelector('form');
    const submitBtn = form.querySelector('button[type="submit"]');
    const textareas = document.querySelectorAll('textarea');
    const replyTextarea = document.getElementById('answer') || textareas[1];

    if (replyTextarea) {
        replyTextarea.readOnly = true;
    }

    form.addEventListener('submit', (e) => {
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
            replyTextarea.value = 'Načítám odpověď serveru...';

            setTimeout(() => {
                try {
                    const isNetworkError = Math.random() < 0.15; 
                    
                    if (isNetworkError) {
                        throw new Error('Nepodařilo se spojit se serverem. Zkontrolujte připojení k internetu a zkuste to znovu.');
                    }
                    
                    const autoReply = `Dobrý den, ${name},\n\npřijali jsme Váš ticket s předmětem "${subject}".\nNáš technický tým hry "Vaříme s tátou" Váš problém momentálně analyzuje. Jakmile najdeme řešení, budeme Vás kontaktovat na zadaný e-mail: ${email}.\n\nS pozdravem,\nTým podpory`;
                          
                    replyTextarea.value = autoReply;

                } catch (serverError) {
                    replyTextarea.style.color = 'red';
                    replyTextarea.value = `⚠️ CHYBA: ${serverError.message}`;
                } finally {
                    submitBtn.textContent = 'Odeslat další ticket';
                    submitBtn.disabled = false;
                }
            }, 1500); 

        } catch (clientError) {
            replyTextarea.style.color = 'red';
            replyTextarea.value = `⚠️ CHYBA: ${clientError.message}`;
            submitBtn.textContent = 'Odeslat ticket';
            submitBtn.disabled = false;
        }
    });
});
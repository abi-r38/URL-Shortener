// static/script.js
document.addEventListener('DOMContentLoaded', () => {
    const urlForm = document.getElementById('url-form');
    const urlInput = document.getElementById('url-input');
    const submitButton = document.getElementById('submit-button');
    const resultArea = document.getElementById('result-area');
    const shortUrlLink = document.getElementById('short-url-link');
    const copyButton = document.getElementById('copy-button');

    urlForm.addEventListener('submit', async (event) => {
        event.preventDefault();

        const longUrl = urlInput.value;
        if (!longUrl) return;

        submitButton.disabled = true;
        submitButton.textContent = 'Shortening...';

        try {
            // THE FIX: Use the correct '/create/' URL and remove the CSRF token header
            const response = await fetch('/create/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    // The 'X-CSRFToken' header has been removed
                },
                body: JSON.stringify({ long_url: longUrl })
            });

            const data = await response.json();

            if (response.ok) {
                shortUrlLink.href = data.short_url;
                shortUrlLink.textContent = data.short_url;
                resultArea.classList.remove('hidden');
                urlInput.value = '';
            } else {
                alert(`Error: ${data.error || 'Something went wrong.'}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An unexpected error occurred.');
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = 'Shorten URL';
        }
    });
    
    copyButton.addEventListener('click', () => {
        navigator.clipboard.writeText(shortUrlLink.href)
            .then(() => {
                copyButton.textContent = 'Copied!';
                setTimeout(() => { copyButton.textContent = 'Copy'; }, 2000);
            });
    });

    function getCookie(name) { // Standard Django function to get the CSRF token
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
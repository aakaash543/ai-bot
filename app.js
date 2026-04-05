document.addEventListener('DOMContentLoaded', () => {
    const errorInput = document.getElementById('error-input');
    const suggestBtn = document.getElementById('suggest-btn');
    const btnText = suggestBtn.querySelector('.btn-text');
    const spinner = suggestBtn.querySelector('.spinner');

    const resultsSection = document.getElementById('results-section');
    const solutionContent = document.getElementById('solution-content');
    const copyBtn = document.getElementById('copy-btn');

    let currentSuggestion = '';

    suggestBtn.addEventListener('click', async () => {
        const errorLog = errorInput.value.trim();

        if (!errorLog) {
            alert('Please paste an error log first.');
            return;
        }

        // Loading UI
        suggestBtn.disabled = true;
        btnText.textContent = 'Analyzing...';
        spinner.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch('/api/suggest', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ error_log: errorLog })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to get suggestion');
            }

            currentSuggestion = data.suggestion || "No output from AI";

            // Display safely
            solutionContent.innerText = currentSuggestion;
            resultsSection.classList.remove('hidden');

        } catch (err) {
            console.error(err);
            solutionContent.innerText = "Error: " + err.message;
            resultsSection.classList.remove('hidden');
        } finally {
            suggestBtn.disabled = false;
            btnText.textContent = 'Generate Fix';
            spinner.classList.add('hidden');
        }
    });

    copyBtn.addEventListener('click', () => {
        if (!currentSuggestion) return;

        navigator.clipboard.writeText(currentSuggestion);
        copyBtn.textContent = '✅';

        setTimeout(() => {
            copyBtn.textContent = 'Copy';
        }, 2000);
    });
});
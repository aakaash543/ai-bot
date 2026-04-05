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

        // Set Loading state
        suggestBtn.disabled = true;
        btnText.textContent = 'Analyzing...';
        spinner.classList.remove('hidden');
        resultsSection.classList.add('hidden');

        try {
            const response = await fetch('/api/suggest', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ error_log: errorLog })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'An error occurred while generating the fix.');
            }

            // Display Results
            currentSuggestion = data.suggestion;
            solutionContent.innerHTML = marked.parse(currentSuggestion);
            resultsSection.classList.remove('hidden');

        } catch (error) {
            console.error('Error:', error);
            currentSuggestion = `**Error:**\n${error.message}`;
            solutionContent.innerHTML = marked.parse(currentSuggestion);
            resultsSection.classList.remove('hidden');
        } finally {
            // Restore button state
            suggestBtn.disabled = false;
            btnText.textContent = 'Generate Fix';
            spinner.classList.add('hidden');
        }
    });

    copyBtn.addEventListener('click', () => {
        if (!currentSuggestion) return;
        
        navigator.clipboard.writeText(currentSuggestion).then(() => {
            const originalIcon = copyBtn.textContent;
            copyBtn.textContent = '✅';
            setTimeout(() => {
                copyBtn.textContent = originalIcon;
            }, 2000);
        }).catch(err => {
            console.error('Failed to copy: ', err);
            alert('Failed to copy to clipboard.');
        });
    });
});

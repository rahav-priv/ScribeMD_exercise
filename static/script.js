document.addEventListener('DOMContentLoaded', function() {
    const rawTranscriptInput = document.getElementById('raw-transcript');
    const parsedDataOutput = document.getElementById('parsed-data');
    const submitBtn = document.getElementById('submit-btn');
    const clearBtn = document.getElementById('clear-btn');
    const statusMessage = document.getElementById('status-message');

    // Submit button handler
    submitBtn.addEventListener('click', async function() {
        const transcript = rawTranscriptInput.value.trim();

        if (!transcript) {
            showStatus('Please enter some text', 'error');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';

        try {
            const response = await fetch('/api/parse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ transcript: transcript })
            });

            if (!response.ok) {
                throw new Error(`Server error: ${response.status}`);
            }

            const parsedData = await response.json();
            parsedDataOutput.value = JSON.stringify(parsedData, null, 2);
            showStatus('Transcript parsed successfully!', 'success');
        } catch (error) {
            console.error('Error:', error);
            showStatus('Error processing transcript: ' + error.message, 'error');
            parsedDataOutput.value = '';
        } finally {
            submitBtn.disabled = false;
            submitBtn.textContent = 'Submit';
        }
    });

    // Clear button handler
    clearBtn.addEventListener('click', function() {
        rawTranscriptInput.value = '';
        parsedDataOutput.value = '';
        rawTranscriptInput.focus();
        showStatus('Cleared!', 'success');
    });

    // Utility function to show status messages
    function showStatus(message, type) {
        statusMessage.textContent = message;
        statusMessage.className = `status-message ${type} show`;

        setTimeout(() => {
            statusMessage.classList.remove('show');
        }, 3000);
    }
});


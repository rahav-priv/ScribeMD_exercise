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
            displayError('❌ ERROR: Please enter some text');
            return;
        }

        submitBtn.disabled = true;
        submitBtn.textContent = 'Processing...';
        parsedDataOutput.value = '⏳ Processing...';

        try {
            const response = await fetch('/api/parse', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ transcript: transcript })
            });

            const result = await response.json();

            if (!response.ok) {
                throw new Error(result.error || `Server error: ${response.status}`);
            }

            if (result.success && result.data) {
                // Display the parsed data with proper formatting
                parsedDataOutput.value = JSON.stringify(result.data, null, 2);
                showStatus('✅ Transcript analyzed successfully!', 'success');
            } else {
                throw new Error(result.error || 'Unknown error parsing transcript');
            }
        } catch (error) {
            console.error('Error:', error);
            displayError(`❌ ERROR: ${error.message}`);
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
        showStatus('🗑️ Cleared!', 'success');
    });

    // Display error in the textarea (not popup)
    function displayError(errorMessage) {
        parsedDataOutput.value = errorMessage;
    }

    // Utility function to show temporary status messages
    function showStatus(message, type) {
        statusMessage.textContent = message;
        statusMessage.className = `status-message ${type} show`;

        setTimeout(() => {
            statusMessage.classList.remove('show');
        }, 3000);
    }
});


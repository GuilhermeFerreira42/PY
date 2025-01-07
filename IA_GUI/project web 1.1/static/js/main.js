document.addEventListener('DOMContentLoaded', function() {
    const videoUrlInput = document.getElementById('video-url');
    const pasteButton = document.getElementById('paste-button');
    const processButton = document.getElementById('process-button');
    const clearButton = document.getElementById('clear-button');
    const copyButton = document.getElementById('copy-button');
    const summarizeButton = document.getElementById('summarize-button');
    const originalText = document.getElementById('original-text');
    const summaryText = document.getElementById('summary-text');
    const progressBar = document.getElementById('progress-bar');

    // Paste button handler
    pasteButton.addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            videoUrlInput.value = text;
        } catch (err) {
            console.error('Failed to read clipboard:', err);
        }
    });

    // Process button handler
    processButton.addEventListener('click', async () => {
        const url = videoUrlInput.value.trim();
        if (!url) {
            alert('Please enter a YouTube URL');
            return;
        }

        progressBar.classList.remove('d-none');
        try {
            const response = await fetch('/api/process-video', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ url }),
            });

            const data = await response.json();
            if (response.ok) {
                originalText.value = data.subtitles;
                updateWordCount();
            } else {
                alert(data.error || 'Error processing video');
            }
        } catch (error) {
            alert('Error processing video');
        } finally {
            progressBar.classList.add('d-none');
        }
    });

    // Clear button handler
    clearButton.addEventListener('click', () => {
        videoUrlInput.value = '';
        originalText.value = '';
        summaryText.value = '';
        updateWordCount();
    });

    // Copy button handler
    copyButton.addEventListener('click', async () => {
        const textToCopy = originalText.value;
        if (textToCopy) {
            try {
                await navigator.clipboard.writeText(textToCopy);
                alert('Text copied successfully!');
            } catch (err) {
                console.error('Failed to copy text:', err);
            }
        }
    });

    // Word count function
    function updateWordCount() {
        const originalWords = originalText.value.trim().split(/\s+/).length;
        const summaryWords = summaryText.value.trim().split(/\s+/).length;
        
        document.getElementById('original-word-count').textContent = `Palavras: ${originalWords}`;
        document.getElementById('summary-word-count').textContent = `Palavras: ${summaryWords}`;
    }

    // Add input listeners for word count updates
    originalText.addEventListener('input', updateWordCount);
    summaryText.addEventListener('input', updateWordCount);
});
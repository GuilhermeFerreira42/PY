document.getElementById('youtube-form').addEventListener('submit', function(event) {
    event.preventDefault();
    const videoUrl = document.getElementById('video-url').value;

    fetch('/youtube/summarize', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ video_url: videoUrl })
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('transcription').innerText = "Transcrição: " + data.transcription; // Exiba a transcrição
        document.getElementById('summary').innerText = "Resumo: " + data.summary; // Exiba o resumo
    })
    .catch(error => {
        console.error('Erro:', error);
    });
});
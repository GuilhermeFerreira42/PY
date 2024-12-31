document.addEventListener('DOMContentLoaded', function() {
    const videoUrl = document.getElementById('videoUrl');
    const processedText = document.getElementById('processedText');
    const summaryText = document.getElementById('summaryText');
    const progressBar = document.getElementById('progressBar');
    const wordCount = document.getElementById('wordCount');
    const summaryWordCount = document.getElementById('summaryWordCount');
    const sidebar = document.getElementById('sidebar');
    const summarizeButton = document.getElementById('summarizeButton');
    const summarizeLoader = document.getElementById('summarizeLoader');
    let currentVideoName = '';

    // Botões
    document.getElementById('toggleSidebar').addEventListener('click', () => {
        sidebar.classList.toggle('hidden');
    });

    document.getElementById('pasteButton').addEventListener('click', async () => {
        try {
            const text = await navigator.clipboard.readText();
            videoUrl.value = text;
        } catch (err) {
            alert('Erro ao colar texto: ' + err);
        }
    });

    document.getElementById('processButton').addEventListener('click', async () => {
        const url = videoUrl.value.trim();
        if (!url) {
            alert('Por favor, insira uma URL do vídeo.');
            return;
        }

        progressBar.style.width = '10%';
        
        try {
            const response = await fetch('/process', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `url=${encodeURIComponent(url)}`
            });

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            progressBar.style.width = '100%';
            processedText.value = data.content;
            wordCount.textContent = data.word_count;
            currentVideoName = data.video_name;

            // Adicionar ao histórico se não existir
            const historyList = document.getElementById('historyList');
            const existingItem = Array.from(historyList.children)
                .find(li => li.textContent.trim() === currentVideoName);

            if (!existingItem) {
                const li = document.createElement('li');
                li.textContent = currentVideoName;
                li.dataset.url = url;
                li.dataset.processedText = data.content;
                historyList.appendChild(li);
            }
        } catch (error) {
            alert('Erro ao processar vídeo: ' + error.message);
        } finally {
            setTimeout(() => {
                progressBar.style.width = '0%';
            }, 1000);
        }
    });

    document.getElementById('clearButton').addEventListener('click', () => {
        videoUrl.value = '';
        processedText.value = '';
        summaryText.value = '';
        wordCount.textContent = '0';
        summaryWordCount.textContent = '0';
        progressBar.style.width = '0%';
    });

    document.getElementById('copyButton').addEventListener('click', async () => {
        const text = processedText.value;
        if (!text) {
            alert('Nada para copiar.');
            return;
        }

        try {
            await navigator.clipboard.writeText(text);
            alert('Texto copiado com sucesso!');
        } catch (err) {
            alert('Erro ao copiar texto: ' + err);
        }
    });

    document.getElementById('summarizeButton').addEventListener('click', async () => {
        const text = processedText.value;
        const url = videoUrl.value;
        if (!text) {
            alert('Não há texto para resumir.');
            return;
        }

        // Mostrar loader
        summarizeLoader.classList.remove('hidden');
        summarizeButton.disabled = true;

        try {
            const response = await fetch('/summarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: `text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}&video_name=${encodeURIComponent(currentVideoName)}`
            });

            const data = await response.json();
            
            if (data.error) {
                throw new Error(data.error);
            }

            summaryText.value = data.summary;
            summaryWordCount.textContent = data.word_count;

            // Atualizar histórico visualmente
            const historyList = document.getElementById('historyList');
            const existingItem = Array.from(historyList.children)
                .find(li => li.textContent.trim() === currentVideoName);

            if (existingItem) {
                existingItem.dataset.url = url;
                existingItem.dataset.processedText = text;
                existingItem.dataset.summary = data.summary;
            }

        } catch (error) {
            alert('Erro ao gerar resumo: ' + error.message);
        } finally {
            // Esconder loader
            summarizeLoader.classList.add('hidden');
            summarizeButton.disabled = false;
        }
    });

    // Histórico
    document.getElementById('historyList').addEventListener('click', (e) => {
        if (e.target.tagName === 'LI') {
            videoUrl.value = e.target.dataset.url || '';
            processedText.value = e.target.dataset.processedText || '';
            summaryText.value = e.target.dataset.summary || '';
            
            // Atualizar contadores de palavras
            wordCount.textContent = (e.target.dataset.processedText || '').split(/\s+/).length;
            summaryWordCount.textContent = (e.target.dataset.summary || '').split(/\s+/).length;
        }
    });
});
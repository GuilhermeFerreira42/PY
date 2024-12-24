import requests
import json
import os

class ChatIA:
    def __init__(self):
        self.api_url = "http://localhost:11434/v1/chat/completions"
        self.model_name = "gemma2:2b"
        self.history_file = "história do YouTube/histórico.json"

    def generate_summary(self, text):
        payload = {
            "model": self.model_name,
            "messages": [
                {"role": "system", "content": "Fale Pt-BR. Faça um resumo do texto abaixo de forma coerente e concisa, sem adicionar informações desnecessárias ou distorcer a mensagem principal."},
                {"role": "user", "content": text}
            ]
        }
        headers = {"Content-Type": "application/json"}
        
        try:
            response = requests.post(self.api_url, headers=headers, data=json.dumps(payload))
            response.raise_for_status()
            result = response.json()
            ai_response = result.get("choices", [{}])[0].get("message", {}).get("content", None)
            if ai_response is None:
                raise ValueError("A resposta da IA é None.")
            return ai_response
        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP: {http_err}")
            return None
        except Exception as err:
            print(f"Erro: {err}")
            return None
          
    def save_summary(self, video_name, video_url, subtitles_path, summary):
        """Salva todas as informações do vídeo, incluindo o resumo, no arquivo JSON associado ao vídeo."""
        if not os.path.exists("história do YouTube"):
            os.makedirs("história do YouTube")

        history = []
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as file:
                history = json.load(file)

        # Atualiza ou adiciona o vídeo no histórico
        for video in history:
            if video['name'] == video_name:
                video['url'] = video_url  # Atualiza a URL
                video['subtitles'] = subtitles_path  # Atualiza o caminho das legendas
                video['summary'] = summary  # Adiciona ou atualiza o resumo
                break
        else:
            # Se o vídeo não estiver no histórico, adiciona uma nova entrada
            history.append({
                "name": video_name,
                "url": video_url,
                "subtitles": subtitles_path,
                "summary": summary  # Adiciona o resumo
            })

        with open(self.history_file, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=4)  

    def load_summary(self, video_name):
        """Carrega todas as informações do arquivo JSON associado ao vídeo."""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as file:
                history = json.load(file)
                for video in history:
                    if video['name'] == video_name:
                        return video  # Retorna todas as informações do vídeo
        return None            

    def LoadVideo(self, video_url, subtitles_path):
        """Carrega a URL e as legendas do vídeo selecionado."""
        self.url_text.SetValue(video_url)
        if os.path.exists(subtitles_path):
            with open(subtitles_path, 'r', encoding='utf-8') as subtitle_file:
                content = subtitle_file.read()
                self.text_ctrl.SetValue(content)
                word_count = len(content.split())
                self.word_count_label.SetLabel(f"Palavras: {word_count}")

        # Carregar todas as informações do vídeo
        video_name = self.GetVideoNameFromURL(video_url)
        video_info = self.chat_ia.load_summary(video_name)
        if video_info:
            self.summary_ctrl.SetValue(video_info['summary'])  # Exibir o resumo na caixa de texto de resumo
            # Você pode também exibir a URL e o caminho das legendas, se necessário
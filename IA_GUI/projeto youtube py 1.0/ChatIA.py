import requests
import json
from VideoHistory import VideoHistory  # Certifique-se de que a classe VideoHistory está importada corretamente

class ChatIA:
    def __init__(self):
        self.api_url = "http://localhost:11434/v1/chat/completions"
        self.model_name = "gemma2:2b"
        self.history = VideoHistory()  # Instancia a nova classe VideoHistory

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
        self.history.save_history(video_name, video_url, subtitles_path, summary)

    def load_summary(self, video_name):
        """Carrega todas as informações do arquivo JSON associado ao vídeo."""
        history = self.history.load_history()
        for video in history:
            if video['name'] == video_name:
                return video  # Retorna todas as informações do vídeo
        return None
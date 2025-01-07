import requests
import json
from utils.video_history import VideoHistory

class ChatIA:
    def __init__(self):
        self.api_url = "http://localhost:11434/v1/chat/completions"
        self.model_name = "gemma2:2b"
        self.history = VideoHistory()

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
        except Exception as e:
            print(f"Erro ao gerar resumo: {e}")
            return None

    def save_summary(self, video_name, video_url, subtitles_path, summary, processed_text=None):
        self.history.save_history(video_name, video_url, subtitles_path, summary, processed_text)
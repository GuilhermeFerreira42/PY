import requests
import json
import os

class VideoHistory:
    def __init__(self, history_file="história do YouTube/histórico.json"):
        self.history_file = history_file
        if not os.path.exists("história do YouTube"):
            os.makedirs("história do YouTube")

    def load_history(self):
        """Carrega o histórico de vídeos do arquivo JSON."""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []

    def save_history(self, video_name, video_url, subtitles_path, summary=None, transcription=None):
        """Salva ou atualiza as informações do vídeo no arquivo JSON."""
        history = self.load_history()

        # Atualiza ou adiciona o vídeo no histórico
        for video in history:
            if video['name'] == video_name:
                video['url'] = video_url  # Atualiza a URL
                video['subtitles'] = subtitles_path  # Atualiza o caminho das legendas
                if summary:
                    video['summary'] = summary  # Adiciona ou atualiza o resumo
                if transcription:
                    video['transcription'] = transcription  # Adiciona ou atualiza a transcrição
                break
        else:
            # Se o vídeo não estiver no histórico, adiciona uma nova entrada
            history.append({
                "name": video_name,
                "url": video_url,
                "subtitles": subtitles_path,
                "summary": summary,  # Adiciona o resumo se fornecido
                "transcription": transcription  # Adiciona a transcrição se fornecida
            })

        with open(self.history_file, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
            
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

# O restante do código permanece inalterado
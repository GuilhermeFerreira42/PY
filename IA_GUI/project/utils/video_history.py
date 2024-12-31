import json
import os

class VideoHistory:
    def __init__(self):
        self.history_dir = "história do YouTube"
        self.history_file = os.path.join(self.history_dir, "histórico.json")
        os.makedirs(self.history_dir, exist_ok=True)

    def load_history(self):
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as file:
                return json.load(file)
        return []

    def save_history(self, video_name, video_url, subtitles_path, summary=None, processed_text=None):
        history = self.load_history()
        
        # Procura por entrada existente
        for video in history:
            if video['name'] == video_name:
                video.update({
                    'url': video_url,
                    'subtitles': subtitles_path,
                    'summary': summary,
                    'processed_text': processed_text
                })
                break
        else:
            # Adiciona nova entrada se não existir
            history.append({
                'name': video_name,
                'url': video_url,
                'subtitles': subtitles_path,
                'summary': summary,
                'processed_text': processed_text
            })

        # Salva o histórico atualizado
        with open(self.history_file, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
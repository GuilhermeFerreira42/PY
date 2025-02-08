import yt_dlp
import re
import os
from pathlib import Path

class SubtitleService:
    def __init__(self):
        # Criar diretório para legendas se não existir
        self.subtitles_dir = Path("subtitles")
        self.subtitles_dir.mkdir(exist_ok=True)
        
        self.ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['pt', 'pt-br'],
            'skip_download': True,
            'quiet': False,
            'outtmpl': str(self.subtitles_dir / '%(id)s.%(ext)s')
        }

    def process_video(self, video_url):
        """Process video URL and return subtitles"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Extrair informações do vídeo
                info = ydl.extract_info(video_url, download=False)
                video_id = info['id']
                
                # Verificar se há legendas disponíveis
                if not info.get('subtitles') and not info.get('automatic_captions'):
                    raise Exception("No Portuguese subtitles available")
                
                # Download e processamento das legendas
                subtitles = self._download_and_clean_subtitles(video_url, video_id)
                return subtitles
                
        except Exception as e:
            raise Exception(f"Error processing video: {str(e)}")
    
    def _download_and_clean_subtitles(self, video_url, video_id):
        """Download and clean subtitles"""
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Download das legendas
                ydl.download([video_url])
                
                # Procurar pelo arquivo de legendas
                subtitle_file = None
                for ext in ['.pt.vtt', '.pt-BR.vtt']:
                    possible_file = self.subtitles_dir / f"{video_id}{ext}"
                    if possible_file.exists():
                        subtitle_file = possible_file
                        break
                
                if not subtitle_file:
                    raise Exception("Could not find subtitle file after download")
                
                # Ler e limpar o conteúdo das legendas
                with open(subtitle_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Limpar formatação VTT
                content = re.sub(r'WEBVTT\n\n', '', content)
                content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\n', '', content)
                content = re.sub(r'<[^>]+>', '', content)  # Remove tags HTML
                content = re.sub(r'\n\n+', '\n\n', content)  # Remove linhas extras
                
                # Limpar o arquivo após processamento
                os.remove(subtitle_file)
                
                return content.strip()
                
        except Exception as e:
            raise Exception(f"Error processing subtitles: {str(e)}")
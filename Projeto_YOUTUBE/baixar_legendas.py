import yt_dlp
import re
import json
import os

class SubtitleProcessor:
    def __init__(self):
        pass

    def download_subtitles(self, video_url):
        ydl_opts = {
            'writesubtitles': True,
            'writeautomaticsub': True,
            'subtitleslangs': ['pt', 'pt-br'],
            'skip_download': True,
            'quiet': False
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                result = ydl.extract_info(video_url, download=False)
                subtitle_file = None

                if 'requested_subtitles' in result:
                    subtitle_file = ydl.prepare_filename(result)
                    subtitle_file = subtitle_file.rsplit('.', 1)[0] + '.pt.vtt'
                    ydl.download([video_url])
                    print(f"Legendas baixadas para: {subtitle_file}")
                else:
                    print("Nenhuma legenda em português disponível.")
                return subtitle_file
            except Exception as e:
                print(f"Erro ao baixar legendas: {e}")
                return None

    def clean_and_consolidate_subtitles(self, subtitle_file, video_name):
        try:
            with open(subtitle_file, 'r', encoding='utf-8') as file:
                content = file.read()

            content = re.sub(r'(WEBVTT|Kind:.*|Language:.*)', '', content)
            content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> .*?\n', '', content)
            content = re.sub(r'<.*?>', '', content)
            content = re.sub(r'&nbsp;', ' ', content)
            content = re.sub(r'align:start position:\d+%|\n+', '\n', content).strip()

            lines = content.splitlines()
            unique_lines = list(dict.fromkeys(line.strip() for line in lines if line.strip()))

            consolidated_text = '\n'.join(unique_lines).strip()

            # Salvar as legendas em um arquivo JSON
            json_filename = f"{video_name}_subtitles.json"
            with open(json_filename, 'w', encoding='utf-8') as json_file:
                json.dump({"subtitles": unique_lines}, json_file, ensure_ascii=False, indent=4)

            print(f"Texto consolidado salvo em: {json_filename}")
            return json_filename
        except Exception as e:
            print(f"Erro ao limpar e consolidar as legendas: {e}")
            return None

if __name__ == "__main__":
    video_url = input("Digite a URL do vídeo do YouTube: ")
    processor = SubtitleProcessor()
    subtitle_file = processor.download_subtitles(video_url)
    if subtitle_file:
        video_name = os.path.basename(subtitle_file).replace('.pt.vtt', '')
        processor.clean_and_consolidate_subtitles(subtitle_file, video_name)

import yt_dlp
import re
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

    def clean_and_consolidate_subtitles(self, subtitle_file):
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

            cleaned_filename = subtitle_file.replace('.vtt', '_consolidated.txt')
            with open(cleaned_filename, 'w', encoding='utf-8') as file:
                file.write(consolidated_text)

            print(f"Texto consolidado salvo em: {cleaned_filename}")
            return cleaned_filename
        except Exception as e:
            print(f"Erro ao limpar e consolidar as legendas: {e}")
            return None
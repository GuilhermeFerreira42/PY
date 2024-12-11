import yt_dlp
import re
import os

def download_subtitles(video_url):
    """
    Função para baixar as legendas do vídeo no YouTube em português (pt-br).
    """
    ydl_opts = {
        'writesubtitles': True,         # Habilita o download de legendas
        'writeautomaticsub': True,      # Habilita o download de legendas automáticas
        'subtitleslangs': ['pt', 'pt-br'], # Idioma das legendas
        'skip_download': True,          # Pula o download do vídeo
        'quiet': False                  # Exibe mensagens de log para depuração
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

def clean_and_consolidate_subtitles(subtitle_file):
    """
    Função para consolidar legendas em um texto contínuo sem repetições.
    """
    try:
        with open(subtitle_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove linhas de tempo e metadados como "WEBVTT" ou "Kind: captions"
        content = re.sub(r'(WEBVTT|Kind:.*|Language:.*)', '', content)
        content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> .*?\n', '', content)

        # Remove tags detalhadas (<00:00:00.030><c>) e espaços extras
        content = re.sub(r'<.*?>', '', content)
        content = re.sub(r'align:start position:\d+%|\n+', '\n', content).strip()

        # Processa as linhas e elimina duplicatas (não apenas consecutivas)
        lines = content.splitlines()
        unique_lines = list(dict.fromkeys(line.strip() for line in lines if line.strip()))

        # Junta as linhas em um texto contínuo com quebras de linha apropriadas
        consolidated_text = '\n'.join(unique_lines).strip()

        # Salva o texto consolidado
        cleaned_filename = subtitle_file.replace('.vtt', '_consolidated.txt')
        with open(cleaned_filename, 'w', encoding='utf-8') as file:
            file.write(consolidated_text)

        print(f"Texto consolidado salvo em: {cleaned_filename}")
        return cleaned_filename
    except Exception as e:
        print(f"Erro ao limpar e consolidar as legendas: {e}")
        return None


def main():
    print("Bem-vindo ao Programa de Transcrição de Vídeos do YouTube!")
    video_url = input("Por favor, insira o link do vídeo do YouTube: ")

    # Baixa as legendas
    subtitle_file = download_subtitles(video_url)
    
    if subtitle_file:
        # Consolida o texto das legendas
        consolidated_file = clean_and_consolidate_subtitles(subtitle_file)
        if consolidated_file:
            print(f"As legendas foram processadas e salvas em: {consolidated_file}")
        else:
            print("Erro ao consolidar as legendas.")
    else:
        print("Não foi possível obter as legendas.")

if __name__ == "__main__":
    main()


# https://www.youtube.com/watch?v=jNjKMuQASio

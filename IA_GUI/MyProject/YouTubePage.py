from flask import Blueprint, render_template, request, jsonify
from Utils.YouTubeUtils import download_subtitles, clean_and_consolidate_subtitles

youtube_page = Blueprint('youtube_page', __name__)

@youtube_page.route('/')
def youtube():
    return render_template('youtube.html')  # Crie este arquivo HTML

@youtube_page.route('/summarize', methods=['POST'])
def summarize_youtube():
    video_url = request.json.get('video_url')
    subtitle_file = download_subtitles(video_url)

    if subtitle_file:
        consolidated_file = clean_and_consolidate_subtitles(subtitle_file)
        if consolidated_file:
            with open(consolidated_file, 'r', encoding='utf-8') as file:
                content = file.read()
            return jsonify({'transcription': content, 'summary': "Resumo ainda não implementado."})
        else:
            return jsonify({'error': 'Erro ao consolidar as legendas.'}), 500
    else:
        return jsonify({'error': 'Não foi possível obter as legendas.'}), 500
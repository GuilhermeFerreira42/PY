from flask import Flask, render_template, request, jsonify
import json
import os
from utils.subtitle_processor import SubtitleProcessor
from utils.chat_ia import ChatIA
from utils.video_history import VideoHistory

app = Flask(__name__)
subtitle_processor = SubtitleProcessor()
chat_ia = ChatIA()
video_history = VideoHistory()

@app.route('/')
def index():
    history = video_history.load_history()
    return render_template('index.html', history=history)

@app.route('/process', methods=['POST'])
def process_video():
    video_url = request.form.get('url')
    if not video_url:
        return jsonify({'error': 'URL não fornecida'}), 400
    
    try:
        subtitle_file = subtitle_processor.download_subtitles(video_url)
        if not subtitle_file:
            return jsonify({'error': 'Não foi possível baixar as legendas'}), 400
        
        video_name = os.path.basename(subtitle_file).replace('.pt.vtt', '')
        consolidated_file = subtitle_processor.clean_and_consolidate_subtitles(subtitle_file, video_name)
        
        with open(consolidated_file, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return jsonify({
            'success': True,
            'content': content,
            'word_count': len(content.split()),
            'video_name': video_name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/summarize', methods=['POST'])
def summarize_text():
    text = request.form.get('text')
    video_url = request.form.get('url')
    video_name = request.form.get('video_name')
    
    if not text:
        return jsonify({'error': 'Texto não fornecido'}), 400
    
    try:
        summary = chat_ia.generate_summary(text)
        if summary:
            chat_ia.save_summary(video_name, video_url, 
                                  f"história do YouTube/{video_name}_subtitles.json", 
                                  summary, 
                                  processed_text=text)
            return jsonify({
                'success': True,
                'summary': summary,
                'word_count': len(summary.split())
            })
        return jsonify({'error': 'Não foi possível gerar o resumo'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
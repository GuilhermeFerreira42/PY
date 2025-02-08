from flask import Blueprint, request, jsonify
from services.subtitle_service import SubtitleService

youtube_bp = Blueprint('youtube', __name__)
subtitle_service = SubtitleService()

@youtube_bp.route('/api/process-video', methods=['POST'])
def process_video():
    data = request.json
    video_url = data.get('url')
    
    if not video_url:
        return jsonify({'error': 'URL is required'}), 400
        
    try:
        subtitles = subtitle_service.process_video(video_url)
        return jsonify({'subtitles': subtitles})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
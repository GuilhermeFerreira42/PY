from flask import Flask, render_template
from YouTubePage import youtube_page
from OfflineVideoPage import offline_video_page
from PDFPage import pdf_page
from ChatHandler import chat_handler

app = Flask(__name__)

# Registrando as rotas para cada aba
app.register_blueprint(youtube_page, url_prefix='/youtube')
app.register_blueprint(offline_video_page, url_prefix='/offline')
app.register_blueprint(pdf_page, url_prefix='/pdf')
app.register_blueprint(chat_handler, url_prefix='/chat')

@app.route('/')
def index():
    return render_template('index.html')  # Página inicial

if __name__ == '__main__':
    app.run(debug=True)
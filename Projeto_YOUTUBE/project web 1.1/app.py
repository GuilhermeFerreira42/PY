from flask import Flask, render_template
from routes.youtube_routes import youtube_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

# Register blueprints
app.register_blueprint(youtube_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
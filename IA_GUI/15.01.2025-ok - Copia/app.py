from flask import Flask, render_template, request, jsonify
import json
import requests
from datetime import datetime

app = Flask(__name__, static_url_path='/static')

# Configuração da API local
API_URL = "http://localhost:11434/v1/chat/completions"
DEFAULT_MODEL = "gemma2:2b"

# Armazenamento temporário de conversas
conversas = []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/enviar_mensagem', methods=['POST'])
def enviar_mensagem():
    try:
        dados = request.get_json()
        mensagem = dados.get('mensagem', '')
        modelo = dados.get('modelo', DEFAULT_MODEL)
        
        # Adicionar instrução para responder em português
        mensagem_sistema = "Por favor, responda sempre em português do Brasil de forma clara e objetiva."
        mensagem_completa = f"{mensagem_sistema}\n\nUsuário: {mensagem}"
        
        # Preparar payload para a API local
        payload = {
            "model": modelo,
            "messages": [
                {"role": "system", "content": mensagem_sistema},
                {"role": "user", "content": mensagem}
            ]
        }
        
        # Fazer requisição para a API local
        response = requests.post(API_URL, json=payload)
        resposta_ia = response.json()
        
        # Extrair a resposta da IA
        resposta = resposta_ia.get('choices', [{}])[0].get('message', {}).get('content', 'Erro ao processar resposta')
        
        # Armazenar conversa
        conversas.append({
            'id': len(conversas) + 1,
            'titulo': f"Conversa {len(conversas) + 1}",
            'mensagens': [
                {'tipo': 'usuario', 'conteudo': mensagem, 'timestamp': datetime.now().strftime("%H:%M")},
                {'tipo': 'assistente', 'conteudo': resposta, 'timestamp': datetime.now().strftime("%H:%M")}
            ]
        })
        
        return jsonify({
            'resposta': resposta,
            'conversa_id': len(conversas)
        })
        
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

@app.route('/conversas', methods=['GET'])
def listar_conversas():
    return jsonify(conversas)

@app.route('/conversa/<int:id>', methods=['GET'])
def obter_conversa(id):
    for conversa in conversas:
        if conversa['id'] == id:
            return jsonify(conversa)
    return jsonify({'erro': 'Conversa não encontrada'}), 404

if __name__ == '__main__':
    app.run(debug=True)
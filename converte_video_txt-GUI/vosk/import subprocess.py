import subprocess
import json
import os

def extract_audio(video_path, audio_path):
    command = [
        'ffmpeg',
        '-i', video_path,
        '-q:a', '0',
        '-map', 'a',
        audio_path
    ]
    print(f"Executando comando: {' '.join(command)}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print("Erro ao extrair áudio:", result.stderr)
    else:
        print("Áudio extraído com sucesso!")

def recognize_speech(audio_path, model_path, output_text_path):
    command = [
        'python', '-m', 'vosk', 'transcribe', 
        '--model', model_path, 
        '--audio', audio_path
    ]
    
    print(f"Executando comando: {' '.join(command)}")
    
    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as process:
        with open(output_text_path, 'w') as file:
            for line in process.stdout:
                print(line.strip())  # Para depuração
                try:
                    result = json.loads(line)
                    if 'text' in result:
                        file.write(result['text'] + '\n')
                except json.JSONDecodeError:
                    continue  # Ignorar linhas que não podem ser decodificadas

def main():
    video_path = 'C:/Users/Usuario/Downloads/Meme.mp4'
    audio_path = 'C:/Users/Usuario/audio_extraido.wav'
    model_path = 'C:/Users/Usuario/Desktop/model'  # Caminho para o diretório do modelo
    output_text_path = 'C:/Users/Usuario/texto_extraido.txt'

    extract_audio(video_path, audio_path)
    recognize_speech(audio_path, model_path, output_text_path)

if __name__ == "__main__":
    main()

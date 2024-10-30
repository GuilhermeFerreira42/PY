import os
import subprocess
import vosk
import json
import wave
from tkinter import Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


def convert_audio_to_wav(video_path):
    # Define o caminho do arquivo de áudio temporário na mesma pasta do vídeo
    dir_path = os.path.dirname(video_path)
    audio_path = os.path.join(dir_path, 'temp_audio.wav')

    # Converte o áudio para 16000 Hz e salva como WAV, sobrescrevendo se o arquivo já existir
    command = [
        'ffmpeg',
        '-y',  # Adiciona esta linha para sobrescrever o arquivo existente sem perguntar
        '-i', video_path,
        '-ar', '16000',
        '-ac', '1',
        audio_path
    ]
    subprocess.run(command, check=True)

    return audio_path


def transcribe_audio(audio_path, model_path):
    # Carrega o modelo de reconhecimento de fala
    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)
    
    with wave.open(audio_path, 'rb') as wf:
        results = []
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                results.append(result)
        final_result = recognizer.FinalResult()
        results.append(final_result)

    return '\n'.join(results)


def main():
    # Configuração inicial
    Tk().withdraw()  # Esconde a janela principal do Tkinter
    
    # Solicita ao usuário o arquivo de vídeo
    video_path = askopenfilename(title='Selecione o arquivo de vídeo', filetypes=[('Arquivos de vídeo', '*.mp4')])
    if not video_path:
        print("Nenhum arquivo de vídeo selecionado. Saindo...")
        return

    # Converte o áudio do vídeo para 16000 Hz e salva como WAV
    audio_path = convert_audio_to_wav(video_path)

    # Define o caminho absoluto do modelo Vosk
    model_path = 'C:/Users/Usuario/Desktop/model'

    # Transcreve o áudio
    transcript = transcribe_audio(audio_path, model_path)

    # Solicita ao usuário o local para salvar o arquivo de texto
    txt_path = asksaveasfilename(title='Salvar transcrição', defaultextension='.txt', filetypes=[('Arquivo de Texto', '*.txt')])
    if txt_path:
        with open(txt_path, 'w') as f:
            f.write(transcript)
    
    # Remove o arquivo de áudio temporário
    os.remove(audio_path)

if __name__ == "__main__":
    main()

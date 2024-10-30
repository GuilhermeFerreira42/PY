import subprocess
import tkinter as tk
from tkinter import filedialog

def extract_and_convert_audio(video_path, output_audio_path):
    # Extrair o áudio do vídeo
    temp_audio_path = "temp_audio.wav"
    subprocess.run(['ffmpeg', '-i', video_path, '-q:a', '0', '-map', 'a', temp_audio_path])
    
    # Converter o áudio para 16000 Hz
    subprocess.run(['ffmpeg', '-i', temp_audio_path, '-ar', '16000', output_audio_path])
    
    # Remover o arquivo temporário
    subprocess.run(['rm', temp_audio_path])

def select_file():
    # Selecionar o arquivo de vídeo
    video_path = filedialog.askopenfilename(title="Selecione o vídeo", filetypes=[("Arquivos de vídeo", "*.mp4")])
    if video_path:
        # Selecionar o local de salvamento do áudio
        output_audio_path = filedialog.asksaveasfilename(title="Salvar áudio como", defaultextension=".wav", filetypes=[("Arquivos de áudio", "*.wav")])
        if output_audio_path:
            extract_and_convert_audio(video_path, output_audio_path)
            print("Processo concluído com sucesso!")

# Configurar a interface gráfica
root = tk.Tk()
root.withdraw()  # Esconder a janela principal
select_file()

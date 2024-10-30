from vosk import Model, KaldiRecognizer
import wave
import json

# Caminhos dos arquivos
audio_path = "C:/Users/Usuario/Desktop/Entendi.wav"  # Use o áudio convertido
model_path = "C:/Users/Usuario/Desktop/model"
output_text_path = "C:/Users/Usuario/texto_extraido.txt"

# Carregar o modelo
model = Model(model_path)
rec = KaldiRecognizer(model, 16000)  # 16000 é a taxa de amostragem comum

# Abrir o arquivo de áudio
wf = wave.open(audio_path, "rb")

# Verificar a taxa de amostragem
if wf.getframerate() != 16000:
    raise ValueError("Taxa de amostragem do áudio deve ser 16000 Hz")

# Processar o áudio
text = ""
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        result = rec.Result()
        text += json.loads(result)["text"] + " "

# Adicionar o texto final
text += json.loads(rec.FinalResult())["text"]

# Salvar o texto em um arquivo
with open(output_text_path, "w") as f:
    f.write(text)

print("Reconhecimento de fala concluído. Texto salvo em", output_text_path)

import re
import tkinter as tk
from tkinter import scrolledtext, ttk

def remover_formatacao(texto):
    # Regex para emojis
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"
                               u"\U0001F300-\U0001F5FF"
                               u"\U0001F680-\U0001F6FF"
                               u"\U0001F1E0-\U0001F1FF"
                               u"\U00002500-\U00002BEF"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    
    # Remove caracteres de formatação
    texto_sem_formatacao = re.sub(r'[\*\_\`\~\>\#\-\+\[\]\(\)\{\}\\\|]', '', texto)
    # Remove emojis
    texto_sem_emoji = emoji_pattern.sub('', texto_sem_formatacao)
    
    # Processar cada linha para preservar espaçamento
    linhas = texto_sem_emoji.splitlines()
    linhas_limpas = []
    for linha in linhas:
        # Capturar espaços iniciais e finais
        leading = re.match(r'^(\s*)', linha).group(1)
        trailing = re.search(r'(\s*)$', linha).group(1)
        conteudo = linha[len(leading):-len(trailing)] if trailing else linha[len(leading):]
        # Substituir múltiplos espaços no conteúdo
        conteudo_limpo = re.sub(r'\s+', ' ', conteudo)
        linha_limpa = leading + conteudo_limpo + trailing
        linhas_limpas.append(linha_limpa)
    
    # Juntar linhas preservando quebras
    texto_limpo = '\n'.join(linhas_limpas)
    return texto_limpo

def processar_texto():
    texto_entrada = entrada_texto.get("1.0", tk.END)
    texto_processado = remover_formatacao(texto_entrada)
    saida_texto.delete("1.0", tk.END)
    saida_texto.insert(tk.INSERT, texto_processado)

# Configuração da janela principal
janela = tk.Tk()
janela.title("Removedor de Formatação")
janela.geometry("600x400")

# Frame principal
frame = ttk.Frame(janela, padding=10)
frame.pack(fill=tk.BOTH, expand=True)

# Texto de entrada
ttk.Label(frame, text="Cole o texto com formatação:").pack(anchor=tk.W)
entrada_texto = scrolledtext.ScrolledText(frame, width=70, height=10)
entrada_texto.pack(pady=5)

# Botão de processamento
btn_processar = ttk.Button(frame, text="Remover Formatação", command=processar_texto)
btn_processar.pack(pady=5)

# Texto de saída
ttk.Label(frame, text="Texto limpo:").pack(anchor=tk.W)
saida_texto = scrolledtext.ScrolledText(frame, width=70, height=10)
saida_texto.pack(pady=5)

# Executar a aplicação
janela.mainloop()
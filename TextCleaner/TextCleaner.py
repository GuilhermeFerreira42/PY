import tkinter as tk
from tkinter import ttk

# Função para processar o texto
def processar_texto():
    caracteres_remover = entry_remover.get()
    texto = entry_texto.get("1.0", tk.END)
    texto_processado = ''.join([char for char in texto if char not in caracteres_remover])
    entry_resultado.delete("1.0", tk.END)  # Limpa o campo de resultado
    entry_resultado.insert(tk.END, texto_processado)  # Exibe o texto processado

# Funções para copiar, colar, selecionar tudo e limpar
def copiar(widget):
    widget.event_generate("<<Copy>>")

def colar(widget):
    widget.event_generate("<<Paste>>")

def selecionar_tudo(widget):
    widget.tag_add("sel", "1.0", "end")  # Adiciona a tag "sel" para selecionar visualmente
    widget.mark_set("insert", "1.0")
    widget.see("insert")
    widget.focus()

def limpar(widget):
    widget.delete("1.0", tk.END)

# Função para criar menu de contexto
def criar_menu_contexto(widget):
    menu_contexto = tk.Menu(widget, tearoff=0)
    menu_contexto.add_command(label="Copiar", command=lambda: copiar(widget))
    menu_contexto.add_command(label="Colar", command=lambda: colar(widget))
    menu_contexto.add_command(label="Selecionar Tudo", command=lambda: selecionar_tudo(widget))

    def exibir_menu(event):
        menu_contexto.tk_popup(event.x_root, event.y_root)

    widget.bind("<Button-3>", exibir_menu)

# Configuração da janela principal
root = tk.Tk()
root.title("Remover Caracteres Especiais")
root.geometry("600x650")  # Aumentando o tamanho da janela principal

# Rótulo e campo para informar os caracteres a serem removidos
label_remover = ttk.Label(root, text="Caracteres para remover:")
label_remover.pack(pady=5)
entry_remover = ttk.Entry(root, width=70)  # Aumentando a largura do campo de entrada
entry_remover.pack(pady=5)

# Adicionando menu de contexto ao campo entry_remover
criar_menu_contexto(entry_remover)

# Rótulo e campo para inserir o texto a ser processado
label_texto = ttk.Label(root, text="Insira o texto:")
label_texto.pack(pady=5)
entry_texto = tk.Text(root, height=10, width=70)  # Aumentando a altura e largura do campo de texto
entry_texto.pack(pady=5)

# Adicionando menu de contexto ao campo entry_texto
criar_menu_contexto(entry_texto)

# Botões para o campo de entrada de texto
frame_botoes_texto = ttk.Frame(root)
frame_botoes_texto.pack(pady=5)

btn_copiar_texto = ttk.Button(frame_botoes_texto, text="Copiar", command=lambda: copiar(entry_texto))
btn_copiar_texto.grid(row=0, column=0, padx=5)

btn_colar_texto = ttk.Button(frame_botoes_texto, text="Colar", command=lambda: colar(entry_texto))
btn_colar_texto.grid(row=0, column=1, padx=5)

btn_selecionar_tudo_texto = ttk.Button(frame_botoes_texto, text="Selecionar Tudo", command=lambda: selecionar_tudo(entry_texto))
btn_selecionar_tudo_texto.grid(row=0, column=2, padx=5)

btn_limpar_texto = ttk.Button(frame_botoes_texto, text="Limpar", command=lambda: limpar(entry_texto))
btn_limpar_texto.grid(row=0, column=3, padx=5)

# Botão "Processar"
botao_processar = ttk.Button(root, text="Processar", command=processar_texto)
botao_processar.pack(pady=10)

# Rótulo e campo para mostrar o texto processado
label_resultado = ttk.Label(root, text="Texto processado:")
label_resultado.pack(pady=5)
entry_resultado = tk.Text(root, height=10, width=70)  # Aumentando a altura e largura do campo de resultado
entry_resultado.pack(pady=5)

# Adicionando menu de contexto ao campo entry_resultado
criar_menu_contexto(entry_resultado)

# Botões para o campo de texto processado
frame_botoes_resultado = ttk.Frame(root)
frame_botoes_resultado.pack(pady=5)

btn_copiar_resultado = ttk.Button(frame_botoes_resultado, text="Copiar", command=lambda: copiar(entry_resultado))
btn_copiar_resultado.grid(row=0, column=0, padx=5)

btn_colar_resultado = ttk.Button(frame_botoes_resultado, text="Colar", command=lambda: colar(entry_resultado))
btn_colar_resultado.grid(row=0, column=1, padx=5)

btn_selecionar_tudo_resultado = ttk.Button(frame_botoes_resultado, text="Selecionar Tudo", command=lambda: selecionar_tudo(entry_resultado))
btn_selecionar_tudo_resultado.grid(row=0, column=2, padx=5)

btn_limpar_resultado = ttk.Button(frame_botoes_resultado, text="Limpar", command=lambda: limpar(entry_resultado))
btn_limpar_resultado.grid(row=0, column=3, padx=5)

# Iniciar o loop da interface gráfica
root.mainloop()

import tkinter as tk
from tkinter import ttk, simpledialog, messagebox
import json
import os

class LimitadorCaracteresApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Limitador de Caracteres")
        self.root.geometry("600x650")

        # Variáveis para armazenar os textos antes e depois
        self.texto_antes = ""
        self.texto_depois = ""
        self.pular_espacos = tk.BooleanVar()

        # Rótulo e campo para informar a quantidade de caracteres
        label_remover = ttk.Label(self.root, text="Quantidade de caracteres:")
        label_remover.pack(pady=5)
        self.entry_remover = ttk.Entry(self.root, width=70)
        self.entry_remover.pack(pady=5)

        # Rótulo e campo para inserir o texto a ser processado com barra de rolagem
        label_texto = ttk.Label(self.root, text="Insira o texto:")
        label_texto.pack(pady=5)
        frame_texto = ttk.Frame(self.root)
        frame_texto.pack(pady=5)
        scroll_texto = tk.Scrollbar(frame_texto)
        scroll_texto.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_texto = tk.Text(frame_texto, height=10, width=70, yscrollcommand=scroll_texto.set)
        self.entry_texto.pack(side=tk.LEFT, fill=tk.BOTH)
        scroll_texto.config(command=self.entry_texto.yview)

        # Adiciona menu de contexto nas caixas de texto
        self.add_context_menu(self.entry_texto)

        # Botões para o campo de entrada de texto
        frame_botoes_texto = ttk.Frame(self.root)
        frame_botoes_texto.pack(pady=5)
        ttk.Button(frame_botoes_texto, text="Copiar", command=lambda: self.copiar(self.entry_texto)).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes_texto, text="Colar", command=lambda: self.colar(self.entry_texto)).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes_texto, text="Selecionar Tudo", command=lambda: self.selecionar_tudo(self.entry_texto)).grid(row=0, column=2, padx=5)
        ttk.Button(frame_botoes_texto, text="Limpar", command=lambda: self.limpar(self.entry_texto)).grid(row=0, column=3, padx=5)

        # Adiciona Label para contagem de caracteres
        self.label_contagem_texto = ttk.Label(self.root, text="Caracteres: 0")
        self.label_contagem_texto.pack(pady=5)

        # Botão "Configurar Textos" e "Processar"
        frame_botoes = ttk.Frame(self.root)
        frame_botoes.pack(pady=10)

        ttk.Button(frame_botoes, text="Configurar Textos", command=self.configurar_textos).pack(side=tk.LEFT, padx=5)
        ttk.Button(frame_botoes, text="Processar", command=self.processar_texto).pack(side=tk.LEFT, padx=5)


        # Rótulo e campo para mostrar o texto processado com barra de rolagem
        label_resultado = ttk.Label(self.root, text="Texto processado:")
        label_resultado.pack(pady=5)
        frame_resultado = ttk.Frame(self.root)
        frame_resultado.pack(pady=5)
        scroll_resultado = tk.Scrollbar(frame_resultado)
        scroll_resultado.pack(side=tk.RIGHT, fill=tk.Y)
        self.entry_resultado = tk.Text(frame_resultado, height=10, width=70, yscrollcommand=scroll_resultado.set)
        self.entry_resultado.pack(side=tk.LEFT, fill=tk.BOTH)
        scroll_resultado.config(command=self.entry_resultado.yview)

        # Adiciona menu de contexto nas caixas de texto
        self.add_context_menu(self.entry_resultado)

        # Botões para o campo de texto processado
        frame_botoes_resultado = ttk.Frame(self.root)
        frame_botoes_resultado.pack(pady=5)
        ttk.Button(frame_botoes_resultado, text="Copiar", command=lambda: self.copiar(self.entry_resultado)).grid(row=0, column=0, padx=5)
        ttk.Button(frame_botoes_resultado, text="Colar", command=lambda: self.colar(self.entry_resultado)).grid(row=0, column=1, padx=5)
        ttk.Button(frame_botoes_resultado, text="Selecionar Tudo", command=lambda: self.selecionar_tudo(self.entry_resultado)).grid(row=0, column=2, padx=5)
        ttk.Button(frame_botoes_resultado, text="Limpar", command=lambda: self.limpar(self.entry_resultado)).grid(row=0, column=3, padx=5)

        # Adiciona Label para contagem de caracteres no resultado
        self.label_contagem_resultado = ttk.Label(self.root, text="Caracteres: 0")
        self.label_contagem_resultado.pack(pady=5)

        # Bind para atualizar contagem de caracteres
        self.entry_texto.bind("<<Modified>>", self.atualizar_contagem_texto)
        self.entry_resultado.bind("<<Modified>>", self.atualizar_contagem_resultado)

    # Função para contar os caracteres do resto
    def atualizar_contagem_texto(self, evento):
        # Desmarcar o estado de modificação para que o evento seja chamado novamente
        self.entry_texto.edit_modified(False)
        
        texto = self.entry_texto.get("1.0", tk.END)
        self.label_contagem_texto.config(text=f"Caracteres: {len(texto.strip())}")

    def atualizar_contagem_resultado(self, evento):
        # Desmarcar o estado de modificação para que o evento seja chamado novamente
        self.entry_resultado.edit_modified(False)
        
        texto = self.entry_resultado.get("1.0", tk.END)
        self.label_contagem_resultado.config(text=f"Caracteres: {len(texto.strip())}")


    # Função para processar o texto
    def processar_texto(self):
        try:
            limite_caracteres = int(self.entry_remover.get())
            texto = self.entry_texto.get("1.0", tk.END).strip()
            # Considera os textos "antes" e "depois", mantendo suas quebras de linha
            texto_antes = self.texto_antes.rstrip('\n')
            texto_depois = self.texto_depois.lstrip('\n')
            # Calcular quantos caracteres podem ser utilizados para o texto principal
            caracteres_antes = len(texto_antes.replace("\n", ""))
            caracteres_depois = len(texto_depois.replace("\n", ""))
            caracteres_disponiveis = limite_caracteres - (caracteres_antes + caracteres_depois)

            # Variável para armazenar o resultado final
            resultado_final = ""
            if self.pular_espacos.get():
                # Ignora espaços em excesso, mas mantém um espaço simples entre palavras
                i = 0
                while i < len(texto):
                    texto_temp = ""
                    while len(texto_temp) < caracteres_disponiveis and i < len(texto):
                        if texto[i] != ' ' or (texto_temp and texto_temp[-1] != ' '):
                            texto_temp += texto[i]
                        i += 1
                    resultado_final += texto_antes + texto_temp + texto_depois + "\n"
            else:
                texto_processado = texto[:caracteres_disponiveis]
                resultado_final = texto_antes + texto_processado + texto_depois

            self.entry_resultado.delete("1.0", tk.END)
            self.entry_resultado.insert(tk.END, resultado_final)
        except ValueError:
            self.entry_resultado.delete("1.0", tk.END)
            self.entry_resultado.insert(tk.END, "Por favor, insira um número válido.")

    # Função para configurar os textos antes e depois
    def configurar_textos(self):
        janela_config = tk.Toplevel(self.root)
        janela_config.title("Configurar Textos")
        janela_config.geometry("400x500")
        janela_config.transient(self.root)
        janela_config.grab_set()

        # Centralizar a janela
        largura_janela = 400
        altura_janela = 400
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (largura_janela // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (altura_janela // 2)
        janela_config.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

        label_antes = ttk.Label(janela_config, text="Texto antes:")
        label_antes.pack(pady=5)
        entry_antes = tk.Text(janela_config, height=5, width=50)
        entry_antes.pack(pady=5)
        entry_antes.insert("1.0", self.texto_antes)

        label_depois = ttk.Label(janela_config, text="Texto depois:")
        label_depois.pack(pady=5)
        entry_depois = tk.Text(janela_config, height=5, width=50)
        entry_depois.pack(pady=5)
        entry_depois.insert("1.0", self.texto_depois)

        # Adiciona menu de contexto nas caixas de texto
        self.add_context_menu(entry_antes)
        self.add_context_menu(entry_depois)

        check_box = ttk.Checkbutton(janela_config, text="Pular espaços", variable=self.pular_espacos)
        check_box.pack(pady=10)

        def salvar_textos():
            self.texto_antes = entry_antes.get("1.0", tk.END).rstrip() + "\n"
            self.texto_depois = entry_depois.get("1.0", tk.END).rstrip() + "\n"
            janela_config.destroy()

        botao_salvar = ttk.Button(janela_config, text="Salvar", command=salvar_textos)
        botao_salvar.pack(pady=10)

        # Botões para salvar e carregar presets
        frame_presets = ttk.Frame(janela_config)
        frame_presets.pack(pady=10)
        ttk.Button(frame_presets, text="Salvar Preset", command=lambda: self.salvar_preset(entry_antes.get("1.0", tk.END), entry_depois.get("1.0", tk.END))).grid(row=0, column=0, padx=5)
        ttk.Button(frame_presets, text="Carregar Preset", command=lambda: self.mostrar_presets(entry_antes, entry_depois)).grid(row=0, column=1, padx=5)

    def salvar_preset(self, texto_antes, texto_depois):
        if not os.path.exists("presets"):
            os.makedirs("presets")

        janela_presets = tk.Toplevel(self.root)
        janela_presets.title("Salvar Preset")
        janela_presets.geometry("400x500")
        janela_presets.transient(self.root)
        janela_presets.grab_set()

        # Centralizar a janela
        largura_janela = 300
        altura_janela = 300
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (largura_janela // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (altura_janela // 2)
        janela_presets.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

        label_presets = ttk.Label(janela_presets, text="Selecione um preset ou insira um novo nome:")
        label_presets.pack(pady=5)

        lista_presets = tk.Listbox(janela_presets)
        lista_presets.pack(pady=5, fill=tk.BOTH, expand=True)

        # Carregar os nomes dos presets na listbox
        for filename in os.listdir("presets"):
            if filename.endswith(".json"):
                lista_presets.insert(tk.END, filename[:-5])

        entry_preset_name = ttk.Entry(janela_presets, width=30)
        entry_preset_name.pack(pady=5)

        def salvar():
            preset_name = entry_preset_name.get().strip()
            if not preset_name:
                preset_name = lista_presets.get(tk.ACTIVE)

            if preset_name:
                preset_path = f"presets/{preset_name}.json"
                if os.path.exists(preset_path):
                    resposta = messagebox.askyesno("Confirmar Salvar", "Tem certeza que deseja salvar este preset? Isso substituirá o existente.")
                    if not resposta:
                        return

                preset_data = {
                    "texto_antes": texto_antes,
                    "texto_depois": texto_depois,
                    "pular_espacos": self.pular_espacos.get()
                }
                if not os.path.exists("presets"):
                    os.makedirs("presets")
                with open(preset_path, "w") as f:
                    json.dump(preset_data, f)
                janela_presets.destroy()
            else:
                messagebox.showerror("Erro", "Por favor, selecione ou insira um nome para o preset.")

        botao_salvar = ttk.Button(janela_presets, text="Salvar", command=salvar)
        botao_salvar.pack(pady=10)

    def mostrar_presets(self, entry_antes, entry_depois):
        if not os.path.exists("presets"):
            return

        # Criar uma janela para mostrar a lista de presets
        janela_presets = tk.Toplevel(self.root)
        janela_presets.title("Carregar Preset")
        janela_presets.geometry("400x500")
        janela_presets.transient(self.root)
        janela_presets.grab_set()

        # Centralizar a janela
        largura_janela = 300
        altura_janela = 300
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (largura_janela // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (altura_janela // 2)
        janela_presets.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

        label_presets = ttk.Label(janela_presets, text="Selecione um preset:")
        label_presets.pack(pady=5)

        lista_presets = tk.Listbox(janela_presets)
        lista_presets.pack(pady=5, fill=tk.BOTH, expand=True)

        # Carregar os nomes dos presets na listbox
        for filename in os.listdir("presets"):
            if filename.endswith(".json"):
                lista_presets.insert(tk.END, filename[:-5])

        def carregar_preset_selecionado():
            preset_name = lista_presets.get(tk.ACTIVE)
            if preset_name:
                preset_path = f"presets/{preset_name}.json"
                if os.path.exists(preset_path):
                    with open(preset_path, "r") as f:
                        preset_data = json.load(f)
                    entry_antes.delete("1.0", tk.END)
                    entry_antes.insert("1.0", preset_data["texto_antes"])
                    entry_depois.delete("1.0", tk.END)
                    entry_depois.insert("1.0", preset_data["texto_depois"])
                    self.pular_espacos.set(preset_data["pular_espacos"])
                    janela_presets.destroy()

        def deletar_preset():
            preset_name = lista_presets.get(tk.ACTIVE)
            if preset_name:
                resposta = messagebox.askyesno("Confirmar Deletar", "Tem certeza que deseja apagar este preset?")
                if not resposta:
                    return

                preset_path = f"presets/{preset_name}.json"
                if os.path.exists(preset_path):
                    os.remove(preset_path)
                    lista_presets.delete(tk.ACTIVE)
                    messagebox.showinfo("Preset Deletado", f"Preset '{preset_name}' deletado com sucesso!")

        botao_carregar = ttk.Button(janela_presets, text="Carregar", command=carregar_preset_selecionado)
        botao_carregar.pack(pady=10)

        botao_deletar = ttk.Button(janela_presets, text="Deletar", command=deletar_preset)
        botao_deletar.pack(pady=10)


    # Função para adicionar menu de contexto
    def add_context_menu(self, widget):
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label="Desfazer", command=lambda: widget.event_generate("<<Undo>>"))
        menu.add_command(label="Refazer", command=lambda: widget.event_generate("<<Redo>>"))
        menu.add_separator()
        menu.add_command(label="Copiar", command=lambda: widget.event_generate("<<Copy>>"))
        menu.add_command(label="Colar", command=lambda: widget.event_generate("<<Paste>>"))
        menu.add_command(label="Recortar", command=lambda: widget.event_generate("<<Cut>>"))
        menu.add_separator()
        menu.add_command(label="Selecionar Tudo", command=lambda: widget.event_generate("<<SelectAll>>"))
        menu.add_command(label="Limpar", command=lambda: widget.delete(1.0, tk.END))

        widget.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))
    # Funções para copiar, colar, selecionar tudo e limpar
    def copiar(self, widget):
        widget.event_generate("<<Copy>>")

    def colar(self, widget):
        widget.event_generate("<<Paste>>")

    def selecionar_tudo(self, widget):
        widget.tag_add("sel", "1.0", "end")
        widget.mark_set("insert", "1.0")
        widget.see("insert")
        widget.focus()

    def limpar(self, widget):
        widget.delete("1.0", tk.END)

# Inicializando a aplicação
if __name__ == "__main__":
    root = tk.Tk()
    app = LimitadorCaracteresApp(root)
    root.mainloop()

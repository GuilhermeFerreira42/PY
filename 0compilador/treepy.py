import tkinter as tk
from tkinter import ttk, filedialog
from tkinterdnd2 import DND_FILES, TkinterDnD
import ast

# Classe para criar nós da árvore
class Node:
    def __init__(self, nome, nivel=0):
        self.nome = nome
        self.nivel = nivel
        self.filhos = []

    def add_child(self, child_node):
        child_node.nivel = self.nivel + 1
        self.filhos.append(child_node)

# Função para analisar o código Python
def parse_code(code):
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return Node("Sintaxe Python Inválida")
    root = Node("Raiz")
    parse_node(tree, root)
    return root

def parse_node(node, current_node):
    """
    Função recursiva para percorrer a árvore de sintaxe abstrata (AST) do Python
    e adicionar nós à nossa árvore personalizada.
    """
    if isinstance(node, ast.FunctionDef):
        new_node = Node(f"Função: {node.name}")
        current_node.add_child(new_node)
        current_node = new_node
    elif isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                new_node = Node(f"Variável: {target.id}")
                current_node.add_child(new_node)

    for child in ast.iter_child_nodes(node):
        parse_node(child, current_node)

def print_tree(node, indent=""):
    """
    Função recursiva para imprimir a árvore de forma hierárquica.
    """
    indent_str = "│   " * node.nivel + "├── " if node.nivel > 0 else ""
    result = indent_str + node.nome + "\n"
    for child in node.filhos:
        result += print_tree(child)
    return result

def filtrar_arvore(node, nivel_atual, nivel_max):
    """
    Função recursiva para filtrar a árvore de acordo com o nível de profundidade.
    """
    if nivel_atual > nivel_max:
        return None
    new_node = Node(node.nome, node.nivel)
    for child in node.filhos:
        child_node = filtrar_arvore(child, nivel_atual + 1, nivel_max)
        if child_node:
            new_node.add_child(child_node)
    return new_node

def atualizar_arvore(nivel):
    """
    Função para atualizar a árvore de acordo com o nível de profundidade selecionado.
    """
    entry_resultado.delete("1.0", tk.END)
    root_node = parse_code(codigo_original)
    filtered_root = filtrar_arvore(root_node, 0, nivel)
    tree_output = print_tree(filtered_root)
    entry_resultado.insert(tk.END, tree_output)

def processar_arquivo(filepath):
    """
    Função para abrir um arquivo, processar o código e exibir a árvore de declarações.
    """
    global codigo_original
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as file:
            codigo_original = file.read()
            if filepath.endswith(('.py', '.txt', '.html')):
                root = parse_code(codigo_original)
                tree_output = print_tree(root)
            else:
                tree_output = codigo_original
        
        entry_resultado.delete("1.0", tk.END)
        entry_resultado.insert(tk.END, tree_output)

def on_drop(event):
    """
    Função para lidar com o evento de arrastar e soltar arquivos.
    """
    file_path = event.data.strip('{}')
    processar_arquivo(file_path)

def copiar(widget):
    """
    Função para copiar texto selecionado.
    """
    widget.event_generate("<<Copy>>")

def colar(widget):
    """
    Função para colar texto.
    """
    widget.event_generate("<<Paste>>")

def selecionar_tudo(widget):
    """
    Função para selecionar todo o texto.
    """
    widget.tag_add("sel", "1.0", "end")
    widget.mark_set("insert", "1.0")
    widget.see("insert")
    widget.focus()

def limpar(widget):
    """
    Função para limpar o texto.
    """
    widget.delete("1.0", tk.END)

def criar_menu_contexto(widget):
    """
    Função para criar um menu de contexto com opções de copiar, colar, selecionar tudo e limpar.
    """
    menu_contexto = tk.Menu(widget, tearoff=0)
    menu_contexto.add_command(label="Copiar", command=lambda: copiar(widget))
    menu_contexto.add_command(label="Colar", command=lambda: colar(widget))
    menu_contexto.add_command(label="Selecionar Tudo", command=lambda: selecionar_tudo(widget))
    menu_contexto.add_command(label="Limpar", command=lambda: limpar(widget))
    def exibir_menu(event):
        menu_contexto.tk_popup(event.x_root, event.y_root)
    widget.bind("<Button-3>", exibir_menu)

def criar_botoes_niveis(frame):
    """
    Função para criar botões de seleção de nível de detalhes da árvore binária.
    """
    ttk.Button(frame, text="Nível 1", command=lambda: atualizar_arvore(1)).grid(row=0, column=0, padx=5)
    ttk.Button(frame, text="Nível 2", command=lambda: atualizar_arvore(2)).grid(row=0, column=1, padx=5)
    ttk.Button(frame, text="Nível 3", command=lambda: atualizar_arvore(3)).grid(row=0, column=2, padx=5)

# Configuração da janela principal
root = TkinterDnD.Tk()
root.title("TreePy")
root.geometry("600x650")

# Área de arrastar e soltar arquivos
frame_dragdrop = ttk.Frame(root)
frame_dragdrop.pack(pady=10, fill=tk.BOTH, expand=True)

label_dragdrop = ttk.Label(frame_dragdrop, text="Arraste e solte um arquivo aqui")
label_dragdrop.pack(pady=10)

root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Rótulo e campo para mostrar o texto processado
label_resultado = ttk.Label(root, text="Resultado:")
label_resultado.pack(pady=5)

# Frame para entrada de texto com barra de rolagem
frame_texto = ttk.Frame(root)
frame_texto.pack(pady=5, fill=tk.BOTH, expand=True)

# Barra de rolagem
scrollbar = ttk.Scrollbar(frame_texto)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Campo de texto para mostrar o resultado
entry_resultado = tk.Text(frame_texto, height=30, width=70, yscrollcommand=scrollbar.set)
entry_resultado.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=entry_resultado.yview)

criar_menu_contexto(entry_resultado)

# Frame para botões de seleção de nível de detalhes
frame_botoes_niveis = ttk.Frame(root)
frame_botoes_niveis.pack(pady=10)
criar_botoes_niveis(frame_botoes_niveis)

# Iniciar o loop da interface gráfica
root.mainloop()

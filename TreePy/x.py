import tkinter as tk
from tkinter import ttk, filedialog
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

def processar_arquivo():
    """
    Função para abrir um arquivo, processar o código e exibir a árvore de declarações.
    """
    filepath = filedialog.askopenfilename()
    if filepath:
        with open(filepath, 'r', encoding='utf-8') as file:
            code = file.read()
            if filepath.endswith(('.py', '.txt', '.html')):
                root = parse_code(code)
                tree_output = print_tree(root)
            else:
                tree_output = code
        
        entry_resultado.delete("1.0", tk.END)
        entry_resultado.insert(tk.END, tree_output)

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

# Configuração da janela principal
root = tk.Tk()
root.title("Analisador de Código Python")
root.geometry("600x650")

# Botão para abrir o arquivo e processar o texto
botao_abrir = ttk.Button(root, text="Abrir Arquivo", command=processar_arquivo)
botao_abrir.pack(pady=10)

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

# Iniciar o loop da interface gráfica
root.mainloop()

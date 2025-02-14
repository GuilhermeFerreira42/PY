import os
import re

def find_js_files(path):
    """Encontra todos os arquivos .js em um diretório e subdiretórios"""
    js_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.js'):
                js_files.append(os.path.join(root, file))
    return js_files

def parse_js_content(file_path):
    """Analisa o conteúdo do arquivo JS retornando funções e exportações"""
    local_functions = []
    module_exports = []
    
    # Padrões de regex
    function_patterns = [
        r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\(',
        r'(?:export\s+)?(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>',
        r'class\s+\w+\s*{[^}]*?\b(\w+)\s*\([^)]*\)\s*\{'
    ]
    
    export_patterns = [
        r'export\s*{\s*([^}]+)\s*}\s*from\s*[\'"]([^\'"]+)',
        r'export\s+{\s*([^}]+)\s*}',
        r'export\s+default\s+(\w+)'
    ]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Captura funções locais
    for pattern in function_patterns:
        matches = re.findall(pattern, content)
        local_functions.extend(matches)
        
    # Captura exportações
    for pattern in export_patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if isinstance(match, tuple):
                exports = match[0].split(',')
                module_exports.extend([e.strip() for e in exports])
            else:
                module_exports.append(match.strip())
    
    return {
        'local': sorted(set(local_functions)),
        'exports': sorted(set(module_exports))
    }

def generate_tree(path):
    """Gera a estrutura da árvore com metadados"""
    tree = []
    
    files = [path] if os.path.isfile(path) and path.endswith('.js') else find_js_files(path)
    
    for file in files:
        relative_path = os.path.relpath(file, start=path)
        dirs, filename = os.path.split(relative_path)
        
        content = parse_js_content(file)
        
        tree.append({
            'path': dirs.split(os.sep) if dirs else [],
            'name': filename,
            'local_functions': content['local'],
            'module_exports': content['exports']
        })
    
    return tree

def format_tree(tree, root_name):
    """Formata a árvore com distinção entre tipos"""
    output = [f"📁 {root_name}/"]
    last_index = len(tree) - 1
    
    for i, node in enumerate(tree):
        indent = ''.join(['│   ' for _ in node['path']])
        
        # Caminho do diretório
        for j, p in enumerate(node['path']):
            line = '├── ' if (i < last_index) or (j < len(node['path'])-1) else '└── '
            output.append(f"{indent[:4*j]}{line}📁 {p}/")
        
        # Arquivo
        line = '└── ' if i == last_index else '├── '
        output.append(f"{indent}{line}📄 {node['name']}")
        
        # Funções locais
        if node['local_functions']:
            output.append(f"{indent}│   ├── 🔧 Funções Locais")
            for func in node['local_functions']:
                output.append(f"{indent}│   │   ├── {func}()")
        
        # Exportações
        if node['module_exports']:
            output.append(f"{indent}│   ├── 📤 Exportações")
            for export in node['module_exports']:
                output.append(f"{indent}│   │   ├── {export}")
    
    return '\n'.join(output)

def save_tree_to_file(tree, output_path):
    """Salva a árvore em arquivo de texto"""
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(tree)
        print(f"\n✅ Árvore salva em: {output_path}")
    except PermissionError:
        print(f"\n❌ Erro: Permissão negada para salvar em {output_path}")
    except Exception as e:
        print(f"\n❌ Erro ao salvar arquivo: {str(e)}")

def main():
    """Função principal com interação do usuário"""
    print("🛠  Gerador de Árvore de Funções JavaScript\n")
    
    # Pede caminho de entrada
    while True:
        input_path = input("📍 Caminho da pasta/arquivo JS: ").strip()
        if os.path.exists(input_path):
            break
        print("❌ Caminho inválido! Tente novamente.\n")
    
    # Pede caminho de saída
    while True:
        output_path = input("\n💾 Onde salvar a árvore (ex: C:/arvore.txt): ").strip()
        if output_path:
            if os.path.isdir(output_path):
                output_path = os.path.join(output_path, "arvore-funcoes.txt")
                print(f"📁 Usando: {output_path}")
            break
        print("❌ Insira um caminho válido!")
    
    # Processa os arquivos
    print("\n⏳ Analisando arquivos...")
    root_name = os.path.basename(input_path) if os.path.isdir(input_path) else os.path.basename(input_path)
    tree = generate_tree(input_path)
    
    if tree:
        formatted_tree = format_tree(tree, root_name)
        print("\n🌳 Árvore de Funções Gerada:\n")
        print(formatted_tree)
        save_tree_to_file(formatted_tree, output_path)  # Função agora definida!
    else:
        print("\n🔍 Nenhuma função encontrada nos arquivos!")

if __name__ == '__main__':
    main()
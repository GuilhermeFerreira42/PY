import os

def consolidate_python_files(source_dir, output_file):
    with open(output_file, 'w') as outfile:
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as infile:
                        outfile.write(f'# {file}\n')
                        outfile.write(infile.read())
                        outfile.write('\n\n')

# Substitua pelo diretório onde estão seus arquivos Python
source_directory = r'C:\Users\Usuario\Desktop\PY\PY\IA_GUI\MyProject'
output_file = 'codigo_completo.txt'

consolidate_python_files(source_directory, output_file)
print(f'Arquivo consolidado: {output_file}')

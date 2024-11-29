import os
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from nltk.tokenize import sent_tokenize

# Caminho do arquivo de entrada
input_file_path = r'C:\Users\Usuario\Desktop\OS CÓDIGOS DO MILHÃO COMO DESBLOQUEAR AS TRILHAS NEURONAIS DA RIQUEZA.txt'
# Caminho da pasta de saída
output_folder = r'C:\Users\Usuario\Desktop'

# Função para resumir o texto
def summarize_text(input_file, output_folder):
    # Ler o conteúdo do arquivo
    with open(input_file, 'r', encoding='utf-8') as file:
        text = file.read()

    # Usar o sent_tokenize do NLTK para tokenizar o texto
    sentences = sent_tokenize(text, language='portuguese')

    # Criar um parser a partir das sentenças tokenizadas
    parser = PlaintextParser.from_string(' '.join(sentences), Tokenizer("portuguese"))
    summarizer = LsaSummarizer()

    # Resumir o texto
    summary = summarizer(parser.document, 10)  # Resumir para 3 frases

    # Definir o caminho do arquivo de saída
    output_file_path = os.path.join(output_folder, 'resumo.txt')

    # Salvar o resumo em um novo arquivo
    with open(output_file_path, 'w', encoding='utf-8') as output_file:
        for sentence in summary:
            output_file.write(str(sentence) + '\n')

    print(f"Resumo salvo em: {output_file_path}")

# Executar a função
summarize_text(input_file_path, output_folder)
# Resumir.py

Um script Python para resumir textos em português usando a biblioteca NLTK para tokenização e o algoritmo LSA (Latent Semantic Analysis) da biblioteca Sumy para gerar um resumo conciso.

## Descrição

O `resumir.py` lê um arquivo de texto, processa o conteúdo e cria um resumo reduzido do texto original, salvando-o em um novo arquivo chamado `resumo.txt`.

## Pré-requisitos

1. **Instalar o Python:** Verifique se você tem o Python instalado na máquina.
2. **Instalar dependências:** Execute o seguinte comando para instalar as bibliotecas necessárias:

   ```bash
   pip install nltk sumy
   ```

3. **Configuração do NLTK:** No console Python, execute o seguinte para baixar recursos essenciais:

   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('punkt_tab')
   ```

## Como Usar

1. **Clone ou baixe** o arquivo `resumir.py` para sua máquina.
2. **Prepare seu arquivo de texto** que será resumido e salve-o em um local acessível.
3. **Configure os caminhos no script**:
   - No código, atualize os caminhos para o arquivo de entrada e a pasta de saída, conforme o exemplo:

     ```python
     input_file_path = r'C:\Users\Usuario\Desktop\seu_arquivo.txt'
     output_folder = r'C:\Users\Usuario\Desktop'
     ```

4. **Execute o script**:

   ```bash
   python C:/caminho/para/resumir.py
   ```

   O resumo será salvo como `resumo.txt` na pasta de saída especificada.

## Exemplo de Uso

```python
# Caminho do arquivo de entrada
input_file_path = r'C:\Users\Usuario\Desktop\seu_arquivo.txt'
# Caminho da pasta de saída
output_folder = r'C:\Users\Usuario\Desktop'
```

## Estrutura do Código

O script funciona da seguinte forma:

- **Carrega o texto** do arquivo de entrada.
- **Tokeniza as sentenças** usando a NLTK.
- **Usa o algoritmo LSA** para gerar um resumo conciso, configurado para reduzir a 10 frases.
- **Salva o resumo** em `resumo.txt` na pasta de saída especificada.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir um *issue* ou enviar um *pull request* no GitHub.

## Licença

Este projeto está licenciado sob a **MIT License**. Consulte o arquivo LICENSE para mais detalhes.

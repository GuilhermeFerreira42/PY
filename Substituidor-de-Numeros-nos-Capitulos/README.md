# Substituidor de Números nos Capítulos

Este programa em Python permite que você substitua automaticamente números por extenso nos capítulos de um arquivo de texto, PDF ou Word. Somente os números que seguem a palavra "Capítulo" serão convertidos para a forma escrita por extenso, enquanto outros números permanecem inalterados.

## Funcionalidades

- Interface gráfica construída com `wxPython`.
- Suporte para arquivos `.txt`, `.pdf` e `.docx`.
- Substituição automática dos números após a palavra "Capítulo" por palavras em português (de 1 até 150).
- Salva o resultado em um novo arquivo chamado `livro_modificado.txt`.

## Pré-requisitos

Para executar este projeto, você precisa instalar as seguintes bibliotecas:

1. wxPython:
   ```bash
   pip install wxPython
   ```
2. PyMuPDF (para manipulação de arquivos PDF):
   ```bash
   pip install pymupdf
   ```
3. python-docx (para manipulação de arquivos Word):
   ```bash
   pip install python-docx
   ```

## Estrutura do Código

O código está organizado da seguinte forma:

- Um dicionário chamado `numeros_por_extenso` contém os números por extenso de 1 a 150.
- A função `substituir_numeros` usa uma expressão regular para localizar a palavra "Capítulo" seguida por um número e substitui o número pela versão por extenso.
- A função `ler_arquivo` carrega o conteúdo dos arquivos `.txt`, `.pdf`, e `.docx`.
- A interface wxPython exibe uma janela com:
  - Um botão para selecionar o arquivo.
  - Um botão para iniciar a substituição.
  - Uma caixa de texto para exibir o conteúdo modificado.

## Como Usar

1. Clone este repositório ou faça o download do arquivo `biblia.py`.
2. Instale os pacotes necessários com os comandos listados acima.
3. Execute o script:
   ```bash
   python biblia.py
   ```
4. Na interface gráfica:
   - Clique em "Selecionar Arquivo" e escolha um arquivo no formato `.txt`, `.pdf` ou `.docx`.
   - Clique em "Substituir Números nos Capítulos" para realizar a substituição.
   - O conteúdo modificado será exibido na interface, e o arquivo modificado será salvo como `livro_modificado.txt` na pasta do projeto.

## Exemplo

- **Arquivo original:** `Capítulo 1 - Introdução`
- **Arquivo modificado:** `Capítulo um. - Introdução`

## Contribuições

Sinta-se à vontade para contribuir com melhorias ou sugestões. Clone o repositório, crie uma branch com suas alterações e envie um pull request!

## Licença

Este projeto é de código aberto e está disponível sob a licença MIT.

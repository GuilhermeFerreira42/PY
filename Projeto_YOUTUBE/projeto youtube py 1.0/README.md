# Documentação do Projeto: Resumidor de Vídeos

## Visão Geral do Projeto

### Descrição Geral
Este projeto é um aplicativo de desktop desenvolvido em Python que permite aos usuários resumir vídeos do YouTube. Ele utiliza a biblioteca wxPython para a interface gráfica e integra várias funcionalidades, como download de legendas e geração de resumos.

### Objetivo do Projeto e Funcionalidades Principais
O objetivo do projeto é facilitar a obtenção de resumos de vídeos, permitindo que os usuários coletem informações de forma rápida e eficiente. As principais funcionalidades incluem:
- Download de legendas de vídeos do YouTube.
- Processamento e limpeza das legendas.
- Geração de resumos utilizando uma API de IA.
- Interface gráfica amigável para interação do usuário.

### Tecnologias Utilizadas
- Python
- wxPython
- yt-dlp
- requests
- JSON

## Árvore de Diretórios

```
projeto/
│
├── ChatIA.py
│   ├── Classe responsável por interagir com a API para gerar resumos de texto.
│   ├── Métodos:
│   │   ├── generate_summary(text): Gera um resumo do texto fornecido.
│   │   ├── save_summary(video_name, video_url, subtitles_path, summary): Salva informações do vídeo.
│   │   └── load_summary(video_name): Carrega informações do vídeo a partir do histórico.
│
├── HistorySidebar.py
│   ├── Classe que gerencia a barra lateral de histórico de vídeos.
│   ├── Métodos:
│   │   ├── Append(video_name): Adiciona um vídeo ao histórico.
│   │   └── load_history(): Carrega o histórico de vídeos.
│
├── Main.py
│   ├── Classe principal da aplicação que inicializa a interface gráfica.
│   ├── Métodos:
│   │   └── __init__(): Configura a janela principal e as abas.
│
├── SubtitleProcessor.py
│   ├── Classe responsável por baixar e processar legendas de vídeos.
│   ├── Métodos:
│   │   ├── download_subtitles(video_url): Baixa as legendas do vídeo.
│   │   └── clean_and_consolidate_subtitles(subtitle_file, video_name): Limpa e consolida as legendas.
│
└── YouTubePage.py
    ├── Classe que gerencia a interação do usuário com a página do YouTube.
    ├── Métodos:
    │   ├── OnToggleSidebar(event): Alterna a visibilidade da barra lateral.
    │   ├── LoadVideo(video_url, subtitles_path): Carrega a URL e as legendas do vídeo.
    │   ├── OnPaste(event): Cola a URL do vídeo.
    │   ├── OnCopy(event): Copia o texto processado.
    │   ├── OnClear(event): Limpa todos os campos.
    │   ├── GetVideoNameFromURL(url): Obtém o nome do vídeo a partir da URL.
    │   ├── OnSummarize(event): Gera um resumo do texto.
    │   └── OnProcess(event): Inicia o processamento do vídeo.
```

## Descrição Detalhada das Funções

### ChatIA.py
- **generate_summary(text)**: 
  - **Descrição**: Gera um resumo do texto fornecido.
  - **Parâmetros**: `text` (str) - Texto a ser resumido.
  - **Retorno**: Resumo gerado pela IA (str).

- **save_summary(video_name, video_url, subtitles_path, summary)**: 
  - **Descrição**: Salva informações do vídeo, incluindo o resumo.
  - **Parâmetros**: `video_name` (str), `video_url` (str), `subtitles_path` (str), `summary` (str).
  
- **load_summary(video_name)**: 
  - **Descrição**: Carrega informações do vídeo a partir do histórico.
  - **Parâmetros**: `video_name` (str).
  - **Retorno**: Informações do vídeo (dict) ou None.

### HistorySidebar.py
- **Append(video_name)**: 
  - **Descrição**: Adiciona um vídeo ao histórico.
  - **Parâmetros**: `video_name` (str).

- **load_history()**: 
  - **Descrição**: Carrega o histórico de vídeos.
  - **Retorno**: Lista de vídeos (list).

### Main.py
- **__init__()**: 
  - **Descrição**: Configura a janela principal e as abas.

### SubtitleProcessor.py
- **download_subtitles(video_url)**: 
  - **Descrição**: Baixa as legendas do vídeo.
  - **Parâmetros**: `video_url` (str).
  - **Retorno**: Caminho do arquivo de legendas (str) ou None.

- **clean_and_consolidate_subtitles(subtitle_file, video_name)**: 
  - **Descrição**: Limpa e consolida as legendas.
  - **Parâmetros**: `subtitle_file` (str), `video_name` (str).
  - **Retorno**: Caminho do arquivo JSON com as legendas (str) ou None.

### YouTubePage.py
- **OnToggleSidebar(event)**: 
  - **Descrição**: Alterna a visibilidade da barra lateral.

- **LoadVideo(video_url, subtitles_path)**: 
  - **Descrição**: Carrega a URL e as legendas do vídeo.
  - **Parâmetros**: `video_url` (str), `subtitles_path` (str).

- **OnPaste(event)**: 
  - **Descrição**: Cola a URL do vídeo.

- **OnCopy(event)**: 
  - **Descrição**: Copia o texto processado.

- **OnClear(event)**: 
  - **Descrição**: Limpa todos os campos.

- **GetVideoNameFromURL(url)**: 
  - **Descrição**: Obtém o nome do vídeo a partir da URL.
  - **Parâmetros**: `url` (str).
  - **Retorno**: Nome do vídeo (str).

- **OnSummarize(event)**: 
  - **Descrição**: Gera um resumo do texto.

- **OnProcess(event)**: 
  - **Descrição**: Inicia o processamento do vídeo.

## Fluxo de Execução

O fluxo de execução do projeto começa com a inicialização do servidor e a abertura da interface gráfica. O usuário pode inserir a URL de um vídeo do YouTube e clicar em "Processar" para baixar as legendas. Após o download, o usuário pode gerar um resumo do texto das legendas. O histórico de vídeos processados é mantido na barra lateral.

## Estrutura do Código

O código está estruturado em várias classes, cada uma responsável por uma parte específica da funcionalidade do aplicativo. As classes se comunicam entre si através de métodos e eventos, permitindo uma interação fluida na interface gráfica. Boas práticas de programação, como encapsulamento e separação de responsabilidades, foram utilizadas para manter o código organizado e fácil de manter.

## Instruções de Instalação

1. **Configuração do Ambiente de Desenvolvimento Local**:
   - Certifique-se de ter o Python instalado em sua máquina.
   - Instale as dependências necessárias usando o seguinte comando:
     ```
     pip install wxPython yt-dlp requests
     ```

2. **Rodar o Servidor**:
   - Execute o arquivo `Main.py` para iniciar a aplicação:
     ```
     python Main.py
     ```

## Considerações Finais

- **Recomendações de Melhorias**: 
  - Implementar suporte a mais idiomas para legendas.
  - Melhorar a interface gráfica para uma experiência de usuário mais intuitiva.

- **Sugestões de Futuras Funcionalidades**: 
  - Adicionar a capacidade de compartilhar resumos em redes sociais.
  - Implementar uma funcionalidade de busca para vídeos no YouTube diretamente pela aplicação.

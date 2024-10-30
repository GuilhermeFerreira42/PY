# converte-video---GUI

## Descrição
Este programa permite a conversão de arquivos de vídeo em diferentes formatos utilizando a ferramenta FFmpeg. Ele fornece uma interface gráfica para facilitar a seleção de arquivos de vídeo e o diretório de saída, além de permitir a escolha do formato desejado. O programa exibe uma barra de progresso durante o processamento da conversão.

## Funcionalidades
- **Conversão de Vídeo**: Converte vídeos em diversos formatos, como MP4, AVI, MKV, MOV, FLV e WMV.
- **Interface Gráfica**: Oferece uma interface gráfica amigável para seleção de arquivos e configurações.
- **Barra de Progresso**: Mostra o progresso da conversão em tempo real.
- **Histórico de Caminhos**: Salva o último caminho de saída selecionado para facilitar futuras conversões.

## Dependências
Antes de executar o programa, você precisa instalar as seguintes dependências:

- **FFmpeg**: Baixe e instale o FFmpeg a partir do site oficial [FFmpeg](https://ffmpeg.org/download.html) e adicione o executável `ffmpeg.exe` ao seu PATH do sistema.

- **Bibliotecas Python**:
  ```bash
  pip install tkinter
  ```

## Instruções de Uso
1. Execute o script Python.
2. Use a interface gráfica para selecionar os arquivos de vídeo que deseja converter.
3. Selecione o diretório de saída e o formato desejado.
4. O programa começará a conversão, exibindo o progresso na barra de progresso.
5. Ao final do processamento, uma mensagem de conclusão será exibida.

## Manual de Instalação
Este manual orienta você na instalação das ferramentas necessárias para executar o programa de conversão de vídeo.

1. **Instalar Python**:
   - Acesse [Python.org](https://www.python.org/).
   - Baixe e instale a versão mais recente do Python, garantindo que a opção "Add Python to PATH" esteja marcada.

2. **Instalar FFmpeg**:
   - Acesse [FFmpeg Downloads](https://ffmpeg.org/download.html) e faça o download da versão compatível com o seu sistema.
   - Extraia o arquivo baixado e adicione o caminho do executável `ffmpeg.exe` ao seu PATH.

3. **Executar o Programa**:
   - Salve o código Python em um arquivo (por exemplo, `conversor_video.py`).
   - Abra o terminal ou prompt de comando e navegue até o diretório onde o arquivo está salvo.
   - Execute o programa com o seguinte comando:
     ```bash
     python converte video -GUI.py
     ```
   - A interface gráfica será aberta, permitindo que você comece a conversão.

Para mais detalhes e atualizações, consulte a documentação do projeto.

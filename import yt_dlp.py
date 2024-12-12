import wx
import yt_dlp
import re
import os
from wx.lib.pubsub import pub
import threading

class SubtitleApp(wx.Frame):
    def __init__(self, parent, title):
        super(SubtitleApp, self).__init__(parent, title=title, size=(800, 600))

        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Linha para URL e botão "Colar"
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.url_label = wx.StaticText(panel, label="URL do Vídeo:")
        hbox1.Add(self.url_label, flag=wx.RIGHT, border=8)
        self.url_text = wx.TextCtrl(panel)
        hbox1.Add(self.url_text, proportion=1)
        
        self.paste_button = wx.Button(panel, label="Colar")
        self.paste_button.Bind(wx.EVT_BUTTON, self.OnPaste)
        hbox1.Add(self.paste_button, flag=wx.LEFT, border=8)
        
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Botões principais e contador de palavras
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        # Alinhado à esquerda
        left_box = wx.BoxSizer(wx.HORIZONTAL)
        self.process_button = wx.Button(panel, label="Processar")
        self.process_button.Bind(wx.EVT_BUTTON, self.OnProcess)
        left_box.Add(self.process_button)

        self.clear_button = wx.Button(panel, label="Limpar")
        self.clear_button.Bind(wx.EVT_BUTTON, self.OnClear)
        left_box.Add(self.clear_button, flag=wx.LEFT | wx.RIGHT, border=5)

        self.copy_button = wx.Button(panel, label="Copiar")
        self.copy_button.Bind(wx.EVT_BUTTON, self.OnCopy)
        left_box.Add(self.copy_button, flag=wx.LEFT | wx.RIGHT, border=5)

        self.progress_bar = wx.Gauge(panel, range=100, size=(250, 25))
        left_box.Add(self.progress_bar, flag=wx.LEFT, border=10)

        hbox2.Add(left_box, flag=wx.ALIGN_LEFT)

        # Alinhado à direita
        self.word_count_label = wx.StaticText(panel, label="Palavras: 0")
        hbox2.AddStretchSpacer()
        hbox2.Add(self.word_count_label, flag=wx.ALIGN_CENTER_VERTICAL | wx.RIGHT, border=10)

        vbox.Add(hbox2, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        # Caixa de texto para texto processado
        self.text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)

    def OnPaste(self, event):
        """Cola o conteúdo da área de transferência na URL e limpa o campo antes."""
        if wx.TheClipboard.Open():
            if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
                data = wx.TextDataObject()
                wx.TheClipboard.GetData(data)
                self.url_text.SetValue(data.GetText())
            wx.TheClipboard.Close()

    def OnProcess(self, event):
        """Inicia o processamento do vídeo."""
        video_url = self.url_text.GetValue()
        if not video_url:
            wx.MessageBox("Por favor, insira uma URL do vídeo.", "Erro", wx.ICON_ERROR)
            return

        self.progress_bar.SetValue(10)  # Atualiza a barra de progresso

        def run():
            subtitle_file = download_subtitles(video_url)
            if subtitle_file:
                self.progress_bar.SetValue(70)
                consolidated_file = clean_and_consolidate_subtitles(subtitle_file)
                self.progress_bar.SetValue(100)
                if consolidated_file:
                    with open(consolidated_file, 'r', encoding='utf-8') as file:
                        content = file.read()
                    wx.CallAfter(self.text_ctrl.SetValue, content)

                    # Contar palavras e atualizar o contador
                    word_count = len(content.split())
                    wx.CallAfter(self.word_count_label.SetLabel, f"Palavras: {word_count}")
                else:
                    wx.CallAfter(wx.MessageBox, "Erro ao consolidar as legendas.", "Erro", wx.ICON_ERROR)
            else:
                wx.CallAfter(wx.MessageBox, "Não foi possível obter as legendas.", "Erro", wx.ICON_ERROR)

        thread = threading.Thread(target=run)
        thread.start()

    def OnClear(self, event):
        """Limpa todos os campos."""
        self.url_text.SetValue("")
        self.text_ctrl.SetValue("")
        self.progress_bar.SetValue(0)
        self.word_count_label.SetLabel("Palavras: 0")

    def OnCopy(self, event):
        """Copia o texto processado para a área de transferência."""
        text = self.text_ctrl.GetValue()
        if text:
            if wx.TheClipboard.Open():
                wx.TheClipboard.SetData(wx.TextDataObject(text))
                wx.TheClipboard.Close()
                wx.MessageBox("Texto copiado com sucesso!", "Informação", wx.ICON_INFORMATION)
        else:
            wx.MessageBox("Nada para copiar.", "Erro", wx.ICON_ERROR)

def download_subtitles(video_url):
    """
    Função para baixar as legendas do vídeo no YouTube em português (pt-br).
    """
    ydl_opts = {
        'writesubtitles': True,         # Habilita o download de legendas
        'writeautomaticsub': True,      # Habilita o download de legendas automáticas
        'subtitleslangs': ['pt', 'pt-br'], # Idioma das legendas
        'skip_download': True,          # Pula o download do vídeo
        'quiet': False                  # Exibe mensagens de log para depuração
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(video_url, download=False)
            subtitle_file = None

            if 'requested_subtitles' in result:
                subtitle_file = ydl.prepare_filename(result)
                subtitle_file = subtitle_file.rsplit('.', 1)[0] + '.pt.vtt'
                ydl.download([video_url])
                print(f"Legendas baixadas para: {subtitle_file}")
            else:
                print("Nenhuma legenda em português disponível.")
            return subtitle_file
        except Exception as e:
            print(f"Erro ao baixar legendas: {e}")
            return None

def clean_and_consolidate_subtitles(subtitle_file):
    """
    Função para consolidar legendas em um texto contínuo sem repetições.
    """
    try:
        with open(subtitle_file, 'r', encoding='utf-8') as file:
            content = file.read()

        # Remove linhas de tempo e metadados como "WEBVTT" ou "Kind: captions"
        content = re.sub(r'(WEBVTT|Kind:.*|Language:.*)', '', content)
        content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> .*?\n', '', content)

        # Remove tags detalhadas (<00:00:00.030><c>) e espaços extras
        content = re.sub(r'<.*?>', '', content)
        content = re.sub(r'&nbsp;', ' ', content)  # Substitui &nbsp; por espaço
        content = re.sub(r'align:start position:\d+%|\n+', '\n', content).strip()

        # Processa as linhas e elimina duplicatas (não apenas consecutivas)
        lines = content.splitlines()
        unique_lines = list(dict.fromkeys(line.strip() for line in lines if line.strip()))

        # Junta as linhas em um texto contínuo com quebras de linha apropriadas
        consolidated_text = '\n'.join(unique_lines).strip()

        # Salva o texto consolidado
        cleaned_filename = subtitle_file.replace('.vtt', '_consolidated.txt')
        with open(cleaned_filename, 'w', encoding='utf-8') as file:
            file.write(consolidated_text)

        print(f"Texto consolidado salvo em: {cleaned_filename}")
        return cleaned_filename
    except Exception as e:
        print(f"Erro ao limpar e consolidar as legendas: {e}")
        return None

if __name__ == "__main__":
    app = wx.App()
    SubtitleApp(None, title="Transcrição de Vídeos do YouTube")
    app.MainLoop()

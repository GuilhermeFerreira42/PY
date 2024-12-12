import wx
import yt_dlp
import re
import os

def download_subtitles(video_url):
    """
    Função para baixar as legendas do vídeo no YouTube em português (pt-br).
    """
    ydl_opts = {
        'writesubtitles': True,         # Habilita o download de legendas
        'writeautomaticsub': True,      # Habilita o download de legendas automáticas
        'subtitleslangs': ['pt', 'pt-br'], # Idioma das legendas
        'skip_download': True,          # Pula o download do vídeo
        'quiet': True                   # Suprime mensagens de log
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            result = ydl.extract_info(video_url, download=False)
            subtitle_file = None

            if 'requested_subtitles' in result:
                subtitle_file = ydl.prepare_filename(result)
                subtitle_file = subtitle_file.rsplit('.', 1)[0] + '.pt.vtt'
                ydl.download([video_url])
                return subtitle_file
            else:
                return None
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
        content = re.sub(r'align:start position:\d+%|\n+', '\n', content).strip()

        # Processa as linhas e elimina duplicatas
        lines = content.splitlines()
        unique_lines = list(dict.fromkeys(line.strip() for line in lines if line.strip()))

        # Junta as linhas em um texto contínuo
        consolidated_text = '\n'.join(unique_lines).strip()
        return consolidated_text
    except Exception as e:
        print(f"Erro ao limpar e consolidar as legendas: {e}")
        return None

class YouTubeSubtitleApp(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Processador de Legendas do YouTube", size=(800, 600))

        # Painel principal
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Campo de entrada para URL
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        lbl_url = wx.StaticText(panel, label="URL do vídeo:")
        hbox1.Add(lbl_url, flag=wx.RIGHT, border=8)
        self.txt_url = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        hbox1.Add(self.txt_url, proportion=1)
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Botões de ação
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        btn_process = wx.Button(panel, label="Processar")
        btn_process.Bind(wx.EVT_BUTTON, self.on_process)
        hbox2.Add(btn_process, flag=wx.RIGHT, border=10)

        btn_clear = wx.Button(panel, label="Limpar")
        btn_clear.Bind(wx.EVT_BUTTON, self.on_clear)
        hbox2.Add(btn_clear, flag=wx.RIGHT, border=10)

        vbox.Add(hbox2, flag=wx.ALIGN_CENTER | wx.TOP | wx.BOTTOM, border=10)

        # Campo de saída para o texto processado
        self.txt_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.txt_output, proportion=1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM, border=10)

        panel.SetSizer(vbox)
        self.Centre()

    def on_process(self, event):
        video_url = self.txt_url.GetValue().strip()
        if not video_url:
            wx.MessageBox("Por favor, insira a URL do vídeo.", "Erro", wx.OK | wx.ICON_ERROR)
            return

        self.txt_output.SetValue("Processando... Por favor, aguarde.")

        # Baixar as legendas
        subtitle_file = download_subtitles(video_url)
        if not subtitle_file:
            wx.MessageBox("Não foi possível baixar as legendas em português.", "Erro", wx.OK | wx.ICON_ERROR)
            self.txt_output.SetValue("")
            return

        # Consolidar o texto das legendas
        consolidated_text = clean_and_consolidate_subtitles(subtitle_file)
        if consolidated_text:
            self.txt_output.SetValue(consolidated_text)
        else:
            wx.MessageBox("Erro ao processar as legendas.", "Erro", wx.OK | wx.ICON_ERROR)

    def on_clear(self, event):
        self.txt_url.SetValue("")
        self.txt_output.SetValue("")

if __name__ == "__main__":
    app = wx.App()
    frame = YouTubeSubtitleApp()
    frame.Show()
    app.MainLoop()

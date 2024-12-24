import wx
import json
import os
import yt_dlp  # Certifique-se de que o yt-dlp está instalado

class HistorySidebar(wx.ListBox):
    def __init__(self, parent):
        super(HistorySidebar, self).__init__(parent, style=wx.LB_SINGLE)
        self.history_file = "história do YouTube/histórico.json"
        self.parent = parent  # Referência ao pai para chamar métodos
        self.Bind(wx.EVT_LISTBOX, self.OnSelectHistory)
        self.LoadHistory()

    def LoadHistory(self):
        """Carrega o histórico de vídeos da pasta 'história do YouTube'."""
        if not os.path.exists("história do YouTube"):
            os.makedirs("história do YouTube")

        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as file:
                history = json.load(file)
                for video in history:
                    self.Append(video['name'])  # Adiciona o nome do vídeo à lista

    def OnSelectHistory(self, event):
        """Carrega as informações do vídeo selecionado na barra lateral."""
        selection = self.GetSelection()
        if selection != wx.NOT_FOUND:
            video_name = self.GetString(selection)
            print(f"Selecionado: {video_name}")  # Para depuração
            self.LoadVideoInfo(video_name)

    def LoadVideoInfo(self, video_name):
        """Carrega as informações do vídeo selecionado."""
        if os.path.exists(self.history_file):
            with open(self.history_file, 'r', encoding='utf-8') as file:
                history = json.load(file)
                for video in history:
                    if video['name'] == video_name:
                        # Chama um método do parent para carregar a URL e legendas
                        self.parent.LoadVideo(video['url'], video['subtitles'])
                        break

    def GetVideoTitle(self, url):
        """Obtém o título do vídeo a partir da URL usando yt-dlp."""
        ydl_opts = {
            'quiet': True,
            'force_generic_extractor': True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            return info_dict.get('title', None)

    def SaveHistory(self, video_name, video_url, subtitles_path, summary):
        """Salva o nome do vídeo, URL, caminho das legendas e resumo no histórico."""
        if not os.path.exists("história do YouTube"):
            os.makedirs("história do YouTube")

        history = []
        if os.path.exists(self.history_sidebar.history_file):
            with open(self.history_sidebar.history_file, 'r', encoding='utf-8') as file:
                history = json.load(file)

        # Adiciona ou atualiza o vídeo no histórico
        for video in history:
            if video['name'] == video_name:
                video['url'] = video_url  # Atualiza a URL
                video['subtitles'] = subtitles_path  # Atualiza o caminho das legendas
                video['summary'] = summary  # Adiciona ou atualiza o resumo
                break
        else:
            # Se o vídeo não estiver no histórico, adiciona uma nova entrada
            history.append({
                "name": video_name,
                "url": video_url,
                "subtitles": subtitles_path,
                "summary": summary  # Adiciona o resumo
            })

        with open(self.history_sidebar.history_file, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
import wx
from YouTubePage import YouTubePage

class MainFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Resumidor de Vídeos", size=(800, 600))

        # Criar um notebook para as abas
        self.notebook = wx.Notebook(self)

        # Adicionar a aba do YouTube
        self.youtube_page = YouTubePage(self.notebook)
        self.notebook.AddPage(self.youtube_page, "YouTube")

        # Configurar o layout principal
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.notebook, 1, wx.EXPAND)
        self.SetSizer(sizer)

        self.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()
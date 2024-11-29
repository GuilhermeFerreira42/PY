import wx
import requests
from bs4 import BeautifulSoup

class ScraperApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(ScraperApp, self).__init__(*args, **kw)
        
        self.InitUI()
        
    def InitUI(self):
        panel = wx.Panel(self)
        
        # Layout do painel
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Caixa de texto para o URL
        self.url_input = wx.TextCtrl(panel, style=wx.TE_LEFT)
        vbox.Add(self.url_input, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Caixa de botões (Processar e Limpar)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        # Botão para processar o scraping
        process_button = wx.Button(panel, label="Processar")
        hbox.Add(process_button, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Botão para limpar o conteúdo
        clear_button = wx.Button(panel, label="Limpar")
        hbox.Add(clear_button, flag=wx.EXPAND | wx.ALL, border=10)
        
        vbox.Add(hbox, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Caixa de texto para exibir o conteúdo extraído
        self.result_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(500, 300))
        vbox.Add(self.result_output, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)
        
        # Conectar os botões aos métodos
        process_button.Bind(wx.EVT_BUTTON, self.OnProcess)
        clear_button.Bind(wx.EVT_BUTTON, self.OnClear)
        
        panel.SetSizer(vbox)
        
        # Configurações da janela
        self.SetTitle('Scraper de Notícias')
        self.SetSize((600, 400))
        self.Centre()
        self.Show(True)
    
    def OnProcess(self, event):
        url = self.url_input.GetValue()
        
        if not url:
            self.result_output.SetValue("Por favor, insira um URL válido.")
            return
        
        try:
            # Adicionando um User-Agent para contornar o bloqueio de alguns sites
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
            }

            # Requisição HTTP
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

            # Analisando a página com BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Encontrando o conteúdo do artigo
            article_content = soup.find_all("p")
            article_text = "\n\n".join([p.get_text() for p in article_content])

            # Exibindo o conteúdo extraído
            if article_text:
                self.result_output.SetValue(article_text)
            else:
                self.result_output.SetValue("Conteúdo não encontrado.")

        except Exception as e:
            self.result_output.SetValue(f"Erro ao processar o link: {str(e)}")
    
    def OnClear(self, event):
        # Limpar os campos de URL e resultado
        self.url_input.SetValue("")
        self.result_output.SetValue("")


if __name__ == '__main__':
    app = wx.App(False)
    ScraperApp(None, title='Scraper de Notícias', size=(600, 400))
    app.MainLoop()

import wx
import re

class ConversaCleaner(wx.Frame):
    def __init__(self, *args, **kw):
        super(ConversaCleaner, self).__init__(*args, **kw)

        # Criar painel
        panel = wx.Panel(self)

        # Layout
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Campo de texto para entrada
        self.input_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        vbox.Add(self.input_text, 1, wx.EXPAND | wx.ALL, 10)

        # Botão de processar
        process_button = wx.Button(panel, label="Processar")
        process_button.Bind(wx.EVT_BUTTON, self.on_processar)
        vbox.Add(process_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Campo de texto para saída
        self.output_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(self.output_text, 1, wx.EXPAND | wx.ALL, 10)

        # Botão de limpar
        clear_button = wx.Button(panel, label="Limpar")
        clear_button.Bind(wx.EVT_BUTTON, self.on_limpar)
        vbox.Add(clear_button, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        panel.SetSizer(vbox)

        # Menu de contexto
        self.Bind(wx.EVT_RIGHT_DOWN, self.on_right_click)

        self.SetTitle("Limpar Conversas do WhatsApp")
        self.SetSize((600, 400))
        self.Centre()

    def on_processar(self, event):
        texto = self.input_text.GetValue()
        texto_limpo = self.limpar_conversa(texto)
        self.output_text.SetValue(texto_limpo)

    def on_limpar(self, event):
        self.input_text.SetValue("")
        self.output_text.SetValue("")

    def on_right_click(self, event):
        menu = wx.Menu()
        clear_item = menu.Append(wx.ID_ANY, "Limpar")
        self.Bind(wx.EVT_MENU, self.on_limpar, clear_item)
        self.PopupMenu(menu)
        menu.Destroy()

    def limpar_conversa(self, texto):
        # Quebra o texto em linhas
        linhas = texto.splitlines()
        mensagens_limpas = []

        for linha in linhas:
            # Remove o formato "DD/MM/AAAA HH:MM - +55 XX XXXXX-XXXX:"
            linha = re.sub(r'\d{2}/\d{2}/\d{4} \d{2}:\d{2} - \+\d{2} \d{2} \d{4,5}-\d{4}:', '', linha)
            # Remove o formato "[HH:MM, DD/MM/AAAA]"
            linha = re.sub(r'\[\d{2}:\d{2}, \d{2}/\d{2}/\d{4}\]', '', linha)
            # Remove números de telefone
            linha = re.sub(r'\+\d{2} \d{2} \d{4,5}-\d{4}', '', linha)
            # Remove espaços extras
            linha = re.sub(r'\s+', ' ', linha).strip()
            if linha:  # Adiciona apenas se a linha não estiver vazia
                mensagens_limpas.append(linha)

        # Junta as mensagens com quebras de linha
        return '\n'.join(mensagens_limpas)

if __name__ == "__main__":
    app = wx.App(False)
    frame = ConversaCleaner(None)
    frame.Show()
    app.MainLoop()
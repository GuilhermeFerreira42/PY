import wx
import threading
from SubtitleProcessor import SubtitleProcessor

class YouTubePage(wx.Panel):
    def __init__(self, parent):
        super(YouTubePage, self).__init__(parent)
        self.subtitle_processor = SubtitleProcessor()
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Linha para URL e botão "Colar"
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.url_label = wx.StaticText(self, label="URL do Vídeo:")
        hbox1.Add(self.url_label, flag=wx.RIGHT, border=8)
        self.url_text = wx.TextCtrl(self)
        hbox1.Add(self.url_text, proportion=1)
        
        self.paste_button = wx.Button(self, label="Colar")
        self.paste_button.Bind(wx.EVT_BUTTON, self.OnPaste)
        hbox1.Add(self.paste_button, flag=wx.LEFT, border=8)
        
        vbox.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

        # Botões principais e barra de progresso
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)

        # Alinhado à esquerda
        left_box = wx.BoxSizer(wx.HORIZONTAL)
        self.process_button = wx.Button(self, label="Processar")
        self.process_button.Bind(wx.EVT_BUTTON, self.OnProcess)
        left_box.Add(self.process_button)

        self.clear_button = wx.Button(self, label="Limpar")
        self.clear_button.Bind(wx.EVT_BUTTON, self.OnClear)
        left_box.Add(self.clear_button, flag=wx.LEFT | wx.RIGHT, border=5)

        self.copy_button = wx.Button(self, label="Copiar")
        self.copy_button.Bind(wx.EVT_BUTTON, self.OnCopy)
        left_box.Add(self.copy_button, flag=wx.LEFT | wx.RIGHT, border=5)

        self.summarize_button = wx.Button(self, label="Resumir")
        self.summarize_button.Bind(wx.EVT_BUTTON, self.OnSummarize)
        left_box.Add(self.summarize_button, flag=wx.LEFT | wx.RIGHT, border=5)

        self.progress_bar = wx.Gauge(self, range=100, size=(250, 25))
        left_box.Add(self.progress_bar, flag=wx.LEFT, border=10)

        hbox2.Add(left_box, flag=wx.ALIGN_LEFT)
        vbox.Add(hbox2, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        # Caixa de texto para texto processado
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        # Tela original de texto
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        hbox3.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # Nova tela para resumo
        self.summary_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        hbox3.Add(self.summary_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        vbox.Add(hbox3, proportion=1, flag=wx.EXPAND)

        # Contador de palavras para o texto original
        self.word_count_label = wx.StaticText(self, label="Palavras: 0")
        vbox.Add(self.word_count_label, flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, border=10)

        # Contador de palavras para o resumo
        self.summary_word_count_label = wx.StaticText(self, label="Palavras (Resumo): 0")
        vbox.Add(self.summary_word_count_label, flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, border=10)

        self.SetSizer(vbox)

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
            subtitle_file = self.subtitle_processor.download_subtitles(video_url)
            if subtitle_file:
                self.progress_bar.SetValue(70)
                consolidated_file = self.subtitle_processor.clean_and_consolidate_subtitles(subtitle_file)
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
        self.summary_ctrl.SetValue("")
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

    def OnSummarize(self, event):
        """Evento para resumir o texto (a funcionalidade será implementada depois)."""
        wx.MessageBox("Função de resumo ainda não implementada.", "Informação", wx.ICON_INFORMATION)

        # Exemplo de como contar palavras no texto resumido (após implementar o resumo)
        summary_content = self.summary_ctrl.GetValue()  # Texto do resumo
        summary_word_count = len(summary_content.split())
        self.summary_word_count_label.SetLabel(f"Palavras (Resumo): {summary_word_count}")
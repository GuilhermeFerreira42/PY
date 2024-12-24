import wx
import json
import os
import threading
from SubtitleProcessor import SubtitleProcessor
from HistorySidebar import HistorySidebar  # Importa a nova classe
from ChatIA import ChatIA

class YouTubePage(wx.Panel):
    def __init__(self, parent):
        super(YouTubePage, self).__init__(parent)
        self.subtitle_processor = SubtitleProcessor()
        self.history_sidebar = HistorySidebar(self)
        self.chat_ia = ChatIA()  # Instanciar a classe ChatIA
        self.is_sidebar_visible = True
        self.InitUI()

    def InitUI(self):
        vbox = wx.BoxSizer(wx.HORIZONTAL)

        # Botão discreto para expandir/colapsar a barra lateral (hamburger menu)
        self.toggle_button = wx.Button(self, label="☰")  # Usando um ícone de menu
        self.toggle_button.Bind(wx.EVT_BUTTON, self.OnToggleSidebar)
        self.toggle_button.SetSize((40, 40))  # Tamanho do botão
        vbox.Add(self.toggle_button, flag=wx.ALL, border=5)

        # Adiciona a barra lateral ao layout
        vbox.Add(self.history_sidebar, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # Pane para o conteúdo do YouTube
        content_box = wx.BoxSizer(wx.VERTICAL)

        # Linha para URL e botão "Colar"
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        self.url_label = wx.StaticText(self, label="URL do Vídeo:")
        hbox1.Add(self.url_label, flag=wx.RIGHT, border=8)
        self.url_text = wx.TextCtrl(self)
        hbox1.Add(self.url_text, proportion=1)
        
        self.paste_button = wx.Button(self, label="Colar")
        self.paste_button.Bind(wx.EVT_BUTTON, self.OnPaste)
        hbox1.Add(self.paste_button, flag=wx.LEFT, border=8)
        
        content_box.Add(hbox1, flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=10)

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
        content_box.Add(hbox2, flag=wx.EXPAND | wx.TOP | wx.BOTTOM, border=10)

        # Caixa de texto para texto processado
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)

        # Tela original de texto
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        hbox3.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        # Nova tela para resumo
        self.summary_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)
        hbox3.Add(self.summary_ctrl, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        content_box.Add(hbox3, proportion=1, flag=wx.EXPAND)

        # Contador de palavras para o texto original
        self.word_count_label = wx.StaticText(self, label="Palavras: 0")
        content_box.Add(self.word_count_label, flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, border=10)

        # Contador de palavras para o resumo
        self.summary_word_count_label = wx.StaticText(self, label="Palavras (Resumo): 0")
        content_box.Add(self.summary_word_count_label, flag=wx.ALIGN_RIGHT | wx.RIGHT | wx.BOTTOM, border=10)

        vbox.Add(content_box, proportion=3, flag=wx.EXPAND)

        self.SetSizer(vbox)

    def OnToggleSidebar(self, event):
        """Alterna a visibilidade da barra lateral."""
        if self.is_sidebar_visible:
            self.history_sidebar.Hide()  # Esconde a barra lateral
            self.toggle_button.SetLabel("☰")  # Mantém o ícone do botão
        else:
            self.history_sidebar.Show()  # Mostra a barra lateral
            self.toggle_button.SetLabel("☰")  # Mantém o ícone do botão
        self.is_sidebar_visible = not self.is_sidebar_visible  # Alterna o estado
        self.Layout()  # Atualiza o layout

    def LoadVideo(self, video_url, subtitles_path):
        """Carrega a URL e as legendas do vídeo selecionado."""
        self.url_text.SetValue(video_url)
        if os.path.exists(subtitles_path):
            with open(subtitles_path, 'r', encoding='utf-8') as subtitle_file:
                content = subtitle_file.read()
                self.text_ctrl.SetValue(content)
                # Contar palavras e atualizar o contador
                word_count = len(content.split())
                self.word_count_label.SetLabel(f"Palavras: {word_count}")

    def OnPaste(self, event):
        """Cola o conteúdo da área de transferência na URL e limpa o campo antes."""
        if wx.TheClipboard.Open():
            if wx.TheClipboard.IsSupported(wx.DataFormat(wx.DF_TEXT)):
                data = wx.TextDataObject()
                wx.TheClipboard.GetData(data)
                self.url_text.SetValue(data.GetText())
            wx.TheClipboard.Close()

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
        """Evento para resumir o texto."""
        original_text = self.text_ctrl.GetValue()
        if not original_text:
            wx.MessageBox("Não há texto para resumir.", "Erro", wx.ICON_ERROR)
            return

        try:
            # Gerar o resumo usando a classe ChatIA
            summary = self.chat_ia.generate_summary(original_text)
            self.summary_ctrl.SetValue(summary)  # Exibir o resumo na caixa de texto de resumo

            # Salvar o resumo no JSON
            video_name = self.GetVideoNameFromURL(self.url_text.GetValue())
            video_url = self.url_text.GetValue()  # Obtenha a URL do vídeo
            subtitles_path = "caminho/para/as/legendas"  # Substitua pelo caminho correto das legendas

            # Chame o método save_summary com todos os parâmetros necessários
            self.chat_ia.save_summary(video_name, video_url, subtitles_path, summary)

            wx.MessageBox("Resumo gerado e salvo com sucesso!", "Sucesso", wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Erro ao gerar resumo: {str(e)}", "Erro", wx.ICON_ERROR)

    def OnClear(self, event):
        """Limpa todos os campos e remove os arquivos de legendas armazenados."""
        self.url_text.SetValue("")
        self.text_ctrl.SetValue("")
        self.summary_ctrl.SetValue("")
        self.progress_bar.SetValue(0)
        self.word_count_label.SetLabel("Palavras: 0")

        # Limpar os arquivos de legendas na pasta
        subtitle_files = [f for f in os.listdir("história do YouTube") if f.endswith('.txt')]
        for file in subtitle_files:
            os.remove(os.path.join("história do YouTube", file))

        wx.MessageBox("Arquivos de legendas limpos.", "Informação", wx.ICON_INFORMATION)

    def GetVideoNameFromURL(self, url):
        """Obtém o nome do vídeo a partir da URL."""
        return url.split('v=')[-1]

    def SaveHistory(self, video_name, video_url, subtitles_path):
        """Salva o nome do vídeo, URL e caminho das legendas no histórico."""
        if not os.path.exists("história do YouTube"):
            os.makedirs("história do YouTube")

        history = []
        if os.path.exists(self.history_sidebar.history_file):
            with open(self.history_sidebar.history_file, 'r', encoding='utf-8') as file:
                history = json.load(file)

        # Adiciona o vídeo ao histórico
        history.append({
            "name": video_name,  # Aqui você já está usando o nome do vídeo
            "url": video_url,
            "subtitles": subtitles_path
        })

        with open(self.history_sidebar.history_file, 'w', encoding='utf-8') as file:
            json.dump(history, file, ensure_ascii=False, indent=4)
        

    def OnProcess(self, event):
        """Inicia o processamento do vídeo e atualiza o histórico na sidebar."""
        video_url = self.url_text.GetValue()
        if not video_url:
            wx.MessageBox("Por favor, insira uma URL do vídeo.", "Erro", wx.ICON_ERROR)
            return

        self.progress_bar.SetValue(10)  # Atualiza a barra de progresso

        def run():
            subtitle_file = self.subtitle_processor.download_subtitles(video_url)
            if subtitle_file:
                self.progress_bar.SetValue(70)
                # Extraindo o nome do vídeo sem a parte entre colchetes
                video_name = os.path.basename(subtitle_file).replace('.pt.vtt', '')  # Remove a extensão
                video_name = video_name.split('[')[0].strip()  # Remove a parte entre colchetes e espaços em branco
                consolidated_file = self.subtitle_processor.clean_and_consolidate_subtitles(subtitle_file, video_name)
                self.progress_bar.SetValue(100)
                if consolidated_file:
                    with open(consolidated_file, 'r', encoding='utf-8') as file:
                        content = file.read()
                    wx.CallAfter(self.text_ctrl.SetValue, content)

                    # Contar palavras e atualizar o contador
                    word_count = len(content.split())
                    wx.CallAfter(self.word_count_label.SetLabel, f"Palavras: {word_count}")

                    # Adicionar o nome do vídeo à sidebar e salvar o histórico
                    wx.CallAfter(self.history_sidebar.Append, video_name)  # Atualiza a barra lateral
                    self.SaveHistory(video_name, video_url, consolidated_file)  # Salva o histórico

                else:
                    wx.CallAfter(wx.MessageBox, "Erro ao consolidar as legendas.", "Erro", wx.ICON_ERROR)
            else:
                wx.CallAfter(wx.MessageBox, "Não foi possível obter as legendas.", "Erro", wx.ICON_ERROR)

        thread = threading.Thread(target=run)
        thread.start()
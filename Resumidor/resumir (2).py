import wx
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from nltk.tokenize import sent_tokenize

class TextSummarizerApp(wx.Frame):
    def __init__(self, *args, **kw):
        super(TextSummarizerApp, self).__init__(*args, **kw)
        self.setup_ui()

    def setup_ui(self):
        # Configurações da janela
        self.SetTitle("Resumidor de Texto com Contador de Palavras")
        self.SetSize(600, 500)

        # Painel principal
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Área de texto para entrada
        self.text_input = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        vbox.Add(self.text_input, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Contador de palavras para o texto de entrada
        self.word_count_label = wx.StaticText(panel, label="Palavras no texto de entrada: 0")
        vbox.Add(self.word_count_label, flag=wx.ALIGN_LEFT | wx.ALL, border=10)

        # Slider para selecionar o número de frases
        self.slider = wx.Slider(panel, value=3, minValue=3, maxValue=10, style=wx.SL_HORIZONTAL)
        vbox.Add(self.slider, flag=wx.EXPAND | wx.ALL, border=10)

        # Label para mostrar o número de frases selecionadas
        self.slider_label = wx.StaticText(panel, label="Número de Frases: 3")
        vbox.Add(self.slider_label, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Botão para processar o resumo
        process_button = wx.Button(panel, label="Processar Resumo")
        vbox.Add(process_button, flag=wx.ALIGN_CENTER | wx.ALL, border=10)

        # Conectar eventos
        self.text_input.Bind(wx.EVT_TEXT, self.update_word_count)
        process_button.Bind(wx.EVT_BUTTON, self.on_process)
        self.slider.Bind(wx.EVT_SLIDER, self.on_slider_change)
        
        panel.SetSizer(vbox)

    def update_word_count(self, event):
        # Atualiza o contador de palavras do texto de entrada
        text = self.text_input.GetValue()
        word_count = len(text.split())
        self.word_count_label.SetLabel(f"Palavras no texto de entrada: {word_count}")

    def on_slider_change(self, event):
        # Atualiza o label com o número de frases selecionadas
        self.slider_label.SetLabel(f"Número de Frases: {self.slider.GetValue()}")

    def on_process(self, event):
        # Obtém o texto da área de texto
        text = self.text_input.GetValue()
        num_sentences = self.slider.GetValue()

        # Chama a função de resumo
        if text:
            summary = self.summarize_text(text, num_sentences)
            self.show_summary_window(summary)
        else:
            wx.MessageBox("Insira o texto para resumir.", "Erro", wx.OK | wx.ICON_ERROR)

    def summarize_text(self, text, num_sentences):
        # Usa o Sumy para criar um resumo com TextRank
        sentences = sent_tokenize(text, language='portuguese')
        parser = PlaintextParser.from_string(' '.join(sentences), Tokenizer("portuguese"))
        summarizer = TextRankSummarizer()

        summary = summarizer(parser.document, num_sentences)
        summary_text = "\n".join(str(sentence) for sentence in summary)

        # Atualiza o contador de palavras do texto resumido
        self.summary_word_count = len(summary_text.split())
        
        return summary_text

    def show_summary_window(self, summary_text):
        # Cria uma nova janela para mostrar o resumo
        summary_frame = wx.Frame(None, title="Resumo do Texto", size=(400, 300))
        panel = wx.Panel(summary_frame)
        vbox = wx.BoxSizer(wx.VERTICAL)

        # Área de texto para exibir o resumo
        summary_display = wx.TextCtrl(panel, value=summary_text, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox.Add(summary_display, proportion=1, flag=wx.EXPAND | wx.ALL, border=10)

        # Contador de palavras para o texto resumido
        summary_word_count_label = wx.StaticText(panel, label=f"Palavras no resumo: {self.summary_word_count}")
        vbox.Add(summary_word_count_label, flag=wx.ALIGN_LEFT | wx.ALL, border=10)

        panel.SetSizer(vbox)
        summary_frame.Show()

if __name__ == "__main__":
    app = wx.App(False)
    frame = TextSummarizerApp(None)
    frame.Show()
    app.MainLoop()

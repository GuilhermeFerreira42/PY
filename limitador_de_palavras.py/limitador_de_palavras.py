import wx
import wx.stc

class LimitadorPalavrasApp(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title="Limitador de Palavras", size=(600, 700))

        # Criar painel principal
        panel = wx.Panel(self)
        
        # Criar sizer principal
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # Área de quantidade de palavras
        palavras_sizer = wx.BoxSizer(wx.HORIZONTAL)
        label_remover = wx.StaticText(panel, label="Quantidade de palavras:")
        self.entry_remover = wx.TextCtrl(panel, size=(200, -1))
        palavras_sizer.Add(label_remover, 0, wx.ALL | wx.CENTER, 5)
        palavras_sizer.Add(self.entry_remover, 1, wx.ALL | wx.EXPAND, 5)
        
        # Área de texto de entrada
        texto_label = wx.StaticText(panel, label="Insira o texto:")
        self.entry_texto = wx.stc.StyledTextCtrl(panel, size=(580, 150))
        self.entry_texto.SetWrapMode(wx.stc.STC_WRAP_WORD)
        self.entry_texto.SetMarginWidth(1, 0)

        # Área de texto de resultado
        resultado_label = wx.StaticText(panel, label="Texto processado:")
        self.entry_resultado = wx.stc.StyledTextCtrl(panel, size=(580, 150))
        self.entry_resultado.SetWrapMode(wx.stc.STC_WRAP_WORD)
        self.entry_resultado.SetMarginWidth(1, 0)
                
        # Botões principais
        botoes_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.btn_processar = wx.Button(panel, label="Processar")
        self.btn_proximo = wx.Button(panel, label="Próximo")
        self.btn_anterior = wx.Button(panel, label="Anterior")
        self.btn_limpar = wx.Button(panel, label="Limpar")
        botoes_sizer.Add(self.btn_processar, 0, wx.ALL, 5)
        botoes_sizer.Add(self.btn_anterior, 0, wx.ALL, 5)
        botoes_sizer.Add(self.btn_proximo, 0, wx.ALL, 5)
        botoes_sizer.Add(self.btn_limpar, 0, wx.ALL, 5)
        
        # Labels de contagem
        self.label_contagem_texto = wx.StaticText(panel, label="Palavras: 0")
        self.label_contagem_resultado = wx.StaticText(panel, label="Palavras: 0")
        self.label_contador_partes = wx.StaticText(panel, label="Parte 0 de 0")
        
        # Adicionar elementos ao sizer principal
        main_sizer.Add(palavras_sizer, 0, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(texto_label, 0, wx.ALL, 5)
        main_sizer.Add(self.entry_texto, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.label_contagem_texto, 0, wx.ALL, 5)
        main_sizer.Add(botoes_sizer, 0, wx.CENTER | wx.ALL, 5)
        main_sizer.Add(resultado_label, 0, wx.ALL, 5)
        main_sizer.Add(self.entry_resultado, 1, wx.EXPAND | wx.ALL, 5)
        main_sizer.Add(self.label_contagem_resultado, 0, wx.ALL, 5)
        main_sizer.Add(self.label_contador_partes, 0, wx.ALL, 5)
        
        # Configurar o sizer
        panel.SetSizer(main_sizer)
        
        # Centralizar a janela
        self.Center()
        
        # Bind de eventos
        self.entry_texto.Bind(wx.stc.EVT_STC_CHANGE, self.atualizar_contagem_texto)
        self.entry_resultado.Bind(wx.stc.EVT_STC_CHANGE, self.atualizar_contagem_resultado)
        self.btn_processar.Bind(wx.EVT_BUTTON, self.processar_texto)
        self.btn_proximo.Bind(wx.EVT_BUTTON, self.proximo)
        self.btn_anterior.Bind(wx.EVT_BUTTON, self.anterior)
        self.btn_limpar.Bind(wx.EVT_BUTTON, self.limpar_campos)
        
        # Variáveis para controle de partes
        self.texto_original = ""
        self.limite_palavras = 0
        self.partes = []
        self.parte_atual = 0
        
        # Mostrar a janela
        self.Show()

    def atualizar_contagem_texto(self, event):
        texto = self.entry_texto.GetText()
        self.label_contagem_texto.SetLabel(f"Palavras: {len(texto.split())}")
        event.Skip()

    def atualizar_contagem_resultado(self, event):
        texto = self.entry_resultado .GetText()
        self.label_contagem_resultado.SetLabel(f"Palavras: {len(texto.split())}")
        event.Skip()

    def processar_texto(self, event):
        try:
            self.limite_palavras = int(self.entry_remover.GetValue())
            texto = self.entry_texto.GetText().strip()
            self.texto_original = texto
            
            palavras = texto.split()
            self.partes = [' '.join(palavras[i:i + self.limite_palavras]) for i in range(0, len(palavras), self.limite_palavras)]
            self.parte_atual = 0
            
            self.mostrar_parte()
        except ValueError:
            wx.MessageBox("Por favor, insira um número válido.", "Erro", wx.OK | wx.ICON_ERROR)

    def mostrar_parte(self):
        if self.partes:
            parte_texto = self.partes[self.parte_atual]
            self.entry_resultado.SetText(parte_texto)
            self.label_contador_partes.SetLabel(f"Parte {self.parte_atual + 1} de {len(self.partes)}")

    def proximo(self, event):
        if self.parte_atual < len(self.partes) - 1:
            self.parte_atual += 1
            self.mostrar_parte()

    def anterior(self, event):
        if self.parte_atual > 0:
            self.parte_atual -= 1
            self.mostrar_parte()

    def limpar_campos(self, event):
        self.entry_remover.SetValue("")
        self.entry_texto.SetText("")
        self.entry_resultado.SetText("")
        self.label_contagem_texto.SetLabel("Palavras: 0")
        self.label_contagem_resultado.SetLabel("Palavras: 0")
        self.label_contador_partes.SetLabel("Parte 0 de 0")

if __name__ == "__main__":
    app = wx.App(False)
    frame = LimitadorPalavrasApp()
    app.MainLoop()

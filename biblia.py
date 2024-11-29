import wx
import re
import fitz  # PyMuPDF para ler PDF
from docx import Document

# Dicionário para conversão dos números para palavras (adicione todos até 150)
numeros_por_extenso = {
    1: "um.", 2: "dois.", 3: "três.", 4: "quatro.", 5: "cinco.", 6: "seis.", 7: "sete.", 8: "oito.", 9: "nove.", 10: "dez.",
    11: "onze.", 12: "doze.", 13: "treze.", 14: "quatorze.", 15: "quinze.", 16: "dezesseis.", 17: "dezessete.", 18: "dezoito.", 19: "dezenove.", 20: "vinte.",
    21: "vinte e um.", 22: "vinte e dois.", 23: "vinte e três.", 24: "vinte e quatro.", 25: "vinte e cinco.", 26: "vinte e seis.", 27: "vinte e sete.", 28: "vinte e oito.", 29: "vinte e nove.", 30: "trinta.",
    31: "trinta e um.", 32: "trinta e dois.", 33: "trinta e três.", 34: "trinta e quatro.", 35: "trinta e cinco.", 36: "trinta e seis.", 37: "trinta e sete.", 38: "trinta e oito.", 39: "trinta e nove.", 40: "quarenta.",
    41: "quarenta e um.", 42: "quarenta e dois.", 43: "quarenta e três.", 44: "quarenta e quatro.", 45: "quarenta e cinco.", 46: "quarenta e seis.", 47: "quarenta e sete.", 48: "quarenta e oito.", 49: "quarenta e nove.", 50: "cinquenta.",
    51: "cinquenta e um.", 52: "cinquenta e dois.", 53: "cinquenta e três.", 54: "cinquenta e quatro.", 55: "cinquenta e cinco.", 56: "cinquenta e seis.", 57: "cinquenta e sete.", 58: "cinquenta e oito.", 59: "cinquenta e nove.", 60: "sessenta.",
    61: "sessenta e um.", 62: "sessenta e dois.", 63: "sessenta e três.", 64: "sessenta e quatro.", 65: "sessenta e cinco.", 66: "sessenta e seis.", 67: "sessenta e sete.", 68: "sessenta e oito.", 69: "sessenta e nove.", 70: "setenta.",
    71: "setenta e um.", 72: "setenta e dois.", 73: "setenta e três.", 74: "setenta e quatro.", 75: "setenta e cinco.", 76: "setenta e seis.", 77: "setenta e sete.", 78: "setenta e oito.", 79: "setenta e nove.", 80: "oitenta.",
    81: "oitenta e um.", 82: "oitenta e dois.", 83: "oitenta e três.", 84: "oitenta e quatro.", 85: "oitenta e cinco.", 86: "oitenta e seis.", 87: "oitenta e sete.", 88: "oitenta e oito.", 89: "oitenta e nove.", 90: "noventa.",
    91: "noventa e um.", 92: "noventa e dois.", 93: "noventa e três.", 94: "noventa e quatro.", 95: "noventa e cinco.", 96: "noventa e seis.", 97: "noventa e sete.", 98: "noventa e oito.", 99: "noventa e nove.", 100: "cem.",
    101: "cento e um.", 102: "cento e dois.", 103: "cento e três.", 104: "cento e quatro.", 105: "cento e cinco.", 106: "cento e seis.", 107: "cento e sete.", 108: "cento e oito.", 109: "cento e nove.", 110: "cento e dez.",
    111: "cento e onze.", 112: "cento e doze.", 113: "cento e treze.", 114: "cento e quatorze.", 115: "cento e quinze.", 116: "cento e dezesseis.", 117: "cento e dezessete.", 118: "cento e dezoito.", 119: "cento e dezenove.", 120: "cento e vinte.",
    121: "cento e vinte e um.", 122: "cento e vinte e dois.", 123: "cento e vinte e três.", 124: "cento e vinte e quatro.", 125: "cento e vinte e cinco.", 126: "cento e vinte e seis.", 127: "cento e vinte e sete.", 128: "cento e vinte e oito.", 129: "cento e vinte e nove.", 130: "cento e trinta.",
    131: "cento e trinta e um.", 132: "cento e trinta e dois.", 133: "cento e trinta e três.", 134: "cento e trinta e quatro.", 135: "cento e trinta e cinco.", 136: "cento e trinta e seis.", 137: "cento e trinta e sete.", 138: "cento e trinta e oito.", 139: "cento e trinta e nove.", 140: "cento e quarenta.",
    141: "cento e quarenta e um.", 142: "cento e quarenta e dois.", 143: "cento e quarenta e três.", 144: "cento e quarenta e quatro.", 145: "cento e quarenta e cinco.", 146: "cento e quarenta e seis.", 147: "cento e quarenta e sete.", 148: "cento e quarenta e oito.", 149: "cento e quarenta e nove.", 150: "cento e cinquenta."
}


# Função para substituir o número após "Capítulo"
def substituir_numeros(texto):
    # Expressão regular para encontrar "Capítulo" seguido de um número, ignorando a capitalização
    padrao = re.compile(r'\b(Cap[ií]tulo)\s+(\d+)\b', re.IGNORECASE)
    
    def converter(match):
        capitulo = match.group(1)  # Pega "Capítulo" com a mesma capitalização do texto original
        numero = int(match.group(2))
        # Substitui o número por extenso apenas se estiver no dicionário
        if numero in numeros_por_extenso:
            return f"{capitulo} {numeros_por_extenso[numero]}"
        return match.group(0)  # Mantém o texto original se o número não estiver no dicionário
    
    return padrao.sub(converter, texto)

# Função para ler conteúdo do arquivo
def ler_arquivo(caminho):
    if caminho.endswith(".txt"):
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return arquivo.read()
    elif caminho.endswith(".pdf"):
        texto = ""
        with fitz.open(caminho) as pdf:
            for pagina in pdf:
                texto += pagina.get_text()
        return texto
    elif caminho.endswith(".docx"):
        doc = Document(caminho)
        texto = "\n".join(paragrafo.text for paragrafo in doc.paragraphs)
        return texto
    else:
        raise ValueError("Formato de arquivo não suportado.")

class JanelaPrincipal(wx.Frame):
    def __init__(self, *args, **kw):
        super(JanelaPrincipal, self).__init__(*args, **kw)
        self.init_ui()
        self.caminho_arquivo = None

    def init_ui(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        btn_selecionar = wx.Button(panel, label="Selecionar Arquivo")
        btn_selecionar.Bind(wx.EVT_BUTTON, self.on_selecionar_arquivo)
        vbox.Add(btn_selecionar, flag=wx.ALL | wx.CENTER, border=5)

        btn_substituir = wx.Button(panel, label="Substituir Números nos Capítulos")
        btn_substituir.Bind(wx.EVT_BUTTON, self.on_substituir)
        vbox.Add(btn_substituir, flag=wx.ALL | wx.CENTER, border=5)

        self.resultado_texto = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(500, 400))
        vbox.Add(self.resultado_texto, proportion=1, flag=wx.EXPAND | wx.ALL, border=5)

        panel.SetSizer(vbox)
        self.SetSize((600, 500))
        self.SetTitle("Substituidor de Números nos Capítulos")
        self.Centre()

    def on_selecionar_arquivo(self, event):
        with wx.FileDialog(self, "Abrir Arquivo", wildcard="Arquivos de texto e documentos (*.txt;*.pdf;*.docx)|*.txt;*.pdf;*.docx",
                           style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST) as dialog:
            if dialog.ShowModal() == wx.ID_OK:
                self.caminho_arquivo = dialog.GetPath()
                self.resultado_texto.SetValue(f"Arquivo selecionado: {self.caminho_arquivo}")

    def on_substituir(self, event):
        if not self.caminho_arquivo:
            wx.MessageBox("Selecione um arquivo primeiro!", "Erro", wx.ICON_ERROR)
            return

        try:
            conteudo = ler_arquivo(self.caminho_arquivo)
        except ValueError as e:
            wx.MessageBox(str(e), "Erro", wx.ICON_ERROR)
            return

        conteudo_modificado = substituir_numeros(conteudo)

        # Exibe o conteúdo modificado e salva em um novo arquivo
        self.resultado_texto.SetValue(conteudo_modificado)
        with open("livro_modificado.txt", "w", encoding="utf-8") as arquivo_modificado:
            arquivo_modificado.write(conteudo_modificado)

        wx.MessageBox("Substituição concluída! Arquivo salvo como 'livro_modificado.txt'.", "Concluído", wx.ICON_INFORMATION)

# Execução do aplicativo
if __name__ == "__main__":
    app = wx.App(False)
    frame = JanelaPrincipal(None)
    frame.Show()
    app.MainLoop()

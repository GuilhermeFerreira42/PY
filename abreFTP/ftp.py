import tkinter as tk
import subprocess
import os
from tkinter import messagebox

def ping(host):
    command = ['ping', '-n', '1', host]  # '-n' para Windows
    result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def abrir_ftp(url):
    subprocess.Popen(['explorer', url])

def abrir_pasta(caminho):
    host = "192.168.1.254"
    if ping(host):
        if os.path.exists(caminho):
            os.startfile(caminho)
        else:
            messagebox.showerror("Erro", f"Caminho {caminho} não acessível.")
    else:
        messagebox.showerror("Erro", f"Servidor {host} não está acessível.")

def sair():
    janela.quit()

# Criar a janela principal
janela = tk.Tk()
janela.title("Menu de Tarefas")
janela.geometry("500x600")  # Tamanho fixo da janela
janela.configure(bg='#444444')
janela.resizable(False, False)  # Impede redimensionamento

# Título
titulo = tk.Label(janela, text="[ MENU DE TAREFAS ]", bg='#444444', fg='#FFFFFF', font=("Arial", 16))
titulo.pack(pady=10)

# Botões
botoes = [
    ("FTP SG", lambda: abrir_ftp(r"ftp://sg:$up04t3SG@ftp.sgsistemas.com.br")),
    ("FTP RJK", lambda: abrir_ftp(r"ftp://rjk:rjk2015@ftp.sgsistemas.com.br")),
    ("FTP UTIL", lambda: abrir_ftp(r"ftp://util:util@ftp.sgsistemas.com.br")),
    ("FTP UTIL TEF", lambda: abrir_ftp(r"ftp://util:util@ftp.sgsistemas.com.br/tef")),
    ("EXES 254", lambda: abrir_pasta(r"\\192.168.1.254\_exes_")),
    ("SUPER_OK 254", lambda: abrir_pasta(r"\\192.168.1.254\_exes_\versao_super_ok")),
    ("OK 254", lambda: abrir_pasta(r"\\192.168.1.254\_exes_\versao_ok")),
    ("BETA 254", lambda: abrir_pasta(r"\\192.168.1.254\_exes_\versao_beta")),
    ("TRUNK 254", lambda: abrir_pasta(r"\\192.168.1.254\_exes_\versao_trunk")),
    ("SAIR", sair)
]

# Adicionar os botões à janela
for nome, comando in botoes:
    botao = tk.Button(janela, text=nome, command=comando, width=40, height=2, bg='#006666', fg='#FFFFFF', font=("Arial", 10))
    botao.pack(pady=5)

# Iniciar o loop da interface
janela.mainloop()

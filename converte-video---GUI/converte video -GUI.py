import os
import json
import subprocess
import threading
from tkinter import Tk, filedialog, Button, Label, Entry, StringVar, Menu, messagebox, DoubleVar, Scrollbar
from tkinter.ttk import Progressbar, Treeview
import queue
import time

# Variáveis globais
stop_processing = threading.Event()
process_queue = queue.Queue()
video_counter = 1  # Contador global para os vídeos

# Caminhos para memória persistente
paths_file = "paths.json"

# Função para carregar caminhos salvos
def load_paths():
    if os.path.exists(paths_file):
        with open(paths_file, "r") as f:
            return json.load(f)
    return {"output_path": ""}

# Função para salvar caminhos
def save_paths(output_path):
    with open(paths_file, "w") as f:
        json.dump({"output_path": output_path}, f)

def convert_video(video_path, output_path, format, progress_var):
    output_file = os.path.join(output_path, os.path.splitext(os.path.basename(video_path))[0] + '.' + format)
    command = ['ffmpeg', '-i', video_path, output_file]
    
    # Executa o processo de conversão em uma thread separada e atualiza a barra de progresso
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    while True:
        output = process.stderr.read(1024).decode('utf-8')
        if output == '' and process.poll() is not None:
            break
        if output:
            # Aqui podemos analisar a saída para atualizar a barra de progresso
            if "time=" in output:
                time_str = output.split("time=")[-1].split(" ")[0]
                current_time = time_str_to_seconds(time_str)
                duration = get_video_duration(video_path)
                progress_percentage = (current_time / duration) * 100
                progress_var.set(progress_percentage)
                root.update_idletasks()
    
    progress_var.set(100)  # Define o progresso como concluído

def time_str_to_seconds(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s)

def get_video_duration(video_path):
    result = subprocess.run(['ffmpeg', '-i', video_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    duration_str = [x for x in result.stderr.splitlines() if "Duration" in x][0].split("Duration: ")[1].split(",")[0]
    return time_str_to_seconds(duration_str)

def process_videos(video_paths, output_dir, format, progress_var):
    for index, video_path in enumerate(video_paths, start=video_counter):
        if stop_processing.is_set():
            break

        update_status(index, "Processando")

        convert_video(video_path, output_dir, format, progress_var)

        update_status(index, "Concluído")

def update_status(index, status):
    for item in video_list.get_children():
        if video_list.item(item, 'values')[0] == index:
            video_list.item(item, values=(index, video_list.item(item, 'values')[1], status))
            break

def start_processing():
    video_paths = [video_list.item(item, 'values')[1] for item in video_list.get_children()]
    output_dir = output_path.get()
    format = format_var.get()

    if not video_paths or not output_dir or not format:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        return

    progress_var.set(0)  # Reseta a barra de progresso
    stop_processing.clear()  # Limpa o evento de parar antes de iniciar

    def worker():
        try:
            process_videos(video_paths, output_dir, format, progress_var)
            messagebox.showinfo("Concluído", "O processamento dos vídeos foi concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro: {e}")

    global processing_thread
    processing_thread = threading.Thread(target=worker, daemon=True)
    processing_thread.start()
    messagebox.showinfo("Início", "O processamento dos vídeos foi iniciado.")

def stop_processing_videos():
    stop_processing.set()  # Sinaliza para parar o processamento
    if processing_thread.is_alive():
        process_queue.put("stop")  # Coloca uma mensagem de parada na fila
        processing_thread.join(timeout=5)  # Espera até 5 segundos para terminar a thread
    messagebox.showinfo("Parado", "O processamento dos vídeos foi interrompido.")

def select_videos():
    global video_counter
    video_paths = filedialog.askopenfilenames(title="Selecione os vídeos", filetypes=[("Todos os arquivos", "*.*")])
    if video_paths:
        for path in video_paths:
            video_list.insert("", "end", values=(video_counter, path, "Não Processado"))
            video_counter += 1  # Incrementa o contador

def select_output_dir():
    output_dir = filedialog.askdirectory(title="Selecione o diretório de saída")
    if output_dir:
        output_path.set(output_dir)
        save_paths(output_dir)

def clear_list():
    global video_counter
    video_list.delete(*video_list.get_children())
    video_counter = 1  # Reinicia o contador

def remove_selected_video():
    selected_items = video_list.selection()
    for item in selected_items:
        video_list.delete(item)

def setup_right_click_menu():
    menu = Menu(root, tearoff=0)
    menu.add_command(label="Remover vídeo selecionado", command=remove_selected_video)
    def show_menu(event):
        menu.post(event.x_root, event.y_root)
    video_list.bind("<Button-3>", show_menu)

def main():
    global video_list, output_path, progress_var, format_var, root, processing_thread

    root = Tk()
    root.title("Conversor de Vídeo")

    # Carrega caminhos salvos
    saved_paths = load_paths()

    # Botão "Selecionar vídeos"
    Button(root, text="Selecionar vídeos", command=select_videos).pack(pady=5)

    # Configura lista de vídeos com colunas
    video_list = Treeview(root, columns=("Índice", "Caminho", "Status"), show='headings', selectmode="extended")
    video_list.heading("Índice", text="Índice")
    video_list.heading("Caminho", text="Caminho")
    video_list.heading("Status", text="Status")
    video_list.pack(pady=5, fill='both', expand=True)

    # Barra de rolagem
    scrollbar = Scrollbar(root, orient="vertical", command=video_list.yview)
    scrollbar.pack(side='right', fill='y')
    video_list.configure(yscrollcommand=scrollbar.set)

    # Configura menu de clique direito
    setup_right_click_menu()

    # Campo "Caminho de saída"
    Label(root, text="Caminho de saída:").pack(pady=5)
    output_path = StringVar(value=saved_paths.get("output_path", ""))
    Entry(root, textvariable=output_path).pack(pady=5)
    Button(root, text="Selecionar pasta de saída", command=select_output_dir).pack(pady=5)

    # Menu de seleção de formato
    Label(root, text="Escolha o formato de saída:").pack(pady=5)
    format_var = StringVar(value="mp4")  # Formato padrão
    format_menu = Menu(root, tearoff=0)
    for format in ["mp4", "avi", "mkv", "mov", "flv", "wmv"]:
        format_menu.add_radiobutton(label=format, variable=format_var)
    Button(root, text="Escolher formato", command=lambda: format_menu.post(root.winfo_rootx(), root.winfo_rooty())).pack(pady=5)

    # Botão "Limpar lista"
    Button(root, text="Limpar lista", command=clear_list).pack(pady=5)

    # Barra de progresso
    progress_var = DoubleVar()
    progress = Progressbar(root, orient="horizontal", length=400, mode="determinate", variable=progress_var)
    progress.pack(pady=10)

    # Botão "Executar"
    Button(root, text="Executar", command=start_processing).pack(pady=20)

    # Botão "Parar"
    Button(root, text="Parar", command=stop_processing_videos).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    main()

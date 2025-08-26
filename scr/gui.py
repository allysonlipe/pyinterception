import tkinter as tk
from tkinter import ttk, messagebox
import threading
import interception
import keyboard
import time

interception.auto_capture_devices()

running = False
configs = []
modo_ativo = False  # controle do F12

def clique_esquerdo():
    interception.click(button="left")
    print("[INFO] Clique esquerdo enviado")

def escutar():
    global running, configs
    print("[INFO] Escutando... pressione 'Parar' ou F12 novamente para encerrar")
    while running:
        try:
            for tecla, usar_mouse in configs:
                if keyboard.is_pressed(tecla):
                    interception.press(tecla)
                    if usar_mouse:
                        clique_esquerdo()
                    time.sleep(0.1)
        except:
            pass
        time.sleep(0.01)

def iniciar():
    global running, configs, modo_ativo
    configs.clear()
    for item in tabela.get_children():
        valores = tabela.item(item)["values"]
        tecla = str(valores[0]).strip().lower()
        usar_mouse = valores[1] == "Sim"
        if tecla:
            configs.append((tecla, usar_mouse))

    if not configs:
        lbl_status.config(text="Nenhuma configuração válida!", foreground="red")
        return

    if not running:
        running = True
        threading.Thread(target=escutar, daemon=True).start()
        lbl_status.config(text="Modo turbo ATIVO", foreground="green")
        modo_ativo = True

def parar():
    global running, modo_ativo
    running = False
    modo_ativo = False
    lbl_status.config(text="Parado", foreground="gray")

def adicionar_linha():
    tabela.insert("", "end", values=("", "Não"))

def remover_linha():
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Atenção", "Selecione uma linha para remover.")
        return
    for item in selecionado:
        tabela.delete(item)

def alternar_clique(event):
    item = tabela.selection()[0]
    valores = tabela.item(item)["values"]
    atual = valores[1]
    novo = "Sim" if atual == "Não" else "Não"
    tabela.item(item, values=(valores[0], novo))

def editar_tecla(event):
    item = tabela.selection()[0]
    valores = tabela.item(item)["values"]
    entry_tecla_popup = tk.Entry(janela)
    entry_tecla_popup.insert(0, valores[0])

    def salvar():
        nova_tecla = entry_tecla_popup.get()
        tabela.item(item, values=(nova_tecla, valores[1]))
        entry_tecla_popup.destroy()

    entry_tecla_popup.bind("<Return>", lambda e: salvar())
    entry_tecla_popup.place(x=event.x_root - janela.winfo_rootx(),
                            y=event.y_root - janela.winfo_rooty())

def toggle_f12_hotkey():
    global modo_ativo
    if modo_ativo:
        parar()
    else:
        iniciar()

# Ativação da hotkey F12
def iniciar_hotkey_f12():
    keyboard.add_hotkey('f12', toggle_f12_hotkey)

# GUI
janela = tk.Tk()
janela.title("Turbo Key GUI - Tabela")
janela.geometry("420x380")

frame = ttk.Frame(janela, padding=10)
frame.pack(expand=True, fill="both")

# Tabela
tabela = ttk.Treeview(frame, columns=("Tecla", "Clique"), show="headings", height=8)
tabela.heading("Tecla", text="Tecla")
tabela.heading("Clique", text="Ativar Clique")
tabela.pack(pady=10, fill="x")

tabela.column("Tecla", width=180, anchor="center")
tabela.column("Clique", width=100, anchor="center")

tabela.bind("<Double-1>", editar_tecla)
tabela.bind("<Button-3>", alternar_clique)

# Botões
btn_frame = ttk.Frame(frame)
btn_frame.pack(pady=5)

btn_adicionar = ttk.Button(btn_frame, text="Adicionar Linha", command=adicionar_linha)
btn_adicionar.grid(row=0, column=0, padx=5)

btn_remover = ttk.Button(btn_frame, text="Remover Linha", command=remover_linha)
btn_remover.grid(row=0, column=1, padx=5)

btn_iniciar = ttk.Button(btn_frame, text="Iniciar", command=iniciar)
btn_iniciar.grid(row=0, column=2, padx=5)

btn_parar = ttk.Button(btn_frame, text="Parar", command=parar)
btn_parar.grid(row=0, column=3, padx=5)

lbl_status = ttk.Label(frame, text="Aguardando...", foreground="gray")
lbl_status.pack(pady=5)

# Linha inicial
adicionar_linha()

# Hotkey F12
threading.Thread(target=iniciar_hotkey_f12, daemon=True).start()

janela.mainloop()

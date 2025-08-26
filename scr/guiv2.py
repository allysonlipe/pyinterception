import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading, interception, keyboard, time, json

interception.auto_capture_devices()

running = False
configs = []
modo_ativo = False  # controle do F12

print('Macro funcionando')

def clique_esquerdo():
    interception.click(button="left")
    # print("[INFO] Clique esquerdo enviado")


def escutar():
    global running, configs
    while running:
        try:
            for tecla, usar_mouse in configs:
                # Se a tecla estiver pressionada...
                if keyboard.is_pressed(tecla):
                    # Ignora se houver algum modificador pressionado
                    if any([
                        keyboard.is_pressed("alt"),
                        keyboard.is_pressed("ctrl"),
                        keyboard.is_pressed("shift"),
                        keyboard.is_pressed("windows")
                    ]):
                        continue  # volta ao loop, ignora esta tecla

                    # Enquanto a tecla continuar pressionada...
                    while keyboard.is_pressed(tecla):
                        interception.press(tecla)
                        if usar_mouse:
                            clique_esquerdo()
                        time.sleep(0.1)  # intervalo entre execuções
        except:
            pass
        time.sleep(0.01)  # pequena pausa para não travar o CPU


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

    # Cria a janelinha modal
    popup = tk.Toplevel(janela)
    popup.title("Editar Tecla")
    popup.geometry("250x120")
    popup.grab_set()  # Torna modal (bloqueia o resto)
    
    popup.bind("<Escape>", lambda e: popup.destroy())

    # Centraliza a janela na tela
    popup.update_idletasks()
    x = janela.winfo_rootx() + (janela.winfo_width() // 2) - 125
    y = janela.winfo_rooty() + (janela.winfo_height() // 2) - 60
    popup.geometry(f"+{x}+{y}")

    ttk.Label(popup, text="Digite a nova tecla:").pack(pady=10)

    entry = ttk.Entry(popup)
    entry.insert(0, valores[0])
    entry.pack()


    def salvar():
        nova_tecla = entry.get().strip().lower()
        if nova_tecla:
            tabela.item(item, values=(nova_tecla, valores[1]))
        popup.destroy()

    btn_salvar = ttk.Button(popup, text="Salvar", command=salvar)
    btn_salvar.pack(pady=10)

    entry.focus_set()
    entry.bind("<Return>", lambda e: salvar())

def carregar_perfil():
    arquivo = filedialog.askopenfilename(
        defaultextension=".json",
        filetypes=[("Perfis Turbo", "*.json")],
        title="Carregar Perfil"
    )

    if not arquivo:
        return

    try:
        with open(arquivo, "r", encoding="utf-8") as f:
            dados = json.load(f)

        tabela.delete(*tabela.get_children())
        for item in dados:
            tecla = item.get("tecla", "")
            clique = "Sim" if item.get("clique", False) else "Não"
            tabela.insert("", "end", values=(tecla, clique))

        lbl_status.config(text=f"Perfil carregado com sucesso", foreground="blue")

    except Exception as e:
        messagebox.showerror("Erro ao carregar", f"Não foi possível carregar o perfil:\n{e}")


def toggle_f12_hotkey():
    global modo_ativo
    if modo_ativo:
        parar()
    else:
        iniciar()


# Ativação da hotkey F12
def iniciar_hotkey_f12():
    keyboard.add_hotkey("f12", toggle_f12_hotkey)


def salvar_perfil():
    dados = []
    for item in tabela.get_children():
        valores = tabela.item(item)["values"]
        dados.append({"tecla": valores[0], "clique": valores[1] == "Sim"})

    arquivo = filedialog.asksaveasfilename(
        defaultextension=".json",
        filetypes=[("Perfis Turbo", "*.json")],
        title="Salvar Perfil",
    )

    if arquivo:
        with open(arquivo, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=4)
        lbl_status.config(text=f"Perfil salvo!", foreground="blue")


# GUI
janela = tk.Tk()
janela.title("Turbo Key GUI - Tabela")
janela.geometry("800x600")

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

# Criação da barra de menu
menu_bar = tk.Menu(janela)
janela.config(menu=menu_bar)

# Menu "Arquivo"
menu_arquivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Arquivo", menu=menu_arquivo)

menu_arquivo.add_command(label="Carregar Perfil", command=carregar_perfil)
menu_arquivo.add_command(label="Salvar Perfil", command=salvar_perfil)
menu_arquivo.add_separator()
menu_arquivo.add_command(label="Sair", command=janela.destroy)

# Linha inicial
adicionar_linha()

# Hotkey F12
threading.Thread(target=iniciar_hotkey_f12, daemon=True).start()

janela.mainloop()

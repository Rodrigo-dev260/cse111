import tkinter as tk
from bot_controller import iniciar_bot, parar_bot

def iniciar():
    habilidades = entrada_habilidades.get().split(',')
    tempo = int(entrada_tempo.get())
    iniciar_bot(habilidades, tempo)

def parar():
    parar_bot()

janela = tk.Tk()
janela.title("Bot MIR4 - Fogo na Canjica")

tk.Label(janela, text="Habilidades (ex: 1,2,3):").pack()
entrada_habilidades = tk.Entry(janela)
entrada_habilidades.pack()

tk.Label(janela, text="Tempo de farm (segundos):").pack()
entrada_tempo = tk.Entry(janela)
entrada_tempo.pack()

tk.Button(janela, text="Iniciar", command=iniciar).pack()
tk.Button(janela, text="Parar", command=parar).pack()

janela.mainloop()

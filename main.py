from tkinter import *
from tkinter import messagebox
import random
import math
import pandas

WORK_MIN = 1
timer = None
texto = ""
total_clicks = 0
clicks_corretos = 0

frases = pandas.read_csv("data/frases.csv", sep=";")

# ---------------------------- ESCOLHE FRASE ------------------------------- #
def random_frase():
    frase = random.choice(frases["Frase"])
    return frase

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global texto
    texto = ""
    frase = random_frase()
    canvas.itemconfig(frase_text, text=frase)
    canvas.itemconfig(resposta_text, text="")

    work_sec = WORK_MIN * 60
    count_down(work_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global timer

    count_min = math.floor(count / 60)
    count_sec = count % 60
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    canvas.itemconfig(timer_text, text=f"{count_min}:{count_sec}")
    if count > 0:
        timer = window.after(1000, count_down, count - 1)
    else:
        messagebox.showinfo(title="Tempo", message="Acabou o tempo")
        wpm = (total_clicks/5)/1
        presicao = (clicks_corretos/total_clicks) * 100
        canvas.itemconfig(frase_text, text=f"Sua velocidade foi de {wpm} wpm e {presicao:.2f}% de precição", fill="black")

# ---------------------------- CAPITURAR TECLA DIGITADA E MOSTRA NO CANVAS ------------------------------- #
def palavra_digitada(event):
    global texto
    global total_clicks
    global clicks_corretos

    if event.keysym == "BackSpace":
        texto = texto[0:-1]
        total_clicks += 1
    else:
        texto = texto + event.char
        total_clicks += 1
        clicks_corretos += 1

    verificar_texto(texto)
    canvas.itemconfig(resposta_text, text=texto)

# ---------------------------- VERIFICAR SE DIGITADO IGUAL A FRASE ------------------------------- #
def verificar_texto(frase_escrita):
    frase_escolhida = canvas.itemcget(frase_text, "text")
    if frase_escrita[-1] == frase_escolhida[0]:
        resto_frase = frase_escolhida[1:]
        canvas.itemconfig(frase_text, text=resto_frase, fill="#04F500")
    else:
        canvas.itemconfig(frase_text, text=frase_escolhida, fill="#e7305b")


window = Tk()
window.title("Velocidade digitação")
window.config(padx=40, pady=40)

canvas = Canvas(width=500, height=300, bg="#b0b1b0")
timer_text = canvas.create_text(250, 30, text="00:00", fill="black", font=("arial", 20, "bold"))
canvas.grid(column=0, row=0, columnspan=2)
frase_text =  canvas.create_text(250, 100,text="click em iniciar", fill="black", font=("arial", 12), width=500)
resposta_text =  canvas.create_text(250, 250,text="", fill="black", font=("arial", 12), width=500)
canvas.grid(column=0, row=1,columnspan=2)

botao_started = Button(window,text="Iniciar",width=15, command=start_timer)
botao_started.grid(row=3, column=0, columnspan=2)

window.bind("<Key>", palavra_digitada)

window.mainloop()
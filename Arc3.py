import tkinter
from tkinter import messagebox
import os
import pandas
import random
import copy
import FuncionesJuego

default_font = ("Arial", 16)


# region Funciones
def null_func():
    return


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")


def agregar_archivo(bfoo, efoo):
    if bfoo.cget("relief") == "raised":
        bfoo.config(relief="sunken", text="Seleccionado")
        efoo.config(state="normal")
    else:
        bfoo.config(relief="raised", text="Deseleccionado")
        efoo.delete(0, tkinter.END)
        efoo.config(state="disabled")


def add_total():
    counter_cero = 0
    for _ in range(len(archivos_excel)):
        if entry_list_root[_].cget("state") == "disabled":
            binarios_root1[_] = 0
        else:
            binarios_root1[_] = 1
    for _ in range(len(binarios_root1)):
        if binarios_root1[_] == 0:
            counter_cero += 1
    if counter_cero == len(binarios_root1):
        btn.config(state="disabled")
        tkinter.messagebox.showinfo(message="Favor de seleccionar al menos una categoría")
        lbl_num_total.config(text="0")
        return
    for _ in range(len(archivos_excel)):
        if entry_list_root[_].get() == "":
            binarios_root2[_] = len(matrices_excel[_])
        else:
            try:
                if (int(entry_list_root[_].get()) > len(matrices_excel[_])) or \
                        (int(entry_list_root[_].get()) < 1):
                    btn.config(state="disabled")
                    tkinter.messagebox.showinfo(message="Favor de no ingresar números mayores al número total de "
                                                        "preguntas por categoría ni menores a uno.")
                    return
                else:
                    binarios_root2[_] = int(entry_list_root[_].get())
            except ValueError:
                btn.config(state="disabled")
                tkinter.messagebox.showinfo(message="Favor de sólo ingresar números.")
                return
    suma = 0
    for _ in range(len(archivos_excel)):
        if binarios_root1[_] == 1:
            suma += binarios_root2[_]
    lbl_num_total.config(text=str(suma))
    if btn.cget("state") == "disabled":
        btn.config(state="normal")
    print(binarios_root1)
    print(binarios_root2)
    print(suma)
    return binarios_root1, binarios_root2, suma


def iniciar():

    def desbloq():
        if btn_salir["state"] == "disabled":
            btn_salir.config(state="normal")
            btn_toggle.config(text="Bloquear")
        else:
            btn_salir.config(state="disabled")
            btn_toggle.config(text="Desbloquear")

    def quitter():
        pantalla_juego.destroy()
        btn["state"] = "normal"
        btn_total["state"] = "normal"
        root.protocol("WM_DELETE_WINDOW", root.destroy)

    resultados_root = add_total()  # binarios_root1, binarios_root2, suma
    if resultados_root is not None:
        if btn.cget("state") == "normal":
            btn.config(state="disabled")
        if btn_total.cget("state") == "normal":
            btn_total.config(state="disabled")
        root.protocol("WM_DELETE_WINDOW", null_func)
        pantalla_juego = tkinter.Tk()
        pantalla_juego.protocol("WM_DELETE_WINDOW", null_func)
        pantalla_juego.title("Juego de repaso")
        lista_entradas_total = []  # Lista de las preguntas a preguntar.
        preguntas = []
        correctas = []
        respuestas = []
        incorrectas = []
        for _ in range(len(matrices_excel)):
            if binarios_root1[_] == 1:
                lista_entradas_total_aux = copy.copy(matrices_excel[_])
                random.shuffle(lista_entradas_total_aux)
                [lista_entradas_total.append(lista_entradas_total_aux[__]) for __ in range(binarios_root2[_])]
                lista_entradas_total_aux = []
        random.shuffle(lista_entradas_total)
        [preguntas.append(lista_entradas_total[_][0]) for _ in range(len(lista_entradas_total))]
        [correctas.append(lista_entradas_total[_][1]) for _ in range(len(lista_entradas_total))]
        for _ in range(len(lista_entradas_total)):
            respuestas_aux1 = []
            [respuestas_aux1.append(lista_entradas_total[_][__+1]) for __ in range(4)]
            random.shuffle(respuestas_aux1)
            respuestas.append(respuestas_aux1)
            respuestas_aux1 = []
        contador = 0
        puntos = 0
        btn_toggle = tkinter.Button(pantalla_juego, text="Desbloquear", command=desbloq)
        btn_salir = tkinter.Button(pantalla_juego, text="Terminar", state="disabled", command=quitter)
        btn_sig = tkinter.Button(pantalla_juego, text="Siguiente", state="disabled")
        lbl_pregunta = tkinter.Label(pantalla_juego)
        btn_toggle.grid(row=5, column=0)
        btn_salir.grid(row=6, column=0)
        btn_sig.grid(row=5, column=2, rowspan=2)
        lbl_pregunta.grid(row=0, column=2)
        FuncionesJuego.puntaje(preguntas, correctas, respuestas, pantalla_juego,
                               incorrectas, btn_sig, contador, puntos, lbl_pregunta)
        center_window(pantalla_juego, 100, 100)
        print(lista_entradas_total)
        print(preguntas, correctas)
        print(respuestas)

    else:
        return
# endregion


root = tkinter.Tk()
root.title("Inicio")

button_list_root = []
entry_list_root = []

main_dir = "directory_excel_files"

matrices_excel = []
archivos_excel = []  # Nombres de los archivos como str.
for _ in os.listdir(main_dir):
    if _.endswith(".xlsx"):
        archivos_excel.append(_)
        matrices_excel.append(pandas.read_excel(os.path.join(main_dir, _)).values.tolist())

lbl_num_total = tkinter.Label(root, text="0", font=default_font)
lbl_archivo = tkinter.Label(root, text="Archivo", font=default_font)
lbl_max = tkinter.Label(root, text="Preguntas totales", font=default_font)
lbl_deseadas = tkinter.Label(root, text="Preguntas deseadas", font=default_font)
lbl_num_total.grid(row=(len(matrices_excel)+1), column=2)
lbl_archivo.grid(row=0, column=1)
lbl_max.grid(row=0, column=2)
lbl_deseadas.grid(row=0, column=3)
binarios_root1 = []
binarios_root2 = []

for _ in range(len(archivos_excel)):
    lbl1 = tkinter.Label(root, text=os.path.splitext(archivos_excel[_])[0], font=default_font)
    lbl2 = tkinter.Label(root, text=len(matrices_excel[_]), font=default_font)
    entry1 = tkinter.Entry(root, state="disabled", font=default_font)
    entry_list_root.append(entry1)
    btn_selec = tkinter.Button(root, text="Deseleccionado", font=default_font)
    button_list_root.append(btn_selec)
    button_list_root[_].config(command=lambda b=button_list_root[_], e=entry_list_root[_]: agregar_archivo(b, e))
    lbl1.grid(row=_+1, column=1)
    lbl2.grid(row=_+1, column=2)
    entry1.grid(row=_+1, column=3)
    btn_selec.grid(row=_+1, column=0)
    binarios_root1.append(0)
    binarios_root2.append(len(matrices_excel[_]))

lbl_total = tkinter.Label(root, text="Total", font=default_font)
lbl_total.grid(row=(len(matrices_excel)+1), column=1)

btn = tkinter.Button(root, text="Iniciar juego", state="disabled", command=iniciar, font=default_font)
btn_total = tkinter.Button(root, text="Calcular Total", command=add_total, font=default_font)
btn.grid(row=(len(matrices_excel)+2), column=2)
btn_total.grid(row=(len(matrices_excel)+1), column=0)
center_window(root, 800, 100+50*len(matrices_excel))

root.mainloop()

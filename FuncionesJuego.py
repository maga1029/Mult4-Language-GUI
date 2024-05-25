# region Import
import tkinter
from tkinter import scrolledtext


def termino(foobot, foowin, foolbl, inc, preg, respcorr, foopoints):
    foobot.destroy()
    foolbl.destroy()

    calif = round((foopoints/len(preg))*10, 2)
    label_calif = tkinter.Label(foowin, text=f"Calificación: {calif}")
    label_calif.grid(row=1, column=0)

    scroll = scrolledtext.ScrolledText(foowin, wrap=tkinter.WORD, bg="#d9d9d9", font=("Arial", 16))
    scroll.grid(row=2, column=0, sticky="nsew")

    for _ in range(len(inc)):
        pregunta_texto = f"Pregunta incorrecta: {preg[inc[_]]}"
        respuesta_texto = f"Respuesta correcta: {respcorr[inc[_]]}"
        if _ != len(inc)-1:
            scroll.insert(tkinter.END, pregunta_texto+"\n"+respuesta_texto+"\n\n")
            scroll.tag_configure(f"pg_{_}", font=("Arial", 16, "bold"), foreground="red")
            scroll.tag_configure(f"rsp_{_}", font=("Arial", 16, "bold"), foreground="green")
            scroll.tag_add(f"pg_{_}", f"{_ * 3 + 1}.0", f"{_ * 3 + 1}.20")
            scroll.tag_add(f"rsp_{_}", f"{_ * 3 + 2}.0", f"{_ * 3 + 2}.19")
        else:
            scroll.insert(tkinter.END, pregunta_texto+"\n"+respuesta_texto+"\n")
            scroll.tag_configure(f"pg_{_}", font=("Arial", 16, "bold"), foreground="red")
            scroll.tag_configure(f"rsp_{_}", font=("Arial", 16, "bold"), foreground="green")
            scroll.tag_add(f"pg_{_}", f"{_ * 3 + 1}.0", f"{_ * 3 + 1}.20")
            scroll.tag_add(f"rsp_{_}", f"{_ * 3 + 2}.0", f"{_ * 3 + 2}.19")

    scroll.config(state="disabled")


def puntaje(p, c, r, w, i, b, counter, points, lbl2):
    counter += 1

    def fun_btn(foo, points, l1):
        for _ in range(4):
            lista_btn[_].config(state="disabled")
        if lista_btn[foo].cget("text") == c[counter-1]:
            lista_btn[foo].config(bg="green")
            points += 1
            l1.config(text=f"Puntaje: {points}/{len(p)}")
        else:
            lista_btn[foo].config(bg="red")
            i.append(counter-1)
            for _ in range(4):
                if lista_btn[_].cget("text") == c[counter-1]:
                    lista_btn[_].config(bg="green")
        if (counter-1) != len(p):
            b["state"] = "normal"
        else:
            b.destroy()

        def fun_sig(butn, lab, listbt):
            lab.destroy()
            [listbt[_].destroy() for _ in range(4)]
            listbt = []
            print(points)
            if (counter - 1) != len(p):
                print(counter)
                print(len(p))
                butn["state"] = "disabled"
            else:
                return None
            puntaje(p, c, r, w, i, b, counter, points, lbl2)

        b.config(command=lambda: fun_sig(b, lbl, lista_btn))

    if (counter - 1) == len(p):
        termino(b, w, lbl2, i, p, c, points)
    else:
        lista_btn = []
        puntaje_lbl = tkinter.Label(w, text=f"Puntaje: {points}/{len(p)}")
        lbl = tkinter.Label(w, text=p[counter-1])
        lbl2.config(text=f"Pregunta {counter} de {len(p)}")
        puntaje_lbl.grid(row=0, column=0)
        lbl.grid(row=0, column=1)
        for _ in range(4):
            btnfoo = tkinter.Button(w, text=r[counter-1][_], command=lambda __=_: fun_btn(__, points, puntaje_lbl))
            lista_btn.append(btnfoo)
            btnfoo.grid(row=_+1, column=1)


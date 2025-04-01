import tkinter as tk
from tkinter import ttk

import calendar
from datetime import datetime

from db.py_gihre_db import obtener_turnos_mes


def mostrar_turnos():
    anho = datetime.now().year
    mes = int(mes_seleccionado.get())
    trabajadores, asignaciones = obtener_turnos_mes(anho, mes)

    for i in tree.get_children():
        tree.delete(i)

    for id_trabajador, nombre in trabajadores:
        valores = [asignaciones[id_trabajador][dia] for dia in range(1, calendar.monthrange(anho, mes)[1] + 1)]
        tree.insert("", "end", values=[nombre] + valores)


root = tk.Tk()
root.title("Visualización de Turnos")

frame = tk.Frame(root)
frame.pack(pady=10)

# Selección de mes
mes_seleccionado = tk.StringVar(value=str(datetime.now().month))
meses = [str(i) for i in range(1, 13)]
ttk.Label(frame, text="Mes:").pack(side=tk.LEFT, padx=5)
ttk.Combobox(frame, textvariable=mes_seleccionado, values=meses, width=5).pack(side=tk.LEFT)
ttk.Button(frame, text="Cargar", command=mostrar_turnos).pack(side=tk.LEFT, padx=10)

# Tabla de turnos
columns = ["Trabajador"] + [str(i) for i in range(1, 32)]
tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=80 if col == "Trabajador" else 40, anchor="center")

tree.pack(expand=True, fill="both")
root.mainloop()


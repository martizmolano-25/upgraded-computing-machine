import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

# ---------- Base de Datos ----------
conn = sqlite3.connect("finanzas.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS transacciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    descripcion TEXT,
    monto REAL,
    fecha TEXT
)
""")
conn.commit()

# ---------- Idiomas ----------
idiomas = {
    "es": {
        "titulo": "Control de Finanzas",
        "tipo": "Tipo",
        "descripcion": "Descripción",
        "monto": "Monto",
        "agregar": "Agregar",
        "ingreso": "Ingreso",
        "gasto": "Gasto",
        "exito": "Transacción guardada",
        "error": "Completa todos los campos",
        "idioma": "Idioma"
    },
    "en": {
        "titulo": "Finance Tracker",
        "tipo": "Type",
        "descripcion": "Description",
        "monto": "Amount",
        "agregar": "Add",
        "ingreso": "Income",
        "gasto": "Expense",
        "exito": "Transaction saved",
        "error": "Please complete all fields",
        "idioma": "Language"
    }
}

idioma_actual = "es"

# ---------- Funciones ----------
def cambiar_idioma(nuevo_idioma):
    global idioma_actual
    idioma_actual = nuevo_idioma

    root.title(idiomas[idioma_actual]["titulo"])
    label_tipo.config(text=idiomas[idioma_actual]["tipo"])
    label_desc.config(text=idiomas[idioma_actual]["descripcion"])
    label_monto.config(text=idiomas[idioma_actual]["monto"])
    boton_agregar.config(text=idiomas[idioma_actual]["agregar"])
    label_idioma.config(text=idiomas[idioma_actual]["idioma"])

    # Actualizar menú tipo
    menu_tipo["menu"].delete(0, "end")
    menu_tipo["menu"].add_command(label=idiomas[idioma_actual]["ingreso"],
                                  command=lambda: tipo_var.set(idiomas[idioma_actual]["ingreso"]))
    menu_tipo["menu"].add_command(label=idiomas[idioma_actual]["gasto"],
                                  command=lambda: tipo_var.set(idiomas[idioma_actual]["gasto"]))

    tipo_var.set(idiomas[idioma_actual]["ingreso"])


def agregar_transaccion():
    tipo = tipo_var.get()
    descripcion = entry_desc.get()
    monto = entry_monto.get()
    fecha = datetime.now().strftime("%Y-%m-%d")

    if descripcion == "" or monto == "":
        messagebox.showwarning("Error", idiomas[idioma_actual]["error"])
        return

    try:
        monto = float(monto)
    except:
        messagebox.showwarning("Error", "Monto inválido")
        return

    cursor.execute("INSERT INTO transacciones (tipo, descripcion, monto, fecha) VALUES (?, ?, ?, ?)",
                   (tipo, descripcion, monto, fecha))
    conn.commit()

    messagebox.showinfo("OK", idiomas[idioma_actual]["exito"])
    limpiar_campos()
    mostrar_datos()


def mostrar_datos():
    for row in tree.get_children():
        tree.delete(row)

    cursor.execute("SELECT * FROM transacciones")
    for fila in cursor.fetchall():
        tree.insert("", "end", values=fila)


def limpiar_campos():
    entry_desc.delete(0, tk.END)
    entry_monto.delete(0, tk.END)


# ---------- Interfaz ----------
root = tk.Tk()
root.geometry("750x550")
root.config(bg="#ffc0cb")

# Estilo tabla
style = ttk.Style()
style.theme_use("default")
style.configure("Treeview",
                background="white",
                foreground="black",
                rowheight=25,
                fieldbackground="white")

# Frame idioma
frame_idioma = tk.Frame(root, bg="#3a1219")
frame_idioma.pack(pady=5)

label_idioma = tk.Label(frame_idioma, bg="#3d191f")
label_idioma.pack(side="left", padx=5)

tk.Button(frame_idioma, text="Español", bg="white",
          command=lambda: cambiar_idioma("es")).pack(side="left", padx=5)

tk.Button(frame_idioma, text="English", bg="white",
          command=lambda: cambiar_idioma("en")).pack(side="left", padx=5)

# Frame formulario
frame = tk.Frame(root, bg="#6b1b28")
frame.pack(pady=10)

# Tipo
label_tipo = tk.Label(frame, bg="#b3485a")
label_tipo.grid(row=0, column=0, padx=5, pady=5)

tipo_var = tk.StringVar()
menu_tipo = tk.OptionMenu(frame, tipo_var, "")
menu_tipo.grid(row=0, column=1, padx=5, pady=5)

# Descripción
label_desc = tk.Label(frame, bg="#c22e47")
label_desc.grid(row=1, column=0, padx=5, pady=5)

entry_desc = tk.Entry(frame)
entry_desc.grid(row=1, column=1, padx=5, pady=5)

# Monto
label_monto = tk.Label(frame, bg="#d40e2f")
label_monto.grid(row=2, column=0, padx=5, pady=5)

entry_monto = tk.Entry(frame)
entry_monto.grid(row=2, column=1, padx=5, pady=5)

# Botón
boton_agregar = tk.Button(frame, bg="white", command=agregar_transaccion)
boton_agregar.grid(row=3, columnspan=2, pady=10)

# Tabla
tree = ttk.Treeview(root, columns=("ID", "Tipo", "Descripción", "Monto", "Fecha"), show="headings")
tree.heading("ID", text="ID")
tree.heading("Tipo", text="Tipo")
tree.heading("Descripción", text="Descripción")
tree.heading("Monto", text="Monto")
tree.heading("Fecha", text="Fecha")
tree.pack(fill="both", expand=True, padx=10, pady=10)

# Inicializar idioma
cambiar_idioma("es")
mostrar_datos()

root.mainloop()
conn.close()

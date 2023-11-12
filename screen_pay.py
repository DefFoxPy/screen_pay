import sqlite3
import tkinter as tk
import datetime
import basesql
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from sqlite3 import Error


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect("base.db")
    except Error as e:
        print(e)

    if conn:
        return conn


def create_table(conn):
    try:
        sql = """CREATE TABLE IF NOT EXISTS Cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT,
            fecha_registro DATE
            );"""
        conn.execute(sql)
    except Error as e:
        print(e)
    try:
        sql = """CREATE TABLE IF NOT EXISTS Servicios (
                id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_plataforma TEXT,
                precio REAL
                );"""
        conn.execute(sql)
    except Error as e:
        print(e)
    try:
        sql = """CREATE TABLE IF NOT EXISTS Pantallas (
                id_pantalla INTEGER PRIMARY KEY AUTOINCREMENT,
                id_cliente INTEGER,
                id_servicio INTEGER,
                usuario TEXT,
                contraseña TEXT,
                fecha_renovacion DATE,
                suspendida INTEGER,
                FOREIGN KEY (id_cliente) REFERENCES Cliente (id_cliente),
                FOREIGN KEY (id_servicio) REFERENCES Servicios (id_servicio)
                );"""
        conn.execute(sql)
    except Error as e:
        print(e)


class ScreenPay:
    def __init__(self):
        self.base = basesql.Base()
        self.ventana = tk.Tk()
        self.ventana.title("ScreenPay")
        self.cuaderno = ttk.Notebook(self.ventana)

        self.agregar_cliente()
        self.consultar_cliente()
        self.listado_clientes()

        self.cuaderno.grid(column=0, row=0, padx=10, pady=10)
        self.ventana.mainloop()

    def agregar_cliente(self):
        self.pagina1 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina1, text="Agregar Cliente")
        self.labelframe1 = ttk.LabelFrame(self.pagina1, text="Cliente")
        self.labelframe1.grid(column=0, row=0, padx=4, pady=4)
        self.label1 = ttk.Label(self.labelframe1, text="Nombre")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.nombreagregar = tk.StringVar()
        self.entrynombreagregar = tk.Entry(
            self.labelframe1, textvariable=self.nombreagregar
        )
        self.entrynombreagregar.grid(column=1, row=0, padx=4, pady=4)
        self.label2 = ttk.Label(self.labelframe1, text="Correo")
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.correoagregar = tk.StringVar()
        self.entrycorreoagregar = ttk.Entry(
            self.labelframe1, textvariable=self.correoagregar
        )
        self.entrycorreoagregar.grid(column=1, row=1, padx=4, pady=4)
        self.boton1 = ttk.Button(
            self.labelframe1, text="Confirmar", command=self.agregar
        )
        self.boton1.grid(column=1, row=2, padx=4, pady=4)

    def agregar(self):
        fecha_hoy = datetime.date.today()
        datos = (self.nombreagregar.get(), self.correoagregar.get(), fecha_hoy)
        respuesta, bandera = self.base.alta(datos)

        if bandera:
            mb.showinfo(
                "Informacion",
                f"Ya existe un cliente con ese correoagregar y su id es:{respuesta}",
            )
        else:
            mb.showinfo(
                "Informacion",
                f"Se ha agregado el cliente con éxito, su id es el:{respuesta}",
            )
        self.nombreagregar.set("")
        self.correoagregar.set("")

    def consultar_cliente(self):
        self.pagina2 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina2, text="Consulta por id")
        self.labelframe2 = ttk.LabelFrame(self.pagina2, text="Cliente")
        self.labelframe2.grid(column=0, row=0, padx=5, pady=10)
        self.label1 = ttk.Label(self.labelframe2, text="ID:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.id = tk.StringVar()
        self.entryid = ttk.Entry(self.labelframe2, textvariable=self.id)
        self.entryid.grid(column=1, row=0, padx=4, pady=4)
        self.label2 = ttk.Label(self.labelframe2, text="Nombre:")
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.nombre = tk.StringVar()
        self.entrynombre = ttk.Entry(
            self.labelframe2, textvariable=self.nombre, state="readonly"
        )
        self.entrynombre.grid(column=1, row=1, padx=4, pady=4)
        self.label3 = ttk.Label(self.labelframe2, text="Correo:")
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.correo = tk.StringVar()
        self.entrycorreo = ttk.Entry(
            self.labelframe2, textvariable=self.correo, state="readonly"
        )
        self.entrycorreo.grid(column=1, row=2, padx=4, pady=4)
        self.boton1 = ttk.Button(
            self.labelframe2, text="Consultar", command=self.consultar
        )
        self.boton1.grid(column=1, row=3, padx=4, pady=4)

    def consultar(self):
        datos = (self.id.get(),)
        respuesta = self.base.consulta(datos)
        if len(respuesta) > 0:
            self.nombre.set(respuesta[0][0])
            self.correo.set(respuesta[0][1])
        else:
            self.correo.set("")
            self.nombre.set("")
            mb.showinfo("Información", "No existe un cliente con dicha id")

    def listado_clientes(self):
        self.pagina3 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina3, text="Listado Clientes")
        self.labelframe3 = ttk.LabelFrame(self.pagina3, text="Clientes")
        self.labelframe3.grid(column=0, row=0, padx=5, pady=10)
        self.boton1 = ttk.Button(
            self.labelframe3, text="Listado completo", command=self.listar
        )
        self.boton1.grid(column=0, row=0, padx=4, pady=4)
        self.scrolledtext1 = st.ScrolledText(self.labelframe3, width=30, height=10)
        self.scrolledtext1.grid(column=0, row=1, padx=10, pady=10)

    def listar(self):
        respuesta = self.base.recuperar_clientes()
        self.scrolledtext1.delete("1.0", tk.END)
        for fila in respuesta:
            self.scrolledtext1.insert(
                tk.END,
                "ID:"
                + str(fila[0])
                + "\nNombre:"
                + fila[1]
                + "\nCorreo:"
                + fila[2]
                + "\n\n",
            )


connection = create_connection()
create_table(connection)
aplicacion = ScreenPay()

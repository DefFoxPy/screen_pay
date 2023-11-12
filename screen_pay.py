import sqlite3
import tkinter as tk
import datetime
from tkinter import ttk
from tkinter import messagebox as mb
from sqlite3 import Error
import basesql


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
        sql = """CREATE TABLE Cliente (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            correo TEXT,
            fecha_registro DATE
            );"""
        conn.execute(sql)
    except Error as e:
        print(e)
    try:
        sql = """CREATE TABLE Servicios (
                id_servicio INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre_plataforma TEXT,
                precio REAL
                );"""
        conn.execute(sql)
    except Error as e:
        print(e)
    try:
        sql = """CREATE TABLE Pantallas (
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

        self.cuaderno.grid(column=0, row=0, padx=10, pady=10)
        self.ventana.mainloop()

    def agregar_cliente(self):
        self.pagina1 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina1, text="Agregar Cliente")
        self.labelframe1 = ttk.LabelFrame(self.pagina1, text="Cliente")
        self.labelframe1.grid(column=0, row=0, padx=4, pady=4)
        self.label1 = ttk.Label(self.labelframe1, text="Nombre")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.nombre = tk.StringVar()
        self.entrynombre = tk.Entry(self.labelframe1, textvariable=self.nombre)
        self.entrynombre.grid(column=1, row=0, padx=4, pady=4)
        self.label2 = ttk.Label(self.labelframe1, text="Correo")
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.correo = tk.StringVar()
        self.entrycorreo = ttk.Entry(self.labelframe1, textvariable=self.correo)
        self.entrycorreo.grid(column=1, row=1, padx=4, pady=4)
        self.boton1 = ttk.Button(
            self.labelframe1, text="Confirmar", command=self.agregar
        )
        self.boton1.grid(column=1, row=2, padx=4, pady=4)

    def agregar(self):
        fecha_hoy = datetime.date.today()
        datos = (self.nombre.get(), self.correo.get(), fecha_hoy)
        respuesta, bandera = self.base.alta(datos)
        
        if bandera:
            mb.showinfo("Informacion", f"Ya existe un cliente con ese correo y su id es:{respuesta}")
        else:
            mb.showinfo(
                "Informacion",
                f"Se ha agregado el cliente con éxito, su id es el:{respuesta}",
            )
        self.nombre.set("")
        self.correo.set("")
        


connection = create_connection()
create_table(connection)
aplicacion = ScreenPay()

import sqlite3
import tkinter as tk
import datetime
import basesql
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from sqlite3 import Error


class ScreenPay:
    def __init__(self):
        self.base = basesql.Base()
        self.ventana = tk.Tk()
        self.ventana.title("ScreenPay")
        self.cuaderno = ttk.Notebook(self.ventana)

        self.agregar_cliente()
        self.modifica_cliente()
        self.listado_clientes()
        self.listado_plataformas()

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

    def modifica_cliente(self):
        self.pagina2 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina2, text="Modifica Cliente")
        self.labelframe2 = ttk.LabelFrame(self.pagina2, text="Cliente")
        self.labelframe2.grid(column=0, row=0, padx=5, pady=10)
        self.label1 = ttk.Label(self.labelframe2, text="ID:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.idmod = tk.StringVar()
        self.entryidmod = ttk.Entry(self.labelframe2, textvariable=self.idmod)
        self.entryidmod.grid(column=1, row=0, padx=4, pady=4)
        self.label2 = ttk.Label(self.labelframe2, text="Nombre:")
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.nombremod = tk.StringVar()
        self.entrynombremod = ttk.Entry(self.labelframe2, textvariable=self.nombremod)
        self.entrynombremod.grid(column=1, row=1, padx=4, pady=4)
        self.label3 = ttk.Label(self.labelframe2, text="Correo:")
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.correomod = tk.StringVar()
        self.entrycorreomod = ttk.Entry(self.labelframe2, textvariable=self.correomod)
        self.entrycorreomod.grid(column=1, row=2, padx=4, pady=4)
        self.boton1 = ttk.Button(
            self.labelframe2, text="Consultar", command=self.consultar
        )
        self.boton1.grid(column=1, row=3, padx=4, pady=4)
        self.boton1 = ttk.Button(
            self.labelframe2, text="Modificar", command=self.modifica
        )
        self.boton1.grid(column=1, row=4, padx=4, pady=4)

    def consultar(self):
        datos = (self.idmod.get(),)
        respuesta = self.base.consulta(datos)
        if len(respuesta) > 0:
            self.nombremod.set(respuesta[0][0])
            self.correomod.set(respuesta[0][1])
        else:
            self.correomod.set("")
            self.nombremod.set("")
            mb.showinfo("Información", "No existe un cliente con dicha id")

    def modifica(self):
        datos = (self.nombremod.get(), self.correomod.get(), self.idmod.get())
        respuesta = self.base.modifica_cliente(datos)
        if respuesta == 1:
            mb.showinfo("Información", f"Se modificó al cliente con id: datos[2]")
        else:
            mb.showinfo("Información", f"No existe un Cliente con la id: datos[2]")

    def listado_clientes(self):
        self.pagina3 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina3, text="Listado Clientes")
        self.labelframe3 = ttk.LabelFrame(self.pagina3, text="Clientes")
        self.labelframe3.grid(column=0, row=0, padx=5, pady=10)
        self.boton1 = ttk.Button(
            self.labelframe3, text="Listado completo", command=self.listar_clientes
        )
        self.boton1.grid(column=0, row=0, padx=4, pady=4)
        self.scrolledtext1 = st.ScrolledText(self.labelframe3, width=30, height=10)
        self.scrolledtext1.grid(column=0, row=1, padx=10, pady=10)

    def listar_clientes(self):
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

    def listado_plataformas(self):
        self.pagina4 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina4, text="Listado Plataformas")
        self.labelframe4 = ttk.LabelFrame(self.pagina4, text="Plataformas")
        self.labelframe4.grid(column=0, row=0, padx=5, pady=10)
        self.boton1 = ttk.Button(
            self.labelframe4, text="Listado completo", command=self.listar_plataformas
        )
        self.boton1.grid(column=0, row=0, padx=4, pady=4)
        self.scrolledtext2 = st.ScrolledText(self.labelframe4, width=30, height=10)
        self.scrolledtext2.grid(column=0, row=1, padx=10, pady=10)

    def listar_plataformas(self):
        respuesta = self.base.recuperar_plataformas()
        self.scrolledtext2.delete("1.0", tk.END)
        for fila in respuesta:
            self.scrolledtext2.insert(
                tk.END,
                "ID:"
                + str(fila[0])
                + "\nNombre:"
                + fila[1]
                + "\nPrecio:"
                + str(fila[2])
                + "\n\n",
            )

aplicacion = ScreenPay()

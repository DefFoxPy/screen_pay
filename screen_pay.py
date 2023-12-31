import sqlite3
import tkinter as tk
import datetime
import basesql
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter import scrolledtext as st
from tkcalendar import Calendar
from sqlite3 import Error


class ScreenPay:
    def __init__(self):
        self.base = basesql.Base()
        self.ventana = tk.Tk()
        self.ventana.title("ScreenPay")
        self.cuaderno = ttk.Notebook(self.ventana)

        self.agregar_cliente()
        self.modifica_cliente()
        self.listado_plataformas()
        self.agregar_pantalla()
        self.gestion_pantallas()

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
        respuesta = self.base.alta(datos)
        mb.showinfo("Información", respuesta)
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

        self.boton2 = ttk.Button(
            self.labelframe2, text="Modificar", command=self.modifica
        )
        self.boton2.grid(column=1, row=4, padx=4, pady=4)

        self.boton3 = ttk.Button(
            self.labelframe2, text="Eliminar", command=self.elimina_cliente
        )
        self.boton3.grid(column=1, row=5, padx=4, pady=4)

        self.labelframe3 = ttk.LabelFrame(self.pagina2, text="Listado")
        self.labelframe3.grid(column=1, row=0, padx=5, pady=10)
        self.boton1 = ttk.Button(
            self.labelframe3, text="Listado completo", command=self.listar_clientes
        )
        self.boton1.grid(column=0, row=0, padx=4, pady=4)
        self.scrolledtext1 = st.ScrolledText(self.labelframe3, width=30, height=10)
        self.scrolledtext1.grid(column=0, row=1, padx=10, pady=10)

    def consultar(self):
        datos = self.idmod.get()
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
        mb.showinfo("Información", respuesta)
        self.idmod.set("")
        self.correomod.set("")
        self.nombremod.set("")

    def elimina_cliente(self):
        datos = self.idmod.get()
        respuesta = self.base.elimina_cliente(datos)
        mb.showinfo("Información", respuesta)
        self.idmod.set("")
        self.correomod.set("")
        self.nombremod.set("")

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
        self.cuaderno.add(self.pagina4, text="Plataformas")
        self.labelframe4 = ttk.LabelFrame(self.pagina4, text="Listado")
        self.labelframe4.grid(column=1, row=0, padx=5, pady=10)
        self.boton1 = ttk.Button(
            self.labelframe4, text="Listado completo", command=self.listar_plataformas
        )
        self.boton1.grid(column=0, row=0, padx=4, pady=4)
        self.scrolledtext2 = st.ScrolledText(self.labelframe4, width=30, height=10)
        self.scrolledtext2.grid(column=0, row=1, padx=10, pady=10)

        self.labelframe6 = ttk.LabelFrame(self.pagina4, text="Plataforma")
        self.labelframe6.grid(column=0, row=0, padx=5, pady=10)
        self.label1 = ttk.Label(self.labelframe6, text="ID:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.id_plat = tk.StringVar()
        self.entryid_plat = ttk.Entry(self.labelframe6, textvariable=self.id_plat)
        self.entryid_plat.grid(column=1, row=0, padx=4, pady=4)
        self.label2 = ttk.Label(self.labelframe6, text="Precio:")
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.precio_plat = tk.StringVar()
        self.entryprecio_plat = ttk.Entry(
            self.labelframe6, textvariable=self.precio_plat
        )
        self.entryprecio_plat.grid(column=1, row=1, padx=4, pady=4)

        self.boton1 = ttk.Button(
            self.labelframe6, text="Modificar", command=self.modifica_plataforma
        )
        self.boton1.grid(column=1, row=6, padx=4, pady=4)

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

    def modifica_plataforma(self):
        if len(self.precio_plat.get()) == 0 or len(self.id_plat.get()) == 0:
            mb.showinfo("Información", "No se permiten espacios en blanco")
            return
        datos = (self.precio_plat.get(), self.id_plat.get())
        respuesta = self.base.modifica_plataforma(datos)
        mb.showinfo("Informacion", respuesta)
        self.id_plat.set("")
        self.precio_plat.set("")

    def agregar_pantalla(self):
        self.pagina5 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina5, text="Agregar Pantalla")
        self.labelframe5 = ttk.LabelFrame(self.pagina5, text="Pantalla")
        self.labelframe5.grid(column=0, row=0, padx=4, pady=4)

        self.label1 = ttk.Label(self.labelframe5, text="ID Cliente:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.id_cliente_agregar = tk.StringVar()
        self.entryid_cliente_agregar = tk.Entry(
            self.labelframe5, textvariable=self.id_cliente_agregar
        )
        self.entryid_cliente_agregar.grid(column=1, row=0, padx=4, pady=4)

        self.label2 = ttk.Label(self.labelframe5, text="ID Servicio:")
        self.label2.grid(column=0, row=1, padx=4, pady=4)
        self.id_servicio_agregar = tk.StringVar()
        self.entryid_servicio_agregar = ttk.Entry(
            self.labelframe5, textvariable=self.id_servicio_agregar
        )
        self.entryid_servicio_agregar.grid(column=1, row=1, padx=4, pady=4)

        self.label3 = ttk.Label(self.labelframe5, text="Usuario:")
        self.label3.grid(column=0, row=2, padx=4, pady=4)
        self.usuario_agregar = tk.StringVar()
        self.entryusuario_agregar = ttk.Entry(
            self.labelframe5, textvariable=self.usuario_agregar
        )
        self.entryusuario_agregar.grid(column=1, row=2, padx=4, pady=4)

        self.label4 = ttk.Label(self.labelframe5, text="Contraseña:")
        self.label4.grid(column=0, row=3, padx=4, pady=4)
        self.contrasenia_agregar = tk.StringVar()
        self.entrycontrasenia_agregar = ttk.Entry(
            self.labelframe5, textvariable=self.contrasenia_agregar
        )
        self.entrycontrasenia_agregar.grid(column=1, row=3, padx=4, pady=4)

        self.label5 = ttk.Label(self.labelframe5, text="Correo:")
        self.label5.grid(column=0, row=4, padx=4, pady=4)
        self.correo_agregar = tk.StringVar()
        self.entrycorreo_agregar = ttk.Entry(
            self.labelframe5, textvariable=self.correo_agregar
        )
        self.entrycorreo_agregar.grid(column=1, row=4, padx=4, pady=4)

        self.label6 = ttk.Label(self.labelframe5, text="Renovacion")
        self.label6.grid(column=0, row=5, padx=4, pady=4)
        self.renovacion = tk.StringVar()
        self.entryrenovacion = ttk.Entry(
            self.labelframe5, textvariable=self.renovacion, state="readonly"
        )
        self.entryrenovacion.grid(column=1, row=5, padx=4, pady=4)

        self.boton1 = ttk.Button(
            self.labelframe5, text="Confirmar", command=self.agrega_pantalla
        )
        self.boton1.grid(column=1, row=6, padx=4, pady=4)

        self.labelframe6 = ttk.LabelFrame(self.pagina5, text="Calendario")
        self.labelframe6.grid(column=1, row=0, padx=4, pady=4)
        self.calendar = Calendar(
            self.labelframe6, selectmode="day", year=2023, month=11, day=2
        )
        self.calendar.grid(column=0)

        self.boton2 = ttk.Button(
            self.labelframe6, text="Obtener Fecha", command=self.agrega_fecha
        )
        self.boton2.grid(column=0, row=1, padx=4, pady=4)

    def agrega_fecha(self):
        self.renovacion.set(self.calendar.get_date())

    def agrega_pantalla(self):
        datos = (
            self.id_cliente_agregar.get(),
            self.id_servicio_agregar.get(),
            self.usuario_agregar.get(),
            self.contrasenia_agregar.get(),
            self.correo_agregar.get(),
            self.renovacion.get(),
        )
        respuesta = self.base.agrega_pantalla(datos)
        mb.showinfo("Información", respuesta)
        self.id_cliente_agregar.set("")
        self.id_servicio_agregar.set("")
        self.usuario_agregar.set("")
        self.contrasenia_agregar.set("")
        self.correo_agregar.set("")
        self.renovacion.set("")

    def gestion_pantallas(self):
        self.pagina6 = ttk.Frame(self.cuaderno)
        self.cuaderno.add(self.pagina6, text="Gestión Pantallas")
        self.labelframe7 = ttk.LabelFrame(self.pagina6, text="Cliente")
        self.labelframe7.grid(column=0, row=0, padx=4, pady=4)

        self.label1 = ttk.Label(self.labelframe7, text="ID Cliente")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.id_cliente_gestion = tk.StringVar()
        self.entryid_cliente_gestion = tk.Entry(
            self.labelframe7, textvariable=self.id_cliente_gestion
        )
        self.entryid_cliente_gestion.grid(column=0, row=1, padx=4, pady=4)

        self.boton1 = ttk.Button(
            self.labelframe7, text="Buscar", command=self.obtener_pantallas
        )
        self.boton1.grid(column=0, row=2, padx=4, pady=4)

        self.scrolledtext3 = st.ScrolledText(self.labelframe7, width=30, height=7)
        self.scrolledtext3.grid(column=0, row=3, padx=10, pady=10)

        self.labelframe8 = ttk.LabelFrame(self.pagina6, text="Estado")
        self.labelframe8.grid(column=1, row=0, padx=4, pady=4)
        self.boton1 = ttk.Button(
            self.labelframe8,
            text="Mostrar Pantallas Suspendidas",
            command=self.mostrar_vencidas,
        )
        self.boton1.grid(column=0, row=1, padx=4, pady=4)

        self.boton2 = ttk.Button(
            self.labelframe8,
            text="Mostrar todas las Pantallas",
            command=self.mostrar_todas_pantallas,
        )
        self.boton2.grid(column=0, row=2, padx=4, pady=4)

        self.scrolledtext4 = st.ScrolledText(self.labelframe8, width=30, height=7)
        self.scrolledtext4.grid(column=0, row=3, padx=10, pady=10)

        self.labelframe9 = ttk.LabelFrame(self.pagina6, text="Pagos")
        self.labelframe9.grid(column=2, row=0, padx=4, pady=4)

        self.label1 = ttk.Label(self.labelframe9, text="ID Pantalla:")
        self.label1.grid(column=0, row=0, padx=4, pady=4)
        self.id_pantalla_gestion = tk.StringVar()
        self.entryid_pantalla_gestion = tk.Entry(
            self.labelframe9, textvariable=self.id_pantalla_gestion
        )
        self.entryid_pantalla_gestion.grid(column=0, row=1, padx=4, pady=4)

        self.boton1 = ttk.Button(
            self.labelframe9,
            text="Consultar",
            command=self.consultar_pantalla,
        )
        self.boton1.grid(column=0, row=2, padx=4, pady=4)

        self.boton2 = ttk.Button(
            self.labelframe9,
            text="Renovar",
            command=self.renovar_pantalla,
        )
        self.boton2.grid(column=0, row=3, padx=4, pady=4)

        self.boton3 = ttk.Button(
            self.labelframe9,
            text="Eliminar",
            command=self.eliminar_pantalla,
        )
        self.boton3.grid(column=0, row=4, padx=4, pady=4)

    def mostrar_pantalla(self, pantallas, scrolledtext):
        for fila in pantallas:
            estado = "suspendida"
            if int(fila[7]) == 0:
                estado = "renovada"
            scrolledtext.insert(
                tk.END,
                "ID pantalla:"
                + str(fila[0])
                + "\nID Cliente:"
                + str(fila[1])
                + "\nID servicio:"
                + str(fila[2])
                + "\nUsuario:"
                + fila[3]
                + "\nContraseña:"
                + fila[4]
                + "\nCorreo:"
                + fila[5]
                + "\nFecha_renovacion:"
                + fila[6]
                + "\nEstado:"
                + f"{estado}"
                + "\n\n",
            )

    def obtener_pantallas(self):
        datos = self.id_cliente_gestion.get()
        respuesta, total = self.base.recuperar_pantallas(datos)
        self.scrolledtext3.delete("1.0", tk.END)
        if len(respuesta) == 0:
            mb.showinfo(
                "Informacion",
                f"El cliente número {datos} no tiene pantallas afiliadas",
            )
        else:
            self.mostrar_pantalla(respuesta, self.scrolledtext3)
            self.scrolledtext3.insert(
                tk.END, f"Precio total por las pantallas: {total}$"
            )

    def mostrar_vencidas(self):
        respuesta = self.base.recuperar_vencidos()
        self.scrolledtext4.delete("1.0", tk.END)
        if respuesta == []:
            mb.showinfo("Información", "No hay pantallas suspendidas para mostrar")
        else:
            self.mostrar_pantalla(respuesta, self.scrolledtext4)

    def mostrar_todas_pantallas(self):
        respuesta = self.base.mostrar_todas_pantallas()
        self.scrolledtext4.delete("1.0", tk.END)
        if respuesta == []:
            mb.showinfo("Información", "No hay pantallas para mostrar")
        else:
            self.mostrar_pantalla(respuesta, self.scrolledtext4)

    def consultar_pantalla(self):
        datos = self.id_pantalla_gestion.get()
        respuesta, mensaje = self.base.consultar_pantalla(datos)
        if not respuesta == []:
            self.scrolledtext4.delete("1.0", tk.END)
            self.mostrar_pantalla(respuesta, self.scrolledtext4)
        mb.showinfo("Información", mensaje)
        self.id_pantalla_gestion.set("")

    def renovar_pantalla(self):
        datos = self.id_pantalla_gestion.get()
        respuesta = self.base.renovar_pantalla(datos)
        mb.showinfo("Información", respuesta)
        self.id_pantalla_gestion.set("")

    def eliminar_pantalla(self):
        datos = self.id_pantalla_gestion.get()
        respuesta = self.base.eliminar_pantalla(datos)
        mb.showinfo("Información", respuesta)
        self.id_pantalla_gestion.set("")


aplicacion = ScreenPay()

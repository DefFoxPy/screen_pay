import sqlite3


class Base:
    def __init__(self):
        self.crear_tablas()
        self.agregar_servicios("Neflix", 7)
        self.agregar_servicios("Disney+", 8)
        self.agregar_servicios("HBO", 10)
        self.agregar_servicios("Star+", 11)

    def abrir(self):
        conn = None
        try:
            conn = sqlite3.connect("base.db")
        except Error as e:
            print(e)

        if conn:
            return conn

    def crear_tablas(self):
        conn = self.abrir()

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

    def verificar_servicio(self, cursor, nombre):
        cursor.execute(
            """ SELECT COUNT(*) FROM Servicios WHERE nombre_plataforma = ? """,
            (nombre,),
        )
        resultado = cursor.fetchone()
        return resultado[0] > 0

    def agregar_servicios(self, nombre, precio):
        conn = self.abrir()
        cursor = conn.cursor()

        if not self.verificar_servicio(cursor, nombre):
            cursor.execute(
                "INSERT INTO Servicios (nombre_plataforma, precio) VALUES (?, ?)",
                (nombre, precio),
            )
            conn.commit()

    def alta(self, datos):
        conn = self.abrir()
        cursor = conn.cursor()

        bandera = False

        cursor.execute(
            """SELECT id_cliente FROM Cliente WHERE correo = ? """, (datos[1],)
        )
        resultado = cursor.fetchone()

        if resultado:
            bandera = True
            return (resultado[0], bandera)

        cursor.execute(
            """INSERT INTO Cliente (nombre, correo, fecha_registro) VALUES (?, ?, ?)""",
            datos,
        )

        id_cliente = cursor.lastrowid

        conn.commit()
        conn.close()

        return (id_cliente, bandera)

    def consulta(self, datos):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(
                """ SELECT nombre, correo FROM Cliente where id_cliente = ? """, datos
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def modifica_cliente(self, datos):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(
                """ UPDATE Cliente SET nombre = ?, correo = ? WHERE id_cliente = ? """,
                datos,
            )
            conn.commit()
            return cursor.rowcount
        except:
            conn.close()

    def modifica_plataforma(self, datos):
        if datos[0] < 0.0:
            precio = 0
        else:
            precio = datos[0]
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(
                """ UPDATE Servicios SET precio = ? WHERE id_servicio = ? """,
                (precio, datos[1]),
            )
            conn.commit()
            return cursor.rowcount
        except:
            conn.close()

    def recuperar_clientes(self):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute("""SELECT id_cliente, nombre, correo FROM Cliente""")
            return cursor.fetchall()
        finally:
            conn.close()

    def recuperar_plataformas(self):
        try:
            conn = self.abrir()
            cursor = conn.cursor()
            cursor.execute(
                """ SELECT id_servicio, nombre_plataforma, precio FROM Servicios """
            )
            return cursor.fetchall()
        finally:
            conn.close()

    def agrega_pantalla(self, datos):
        conn = self.abrir()
        cursor = conn.cursor()

        # verificaciones
        cursor.execute(
            """ SELECT * FROM Cliente WHERE id_cliente = ?""", (datos[0])
        )
        resultado = cursor.fetchone()
        if not resultado:
            conn.close()
            return "No existe un usuario con esa id o fue eliminado"

        cursor.execute(
            """ SELECT * FROM Servicios WHERE id_servicio = ? """, (datos[1],)
        )
        resultado = cursor.fetchone()
        if not resultado:
            conn.close()
            return "No existe un Servicio con esa id o fue eliminado"

        if len(datos[2]) == 0 or len(datos[3]) == 0:
            return "El campo usuario y contraseña no pueden estar vacios"
        
        cursor.execute(
            """ SELECT * FROM Pantallas WHERE usuario = ? """, (datos[2],)
        )
        resultado = cursor.fetchone()
        if resultado:
            conn.close()
            return "Ya existe una pantalla que tiene asiganda dicho usuario" 

        cursor.execute(
            """ INSERT INTO Pantallas (id_cliente, id_servicio, usuario, contraseña,  fecha_renovacion, suspendida) 
            VALUES (?, ?, ?, ?, ?, ?) """,
            datos,
        )

        id_pantalla = cursor.lastrowid

        conn.commit()
        conn.close()
        return id_pantalla

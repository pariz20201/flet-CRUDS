import flet as ft
import mysql.connector
from mysql.connector import Error

def conectar():
    try:
        conexion = mysql.connector.connect(
            host="localhost",
            user="root",
            password="pariz2020",
            database="bat-store"
        )
        if conexion.is_connected():
            return conexion
    except Error as e:
        print(f"Error en la conexión: {e}")
    return None

def ver_usuarios(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM articulo")
    registros = cursor.fetchall()
    result = "\n".join([str(row) for row in registros])
    cursor.close()
    return result

def insertar_usuario(conexion, nombre, precio, reorden, codigo_barras):
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO articulo (codigo_barras, nombre, precio, reorden) VALUES (%s, %s, %s, %s)", 
                   (codigo_barras, nombre, precio, reorden))
    conexion.commit()
    cursor.close()
    return "Artículo insertado correctamente"

def actualizar_usuario(conexion, nombre_nuevo, codigo_barras):
    cursor = conexion.cursor()
    cursor.execute("UPDATE articulo SET nombre = %s WHERE codigo_barras = %s", (nombre_nuevo, codigo_barras))
    conexion.commit()
    cursor.close()
    return "Artículo actualizado correctamente"

def eliminar_usuario(conexion, codigo_barras):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM articulo WHERE codigo_barras = %s", (codigo_barras,))
    conexion.commit()
    cursor.close()
    return "Artículo eliminado correctamente"

def ver_proveedores(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM proveedor")
    registros = cursor.fetchall()
    result = "\n".join([str(row) for row in registros])
    cursor.close()
    return result

def insertar_proveedor(conexion, idProveedor, nombre, telefono, direccion):
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO proveedor (idProveedor, nombre, telefono, direccion) VALUES (%s, %s, %s, %s)", 
                   (idProveedor, nombre, telefono, direccion))
    conexion.commit()
    cursor.close()
    return "Proveedor insertado correctamente"

def actualizar_proveedor(conexion, nombre_nuevo, telefono):
    cursor = conexion.cursor()
    cursor.execute("UPDATE proveedor SET nombre = %s WHERE telefono = %s", (nombre_nuevo, telefono))
    conexion.commit()
    cursor.close()
    return "Proveedor actualizado correctamente"

def eliminar_proveedor(conexion, idProveedor):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM proveedor WHERE idProveedor = %s", (idProveedor,))
    conexion.commit()
    cursor.close()
    return "Proveedor eliminado correctamente"

def ver_cliente(conexion):
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM cliente")
    registros = cursor.fetchall()
    result = "\n".join([str(row) for row in registros])
    cursor.close()
    return result

def insertar_cliente(conexion, idCliente, nombre):
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO cliente (idCliente, nombre) VALUES (%s, %s)", (idCliente, nombre))
    conexion.commit()
    cursor.close()
    return "Clienet insertado correctamente"

def actualizar_cliente(conexion, nuevo_nombre, idCliente):
    cursor = conexion.cursor()
    cursor.execute("UPDATE categoria SET nombre = %s WHERE idCliente = %s", (nuevo_nombre, idCliente))
    conexion.commit()
    cursor.close()
    return "Cliente actualizado correctamente"

def eliminar_cliente(conexion, idCliente):
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM categoria WHERE idCategoria = %s", (idCliente,))
    conexion.commit()
    cursor.close()
    return "Cliente eliminado correctamente"

def main(page: ft.Page):
    page.title = "CRUDS con Pestañas"
    page.scroll = ft.ScrollMode.AUTO

    contenedor_acciones_articulos = ft.Column()
    contenedor_acciones_proveedores = ft.Column()
    contenedor_acciones_categorias = ft.Column()

    def mostrar_mensaje(mensaje):
        page.open( ft.AlertDialog(title=ft.Text("Resultado"), content=ft.Text(mensaje)))
        page.dialog.open = True
        page.update()

    def acciones_articulos(action):
        conexion = conectar()
        if conexion is None:
            mostrar_mensaje("No se pudo conectar a la base de datos")
            return

        contenedor_acciones_articulos.controls.clear()

        if action == "ver":
            result = ver_usuarios(conexion)
            mostrar_mensaje(result)
        elif action == "insertar":
            nombre = ft.TextField(label="Nombre del artículo")
            precio = ft.TextField(label="Precio", keyboard_type=ft.KeyboardType.NUMBER)
            reorden = ft.TextField(label="Reorden")
            codigo = ft.TextField(label="Código de barras")

            def insertar_click(e):
                r = insertar_usuario(conexion, nombre.value, float(precio.value), reorden.value, codigo.value)
                mostrar_mensaje(r)

            contenedor_acciones_articulos.controls.extend([nombre, precio, reorden, codigo, ft.ElevatedButton("Insertar", on_click=insertar_click)])

        elif action == "actualizar":
            nuevo_nombre = ft.TextField(label="Nuevo nombre")
            codigo = ft.TextField(label="Código de barras")

            def actualizar_click(e):
                r = actualizar_usuario(conexion, nuevo_nombre.value, codigo.value)
                mostrar_mensaje(r)

            contenedor_acciones_articulos.controls.extend([nuevo_nombre, codigo, ft.ElevatedButton("Actualizar", on_click=actualizar_click)])

        elif action == "eliminar":
            codigo = ft.TextField(label="Código de barras")

            def eliminar_click(e):
                r = eliminar_usuario(conexion, codigo.value)
                mostrar_mensaje(r)

            contenedor_acciones_articulos.controls.extend([codigo, ft.ElevatedButton("Eliminar", on_click=eliminar_click)])

        page.update()

    def acciones_proveedores(action):
        conexion = conectar()
        if conexion is None:
            mostrar_mensaje("No se pudo conectar a la base de datos")
            return

        contenedor_acciones_proveedores.controls.clear()

        if action == "ver":
            result = ver_proveedores(conexion)
            mostrar_mensaje(result)
        elif action == "insertar":
            idprov = ft.TextField(label="ID Proveedor")
            nombre = ft.TextField(label="Nombre")
            telefono = ft.TextField(label="Teléfono")
            direccion = ft.TextField(label="Dirección")

            def insertar_click(e):
                r = insertar_proveedor(conexion, idprov.value, nombre.value, telefono.value, direccion.value)
                mostrar_mensaje(r)

            contenedor_acciones_proveedores.controls.extend([idprov, nombre, telefono, direccion, ft.ElevatedButton("Insertar", on_click=insertar_click)])

        elif action == "actualizar":
            nuevo_nombre = ft.TextField(label="Nuevo nombre")
            telefono = ft.TextField(label="Teléfono")

            def actualizar_click(e):
                r = actualizar_proveedor(conexion, nuevo_nombre.value, telefono.value)
                mostrar_mensaje(r)

            contenedor_acciones_proveedores.controls.extend([nuevo_nombre, telefono, ft.ElevatedButton("Actualizar", on_click=actualizar_click)])

        elif action == "eliminar":
            idprov = ft.TextField(label="ID Proveedor")

            def eliminar_click(e):
                r = eliminar_proveedor(conexion, idprov.value)
                mostrar_mensaje(r)

            contenedor_acciones_proveedores.controls.extend([idprov, ft.ElevatedButton("Eliminar", on_click=eliminar_click)])

        page.update()

    def acciones_clientes(action):
        conexion = conectar()
        if conexion is None:
            mostrar_mensaje("No se pudo conectar a la base de datos")
            return

        contenedor_acciones_categorias.controls.clear()

        if action == "ver":
            result = ver_cliente(conexion)
            mostrar_mensaje(result)
        elif action == "insertar":
            idcat = ft.TextField(label="IdCliente")
            nombre = ft.TextField(label="Nombre")

            def insertar_click(e):
                r = insertar_cliente(conexion, idcat.value, nombre.value)
                mostrar_mensaje(r)

            contenedor_acciones_categorias.controls.extend([idcat, nombre, ft.ElevatedButton("Insertar", on_click=insertar_click)])

        elif action == "actualizar":
            idcat = ft.TextField(label="IdCliente")
            nuevo_nombre = ft.TextField(label="Nuevo nombre")

            def actualizar_click(e):
                r = actualizar_cliente(conexion, nuevo_nombre.value, idcat.value)
                mostrar_mensaje(r)

            contenedor_acciones_categorias.controls.extend([idcat, nuevo_nombre, ft.ElevatedButton("Actualizar", on_click=actualizar_click)])

        elif action == "eliminar":
            idcat = ft.TextField(label="IdCliente")

            def eliminar_click(e):
                r = eliminar_cliente(conexion, idcat.value)
                mostrar_mensaje(r)

            contenedor_acciones_categorias.controls.extend([idcat, ft.ElevatedButton("Eliminar", on_click=eliminar_click)])

        page.update()

    def tab_articulos():
        return ft.Column([
            ft.Text("Gestión de Artículos", size=24, weight="bold"),
            ft.Row([
                ft.ElevatedButton("Ver", on_click=lambda e: acciones_articulos("ver")),
                ft.ElevatedButton("Insertar", on_click=lambda e: acciones_articulos("insertar")),
                ft.ElevatedButton("Actualizar", on_click=lambda e: acciones_articulos("actualizar")),
                ft.ElevatedButton("Eliminar", on_click=lambda e: acciones_articulos("eliminar")),
            ], alignment=ft.MainAxisAlignment.CENTER),
            contenedor_acciones_articulos
        ])

    def tab_proveedores():
        return ft.Column([
            ft.Text("Gestión de Proveedores", size=24, weight="bold"),
            ft.Row([
                ft.ElevatedButton("Ver", on_click=lambda e: acciones_proveedores("ver")),
                ft.ElevatedButton("Insertar", on_click=lambda e: acciones_proveedores("insertar")),
                ft.ElevatedButton("Actualizar", on_click=lambda e: acciones_proveedores("actualizar")),
                ft.ElevatedButton("Eliminar", on_click=lambda e: acciones_proveedores("eliminar")),
            ], alignment=ft.MainAxisAlignment.CENTER),
            contenedor_acciones_proveedores
        ])

    def tab_clientes():
        return ft.Column([
            ft.Text("Gestión de Clientes", size=24, weight="bold"),
            ft.Row([
                ft.ElevatedButton("Ver", on_click=lambda e: acciones_clientes("ver")),
                ft.ElevatedButton("Insertar", on_click=lambda e: acciones_clientes("insertar")),
                ft.ElevatedButton("Actualizar", on_click=lambda e: acciones_clientes("actualizar")),
                ft.ElevatedButton("Eliminar", on_click=lambda e: acciones_clientes("eliminar")),
            ], alignment=ft.MainAxisAlignment.CENTER),
            contenedor_acciones_categorias
        ])

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(text="Artículos", content=tab_articulos()),
            ft.Tab(text="Proveedores", content=tab_proveedores()),
            ft.Tab(text="Clientes", content=tab_clientes()),
        ],
        expand=True
    )

    page.add(tabs)

ft.app(target=main)
from conexion import conectar, cerrar_conexion 
import mysql.connector

###################### Habitaciones ############################
def obtener_habitaciones_disponibles():
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("SELECT * FROM habitaciones WHERE ocupado = 0")
    habitaciones_disponibles = cursor.fetchall()

    cerrar_conexion(conexion, cursor)
    return habitaciones_disponibles

def agregar_habitaciones(id_habitaciones, numero, capacidad, orientacion, ocupado):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO habitaciones (id_habitacion, numero, capacidad, orientacion, ocupado) VALUES (%s, %s, %s ,%s ,%s)", (id_habitaciones, numero, capacidad, orientacion, ocupado))
    conexion.commit()

    cerrar_conexion(conexion, cursor)

def eliminar_habitaciones():
    id_habitacion = input("Ingrese el ID de la habitación a eliminar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM habitaciones WHERE id_habitacion = %s", (id_habitacion,))
        conexion.commit()
        print("Habitación eliminada correctamente.")
    except mysql.connector.Error as error:
        print(f"No se pudo eliminar la habitación: {error}")
        conexion.rollback()
    finally:
        cerrar_conexion(conexion, cursor)

def modificar_habitaciones():
    id_habitacion = input("Ingrese el ID de la habitación a modificar: ")
    nuevo_numero = input("Ingrese el nuevo número de la habitación: ")
    nueva_capacidad = input("Ingrese la nueva capacidad de la habitación: ")
    nueva_orientacion = input("Ingrese la nueva orientación de la habitación: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("UPDATE habitaciones SET numero = %s, capacidad = %s, orientacion = %s WHERE id_habitacion = %s",
                       (nuevo_numero, nueva_capacidad, nueva_orientacion, id_habitacion))
        conexion.commit()
        print("Habitación modificada correctamente.")
    except mysql.connector.Error as error:
        print(f"No se pudo modificar la habitación: {error}")
        conexion.rollback()
    finally:
        cerrar_conexion(conexion, cursor)

#################################################################

######################### PASAJEROS ##########################################

def mostrar_pasajeros():
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT * FROM pasajeros")
        pasajeros = cursor.fetchall()

        if pasajeros:
            print("ID | Nombre | RUT | ID Habitación | Fecha Entrada | Fecha Salida")
            for pasajero in pasajeros:
                print(f"{pasajero[0]} | {pasajero[1]} | {pasajero[2]} | {pasajero[3]} | {pasajero[4]} | {pasajero[5]}")
        else:
            print("No hay pasajeros registrados.")

    except mysql.connector.Error as error:
        print(f"Error al obtener los pasajeros: {error}")
    finally:
        cerrar_conexion(conexion, cursor)

def agregar_pasajero(nombre, rut, id_habitaciones, fecha_entrada, fecha_salida):
    conexion = conectar()
    cursor = conexion.cursor()

    # Obtener la capacidad máxima de la habitación
    cursor.execute("SELECT capacidad FROM habitaciones WHERE id_habitacion = %s", (id_habitaciones,))
    capacidad_maxima = cursor.fetchone()[0]

    # Obtener la cantidad actual de pasajeros en la habitación
    cursor.execute("SELECT COUNT(*) FROM pasajeros WHERE id_habitacion = %s", (id_habitaciones,))
    cantidad_pasajeros = cursor.fetchone()[0]

    if cantidad_pasajeros < capacidad_maxima:
        # Agregar el nuevo pasajero
        cursor.execute("""
            INSERT INTO pasajeros (nombre, rut, id_habitacion, fecha_entrada, fecha_salida)
            VALUES (%s, %s, %s, %s, %s)
        """, (nombre, rut, id_habitaciones, fecha_entrada, fecha_salida))
        
        # Incrementar la cantidad de pasajeros en la habitación
        cantidad_pasajeros += 1

        # Si se alcanza la capacidad máxima, marcar la habitación como ocupada
        if cantidad_pasajeros >= capacidad_maxima:
            cursor.execute("UPDATE habitaciones SET ocupado = 1 WHERE id_habitacion = %s", (id_habitaciones,))
        
        conexion.commit()
        cerrar_conexion(conexion, cursor)
        print("Pasajero agregado correctamente.")
    else:
        print("La habitación ya está llena.")
        cerrar_conexion(conexion, cursor)

def modificar_pasajero(id_pasajero):
    nuevo_nombre = input("Ingrese el nuevo nombre del pasajero: ")
    nuevo_rut = input("Ingrese el nuevo RUT del pasajero: ")
    nueva_habitacion = input("Ingrese la nueva habitación del pasajero: ")
    nueva_entrada = input("Ingrese la nueva fecha de entrada (YYYY-MM-DD HH:MM:SS): ")
    nueva_salida = input("Ingrese la nueva fecha de salida (YYYY-MM-DD HH:MM:SS): ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("UPDATE pasajeros SET nombre = %s, rut = %s, id_habitacion = %s, fecha_entrada = %s, fecha_salida = %s WHERE id_pasajero = %s",
                       (nuevo_nombre, nuevo_rut, nueva_habitacion, nueva_entrada, nueva_salida, id_pasajero))
        conexion.commit()
        print("Pasajero modificado correctamente.")
    except mysql.connector.Error as error:
        print(f"No se pudo modificar el pasajero: {error}")
        conexion.rollback()
    finally:
        cerrar_conexion(conexion, cursor)


def eliminar_pasajero(id_pasajero):
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        # Obtener la información del pasajero antes de eliminarlo (opcional)
        cursor.execute("SELECT * FROM pasajeros WHERE id_pasajero = %s", (id_pasajero,))
        pasajero = cursor.fetchone()

        # Eliminar al pasajero
        cursor.execute("DELETE FROM pasajeros WHERE id_pasajero = %s", (id_pasajero,))
        
        # Marcar la habitación como no ocupada si no hay más pasajeros en ella
        id_habitacion = pasajero[3]
        cursor.execute("SELECT COUNT(*) FROM pasajeros WHERE id_habitacion = %s", (id_habitacion,))
        cantidad_pasajeros = cursor.fetchone()[0]
        
        if cantidad_pasajeros == 0:
            cursor.execute("UPDATE habitaciones SET ocupado = 0 WHERE id_habitacion = %s", (id_habitacion,))

        conexion.commit()
        cerrar_conexion(conexion, cursor)
        print("Pasajero eliminado correctamente.")
    except Exception as e:
        print(f"No se pudo eliminar el pasajero: {e}")
        cerrar_conexion(conexion, cursor)


########################################################################

########################### USUARIOS #############################################

def ver_usuarios():
    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()

        if usuarios:
            print("Usuarios registrados:")
            for usuario in usuarios:
                print(f"ID: {usuario[0]}, Nombre de usuario: {usuario[1]}, Tipo de usuario: {usuario[3]}")
        else:
            print("No hay usuarios registrados.")

    except mysql.connector.Error as error:
        print(f"Error al obtener usuarios: {error}")
    finally:
        cerrar_conexion(conexion, cursor)

def agregar_usuario(nombre_usuario, contrasena, tipo_usuario):
    conexion = conectar()
    cursor = conexion.cursor()

    cursor.execute("INSERT INTO usuarios (nombre_usuario, contrasena, tipo_usuario) VALUES (%s, %s, %s)", (nombre_usuario, contrasena, tipo_usuario))
    conexion.commit()

    cerrar_conexion(conexion, cursor)

def modificar_usuario():
    id_usuario = input("Ingrese el ID del usuario a modificar: ")
    nuevo_nombre = input("Ingrese el nuevo nombre de usuario: ")
    nueva_contrasena = input("Ingrese la nueva contraseña: ")
    nuevo_tipo = input("Ingrese el nuevo tipo de usuario: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("UPDATE usuarios SET nombre_usuario = %s, contrasena = %s, tipo_usuario = %s WHERE id_usuario = %s",
                       (nuevo_nombre, nueva_contrasena, nuevo_tipo, id_usuario))
        conexion.commit()
        print("Usuario modificado correctamente.")
    except mysql.connector.Error as error:
        print(f"No se pudo modificar el usuario: {error}")
        conexion.rollback()
    finally:
        cerrar_conexion(conexion, cursor)

def eliminar_usuario():
    id_usuario = input("Ingrese el ID del usuario a eliminar: ")

    conexion = conectar()
    cursor = conexion.cursor()

    try:
        cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))
        conexion.commit()
        print("Usuario eliminado correctamente.")
    except mysql.connector.Error as error:
        print(f"No se pudo eliminar el usuario: {error}")
        conexion.rollback()
    finally:
        cerrar_conexion(conexion, cursor)

from funciones import obtener_habitaciones_disponibles, agregar_habitaciones, agregar_pasajero, agregar_usuario, eliminar_usuario, ver_usuarios, modificar_usuario, eliminar_habitaciones, modificar_habitaciones, modificar_pasajero, eliminar_pasajero, mostrar_pasajeros 
from conexion import cerrar_conexion, conectar

def login(): 
    print("\nBIENVENIDO AL SISTEMA DE GESTION DE HOTEL")
    print("\nInicie sesión para continuar")

    while True:
        usuario = input("Usuario: ")
        contrasena = input("Contraseña: ")

        conexion = conectar()
        cursor = conexion.cursor()

        cursor.execute("SELECT tipo_usuario FROM usuarios WHERE nombre_usuario = %s AND contrasena = %s", (usuario, contrasena))
        usuario_encontrado = cursor.fetchone()

        if usuario_encontrado:
            tipo_usuario = usuario_encontrado[0]
            print(f"Bienvenido, {usuario}! Tipo de usuario: {tipo_usuario}")
            if tipo_usuario == 'administrador':
                funciones_administrador()
            elif tipo_usuario == 'encargado':
                funciones_encargado()
            else:
                print("Tipo de usuario no válido")
            break
        else:
            print("\nCredenciales incorrectas. Intente de nuevo.")

        cerrar_conexion(conexion, cursor)


def funciones_administrador():
    while True:
        print("\n===== Menú Administrador =====")
        print("\n1.- Ver usuarios"),
        print("2.- Agregar usuario"),
        print("3.- Modificar usuario"),
        print("4.- Eliminar usuario"),
        print("5.- Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            ver_usuarios()
        elif opcion == "2":
            agregar_nuevo_usuario()
        elif opcion == "3":
            modificar_usuario()
        elif opcion == "4":
            eliminar_usuario()
        elif opcion == "5":
            print("\n¡Hasta luego!")
            break
        else:
            print("\nOpción inválida. Por favor, seleccione una opción válida.")

def funciones_encargado():
    while True:
        print("\n===== Menú Encargado =====")
        print("\n1.- Gestión de Habitaciones"),
        print("2.- Gestión de Pasajeros"),
        print("8.- Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            menu_gestion_habitaciones()
        elif opcion == "2":
            menu_gestion_pasajeros()
        elif opcion == "8":
            print("\n¡Hasta luego!")
            break
        else:
            print("Opción inválida. Por favor, seleccione una opción válida.")

def menu_gestion_habitaciones():
    while True:
        print("\n===== Gestión de Habitaciones =====")
        print("\n1.- Ver habitaciones disponibles"),
        print("2.- Agregar Habitación"),
        print("3.- Modificar Habitación"),
        print("4.- Eliminar Habitación"),
        print("8.- Volver atrás")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_habitaciones()
        elif opcion == "2":
            agregar_nueva_habitaciones()
        elif opcion == "3":
            modificar_habitaciones()
        elif opcion == "4":
            eliminar_habitaciones()
        elif opcion == "8":
            break
        else:
            print("\nOpción inválida. Por favor, seleccione una opción válida.")
            
def menu_gestion_pasajeros():
    while True:
        print("\n===== Gestión de Pasajeros =====")
        print("\n1.- Mostrar Pasajero"),
        print("2.- Agregar Pasajero"),
        print("3.- Eliminar Pasajero"),
        print("4.- Modificar Pasajero"),
        print("8.- Volver atrás")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            mostrar_pasajeros()
        elif opcion == "2":
            agregar_nuevo_pasajero()
        elif opcion == "3":
            # Obtener el ID del pasajero a eliminar
            id_pasajero = input("Ingrese el ID del pasajero a eliminar: ")
            eliminar_pasajero(id_pasajero)  # Pasar el ID del pasajero
        elif opcion == "4":
            # Obtener el ID del pasajero a modificar
            id_pasajero = input("Ingrese el ID del pasajero a modificar: ")
            modificar_pasajero(id_pasajero)

        elif opcion == "8":
            break
        else:
            print("\nOpción inválida. Por favor, seleccione una opción válida.")


def mostrar_habitaciones():
    habitaciones = obtener_habitaciones_disponibles()
    if habitaciones:
        print("\nHabitaciones disponibles:")
        for habitaciones in habitaciones:
            print(habitaciones)
    else:
        print("\nNo hay habitaciones disponibles actualmente.")

def agregar_nueva_habitaciones():
    id_habitaciones = input("Ingrese el id de la habitaciones: ")
    numero = input("Ingrese el número de la habitación: ")
    capacidad = input("Ingrese la capacidad de la habitación: ")
    orientacion = input("Ingrese la orientación de la habitación: ")
    ocupado = input("Ingrese la ocupacion de la habitaciones: ")
    agregar_habitaciones(id_habitaciones, numero, capacidad, orientacion, ocupado)
    print("Habitación agregada correctamente.")

def agregar_nuevo_pasajero():
    nombre = input("Ingrese el nombre del pasajero: ")
    rut = input("Ingrese el RUT del pasajero: ")
    id_habitaciones = input("Ingrese el ID de la habitación: ")
    fecha_entrada = input("Ingrese la fecha de entrada (YYYY-MM-DD HH:MM:SS): ")
    fecha_salida = input("Ingrese la fecha de salida (YYYY-MM-DD HH:MM:SS): ")
    agregar_pasajero(nombre, rut, id_habitaciones, fecha_entrada, fecha_salida)
    print("Pasajero agregado correctamente.")

def agregar_nuevo_usuario():
    nombre_usuario = input("Ingrese el nombre de usuario: ")
    contrasena = input("Ingrese la contraseña: ")
    while True:
        print("Los tipos de USUARIOS son 'administrador' y 'encargado'")
        tipo_usuario = input("Ingrese el tipo de usuario: ")
        if tipo_usuario == 'administrador' or tipo_usuario == 'encargado':
            agregar_usuario(nombre_usuario, contrasena, tipo_usuario)
            print("Usuario agregado correctamente.")
            break
        else:
            print("\nEse tipo de usuario no existe")

if __name__ == "__main__":
    login() 
    
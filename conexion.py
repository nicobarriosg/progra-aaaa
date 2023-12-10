import mysql.connector

def conectar():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='Hotel',
        port='3306'
    )

def cerrar_conexion(conexion, cursor):
    cursor.close()
    conexion.close()

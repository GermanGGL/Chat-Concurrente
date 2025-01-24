import tkinter as tk
from tkinter import scrolledtext
import socket
import threading
import datetime
import mysql.connector 
from mysql.connector import Error



# Lista para almacenar los clientes conectados y sus detalles
clients = []
client_details = {}
server = None
server_running = False


#======================================================================================================
#===============================  Conexion a la bd   ==================================================
#======================================================================================================
def conectar():
    global conexion 
    try:
        # Establecer la conexión
        conexion = mysql.connector.connect(
            host='localhost',      # Por ejemplo, 'localhost' o una dirección IP
            database='dbchat',
            user='root',
            password='', 
            port='3306'
        )

        if conexion.is_connected():
            print('Conexión exitosa a la base de datos')

            # Crear  un cursor
            cursor = conexion.cursor()

            # Ejecutar una consulta
            cursor.execute('SELECT * FROM conexiones')
            #cursor.execute('SELECT * FROM desconexiones')

            # Obtener todos los registros
            registros = cursor.fetchall()

            print('Registros obtenidos de la tabla:')
            for registro in registros:
                print(registro)

    except Error as e:
        print(f'Error al conectar a la base de datos: {e}')
    finally:
        if conexion.is_connected():
            cursor.close()
            conexion.close()
            print('Conexión cerrada')


# Función para manejar la recepción de mensajes de un cliente y retransmitirlos a otros
def handle_client(client_socket, addr):
    nickname = client_socket.recv(1024).decode('utf-8')
    client_details[client_socket] = (addr, nickname, datetime.datetime.now())
    log_event(f"Conexión aceptada de {addr} con nombre de usuario {nickname} a las {client_details[client_socket][2].strftime('%Y-%m-%d %H:%M:%S')}")
    

    cursor = conexion.cursor()

    # Insertar datos en la tabla conexiones
    insert_conexion_query = """
    INSERT INTO conexiones (usuario, fecha, hora, ip, puerto)
    VALUES (%s, %s, %s, %s, %s)
    """
    conexion_data = ('usuario1', '2025-01-24', '14:00:00', '192.168.1.1', 8080)
    cursor.execute(insert_conexion_query, conexion_data)

    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            broadcast(message, client_socket)
        except:
            log_event(f"Usuario {nickname} con IP {addr} se desconectó a las {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            clients.remove(client_socket)
            del client_details[client_socket]
            client_socket.close()
            break

# Función para retransmitir mensajes a todos los clientes
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try:
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)

# Función para iniciar el servidor
def start_server():
    global server, server_running
    if not server_running:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 5555))
        server.listen(5)
        server_running = True
        log_event("Servidor iniciado en el puerto 5555")
        threading.Thread(target=accept_connections).start()

# Función para aceptar conexiones
def accept_connections():
    while server_running:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

# Función para detener el servidor
def stop_server():
    global server, server_running
    if server_running:
        server_running = False
        for client in clients:
            client.close()
        if server:
            server.close()
        clients.clear()
        client_details.clear()
        log_event("Servidor detenido")

# Función para registrar eventos en la interfaz gráfica
def log_event(message):
    event_log.config(state=tk.NORMAL)
    event_log.insert(tk.END, message + "\n")
    event_log.config(state=tk.DISABLED)

# Función para manejar el cierre de la ventana del servidor
def on_closing():
    stop_server()
    root.destroy()


#======================================================================================================
#===============================   Entorno grafico   ==================================================
#======================================================================================================

# Llamar a la funcion de conexion a la bd
conectar()

# Configuración de la ventana principal del servidor
root = tk.Tk()
root.title("Servidor de Chat")
root.geometry("500x425")

# Área de texto para mostrar eventos
event_log = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=60, height=20)
event_log.pack(pady=10, padx=10)

# Botones para iniciar y detener el servidor
start_button = tk.Button(root, text="Iniciar Servidor", command=start_server)
start_button.pack(pady=5)

stop_button = tk.Button(root, text="Detener Servidor", command=stop_server)
stop_button.pack(pady=5)

# Manejar el cierre de la ventana
root.protocol("WM_DELETE_WINDOW", on_closing)

# Ejecutar la aplicación
root.mainloop()
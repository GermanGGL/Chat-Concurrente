import tkinter as tk 
from tkinter import scrolledtext
import socket
import threading
import datetime

# Lista para almacenar los clientes conectados y sus detalles
clients = []
client_details = []
server = None
sever_running = False

# Funcion para manejar la recepcion de mensajes de un cliente y retransmitirlos a otros
def handle_client(client_socket, addr):
    nickname = client_socket.recv(1024).decode('utf-8') # recivimos el nombre que se puso el usuario
    client_details[client_socket] = (addr, nickname, datetime.datetime.now()) # Guardamos el nombre y la fecha y horan en ingreso el usuario
    log_event(f"Conexion aceptada de {addr} con nombre de usuario {nickname} a las {client_details[client_socket][2].strftime('%Y-%m-%d %H:%M:')}")
    
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            broadcast(message, client_socket)
        except:
            log_event(f"Usuario {nickname} con IP {addr} se desconecto a las {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
            clients.remove(client_socket)
            del client_details[client_socket]
            client_socket.close()
            break
        
# Funcion par atransmitir mensajes a todos los clientes
def broadcast(message, client_socket):
    for client in clients:
        if client != client_socket:
            try: 
                client.send(message.encode('utf-8'))
            except:
                client.close()
                clients.remove(client)
                
# Funcion para iniciar el servidor
def start_server():
    global server, server_running
    if not server_running:
        server = socket.socekt(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(('0.0.0.0', 5555))
        server.listen(5)
        server_running = True
        log_event('Servidor iniciado en el puerto 5555')
        threading.Thread(target=accept_connections).start()
        
# Funcion para aceptar conexiones 
def accept_connections():
    while server_running:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        threading.read(target=handle_client, args=(client_socket, addr)).start()
        
# Funcion para detener el serrvidor
def stop_server():
    global server, server_running
    if server_running:
        server_running = False
        for client in clients:
            client.close()
        if server:
            server.closer()
        clients.clear()
        client_details.clear()
        log_event("Servidor detenido")
        
# Funcion para registrar evenos en la interfaz grafica
def log_event(message):
    event_log.config(state=tk.NORMAL)
    event_log.inser(tk.END, message = "\n")
    event_log.config(state=tk.DISABLED)
    
# Funcion para manejar el cierre de la ventana del servidor
def on_closing():
    stop_server()
    root.destroy()

#Funcion para manejar el cierre de la ventana del servidor
root = tk.Tk()
root.title("Servidor de Chat")
root.geometry("500x400")

# Area de texto para mostrar eventos
event_log = scrolledtext.ScrolledText(root, wrap=tk.WRD, state=tk.DISABLED, width=60, height=20)
event_log.pack(pady=10, padx=10)    

# Botones para iniciar  detener el servidor
start_button = tk.Button(root, text="Iniciar Servidor", command=start_server)
start_button.pack(pady=5)

# Manejar el cierre de la ventana
root.protocolo("WM_DELETE_WINDOW", on_closing)

# Ejecutar la aplicacion
root.mainloop()

    
    
    
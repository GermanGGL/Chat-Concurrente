import tkinter as tk
from tkinter import scrolledtext, messagebox
import socket
import threading

client_socket = None

def send_message():
    message = entry_message.get()
    if message:
        chat_window.config(state=tk.NORMAL)
        chat_window.insert(tk.END, f"Tú: {message}\n")
        chat_window.config(state=tk.DISABLED)
        client_socket.send(f"{entry_nickname.get()}: {message}".encode('utf-8'))
        entry_message.delete(0, tk.END)
        
# Funcion para recibir mensaje del servidor 
def receive_messages():
    while True: 
        try:
            message = client_socket.recv(1024).decode('utf-8')
            chat_window.config(state=tk.NORMAL)
            chat_window.insert(tk.END, message + "\n")
            chat_window.config(state=tk.DISABLED)
        except:
            messagebox.showerror("Error", "Se perdió la conexión con el servidor")
            disconnect()
            break
        
# Funcion para establecer conexion con el servidor
def connect():
    global client_socket
    ip = entry_ip.get()    
    port = int(entry_port.get())
    nickname = entry_nickname.get()    
    if ip and port and nickname:
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STEAM)
            client_socket.connect((ip, port))
            client_socket.send(nickname.encode('utf-8'))
            messagebox.showinfo("Conexion", f"Conectado a {ip}:{port} como {nickname}")
            threading.Thread(target=receive_messages).start()
        except:
            messagebox.showerror("Error", "No se pudo conectar al servidor")
    else:
        messagebox.showwarning("Advertencia", "Debe ingresar todos los campos para conectarse")
        
# Funcion para desconectar del servidor
def disconnect():
    global client_socket
    if client_socket:
        try:
            client_socket.close()
        except:
            pass    
        client_socket = None
        messagebox.showinfo("Desconexion", "Desconectado del servidor")
        
# Funcion para menejar el cierre de la ventana del cliente
def on_clossing():
    disconnect()
    root.destroy()
    
# Configuracion de la ventana principal
root = tk.Tk()
root.title("Cliente de Chat")
root.protocol("WM_DELETE_WINDOW", on_clossing)
root.geometry("500x500")

# Crear etiquetas y campos de entrada para la IP, puerto y nickname
tk.Label(root, text="IP:").pack(pady=5)
entry_ip = tk.Entry(root, width=50)
entry_ip.pack(pady=5)

tk.Label(root, text="Puerto:").pack(pady=5)
entry_port = tk.Entry(root, width=50)
entry_port.pack(pady=5)

tk.Label(root, text="Nickname:").pack(pady=5)
entry_nickname = tk.Entry(root, width=50)
entry_nickname.pack(pady=5)

# Boton para conectarse
connect_button = tk.Button(root, text="Conectar", command=connect)
connect_button.pack(pady=10)

# Crear el area de chat
chat_window = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, width=60, height=20)
chat_window.pack(pady=10, padx=10)
  
# Crear el campo de entrada de texto para el mensaje
entry_message = tk.Entry(root, width=50)
entry_message.pack(pady=10, padx=10, fill=tk.X)
entry_message.bind("<Return>", lambda event: send_message())
  
# Crear el boton de enviar
send_button = tk.Button(root, text="Enviar", command=send_message)
send_button.pack(pady=10)

# Boton de desconexion
disconnect_button = tk.Button(root, text="Desconectar", command=disconnect)
disconnect_button.pack(pady=10)

# Ejecutar la aplicacion 
root.mainloop()

        
import subprocess
import sys
import signal

print ("[*] Comprobando e instalando módulos necesarios")
def check_and_install(module):
    try:
        __import__(module)
    except ImportError:
        print(f"[*] El módulo {module} no está instalado. Instalando...")
        subprocess.check_call(["pip", "install", module])

check_and_install('socket')
check_and_install('colorama')
check_and_install('sys')
check_and_install('signal')

print ("[*] Importando módulos necesarios")
import socket
from colorama import init, Fore, Style

init()  # Inicializar colorama para el uso de colores ANSI

print ("[*] Configurando servidor proxy")
HOST = ''  # Dejar en blanco para usar cualquier dirección IP disponible
PORT = input(Fore.YELLOW + "Puerto (Por defecto #8888): " + Style.RESET_ALL) or '8888'  # Puerto del servidor proxy
PORT = int(PORT)

# Función para manejar la señal SIGINT (Ctrl+C)
def sigint_handler(sig, frame):
    print(Fore.RED + "\n[!] Saliendo del servidor proxy..." + Style.RESET_ALL)
    sys.exit(0)

# Registrar el manejador de señal SIGINT (Ctrl+C)
signal.signal(signal.SIGINT, sigint_handler)

print ("[*] Creando socket para escuchar conexiones entrantes")
proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
proxy_socket.bind((HOST, PORT))
proxy_socket.listen(1)
print(Fore.GREEN + f'[*] Escuchando en {HOST}:{PORT}...' + Style.RESET_ALL)

while True:
    print ("[*] Esperando nueva conexión")
    client_socket, client_address = proxy_socket.accept()
    print(Fore.CYAN + f'\n[*] Conexión aceptada desde {client_address[0]}:{client_address[1]}' + Style.RESET_ALL)

    print ("[*] Recibiendo datos del cliente")
    request_data = client_socket.recv(4096)
    print(Fore.YELLOW + f'Recibido {len(request_data)} bytes de datos:' + Style.RESET_ALL)
    print(request_data.decode())

    print ("[*] Enviando datos al servidor de destino")
    target_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    target_socket.connect(('destino.com', 80))
    target_socket.send(request_data)

    print ("[*] Recibiendo datos del servidor de destino")
    response_data = target_socket.recv(4096)

    print ("[*] Enviando datos al cliente")
    client_socket.send(response_data)

    print ("[*] Imprimiendo datos de respuesta")
    print(Fore.YELLOW + f'Recibido {len(response_data)} bytes de datos del servidor de destino:' + Style.RESET_ALL)
    print(response_data.decode())

    print ("[x] Cerrando conexiones")
    target_socket.close()
    client_socket.close()

import socket
import threading
from queue import Queue

# Configurações iniciais
target = input("Digite o IP ou Domínio para escanear (ex: google.com): ")
queue = Queue()
open_ports = []

def port_scan(port):
    """Tenta conectar a uma porta específica."""
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1) # Tempo de espera para não travar
        result = sock.connect_ex((target, port))
        if result == 0:
            open_ports.append(port)
        sock.close()
    except:
        pass

def fill_queue(port_list):
    """Preenche a fila com as portas que queremos testar."""
    for port in port_list:
        queue.put(port)

def worker():
    """Função que cada thread executará."""
    while not queue.empty():
        port = queue.get()
        port_scan(port)

def run_scanner(threads, port_range):
    fill_queue(port_range)
    thread_list = []

    for _ in range(threads):
        thread = threading.Thread(target=worker)
        thread_list.append(thread)
        thread.start()

    for thread in thread_list:
        thread.join() # Espera todas as threads terminarem

    print(f"\n--- Resultado para {target} ---")
    if open_ports:
        for port in sorted(open_ports):
            print(f"Porta {port}: ABERTA")
    else:
        print("Nenhuma porta aberta encontrada.")

if __name__ == "__main__":
    # Escaneando as portas mais comuns (1 a 1024)
    run_scanner(threads=100, port_range=range(1, 1025))

import time
import ctypes
import csv
from datetime import datetime

def send_notification(title, message):
    """Envia uma notificação nativa no Windows."""
    # Para Linux/Mac, poderia usar a biblioteca 'plyer'
    ctypes.windll.user32.MessageBoxW(0, message, title, 64)

def log_break(status):
    """Registra se a pausa foi realizada com sucesso."""
    with open("health_log.csv", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), status])

def start_timer(minutes):
    """Contador de tempo simples no terminal."""
    seconds = minutes * 60
    while seconds > 0:
        mins, secs = divmod(seconds, 60)
        timer = f'{mins:02d}:{secs:02d}'
        print(f"Próxima pausa em: {timer}", end="\r")
        time.sleep(1)
        seconds -= 1

if __name__ == "__main__":
    print("--- Eye Guardian: Monitor de Saúde Ocular ---")
    print("Mantenha este script rodando para proteger sua visão.")
    
    try:
        while True:
            # Espera 20 minutos de foco
            start_timer(20)
            
            # Hora da pausa
            send_notification(
                "Hora de descansar!", 
                "Olhe para algo a 6 metros de distância por 20 segundos."
            )
            
            # Registra a pausa
            log_break("Pausa Realizada")
            print("\n[LOG] Pausa registrada. Retornando ao foco...")
            
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado. Cuide dos seus olhos!")

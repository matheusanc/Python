import pygetwindow as gw
import time
import json
from datetime import datetime

def track_productivity(duration_seconds=60):
    stats = {}
    end_time = time.time() + duration_seconds
    
    print(f"Rastreando produtividade por {duration_seconds} segundos...")
    
    try:
        while time.time() < end_time:
            # Obtém a janela ativa no momento
            active_window = gw.getActiveWindow()
            
            if active_window:
                app_name = active_window.title
                # Simplifica o nome (opcional)
                stats[app_name] = stats.get(app_name, 0) + 1
            
            time.sleep(1) # Verifica a cada segundo
            
    except KeyboardInterrupt:
        print("\nInterrompido pelo usuário.")

    return stats

def save_report(stats):
    filename = f"report_{datetime.now().strftime('%Y-%m-%d_%H-%M')}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)
    print(f"Relatório salvo em: {filename}")

if __name__ == "__main__":
    # Rastreia por 1 minuto como demonstração
    results = track_productivity(60)
    
    print("\n--- Resumo de Atividade ---")
    for app, seconds in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f"{app}: {seconds}s")
    
    save_report(results)

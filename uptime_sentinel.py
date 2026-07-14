import requests
import time
import json
from datetime import datetime

# Lista de serviços para monitorar (adicione as URLs que desejar)
SERVICES_TO_MONITOR = [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "GitHub", "url": "https://api.github.com"},
    {"name": "Exemplo Inválido", "url": "https://httpbin.org/status/404"}
]

def check_services(services):
    """Verifica o status HTTP e o tempo de resposta de cada serviço."""
    report = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "results": []
    }
    
    print(f"\n🚀 Iniciando varredura dos serviços às {report['timestamp']}...")
    
    for service in services:
        try:
            start_time = time.time()
            response = requests.get(service["url"], timeout=5)
            response_time = round((time.time() - start_time) * 1000, 2) # em milissegundos
            
            status_code = response.status_code
            is_online = 200 <= status_code < 300
            
        except requests.exceptions.RequestException as e:
            status_code = None
            response_time = None
            is_online = False
            
        status_msg = "ONLINE ✅" if is_online else "OFFLINE ❌"
        print(f"  [{service['name']}] -> {status_msg} ({response_time or 'N/A'}ms) [Status: {status_code or 'Erro'}]")
        
        report["results"].append({
            "name": service["name"],
            "url": service["url"],
            "online": is_online,
            "status_code": status_code,
            "response_time_ms": response_time
        })
        
    return report

def save_log(report_data, filename="uptime_log.json"):
    """Salva o relatório em um histórico JSON cumulativo."""
    try:
        with open(filename, "r", encoding="utf-8") as f:
            history = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        history = []
        
    history.append(report_data)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    # Executa uma rodada de checagem
    current_report = check_services(SERVICES_TO_MONITOR)
    save_log(current_report)
    print("\n💾 Histórico atualizado em 'uptime_log.json'.")

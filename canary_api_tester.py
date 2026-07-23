import urllib.request
import json
import time
from datetime import datetime

# Configuração dos endpoints para testar (Simulando uma API real com HTTPBin)
API_ROUTES = [
    {
        "name": "Autenticação (Login)",
        "url": "https://httpbin.org/post",
        "method": "POST",
        "payload": {"user": "admin", "token": "secret_canary_123"},
        "expected_keys": ["json", "headers", "url"]
    },
    {
        "name": "Busca de Perfil",
        "url": "https://httpbin.org/get?user_id=42",
        "method": "GET",
        "payload": None,
        "expected_keys": ["args", "origin"]
    }
]

def test_endpoint(route):
    """Executa a requisição HTTP usando apenas a biblioteca nativa urllib."""
    url = route["url"]
    method = route["method"]
    payload = route["payload"]
    
    data = json.dumps(payload).encode('utf-8') if payload else None
    headers = {'Content-Type': 'application/json'} if payload else {}
    
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    start_time = time.time()
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            latency = round((time.time() - start_time) * 1000, 2)
            status = response.status
            body = json.loads(response.read().decode('utf-8'))
            
            # Validação básica de Schema (verifica se as chaves esperadas existem)
            schema_ok = all(key in body for key in route["expected_keys"])
            
            return {
                "success": status == 200 and schema_ok,
                "status": status,
                "latency": f"{latency}ms",
                "error": None if schema_ok else "Falha na validação do Schema JSON"
            }
    except Exception as e:
        return {
            "success": False,
            "status": getattr(e, 'code', 'Erro de Conexão'),
            "latency": "N/A",
            "error": str(e)
        }

def generate_markdown_report(results):
    """Gera um relatório estruturado em Markdown para o console ou arquivo."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md = f"# 🚀 Relatório de Teste Canary API\n**Data/Hora:** {timestamp}\n\n"
    md += "| Endpoint | Método | Status | Latência | Resultado |\n"
    md += "| :--- | :---: | :---: | :---: | :--- |\n"
    
    all_passed = True
    for name, route, res in results:
        status_icon = "🟢 PASSED" if res["success"] else "🔴 FAILED"
        if not res["success"]:
            all_passed = False
        details = res["error"] if res["error"] else "API está saudável"
        md += f"| {name} | `{route['method']}` | {res['status']} | {res['latency']} | {status_icon} ({details}) |\n"
        
    md += f"\n**Status Geral do Sistema:** {'🟢 100% Operacional' if all_passed else '⚠️ Alerta em Produção'}\n"
    return md

if __name__ == "__main__":
    print("🧪 Iniciando testes de fumaça (Smoke/Canary Tests)...")
    test_results = []
    
    for route in API_ROUTES:
        print(f"  Enviando requisição para: {route['name']}...")
        result = test_endpoint(route)
        test_results.append((route['name'], route, result))
        time.sleep(0.5) # Evita rate limiting na API de testes
        
    report = generate_markdown_report(test_results)
    print("\n" + report)
    
    # Salva o relatório automaticamente
    with open("CANARY_REPORT.md", "w", encoding="utf-8") as f:
        f.write(report)
    print("💾 Relatório salvo com sucesso em 'CANARY_REPORT.md'")

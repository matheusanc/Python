import requests
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_exchange_rate(base="USD", target="BRL"):
    """Busca a cotação atual usando a AwesomeAPI (gratuita)."""
    url = f"https://economia.awesomeapi.com.br/json/last/{base}-{target}"
    try:
        response = requests.get(url)
        data = response.json()
        pair = f"{base}{target}"
        return float(data[pair]["bid"])
    except Exception as e:
        print(f"Erro ao buscar cotação: {e}")
        return None

def get_history(base="USD", target="BRL", days=7):
    """Busca o histórico dos últimos X dias."""
    url = f"https://economia.awesomeapi.com.br/json/daily/{base}-{target}/{days}"
    response = requests.get(url)
    data = response.json()
    
    prices = [float(item["bid"]) for item in data][::-1]
    dates = [(datetime.now() - timedelta(days=i)).strftime("%d/%m") for i in range(days)][::-1]
    
    return dates, prices

def plot_data(dates, prices, base, target):
    """Gera um gráfico simples da variação."""
    plt.figure(figsize=(10, 5))
    plt.plot(dates, prices, marker='o', linestyle='-', color='g')
    plt.title(f"Variação {base} para {target} (Últimos dias)")
    plt.xlabel("Data")
    plt.ylabel("Preço de Venda")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    base_currency = "USD"
    target_currency = "BRL"
    
    current_price = get_exchange_rate(base_currency, target_currency)
    
    if current_price:
        print(f"--- Cotação Atual ---")
        print(f"1 {base_currency} = {current_price:.2f} {target_currency}")
        
        print("\nGerando gráfico de histórico...")
        d, p = get_history(base_currency, target_currency)
        plot_data(d, p, base_currency, target_currency)

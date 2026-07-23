import time
from datetime import datetime, timedelta

class CircuitBreakerOpenException(Exception):
    """Exceção lançada quando o disjuntor está aberto e bloqueia a requisição."""
    pass

class CircuitBreaker:
    def __init__(self, failure_threshold=3, recovery_time_seconds=5):
        self.failure_threshold = failure_threshold
        self.recovery_time_seconds = recovery_time_seconds
        
        # Estados: CLOSED (Fechado/Normal), OPEN (Aberto/Bloqueado), HALF-OPEN (Semi-aberto/Teste)
        self.state = "CLOSED"
        self.failure_count = 0
        self.next_attempt_time = datetime.now()

    def call(self, func, *args, **kwargs):
        """Executa a função protegida pelo disjuntor."""
        self._update_state()

        if self.state == "OPEN":
            raise CircuitBreakerOpenException(f"🚨 Disjuntor ABERTO. Requisição bloqueada até {self.next_attempt_time.strftime('%H:%M:%S')}")

        try:
            result = func(*args, **kwargs)
            # Se deu certo e estava em HALF-OPEN, o sistema se recuperou!
            if self.state == "HALF-OPEN":
                print("🟢 Serviço recuperado! Fechando o disjuntor.")
                self.state = "CLOSED"
                self.failure_count = 0
            return result
        except Exception as e:
            self._handle_failure()
            raise e

    def _update_state(self):
        """Gerencia a transição de tempo para o estado HALF-OPEN."""
        if self.state == "OPEN" and datetime.now() >= self.next_attempt_time:
            print("🟡 Tempo de espera esgotado. Movendo para HALF-OPEN (Testando serviço)...")
            self.state = "HALF-OPEN"

    def _handle_failure(self):
        """Contabiliza falhas e abre o disjuntor se atingir o limite."""
        self.failure_count += 1
        print(f"❌ Falha detectada! ({self.failure_count}/{self.failure_threshold})")
        
        if self.state in ("CLOSED", "HALF-OPEN") and self.failure_count >= self.failure_threshold:
            print(f"🔥 Limite de falhas atingido! ABRINDO o disjuntor por {self.recovery_time_seconds}s.")
            self.state = "OPEN"
            self.next_attempt_time = datetime.now() + timedelta(seconds=self.recovery_time_seconds)

# --- Simulação de Uso Prático ---
if __name__ == "__main__":
    print("=== Simulador de Resiliência: Circuit Breaker ===")
    
    # Simula uma API instável
    request_counter = 0
    def unstable_api():
        global request_counter
        request_counter += 1
        # Simula que as primeiras 4 requisições vão falhar (API fora do ar)
        # E a partir da 5ª ela volta ao normal
        if request_counter <= 4:
            raise RuntimeError("Erro 503: Service Unavailable")
        return "✨ Dados retornados com sucesso da API!"

    # Inicializa o disjuntor: abre após 3 falhas, espera 5 segundos para testar novamente
    breaker = CircuitBreaker(failure_threshold=3, recovery_time_seconds=5)

    for i in range(1, 9):
        print(f"\n[Tentativa #{i}]")
        try:
            # Executa a API encapsulada pelo disjuntor
            response = breaker.call(unstable_api)
            print(f"Sucesso: {response}")
        except CircuitBreakerOpenException as e:
            print(e)
            print("💡 Executando lógica de Fallback (ex: carregando dados do cache local)...")
        except Exception as e:
            print(f"Aplicação capturou o erro da API: {e}")
            
        time.sleep(1) # Aguarda 1 segundo entre as chamadas

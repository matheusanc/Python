import threading
import time
from queue import Queue, Empty
from contextlib import contextmanager

class NoConnectionAvailableException(Exception):
    """Exceção lançada quando o timeout expira e nenhuma conexão é liberada."""
    pass

class SimulatedConnection:
    """Simula uma conexão real (como um socket ou conexão de banco de dados)."""
    def __init__(self, id: int):
        self.id = id

    def execute(self, query: str):
        print(f"🔌 [Conexão {self.id}] Executando: '{query}'")
        time.sleep(1)  # Simula o tempo de processamento da query

class ConnectionPool:
    def __init__(self, max_connections: int = 3, timeout: float = 2.0):
        self.timeout = timeout
        self.pool = Queue(maxsize=max_connections)
        
        # Inicializa o pool com conexões pré-abertas
        for i in range(max_connections):
            self.pool.put(SimulatedConnection(id=i + 1))

    @contextmanager
    def acquire(self):
        """Gerenciador de contexto para adquirir e liberar conexões com segurança."""
        connection = None
        try:
            # Tenta pegar uma conexão da fila até o limite do timeout
            connection = self.pool.get(timeout=self.timeout)
            yield connection
        except Empty:
            raise NoConnectionAvailableException(
                f"🚨 Timeout de {self.timeout}s atingido! Todas as conexões estão ocupadas."
            )
        finally:
            if connection:
                # Garante que a conexão volte para o pool, mesmo se o código do usuário falhar
                self.pool.put(connection)

# --- Simulação de Uso com Múltiplas Threads ---
def worker_task(pool: ConnectionPool, thread_name: str, query: str):
    print(f"👤 {thread_name} tentando obter conexão...")
    try:
        # O 'with' aciona o @contextmanager automaticamente
        with pool.acquire() as conn:
            print(f"✅ {thread_name} conseguiu a Conexão {conn.id}")
            conn.execute(query)
            print(f"🔄 {thread_name} liberou a Conexão {conn.id}")
    except NoConnectionAvailableException as e:
        print(f"❌ {thread_name} falhou: {e}")

if __name__ == "__main__":
    print("=== Simulador de Connection Pool Semântico ===")
    print("Configuração: Pool de 3 conexões máximo | Timeout de 2 segundos\n")
    
    # Cria um pool com apenas 3 conexões
    db_pool = ConnectionPool(max_connections=3, timeout=2.0)
    
    # Criamos 5 threads tentando rodar ao mesmo tempo (2 vão ter que esperar ou falhar)
    threads = []
    queries = [
        "SELECT * FROM usuarios",
        "UPDATE produtos SET estoque = 10",
        "INSERT INTO logs VALUES ('info')",
        "SELECT * FROM relatorios",
        "DELETE FROM sessoes_expiradas"
    ]

    for i in range(5):
        t = threading.Thread(
            target=worker_task, 
            args=(db_pool, f"Thread-{i+1}", queries[i])
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

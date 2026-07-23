import time
import threading
from collections import OrderedDict
from typing import Any, Optional

class TTLRUCache:
    """
    Cache LRU thread-safe com suporte a expiração individual por tempo (TTL).
    """
    def __init__(self, capacity: int = 5, default_ttl: float = 3.0):
        self.capacity = capacity
        self.default_ttl = default_ttl
        self.cache: OrderedDict[str, tuple[Any, float]] = OrderedDict()
        self.lock = threading.RLock() # Trava reentrante para segurança concorrente

    def _is_expired(self, expire_at: float) -> bool:
        return time.time() > expire_at

    def get(self, key: str) -> Optional[Any]:
        """Recupera um valor do cache se ele existir e não estiver expirado."""
        with self.lock:
            if key not in self.cache:
                return None

            value, expire_at = self.cache[key]

            # Se expirou, remove do cache e retorna None
            if self._is_expired(expire_at):
                del self.cache[key]
                print(f"⌛ [CACHE MISS] Chave '{key}' expirou.")
                return None

            # Move a chave para o final (marcando-a como Usada Recentemente)
            self.cache.move_to_end(key)
            print(f"⚡ [CACHE HIT] Chave '{key}' encontrada.")
            return value

    def set(self, key: str, value: Any, ttl: Optional[float] = None) -> None:
        """Armazena um valor com TTL customizado ou padrão."""
        ttl_seconds = ttl if ttl is not None else self.default_ttl
        expire_at = time.time() + ttl_seconds

        with self.lock:
            # Se a chave já existe, atualizamos e movemos para o final
            if key in self.cache:
                self.cache.move_to_end(key)
            self.cache[key] = (value, expire_at)

            # Evicção LRU: se ultrapassou a capacidade, remove o item mais antigo (primeiro elemento)
            if len(self.cache) > self.capacity:
                discarded_key, _ = self.cache.popitem(last=False)
                print(f"🗑️ [EVICÇÃO LRU] Capacidade excedida. Removido item menos usado: '{discarded_key}'")

    def cleanup(self) -> int:
        """Varredura manual para remover todas as chaves expiradas da memória."""
        with self.lock:
            expired_keys = [
                k for k, (_, expire_at) in self.cache.items() if self._is_expired(expire_at)
            ]
            for k in expired_keys:
                del self.cache[k]
            return len(expired_keys)

# --- Demonstração Prática ---
if __name__ == "__main__":
    print("=== Simulador de Cache LRU + TTL ===")
    print("Configuração: Capacidade = 3 itens | TTL Padrão = 2 segundos\n")

    cache = TTLRUCache(capacity=3, default_ttl=2.0)

    # 1. Inserção até a capacidade limite
    print("📝 Adicionando 3 itens ao cache...")
    cache.set("user:101", {"nome": "Ana", "cargo": "Dev"})
    cache.set("user:102", {"nome": "Bruno", "cargo": "Scrum Master"})
    cache.set("user:103", {"nome": "Carla", "cargo": "Engenheira"})

    # 2. Acessa o usuário 101 para torná-lo o "Mais Recente"
    time.sleep(0.5)
    print("\n🔍 Acessando 'user:101'...")
    cache.get("user:101")

    # 3. Adiciona um 4º item para forçar a evicção do Menos Recente ('user:102')
    print("\n📝 Inserindo 'user:104' (Excede capacidade do cache)...")
    cache.set("user:104", {"nome": "Daniel", "cargo": "Analista"})

    # 4. Tenta buscar o 'user:102' (deve ter sido descartado)
    print("\n🔍 Buscando 'user:102' descartado:")
    val = cache.get("user:102")
    print(f"Resultado: {val}")

    # 5. Espera o tempo de TTL esgotar para testar a expiração temporal
    print("\n⏳ Aguardando 2.5 segundos para os itens expirarem...")
    time.sleep(2.5)

    print("\n🔍 Buscando 'user:101' após expiração temporal:")
    val = cache.get("user:101")
    print(f"Resultado: {val}")

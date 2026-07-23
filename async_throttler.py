import asyncio
import time
from collections import deque
from typing import Callable, Any, TypeVar

T = TypeVar('T')

class SlidingWindowThrottler:
    """
    Throttler assíncrono baseado no algoritmo de Janela Deslizante (Sliding Window).
    Garante que no máximo `max_calls` sejam executadas a cada `time_frame` segundos.
    """
    def __init__(self, max_calls: int, time_frame: float):
        self.max_calls = max_calls
        self.time_frame = time_frame
        self.timestamps = deque()
        self._lock = asyncio.Lock()

    async def __call__(self, func: Callable[..., Any], *args, **kwargs) -> Any:
        async with self._lock:
            now = time.monotonic()

            # Remove carimbos de data/hora antigos fora da janela atual
            while self.timestamps and (now - self.timestamps[0]) >= self.time_frame:
                self.timestamps.popleft()

            # Se atingiu o limite da janela, calcula o tempo de espera necessário
            if len(self.timestamps) >= self.max_calls:
                sleep_time = self.time_frame - (now - self.timestamps[0])
                if sleep_time > 0:
                    print(f"⏳ [THROTTLER] Limite atingido ({self.max_calls}/{self.time_frame}s). Pausando por {sleep_time:.2f}s...")
                    await asyncio.sleep(sleep_time)
                
                # Atualiza o tempo atual após a pausa e limpa a janela novamente
                now = time.monotonic()
                while self.timestamps and (now - self.timestamps[0]) >= self.time_frame:
                    self.timestamps.popleft()

            # Registra a execução atual na janela
            self.timestamps.append(time.monotonic())

        # Executa a função empacotada
        return await func(*args, **kwargs)

# --- Demonstração Prática com Múltiplas Tasks Assíncronas ---

async def chamada_api_externa(task_id: int):
    """Simula uma requisição para um serviço externo."""
    print(f"🚀 [Task {task_id:02d}] Requisição disparada com sucesso às {time.strftime('%H:%M:%S')}")
    await asyncio.sleep(0.1) # Simula latência de rede
    return f"Resultado Task {task_id}"

async def main():
    print("=== Simulador de Controladora de Vazão (Sliding Window Throttler) ===")
    print("Regra: Máximo de 3 chamadas a cada 2.0 segundos\n")

    # Configura a regra: máx 3 execuções a cada 2 segundos
    throttler = SlidingWindowThrottler(max_calls=3, time_frame=2.0)

    # Dispara 8 tarefas assíncronas concorrentes de uma vez
    tasks = [
        throttler(chamada_api_externa, i) 
        for i in range(1, 9)
    ]

    print("🔥 Disparando 8 chamadas concorrentes simultâneas...\n")
    resultados = await asyncio.gather(*tasks)
    
    print("\n✅ Todas as chamadas foram concluídas dentro do limite estipulado!")

if __name__ == "__main__":
    asyncio.run(main())

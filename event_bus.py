import asyncio
import inspect
from typing import Callable, Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Event:
    """Representa um evento genérico no sistema."""
    topic: str
    data: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)

class EventBus:
    """Barramento de eventos in-memory desacoplado e assíncrono."""
    def __init__(self):
        self._listeners: Dict[str, List[Callable]] = {}

    def subscribe(self, topic: str, listener: Callable) -> None:
        """Registra uma função de retorno (listener) para um tópico específico."""
        if topic not in self._listeners:
            self._listeners[topic] = []
        self._listeners[topic].append(listener)
        print(f"📡 [EVENT BUS] Listener '{listener.__name__}' inscrito no tópico '{topic}'.")

    async def publish(self, topic: str, data: Dict[str, Any]) -> None:
        """Publica um evento para todos os ouvintes inscritos no tópico."""
        if topic not in self._listeners or not self._listeners[topic]:
            print(f"⚠️ [EVENT BUS] Nenhum listener encontrado para o tópico '{topic}'.")
            return

        event = Event(topic=topic, data=data)
        listeners = self._listeners[topic]
        
        print(f"\n📢 [EVENT BUS] Publicando evento no tópico '{topic}' ({len(listeners)} ouvintes)...")

        # Dispara todas as funções inscritas simultaneamente
        tasks = []
        for listener in listeners:
            if inspect.iscoroutinefunction(listener):
                # Se o listener for 'async def', executa como task assíncrona
                tasks.append(asyncio.create_task(listener(event)))
            else:
                # Se for função síncrona comum, executa no loop de eventos
                loop = asyncio.get_running_loop()
                tasks.append(loop.run_in_executor(None, listener, event))

        # Aguarda a execução de todos os listeners inscritos
        await asyncio.gather(*tasks)

# --- Demonstração de Uso Prático ---

# 1. Listeners (Ouvintes)
async def enviar_email_confirmacao(event: Event):
    await asyncio.sleep(0.5) # Simula I/O de rede (API de E-mail)
    cliente = event.data.get("cliente")
    print(f"📧 [E-mail] Mensagem de boas-vindas enviada para {cliente}!")

async def processar_pagamento(event: Event):
    await asyncio.sleep(0.2)
    valor = event.data.get("valor")
    print(f"💳 [Financeiro] Pagamento de R$ {valor:.2f} processado com sucesso.")

def log_auditoria_sincrono(event: Event):
    # Exemplo de listener síncrono para logs
    print(f"📝 [Audit Log - {event.timestamp.strftime('%H:%M:%S')}] Evento '{event.topic}' registrado.")

async def main():
    print("=== Simulador de Arquitetura Baseada em Eventos (EDA) ===\n")
    bus = EventBus()

    # 2. Inscrição de Serviços nos Tópicos
    bus.subscribe("pedidos.criados", log_auditoria_sincrono)
    bus.subscribe("pedidos.criados", processar_pagamento)
    bus.subscribe("pedidos.criados", enviar_email_confirmacao)

    bus.subscribe("usuarios.registrados", enviar_email_confirmacao)

    # 3. Disparo de Eventos
    await bus.publish("pedidos.criados", {
        "pedido_id": 1042,
        "cliente": "Dev FullStack",
        "valor": 299.90
    })

    await bus.publish("usuarios.registrados", {
        "cliente": "novo_usuario@email.com"
    })

if __name__ == "__main__":
    asyncio.run(main())

import subprocess
import sys

# Lista de tipos permitidos no Conventional Commits
COMMIT_TYPES = {
    "feat": "Uma nova funcionalidade para o usuário",
    "fix": "Correção de um bug/problema",
    "docs": "Alterações apenas na documentação",
    "style": "Mudanças que não afetam o significado do código (espaço, formatação, etc.)",
    "refactor": "Alteração de código que não corrige bug nem adiciona funcionalidade",
    "perf": "Mudança de código que melhora o desempenho",
    "test": "Adição de testes ausentes ou correção de testes existentes",
    "chore": "Atualizações em tarefas de build, configurações ou ferramentas secundárias"
}

def get_input(prompt, validator=None):
    """Obtém e valida a entrada do usuário."""
    while True:
        value = input(prompt).strip()
        if not value:
            print("❌ Este campo não pode ficar vazio.")
            continue
        if validator and not validator(value):
            continue
        return value

def build_commit_message():
    print("=== Assistente de Commit Semântico ===")
    
    # 1. Seleção do Tipo
    print("\nSelecione o tipo de alteração:")
    for key, desc in COMMIT_TYPES.items():
        print(f"  [{key}] {desc}")
        
    type_validator = lambda v: v in COMMIT_TYPES
    commit_type = get_input("\nDigite o tipo escolhido: ", type_validator)

    # 2. Escopo (Opcional, mas recomendado)
    scope = input("Digite o escopo/área afetada (ex: auth, ui, parser) [Pressione Enter para pular]: ").strip()
    scope_str = f"({scope})" if scope else ""

    # 3. Descrição Curta (Título)
    desc_validator = lambda v: len(v) <= 50 or (print("⚠️ Mantenha o título abaixo de 50 caracteres para boa legibilidade!") or True)
    description = get_input("Digite uma descrição curta e direta (em letras minúsculas): ", desc_validator)

    # 4. Corpo do Commit (Detalhado - Opcional)
    body = input("\nDigite uma descrição detalhada (corpo) se necessário [Pressione Enter para pular]: ").strip()

    # Monta a mensagem final
    header = f"{commit_type}{scope_str}: {description.lower()}"
    full_message = f"{header}\n\n{body}".strip() if body else header

    return full_message

def execute_git_commit(message):
    """Executa o comando git commit com a mensagem gerada."""
    try:
        # Verifica se há arquivos no stage antes de commitar
        status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True, check=True)
        if not status.stdout.strip():
            print("\n⚠️ Nenhum arquivo preparado (staged) para o commit. Use 'git add' primeiro.")
            return

        print("\nPronto para commitar:")
        print("-" * 40)
        print(message)
        print("-" * 40)
        
        confirm = input("Confirmar e realizar o commit? (s/n): ").strip().lower()
        if confirm == 's':
            subprocess.run(["git", "commit", "-m", message], check=True)
            print("\n✅ Commit realizado com sucesso!")
        else:
            print("\n❌ Operação cancelada pelo usuário.")
            
    except FileNotFoundError:
        print("\n❌ Erro: Git não instalado ou não encontrado no PATH do sistema.")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Erro ao executar comando do Git: {e}")

if __name__ == "__main__":
    try:
        commit_msg = build_commit_message()
        execute_git_commit(commit_msg)
    except KeyboardInterrupt:
        print("\n\nSessão encerrada.")
        sys.exit(0)

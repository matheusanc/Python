import os
import re

def parse_env_file(file_path):
    """Lê um arquivo .env e retorna um dicionário com as chaves encontradas."""
    env_keys = set()
    if not os.path.exists(file_path):
        return env_keys
        
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            # Ignora linhas vazias ou comentários
            if not line or line.startswith("#"):
                continue
            # Captura a chave antes do '='
            match = re.match(r"^([^=]+)=", line)
            if match:
                env_keys.add(match.group(1).strip())
    return env_keys

def audit_secrets(file_path):
    """Detecta se há valores sensíveis possivelmente expostos ou padrões inseguros."""
    issues = []
    if not os.path.exists(file_path):
        return issues

    # Padrões comuns de chaves privadas ou tokens expostos brutos
    secret_pattern = re.compile(r"=(AIzaSy|xoxb-|ghp_|SG\.)", re.IGNORECASE)

    with open(file_path, "r", encoding="utf-8") as f:
        for line_idx, line in enumerate(f, 1):
            if secret_pattern.search(line):
                issues.append(f"Linha {line_idx}: Possível Hardcoded Token/API Key detectado!")
            if "DEBUG=True" in line.replace(" ", ""):
                issues.append(f"Linha {line_idx}: Ambiente em modo DEBUG ativo.")
                
    return issues

def check_env_health(env_path=".env", example_path=".env.example"):
    print("🔍 Inspecionando conformidade das variáveis de ambiente...\n")
    
    if not os.path.exists(env_path):
        print("❌ Arquivo '.env' principal não foi encontrado no diretório atual.")
        return

    actual_keys = parse_env_file(env_path)
    issues = audit_secrets(env_path)

    # Se houver um arquivo de exemplo, compara as chaves
    if os.path.exists(example_path):
        example_keys = parse_env_file(example_path)
        missing_in_env = example_keys - actual_keys
        missing_in_example = actual_keys - example_keys

        if missing_in_env:
            print(f"⚠️ Atenção: Chaves declaradas no exemplo, mas ausentes no seu .env: {missing_in_env}")
        if missing_in_example:
            print(f"💡 Dica: Seu .env possui chaves novas que não estão no .env.example: {missing_in_example}")
    else:
        print("ℹ️ Nenhum arquivo '.env.example' detectado para comparação de escopo.")

    # Exibe problemas de auditoria interna
    if issues:
        print("\n🚨 ALERTAS DE SEGURANÇA ENCONTRADOS:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("\n✅ Nenhuma vulnerabilidade flagrante ou chave exposta detectada no arquivo atual.")

if __name__ == "__main__":
    # Para testar, garanta que possui um arquivo .env no mesmo diretório
    check_env_health()

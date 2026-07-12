import os
import shutil
from pathlib import Path

# Mapeamento de extensões para pastas de destino
FILE_CATEGORIES = {
    "Documentos": [".pdf", ".docx", ".txt", ".csv", ".xlsx"],
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".svg"],
    "Videos": [".mp4", ".mov", ".avi", ".mkv"],
    "Compactados": [".zip", ".rar", ".7z", ".tar"],
    "Instaladores": [".exe", ".msi", ".deb", ".dmg"]
}

def organize_folder(target_dir):
    path = Path(target_dir)
    
    if not path.exists():
        print(f"O caminho {target_dir} não existe.")
        return

    for item in path.iterdir():
        if item.is_file():
            # Identifica a categoria do arquivo
            file_ext = item.suffix.lower()
            dest_folder = "Outros"

            for category, extensions in FILE_CATEGORIES.items():
                if file_ext in extensions:
                    dest_folder = category
                    break

            # Cria a pasta de destino se não existir
            dest_path = path / dest_folder
            dest_path.mkdir(exist_ok=True)

            # Move o arquivo
            try:
                shutil.move(str(item), str(dest_path / item.name))
                print(f"Movido: {item.name} -> {dest_folder}")
            except Exception as e:
                print(f"Erro ao mover {item.name}: {e}")

if __name__ == "__main__":
    # Altere para o caminho que deseja organizar
    folder_to_clean = input("Digite o caminho da pasta para organizar (ex: ./Downloads): ")
    organize_folder(folder_to_clean)

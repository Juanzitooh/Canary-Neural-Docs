#generate/io/setup.py
from pathlib import Path

def setup_directories():  
    # Cria (se necessário) as pastas de input/output dois níveis acima do diretório atual
    print("iniciando verificacao de diretorios")

    # Sobe dois níveis acima do diretório atual
    base_dir = Path(__file__).resolve().parent.parent.parent

    input_dir = base_dir / 'source' / 'src'
    output_dir = base_dir / 'doc' / 'canary_server'
    enum_dir = base_dir / 'doc' / 'Enums'  # Corrigido: enums fora da pasta canary_server
    doc_dir = base_dir / 'doc'
    # Cria todas as pastas necessárias
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    enum_dir.mkdir(parents=True, exist_ok=True)

    return input_dir, output_dir, enum_dir, doc_dir
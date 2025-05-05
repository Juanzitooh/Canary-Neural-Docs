#generate/io/setup.py
from pathlib import Path

def setup_directories():  # Cria (se necessário) as pastas de input/output dois níveis acima do diretório atual
    print("iniciando verificacao de diretorios")

    # Sobe dois níveis acima do diretório atual
    base_dir = Path(__file__).resolve().parent.parent.parent

    input_dir = base_dir / 'source' / 'src'
    output_dir = base_dir / 'doc' / 'hpp'
    
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    return input_dir, output_dir
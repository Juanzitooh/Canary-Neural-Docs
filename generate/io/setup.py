#generate/io/setup.py
from pathlib import Path

def setup_directories(base_dir):
    base_dir = Path(base_dir)  # Garante que é um Path
    doc_dir = base_dir / 'doc_generator'  # Definido uma única vez

    input_dir = base_dir / 'src'
    output_dir = doc_dir / 'canary_server'
    enum_dir = doc_dir / 'Enums'

    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    enum_dir.mkdir(parents=True, exist_ok=True)

    return input_dir, output_dir, enum_dir, doc_dir
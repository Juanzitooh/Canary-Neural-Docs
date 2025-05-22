#generate/io/setup.py
from pathlib import Path
import sys
import os
import shutil

def resource_path(rel_path):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, rel_path)
    return os.path.join(Path(__file__).resolve().parents[2], rel_path)

def copiar_pasta_se_necessario(origem, destino, sobrescrever=False):
    """
    Copia uma pasta do caminho 'origem' para o caminho 'destino'.

    Parâmetros:
    - origem: caminho da pasta de origem (string ou Path)
    - destino: caminho do diretório onde a pasta será copiada (string ou Path)
    - sobrescrever: se True, apaga a pasta destino e copia de novo; se False, só copia se não existir
    """
    origem = Path(origem)
    destino = Path(destino) / origem.name  # Cria a pasta com o mesmo nome no destino

    if destino.exists():
        if sobrescrever:

            shutil.rmtree(destino)  # Apaga a pasta antiga
        else:

            return


    shutil.copytree(origem, destino)


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
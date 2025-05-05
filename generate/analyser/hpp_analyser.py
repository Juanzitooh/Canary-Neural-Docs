# generate/analyser/hpp_analyser.py

from pathlib import Path

from ..analyser.extractors import extract_classes_and_structs, extract_methods, extract_enums, remove_comments

def analyze_file(file_path: Path, current_data: dict):
    """Lê o conteúdo do arquivo `.hpp`, remove comentários /* */, e extrai classes, structs, métodos e enums."""
    content = read_file(file_path)
    content = remove_comments(content)
    extract_classes_and_structs(content, current_data)
    extract_methods(content, current_data)
    extract_enums(content, current_data)

def read_file(file_path: Path) -> str:
    """Lê o arquivo e retorna seu conteúdo."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

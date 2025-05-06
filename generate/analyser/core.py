#generate/analyser/core.py

from pathlib import Path

from ..analyser.hpp_analyser import analyze_file

class FileAnalyzer:
    """
    Classe responsável por analisar arquivos de cabeçalho C++ e extrair vários componentes, como:
    classes, structs, métodos, propriedades e enums.
    """
    def __init__(self):
        """
        Inicializa a estrutura de dados para armazenar os resultados da análise.
        """
        self.current_data = {
            'classes': {},          # Usar um dicionário para armazenar métodos por classe
            'structs': {},          # Usar um dicionário para armazenar métodos por struct
            'function_global': [],  # Lista separada para métodos globais
            'properties': [],       # Propriedades gerais
            'include': [],          # Arquivos incluídos
            'inheritances': [],     # Heranças de classes
            'enums': []             # Enums
        }
        self.current_file = None  # Vai armazenar o arquivo sendo analisado

    def reset(self):
        """
        Reseta a estrutura de dados para preparar uma nova análise.
        Limpa quaisquer dados previamente armazenados.
        """
        self.current_data = {
            'classes': {},          # Usar um dicionário para armazenar métodos por classe
            'structs': {},          # Usar um dicionário para armazenar métodos por struct
            'function_global': [],  # Lista separada para métodos globais
            'properties': [],       # Propriedades gerais
            'include': [],          # Arquivos incluídos
            'inheritances': [],     # Heranças de classes
            'enums': []             # Enums
        }
    def analyze_file(self, file_path: Path):
        """Usa a função de análise de arquivo do módulo de análise."""
        self.reset()
        analyze_file(file_path, self.current_data)
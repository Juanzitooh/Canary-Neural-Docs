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
            'classes': [],    # Lista para armazenar os nomes das classes
            'structs': [],    # Lista para armazenar os nomes das structs
            'methods': [],    # Lista para armazenar as assinaturas dos métodos
            'properties': [], # Lista para armazenar as propriedades das classes
            'enums': []       # Lista para armazenar os enums e seus valores
        }
        self.current_file = None  # Vai armazenar o arquivo sendo analisado

    def reset(self):
        """
        Reseta a estrutura de dados para preparar uma nova análise.
        Limpa quaisquer dados previamente armazenados.
        """
        self.current_data = {
            'classes': [],
            'structs': [],
            'methods': [],
            'properties': [],
            'enums': []
        }
    def analyze_file(self, file_path: Path):
        """Usa a função de análise de arquivo do módulo de análise."""
        self.reset()
        analyze_file(file_path, self.current_data)
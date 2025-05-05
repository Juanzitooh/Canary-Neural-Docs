#generate/analyser/hpp_analyser.py

import re
from pathlib import Path


class FileAnalyzer: # Inicializa a estrutura dos dados que estão sendo analizados
    def __init__(self):
        self.current_data = {
            'classes': [],
            'structs': [],
            'methods': [],
            'properties': [],
            'enums': []
        }
        self.current_file = None

    def reset(self): # reseta a estrutura de dados sendo analizados
        self.current_data = {
            'classes': [],
            'structs': [],
            'methods': [],
            'properties': [],
            'enums': []
        }

    def analyze_file(self, file_path: Path):  # Lê o conteúdo do arquivo `.hpp`, remove comentários /* */, e extrai classes, structs, métodos e enums
        self.reset()
        self.current_file = file_path.stem    
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Remover comentários
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        self._extract_classes_and_structs(content)
        self._extract_methods(content)
        self._extract_enums(content)

    def _extract_classes_and_structs(self, content: str): # Encontra e armazena todas as classes e structs do conteúdo analisado
        pattern = re.compile(
            r'(class|struct)\s+(\w+)\s*{([^}]*)};?',
            re.DOTALL
        )
        
        for match in pattern.finditer(content):
            type_, name, body = match.groups()
            if type_ == 'class':
                self.current_data['classes'].append(name)
            else:
                self.current_data['structs'].append(name)
            self._extract_class_properties(body, name)

    def _extract_class_properties(self, body: str, class_name: str): # Encontra atributos/propriedades dentro do corpo da classe ou struct
        prop_pattern = re.compile(
            r'(\w+)\s+(\w+)\s*;'
        )
        
        for match in prop_pattern.finditer(body):
            type_, name = match.groups()
            self.current_data['properties'].append({
                'class': class_name,
                'type': type_,
                'name': name
            })

    def _extract_methods(self, content: str): # Identifica todos os métodos com seus tipos de retorno e parâmetros
        # Nova regex aprimorada
        method_pattern = re.compile(
            r'(?:(?:static|const|inline|virtual)\s+)*'  # Captura modificadores
            r'([\w:<>\s]+?)\s+'  # Tipos complexos com templates
            r'(\w+)\s*'          # Nome do método
            r'\((.*?)\)\s*'       # Parâmetros
            r'(?:const\s*)?'     # Const no final
            r'(?:\=?\s*(?:default|delete)\s*)?'  # Especificadores especiais
            r'[;{]', 
            re.DOTALL
        )
        
        for match in method_pattern.finditer(content):
            return_type = match.group(1).strip()
            name = match.group(2).strip()
            params = match.group(3).strip()
            
            self.current_data['methods'].append({
                'name': name,
                'return_type': return_type,
                'params': params
            })

    def _extract_enums(self, content: str): # Localiza enums com sufixo `_t` e lista seus valores
        enum_pattern = re.compile(
            r'enum\s+(\w+_t)\s*{([^}]*)}',
            re.DOTALL
        )
        
        for match in enum_pattern.finditer(content):
            name, values = match.groups()
            self.current_data['enums'].append({
                'name': name,
                'values': [v.strip() for v in values.split(',') if v.strip()]
            })

    def generate_enum_markdown(self, enum: dict) -> str:
        """Gera o markdown para cada enum com a lista de seus valores."""
        md = f"# {enum['name']}\n\n"
        md += "### Valores\n"
        
        for value in enum['values']:
            md += f"- {value}\n"
        
        return md

    def generate_markdown(self) -> str: # Gera uma string Markdown formatada com todas as informações coletadas
        md = f"# {self.current_file}\n\n"
        md += f"### Localização\n`{self.current_file}.hpp`\n\n"
        
        if self.current_data['methods']:
            md += "### Funções Lua\n"
            for method in self.current_data['methods']:
                md += f"#{method['name']}\n"  # Alterado para o formato solicitado
            md += "\n"
        
        if self.current_data['structs']:
            md += "### Estruturas\n"
            for struct in self.current_data['structs']:
                md += f"- [[{struct}]]\n"
            md += "\n"
        
        if self.current_data['classes']:
            md += "### Classes\n"
            for cls in self.current_data['classes']:
                md += f"- [[{cls}]]\n" 
            md += "\n"
        
        if self.current_data['enums']:
            md += "### Enums\n"
            for enum in self.current_data['enums']:
                md += f"- [[{enum['name']}]]\n"
            md += "\n"
        
        return md
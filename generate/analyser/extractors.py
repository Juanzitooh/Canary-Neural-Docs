#generate/analyser/extractors.py

import re

def extract_classes_and_structs(content: str, current_data: dict):
    """Encontra e armazena todas as classes e structs do conteúdo analisado."""
    pattern = re.compile(
        r'(class|struct)\s+(\w+)\s*{([^}]*)};?',
        re.DOTALL
    )
    
    for match in pattern.finditer(content):
        type_, name, body = match.groups()
        if type_ == 'class':
            current_data['classes'].append(name)
        else:
            current_data['structs'].append(name)
        extract_class_properties(body, name, current_data)

def extract_class_properties(body: str, class_name: str, current_data: dict):
    """Encontra atributos/propriedades dentro do corpo da classe ou struct."""
    prop_pattern = re.compile(
        r'(\w+)\s+(\w+)\s*;'
    )
    
    for match in prop_pattern.finditer(body):
        type_, name = match.groups()
        current_data['properties'].append({
            'class': class_name,
            'type': type_,
            'name': name
        })

def extract_methods(content: str, current_data: dict):
    """Identifica todos os métodos com seus tipos de retorno e parâmetros."""
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
        
        current_data['methods'].append({
            'name': name,
            'return_type': return_type,
            'params': params
        })

def extract_enums(content: str, current_data: dict):
    """Localiza enums com sufixo `_t` e lista seus valores."""
    enum_pattern = re.compile(
        r'enum\s+(\w+_t)\s*{([^}]*)}',
        re.DOTALL
    )
    
    for match in enum_pattern.finditer(content):
        name, values = match.groups()
        current_data['enums'].append({
            'name': name,
            'values': [v.strip() for v in values.split(',') if v.strip()]
        })

def remove_comments(content: str) -> str:
    """Remove comentários do conteúdo do arquivo."""
    return re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
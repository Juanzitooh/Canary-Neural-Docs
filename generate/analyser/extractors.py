#generate/analyser/extractors.py

import re

def extract_classes_and_structs(content: str, current_data: dict):
    """Encontra e armazena todas as classes e structs do conteúdo analisado."""
    pattern = re.compile(
        r'(class|struct)\s+(\w+)(\s*:\s*(public|private|protected)\s+(\w+))?\s*{([^}]*)};?',
        re.DOTALL
    )
    
    for match in pattern.finditer(content):
        type_, name, _, visibility, base_class, body = match.groups()
        
        # Para classes e structs, agora utilizamos dicionários em vez de listas
        if type_ == 'class':
            if name not in current_data['classes']:
                current_data['classes'][name] = {'methods': [], 'properties': []}
        else:
            if name not in current_data['structs']:
                current_data['structs'][name] = {'methods': [], 'properties': []}

        # Adiciona herança, se houver
        if base_class:
            current_data['inheritances'].append({
                'class': name,
                'visibility': visibility or 'private',
                'base_class': base_class
            })

        # Extraímos as propriedades e métodos
        extract_class_properties(body, name, current_data)
        extract_methods(body, name, current_data)

def extract_class_properties(body: str, class_name: str, current_data: dict):
    """Encontra atributos/propriedades dentro do corpo da classe ou struct."""
    prop_pattern = re.compile(
        r'(\w+(\s*[\*\&\[]+\s*\w+)*)\s+(\w+)\s*(=\s*[\w\(\)\[\]]+)?\s*;',
        re.DOTALL
    )

    # Decide se é uma classe ou struct
    target = None
    if class_name in current_data['classes']:
        target = current_data['classes'][class_name]
    elif class_name in current_data['structs']:
        target = current_data['structs'][class_name]
    else:
        # Em último caso, ignora ou loga o erro
        print(f"[WARN] Classe ou struct '{class_name}' não registrada.")
        return

    for match in prop_pattern.finditer(body):
        type_, name, value = match.group(1).strip(), match.group(3).strip(), match.group(4)
        target['properties'].append({
            'type': type_,
            'name': name,
            'value': value.strip() if value else None
        })

def extract_methods(body: str, class_name: str, current_data: dict):
    """Identifica todos os métodos com tipos de retorno, parâmetros, modificadores, e associa à classe."""
    method_pattern = re.compile(
        r'(?P<modifiers>(?:\b(?:static|virtual|inline|const|override)\b\s*)*)'  # Modificadores opcionais
        r'(?P<return_type>[\w:<>\s\*&]+?)\s+'   # Tipo de retorno
        r'(?P<name>\w+)\s*'                     # Nome do método
        r'\((?P<params>.*?)\)\s*'               # Parâmetros
        r'(?P<const>\bconst\b)?\s*'             # Const pós-parâmetros
        r'(?:=\s*(?P<specifier>default|delete))?' # default/delete
        r'\s*[;{]', 
        re.DOTALL
    )

    for match in method_pattern.finditer(body):
        modifiers_raw = match.group('modifiers').strip()
        modifiers = modifiers_raw.split() if modifiers_raw else []

        # Se a classe ainda não estiver no dicionário, cria uma entrada para ela
        if class_name not in current_data['classes']:
            current_data['classes'][class_name] = {'methods': [], 'properties': []}
        
        current_data['classes'][class_name]['methods'].append({
            'name': match.group('name').strip(),
            'return_type': match.group('return_type').strip(),
            'params': match.group('params').strip(),
            'modifiers': modifiers,
            'const': bool(match.group('const')),
            'specifier': match.group('specifier') or None
        })

def extract_includes(body: str, current_data: dict):
    """Extrai os nomes dos arquivos incluídos, sem a extensão .hpp, e os armazena em current_data."""
    
    # Regex para detectar includes e capturar o nome do arquivo
    include_pattern = re.compile(r'#include\s+"([^"]+)"')
    
    # Busca todos os caminhos dos includes
    includes = []
    for match in include_pattern.finditer(body):
        include_path = match.group(1)  # Extrai o caminho do arquivo entre aspas
        file_name = include_path.split('/')[-1].replace('.hpp', '')  # Remove a extensão .hpp
        includes.append(file_name)
    
    # Armazena os includes no current_data
    current_data['includes'] = includes

def extract_enums(content: str, current_data: dict):
    """Localiza enums tradicionais e enum classes (C++11+), listando nome, tipo base e valores."""
    enum_pattern = re.compile(
        r'enum'                                  # enum obrigatório
        r'(?:\s+(class|struct))?'                # tipo moderno opcional
        r'\s+([a-zA-Z_][\w:]*)'                  # nome da enum (permite :: e _)
        r'(?:\s*:\s*([\w:]+))?'                  # tipo base opcional
        r'\s*\{(.*?)\}'                          # corpo do enum
        r'\s*;',                                 # ponto e vírgula final
        re.DOTALL
    )

    for match in enum_pattern.finditer(content):
        kind, name, base_type, values = match.groups()

        # Adiciona uma vírgula ao final do conteúdo para garantir que o último item seja capturado
        values = values.strip()
        if not values.endswith(','):
            values += ','

        # Separa os itens mesmo se não houver vírgula final no original
        values_list = [v.strip() for v in values.split(',') if v.strip()]

        current_data.setdefault('enums', []).append({
            'name': name,
            'kind': kind if kind else 'enum',
            'base_type': base_type or None,
            'values': values_list
        })


def remove_comments(content: str) -> str:
    """Remove comentários do conteúdo do arquivo."""
    return re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
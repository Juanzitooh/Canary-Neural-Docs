"""
Script para gerar documentação Obsidian para a API Lua do Canary
seguindo a estrutura hierárquica baseada nos caminhos de inclusão
"""

import os
import re
import glob
from pathlib import Path

# Configurações
INPUT_DIR = "source"  # Diretório com os arquivos de código fonte
OUTPUT_DIR = "doc"  # Diretório base de saída

def ensure_dir(directory):
    """Cria um diretório se ele não existir"""
    os.makedirs(directory, exist_ok=True)

def extract_include_path(cpp_file):
    """Extrai o caminho de inclusão do arquivo .hpp a partir do arquivo .cpp"""
    with open(cpp_file, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        # Procurar por padrões como #include "lua/functions/core/game/config_functions.hpp"
        include_match = re.search(r'#include\s+"(lua/functions/.*?_functions\.hpp)"', content)
        if include_match:
            return include_match.group(1)
    return None

def extract_methods(hpp_file, cpp_file):
    """Extrai os métodos Lua de um par de arquivos .hpp e .cpp"""
    methods = []
    
    # Extrair métodos do arquivo .hpp
    with open(hpp_file, 'r', encoding='utf-8', errors='ignore') as f:
        hpp_content = f.read()
        # Procurar por padrões como static int luaActionBlockWalls(lua_State* L);
        method_matches = re.findall(r'static int (lua\w+)\(lua_State\* L\);', hpp_content)
        for method in method_matches:
            if method.startswith("lua"):
                methods.append(method)
    
    # Extrair nomes reais dos métodos do arquivo .cpp
    method_names = {}
    with open(cpp_file, 'r', encoding='utf-8', errors='ignore') as f:
        cpp_content = f.read()
        # Procurar pelo método init
        init_match = re.search(r'void \w+::init\(lua_State\* L\) {(.*?)}', cpp_content, re.DOTALL)
        if init_match:
            init_body = init_match.group(1)
            # Procurar por registros de métodos
            for method in methods:
                # Procurar por padrões como Lua::registerMethod(L, "Action", "blockWalls", ActionFunctions::luaActionBlockWalls);
                method_match = re.search(rf'Lua::registerMethod\(L, "\w+", "(\w+)", \w+::{method}\)', init_body)
                if method_match:
                    method_names[method] = method_match.group(1)
                else:
                    # Tentar extrair o nome do método a partir do nome da função
                    # Por exemplo, luaActionBlockWalls -> blockWalls
                    class_name = os.path.basename(hpp_file).replace("_functions.hpp", "")
                    prefix = f"lua{class_name.capitalize()}"
                    if method.startswith(prefix):
                        name = method[len(prefix):]
                        if name:
                            # Converter primeira letra para minúscula
                            method_names[method] = name[0].lower() + name[1:]
    
    return methods, method_names

def get_class_name(cpp_file):
    """Obtém o nome da classe Lua a partir do arquivo .cpp"""
    with open(cpp_file, 'r', encoding='utf-8', errors='ignore') as f:
        cpp_content = f.read()
        # Procurar por padrões como Lua::registerSharedClass(L, "Action", "", ActionFunctions::luaCreateAction);
        class_match = re.search(r'Lua::registerSharedClass\(L, "(\w+)"', cpp_content)
        if class_match:
            return class_match.group(1)
        
        # Procurar por padrões como Lua::registerTable(L, "db");
        table_match = re.search(r'Lua::registerTable\(L, "(\w+)"', cpp_content)
        if table_match:
            return table_match.group(1)
        
        # Se não encontrar, usar o nome do arquivo
        base_name = os.path.basename(cpp_file).replace("_functions.cpp", "")
        return base_name.capitalize()

def create_hierarchy(include_path):
    """Cria a hierarquia de diretórios com base no caminho de inclusão"""
    if not include_path:
        return None, None
    
    # Remover "lua/functions/" do início e "_functions.hpp" do final
    path_parts = include_path.replace("lua/functions/", "").replace("_functions.hpp", "").split("/")
    
    # Criar a hierarquia de diretórios
    current_dir = OUTPUT_DIR
    parent = None
    
    for i, part in enumerate(path_parts[:-1]):  # Excluir o último elemento (nome do arquivo)
        current_dir = os.path.join(current_dir, part)
        ensure_dir(current_dir)
        
        # Criar arquivo .md para o diretório se não existir
        md_file = os.path.join(current_dir, f"{part}.md")
        if not os.path.exists(md_file):
            with open(md_file, 'w', encoding='utf-8') as f:
                parent_link = "[[functions]]" if i == 0 else f"[[{path_parts[i-1]}]]"
                f.write(f"""---
class: []
tags: 
dependence: "{parent_link}"
---
""")
        
        parent = part
    
    # Diretório para o arquivo final
    final_dir = os.path.join(current_dir, path_parts[-1])
    ensure_dir(final_dir)
    
    return final_dir, parent

def generate_md_file(output_dir, class_name, methods, method_names, parent):
    """Gera o arquivo .md para a classe"""
    # Criar o arquivo .md
    md_file = os.path.join(output_dir, f"{os.path.basename(output_dir)}.md")
    
    # Converter métodos para tags
    tags = []
    for method in methods:
        if method in method_names:
            tags.append(method_names[method])
        else:
            # Se não encontrou o nome real, usar um nome genérico
            if method.startswith("luaCreate") or method.startswith("lua" + class_name + "Create"):
                tags.append("constructor")
            else:
                # Tentar extrair o nome do método
                name = method.replace("lua", "").replace(class_name, "")
                if name:
                    # Converter primeira letra para minúscula
                    tags.append(name[0].lower() + name[1:])
    
    # Remover duplicatas e ordenar
    tags = sorted(set(tags))
    
    # Escrever o arquivo
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write(f"""---
class:
  - "[[{os.path.basename(output_dir)}]]"
tags:
{chr(10).join('  - ' + tag for tag in tags)}
dependence: "[[{parent}]]"
---
""")
    
    return md_file

def process_file(hpp_file, cpp_file):
    """Processa um par de arquivos .hpp e .cpp"""
    print(f"Processando {os.path.basename(hpp_file)}...")
    
    # Extrair caminho de inclusão
    include_path = extract_include_path(cpp_file)
    if not include_path:
        print(f"  Não foi possível determinar o caminho de inclusão para {os.path.basename(hpp_file)}")
        return
    
    # Criar hierarquia de diretórios
    output_dir, parent = create_hierarchy(include_path)
    if not output_dir or not parent:
        print(f"  Não foi possível criar a hierarquia para {os.path.basename(hpp_file)}")
        return
    
    # Extrair métodos
    methods, method_names = extract_methods(hpp_file, cpp_file)
    
    # Obter nome da classe
    class_name = get_class_name(cpp_file)
    
    # Gerar arquivo .md
    md_file = generate_md_file(output_dir, class_name, methods, method_names, parent)
    
    print(f"  Arquivo gerado: {md_file}")
    print(f"  Métodos: {', '.join(method_names.values())}")

def main():
    """Função principal"""
    print("Gerando documentação Obsidian para a API Lua do Canary...")
    
    # Encontrar todos os pares de arquivos .hpp e .cpp
    hpp_files = glob.glob(f"{INPUT_DIR}/**/*_functions.hpp", recursive=True)
    
    for hpp_file in hpp_files:
        cpp_file = hpp_file.replace(".hpp", ".cpp")
        
        if os.path.exists(cpp_file):
            process_file(hpp_file, cpp_file)
    
    print("Documentação gerada com sucesso!")

if __name__ == "__main__":
    main()
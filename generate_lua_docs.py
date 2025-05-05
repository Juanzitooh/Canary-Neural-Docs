#!/usr/bin/env python3
"""
Script para gerar documentação Obsidian para a API Lua do Canary
"""

import os
import re
import glob
import shutil
from pathlib import Path

# Configurações
IMPUT_DIR = "source"  # Diretório com os arquivos de código fonte
OUTPUT_DIR = "doc"      # Diretório de saída para os arquivos Obsidian
CLASSES_DIR = f"{OUTPUT_DIR}/Classes"
METHODS_DIR = f"{OUTPUT_DIR}/Métodos"

def ensure_dirs():
    """Cria os diretórios necessários para a documentação"""
    os.makedirs(CLASSES_DIR, exist_ok=True)
    os.makedirs(METHODS_DIR, exist_ok=True)

def extract_class_info(hpp_file, cpp_file):
    """Extrai informações da classe a partir dos arquivos .hpp e .cpp"""
    class_info = {
        "name": None,
        "methods": []
    }
    
    # Extrair nome da classe do arquivo .hpp
    with open(hpp_file, 'r', encoding='utf-8') as f:
        hpp_content = f.read()
        class_match = re.search(r'class (\w+)', hpp_content)
        if class_match:
            class_info["name"] = class_match.group(1).replace("Functions", "")
    
    # Extrair métodos do arquivo .hpp
    method_matches = re.findall(r'static int (lua\w+)\(lua_State\* L\);', hpp_content)
    for method in method_matches:
        if method.startswith("lua"):
            # Remover o prefixo "lua" e o nome da classe
            prefix = f"lua{class_info['name']}"
            if method.startswith(prefix):
                method_name = method[len(prefix):]
                # Converter primeira letra para minúscula
                if method_name:
                    method_name = method_name[0].lower() + method_name[1:]
                    class_info["methods"].append({
                        "name": method_name,
                        "cpp_function": method
                    })
    
    # Extrair implementações do arquivo .cpp
    with open(cpp_file, 'r', encoding='utf-8') as f:
        cpp_content = f.read()
        
        # Encontrar o método init para verificar como os métodos são registrados
        init_match = re.search(r'void \w+::init\(lua_State\* L\) {(.*?)}', cpp_content, re.DOTALL)
        if init_match:
            init_body = init_match.group(1)
            
            # Verificar o nome real da classe Lua
            class_register = re.search(r'Lua::registerSharedClass\(L, "(\w+)"', init_body)
            if class_register:
                class_info["lua_name"] = class_register.group(1)
            
            # Atualizar informações dos métodos com base nos registros
            for method in class_info["methods"]:
                # Procurar o registro do método para confirmar o nome em Lua
                method_register = re.search(
                    rf'Lua::registerMethod\(L, "{class_info.get("lua_name", class_info["name"])}", "(\w+)", \w+::{method["cpp_function"]}\)', 
                    init_body
                )
                if method_register:
                    method["lua_name"] = method_register.group(1)
                
                # Extrair implementação do método
                method_impl = re.search(
                    rf'int \w+::{method["cpp_function"]}\(lua_State\* L\) {{(.*?)}}', 
                    cpp_content, 
                    re.DOTALL
                )
                if method_impl:
                    method["implementation"] = method_impl.group(0)
                    
                    # Extrair comentário de documentação
                    comment_match = re.search(r'// (.*?)$', method_impl.group(1), re.MULTILINE)
                    if comment_match:
                        method["comment"] = comment_match.group(1)
    
    return class_info

def generate_class_doc(class_info):
    """Gera o arquivo de documentação da classe"""
    lua_name = class_info.get("lua_name", class_info["name"])
    
    content = f"""---
tags: [lua-class]
aliases: [{lua_name}]
---

# {lua_name}

## Descrição
Classe que representa funcionalidades relacionadas a {lua_name.lower()} no jogo.

## Métodos
"""
    
    # Adicionar lista de métodos
    for method in class_info["methods"]:
        method_lua_name = method.get("lua_name", method["name"])
        content += f"- [[{lua_name}.{method_lua_name}|{method_lua_name}]] - "
        if "comment" in method:
            content += method["comment"].split("(")[0].strip()
        content += "\n"
    
    content += f"""
## Exemplo de Uso
```lua
local {lua_name.lower()} = {lua_name}()
-- Use os métodos conforme necessário
```

## Arquivo C++ Relacionado
- `{class_info["name"].lower()}_functions.hpp`
- `{class_info["name"].lower()}_functions.cpp`

## Notas Técnicas
Esta classe é registrada no ambiente Lua através da função `{class_info["name"]}Functions::init()`.
"""
    
    # Escrever o arquivo
    with open(f"{CLASSES_DIR}/{lua_name}.md", 'w', encoding='utf-8') as f:
        f.write(content)
    
    return lua_name

def generate_method_docs(class_info):
    """Gera os arquivos de documentação para cada método da classe"""
    lua_class_name = class_info.get("lua_name", class_info["name"])
    
    for method in class_info["methods"]:
        lua_method_name = method.get("lua_name", method["name"])
        
        content = f"""---
tags: [lua-method]
class: [[{lua_class_name}]]
cpp-function: {method["cpp_function"]}
---

# {lua_class_name}.{lua_method_name}

## Assinatura
```lua
{lua_class_name}:{lua_method_name}()
```

## Parâmetros
- (A ser documentado)

## Retorno
- (A ser documentado)

## Descrição
"""
        if "comment" in method:
            content += method["comment"]
        else:
            content += f"Método da classe {lua_class_name}."
        
        content += f"""

## Implementação C++
```cpp
{method.get("implementation", f"// Implementação não encontrada para {method['cpp_function']}")}
```

## Exemplo de Uso
```lua
local {lua_class_name.lower()} = {lua_class_name}()
{lua_class_name.lower()}:{lua_method_name}()
```

## Notas
- Esta função é registrada no ambiente Lua em `{class_info["name"]}Functions::init()`
"""
        
        # Escrever o arquivo
        with open(f"{METHODS_DIR}/{lua_class_name}.{lua_method_name}.md", 'w', encoding='utf-8') as f:
            f.write(content)

def generate_index():
    """Gera o arquivo de índice para a documentação"""
    classes = [f.stem for f in Path(CLASSES_DIR).glob("*.md")]
    
    content = """# API Lua do Canary

## Classes

"""
    for cls in sorted(classes):
        content += f"- [[{cls}]]\n"
    
    content += """
## Como usar esta documentação

Esta documentação é organizada em:

1. **Classes** - Representam os objetos principais da API Lua
2. **Métodos** - Funções que podem ser chamadas nos objetos

Você pode navegar pelos links ou usar o gráfico do Obsidian para visualizar as relações.
"""
    
    with open(f"{OUTPUT_DIR}/index.md", 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    """Função principal"""
    print("Gerando documentação Obsidian para a API Lua do Canary...")
    
    ensure_dirs()
    
    # Encontrar todos os pares de arquivos .hpp e .cpp
    hpp_files = glob.glob(f"{IMPUT_DIR}/*_functions.hpp")
    
    classes_processed = []
    
    for hpp_file in hpp_files:
        base_name = os.path.basename(hpp_file)
        cpp_file = hpp_file.replace(".hpp", ".cpp")
        
        if os.path.exists(cpp_file):
            print(f"Processando {base_name}...")
            class_info = extract_class_info(hpp_file, cpp_file)
            
            if class_info["name"] and class_info["methods"]:
                lua_class_name = generate_class_doc(class_info)
                generate_method_docs(class_info)
                classes_processed.append(lua_class_name)
    
    generate_index()
    
    print(f"Documentação gerada com sucesso! {len(classes_processed)} classes processadas.")
    print(f"Classes: {', '.join(classes_processed)}")
    print(f"Arquivos gerados em: {os.path.abspath(OUTPUT_DIR)}")

if __name__ == "__main__":
    main()
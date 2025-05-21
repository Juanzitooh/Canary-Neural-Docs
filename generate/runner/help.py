#generate/runner/help.py

from pathlib import Path

def generate_hierarchy_links(relative_path):
    """
    Retorna uma lista de tuplas [(folder_name, full_path_to_index_file)], 
    da pasta mais próxima até a raiz.
    """
    hierarchy = []
    parts = list(relative_path.parts)[:-1]  # remove o próprio arquivo

    current_path = Path()
    for part in parts:
        current_path = current_path / part
        hierarchy.append((part, current_path))
    return hierarchy

def create_markdown_file(output_path, content):
    """Cria e escreve um arquivo `.md` com o conteúdo fornecido."""
    with open(output_path, 'w', encoding='utf-8') as md_file:
        md_file.write(content)

import os

def ensure_wiki_file_exists(wiki_path):
    """
    Garante que o arquivo wiki_canary.md exista com os marcadores mínimos.
    """
    if not os.path.exists(wiki_path):
        os.makedirs(os.path.dirname(wiki_path), exist_ok=True)
        with open(wiki_path, 'w', encoding='utf-8') as f:
            f.write("**Índice da estrutura do canary\n\n*fim indice*\n")
        print(f" Arquivo criado com base padrão: {wiki_path}")

def update_wiki_canary_index(index_list, wiki_path):
    """
    Atualiza o arquivo wiki_canary.md substituindo o conteúdo entre os marcadores
    '**Índice da estrutura do canary' e '*fim indice*' por uma lista formatada dos índices.
    """
    ensure_wiki_file_exists(wiki_path)

    with open(wiki_path, 'r', encoding='utf-8') as f:
        content = f.read()

    start_marker = "**Índice da estrutura do canary"
    end_marker = "*fim indice*"

    start_index = content.find(start_marker)
    end_index = content.find(end_marker, start_index)

    if start_index == -1 or end_index == -1:
        print(" Marcadores de índice não encontrados no arquivo wiki.")
        return

    start_index += len(start_marker)
    new_index_block = "\n\n" + "\n".join(f"- [[{idx}]]" for idx in sorted(index_list)) + "\n\n"

    updated_content = (
        content[:start_index] +
        new_index_block +
        content[end_index:]
    )

    with open(wiki_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print(f" Índice da wiki atualizado com {len(index_list)} entradas.")
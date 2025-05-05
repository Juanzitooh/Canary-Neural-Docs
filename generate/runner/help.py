def generate_hierarchy_links(relative_path):
    """Gera os links hierárquicos para as pastas, como no formato Obsidian."""
    parent_links = []
    for part in reversed(relative_path.parent.parts):
        parent_links.append(f"[[{part}]]")
    return parent_links

def create_markdown_file(output_path, content):
    """Cria e escreve um arquivo `.md` com o conteúdo fornecido."""
    with open(output_path, 'w', encoding='utf-8') as md_file:
        md_file.write(content)
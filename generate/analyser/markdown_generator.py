#generate/analyser/markdown_generator.py

def generate_enum_markdown(enum: dict, source_filename: str = None) -> str:
    """Gera o markdown para enums tradicionais e modernos, com origem opcional."""
    md = f"# Enum: `{enum['name']}`\n\n"
    
    if source_filename:
        md += f"> ⚙️ Arquivo original: [[{source_filename}]]\n\n"

    kind = enum.get('kind', 'enum')
    base = enum.get('base_type')

    md += f"- **Tipo:** `{kind}`\n"
    if base:
        md += f"- **Base:** `{base}`\n"

    md += "\n### Valores\n"

    for value in enum['values']:
        if '=' in value:
            key, val = map(str.strip, value.split('=', 1))
            md += f"- `{key}` = `{val}`\n"
        else:
            md += f"- `{value}`\n"
    
    return md


def generate_markdown(file_name: str, data: dict) -> str:
    """Gera uma string Markdown formatada com todas as informações coletadas."""
    md = f"# {file_name}\n\n"
    md += f"### Localização\n`{file_name}.hpp`\n\n"
    
    # Seção de Includes como links para arquivos .hpp relacionados
    if data.get('includes'):
        md += "### Relacionamento\n"
        for include in data['includes']:
            md += f"- [[{include}]]\n"
        md += "\n"
    
    # Seção de Classes
    if data.get('classes'):
        md += "### Classes\n"
        for class_name, class_data in data['classes'].items():
            md += f"- **{class_name}**\n"
            if class_data.get('methods'):
                md += "  - Métodos:\n"
                for method in class_data['methods']:
                    md += f"    - [[{method['name']}]]\n"
            if class_data.get('properties'):
                md += "  - Propriedades:\n"
                for prop in class_data['properties']:
                    md += f"    - **{prop['name']}**: {prop['type']} = {prop['value']}\n"
            md += "\n"
    
    # Seção de Estruturas
    if data.get('structs'):
        md += "### Estruturas\n"
        for struct_name, struct_data in data['structs'].items():
            md += f"- **{struct_name}**\n"
            if struct_data.get('methods'):
                md += "  - Métodos:\n"
                for method in struct_data['methods']:
                    md += f"    - [[{method['name']}]]\n"
            if struct_data.get('properties'):
                md += "  - Propriedades:\n"
                for prop in struct_data['properties']:
                    md += f"    - **{prop['name']}**: {prop['type']} = {prop['value']}\n"
            md += "\n"
    
    # Seção de Enums
    if data.get('enums'):
        md += "### Enums\n"
        for enum in data['enums']:
            md += f"- [[{enum['name']}]]\n"
        md += "\n"
    
    return md
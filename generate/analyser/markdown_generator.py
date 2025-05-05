#generate/analyser/markdown_generator.py

def generate_enum_markdown(enum: dict) -> str:
    """Gera o markdown para cada enum com a lista de seus valores."""
    md = f"# {enum['name']}\n\n"
    md += "### Valores\n"
    
    for value in enum['values']:
        md += f"- {value}\n"
    
    return md

def generate_markdown(file_name: str, data: dict) -> str:
    """Gera uma string Markdown formatada com todas as informações coletadas."""
    md = f"# {file_name}\n\n"
    md += f"### Localização\n`{file_name}.hpp`\n\n"
    
    if data.get('methods'):
        md += "### Funções Lua\n"
        for method in data['methods']:
            md += f"#{method['name']}\n"  # Alterado para o formato solicitado
        md += "\n"
    
    if data.get('structs'):
        md += "### Estruturas\n"
        for struct in data['structs']:
            md += f"- [[{struct}]]\n"
        md += "\n"
    
    if data.get('classes'):
        md += "### Classes\n"
        for cls in data['classes']:
            md += f"- [[{cls}]]\n"
        md += "\n"
    
    if data.get('enums'):
        md += "### Enums\n"
        for enum in data['enums']:
            md += f"- [[{enum['name']}]]\n"
        md += "\n"
    
    return md
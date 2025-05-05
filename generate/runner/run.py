#generate/runner/run.py

from ..io.setup import setup_directories
from ..analyser.core import FileAnalyzer
from ..analyser.markdown_generator import generate_enum_markdown, generate_markdown

def create_obsidian_notes(): 
    # Percorre todos os arquivos `.hpp` dentro de source/src, analisa e cria arquivos `.md` na pasta de saída
    # formatados para uso no Obsidian
    print("criando notas")
    input_dir, output_dir = setup_directories()
    analyzer = FileAnalyzer()
    
    print("iniciando analise")
    for hpp_file in input_dir.rglob('*.hpp'):
        analyzer.analyze_file(hpp_file)
        
        relative_path = hpp_file.relative_to(input_dir)
        output_path = output_dir / relative_path.with_suffix('.md')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Gera o markdown do arquivo atual
        file_name = hpp_file.stem  # sem extensão
        md_content = generate_markdown(file_name, analyzer.current_data)

        # Adiciona links hierárquicos para as pastas
        parent_links = []
        for part in reversed(relative_path.parent.parts):
            parent_links.append(f"[[{part}]]")
        
        if parent_links:
            md_content += "### Hierarquia\n" + " ➔ ".join(reversed(parent_links)) + "\n"
        
        # Escreve o conteúdo principal no arquivo
        with open(output_path, 'w', encoding='utf-8') as md_file:
            md_file.write(md_content)
        
        # Cria também os arquivos individuais para cada enum
        for enum in analyzer.current_data['enums']:
            enum_md_content = generate_enum_markdown(enum)
            
            # Cria o arquivo para o enum
            enum_output_path = output_dir / f"{enum['name']}.md"
            enum_output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(enum_output_path, 'w', encoding='utf-8') as enum_file:
                enum_file.write(enum_md_content)
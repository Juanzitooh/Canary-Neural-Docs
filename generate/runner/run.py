#generate/runner/run.py

from ..io.setup import setup_directories
from ..analyser.core import FileAnalyzer
from ..analyser.markdown_generator import generate_enum_markdown, generate_markdown
from ..runner.help import generate_hierarchy_links, create_markdown_file

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
        parent_links = generate_hierarchy_links(relative_path)
        
        if parent_links:
            md_content += "### Hierarquia\n" + " ➔ ".join(reversed(parent_links)) + "\n"
        
        # Escreve o conteúdo principal no arquivo
        create_markdown_file(output_path, md_content)
        
        # Cria também os arquivos individuais para cada enum
        for enum in analyzer.current_data['enums']:
            enum_md_content = generate_enum_markdown(enum)
            
            # Cria o arquivo para o enum
            enum_output_path = output_dir / f"{enum['name']}.md"
            enum_output_path.parent.mkdir(parents=True, exist_ok=True)
            
            create_markdown_file(enum_output_path, enum_md_content)
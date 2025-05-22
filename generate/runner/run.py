#generate/runner/run.py

from ..io.setup import setup_directories, resource_path, copiar_pasta_se_necessario
from ..analyser.core import FileAnalyzer
from ..analyser.markdown_generator import generate_enum_markdown, generate_markdown
from ..runner.help import generate_hierarchy_links, create_markdown_file, update_wiki_canary_index
from ..runner.obsidian_helper import abrir_obsidian_ou_alertar

from collections import defaultdict



def create_obsidian_notes(base_dir): 
    print("criando notas")
    input_dir, output_dir, enum_dir, doc_dir = setup_directories(base_dir)
    obsidian_path = resource_path("obsidian")
    analyzer = FileAnalyzer()

    # Mapeia cada pasta para os filhos que ela deve listar no índice
    index_links = defaultdict(set)

    print("iniciando analise")
    for hpp_file in input_dir.rglob('*.hpp'):
        analyzer.analyze_file(hpp_file)
        
        relative_path = hpp_file.relative_to(input_dir)
        output_path = output_dir / relative_path.with_suffix('.md')
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        file_name = hpp_file.stem  # sem extensão
        md_content = generate_markdown(file_name, analyzer.current_data)

        # === HIERARQUIA REAL ===
        hierarchy = generate_hierarchy_links(relative_path)

        if hierarchy:
            # Adiciona links reais no markdown
            hierarchy_links = [f"[[{name}_Index]]" for name, _ in reversed(hierarchy)]
            md_content += "### Hierarquia\n" + " ➔ ".join(hierarchy_links) + "\n"

            # Prepara o mapeamento para os índices
            for i in range(len(hierarchy)):
                folder_name, folder_path = hierarchy[i]
                if i + 1 < len(hierarchy):
                    next_folder_name, _ = hierarchy[i + 1]
                    index_links[folder_path].add(f"{next_folder_name}_Index")
                else:
                    index_links[folder_path].add(file_name)

        # Escreve o markdown principal
        create_markdown_file(output_path, md_content)

        # Escreve os arquivos individuais para enums
        for enum in analyzer.current_data['enums']:
            enum_md_content = generate_enum_markdown(enum, file_name)
            enum_output_path = enum_dir / f"{enum['name']}.md"
            enum_output_path.parent.mkdir(parents=True, exist_ok=True)
            create_markdown_file(enum_output_path, enum_md_content)



    # === GERA OS INDEXES FINAIS ===
    top_level_indexes = []  # <- declare isso no início do script ou da função
    for folder_path, children in index_links.items():
        folder_index_name = f"{folder_path.name}_Index.md"
        folder_index_path = output_dir / folder_path / folder_index_name
        folder_index_path.parent.mkdir(parents=True, exist_ok=True)

        index_content = f"# {folder_path.name} Index\n\n"
        index_content += "### Contém:\n"
        for child in sorted(children):
            index_content += f"- [[{child}]]\n"

        parent_path = folder_path.parent
        if parent_path in index_links:
            parent_index_name = f"{parent_path.name}_Index"
            index_content += f"\n---\nVem de: [[{parent_index_name}]]\n"
        else:
            index_content += f"\n---\nVem de: [[wiki_canary]]\n"
            top_level_indexes.append(folder_index_name.replace(".md", ""))  # salva só o nome do index

        create_markdown_file(folder_index_path, index_content)
    wiki_file_path = doc_dir / "wiki_canary.md"
    update_wiki_canary_index(top_level_indexes, wiki_file_path)
    copiar_pasta_se_necessario(obsidian_path, doc_dir, sobrescrever=False)
    return abrir_obsidian_ou_alertar(doc_dir)

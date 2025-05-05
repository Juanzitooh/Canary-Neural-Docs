#main.py

from generate.runner.run import create_obsidian_notes
from generate.runner.generate_lua_docs import main_lua
from generate.runner.generate_obsidian_docs import main_obsidian_docs


if __name__ == "__main__":
    create_obsidian_notes()
    #main_lua() # comentado pois será incluido nos outros
    #main_obsidian_docs() # comentado pois será incluido nos outros
    print("Documentacao Obsidian gerada com sucesso!")
import os
import subprocess
import json
import webbrowser

CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".obsidian_helper_config.json")

def salvar_caminho_obsidian(path: str):
    with open(CONFIG_FILE, "w") as f:
        json.dump({"obsidian_path": path}, f)

def carregar_caminho_obsidian() -> str | None:
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return data.get("obsidian_path")
    return None

def localizar_obsidian_exe() -> str | None:
    caminhos_possiveis = [
        os.path.expandvars(r"%LOCALAPPDATA%\Programs\Obsidian\Obsidian.exe"),
        os.path.expandvars(r"%LOCALAPPDATA%\Obsidian\Obsidian.exe"),
        r"C:\Program Files\Obsidian\Obsidian.exe",
    ]

    # Verifica caminhos conhecidos
    for caminho in caminhos_possiveis:
        if os.path.isfile(caminho):
            return caminho

    # Tenta recuperar caminho salvo anteriormente
    caminho_salvo = carregar_caminho_obsidian()
    if caminho_salvo and os.path.isfile(caminho_salvo):
        return caminho_salvo

    return None

def abrir_obsidian_ou_alertar(vault_path: str) -> bool:
    obsidian_exe = localizar_obsidian_exe()

    if not obsidian_exe:
        print(" Obsidian não foi encontrado automaticamente.")
        print(" Abrindo site oficial para download no navegador...")
        webbrowser.open("https://obsidian.md/download")
        return False

    if not os.path.isdir(vault_path):
        print(f" O diretório do Vault não existe: {vault_path}")
        return False

    print(f" Abrindo Vault com Obsidian: {vault_path}")
    subprocess.Popen([obsidian_exe, vault_path])
    return True
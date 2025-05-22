import tkinter as tk
import re
from tkinter import ttk,StringVar, Entry , filedialog, messagebox
from ttkthemes import ThemedStyle
from pystray import Icon, MenuItem, Menu
from PIL import Image, ImageDraw, ImageTk
import os
import sys
import webbrowser
import traceback
from pathlib import Path

from ..runner.run import create_obsidian_notes
from ..runner.generate_lua_docs import main_lua
from ..runner.generate_obsidian_docs import main_obsidian_docs
from ..io.setup import resource_path

root = tk.Tk()

# Cores temas
cor_primaria = '#363636'
cor_secundaria = "#474848"
cor_detalhes = "#252626"
cor_texto = '#c9c9c9'
cor_texto_pressionado = '#9f9f22'
cor_preto = '#28292b'

# Variaveis 
directory_assinatura = "./assinaturas"
directory_extras = "./extras"
directory_scripts = "./scripts"

# Caminhos dos arquivos incluídos

icone_file_path = resource_path("icone.ico")
background_file_path = resource_path("background.JPG")

class GenerateDocUI():
    # Declaração de variaveis e inicialização da interface
    def __init__(self):
        self.root = root

        # Variaveis de directory
        self.directory = directory_assinatura
        self.directory2 = directory_extras
        self.directory3 = directory_scripts

        # variaveis de filtros de scripts
        self.scripts = []
        self.scripts_vitalicios = []
        self.scripts_extras = []
        self.scripts_mage = []
        self.scripts_kina = []
        self.scripts_pala = []

        # Variaveis de dados carregados dos scripts
        self.items_data = {}
        self.enchant_data = {}
        self.variables_data = {}

        # Edições feitas no campo para serem trocadas
        self.edit_items_data = {}
        self.edit_enchant_data = {}
        self.edit_variables_data = {}

        # Variaveis dos dados de script que estão sendo editados
        self.temp_items_data = {}
        self.temp_enchant_data = {}
        self.temp_variables_data = {}

        # Variaveis para guardar objetos da interface
        self.tabs_dict = {}
        self.widgets_registry = {}
        self.buttons = []
        
        # Usando o ThemedStyle do ttkthemes
        style = ThemedStyle(self.root)

        # Definir o tema usando o ttkthemes (por exemplo, "arc", "plastik", etc.)
        style.set_theme("black")  # Substitua "arc" por qualquer tema disponível do ttkthemes

        # Estilo para botões personalizados pequenos
        style.configure(
            "Custom.TButton",
            font=("Verdana", 12, "bold"),
            foreground=cor_texto,  # Cor do texto
            background="#363636",  # Cor de fundo
            padding=2,  # Espaçamento interno
            borderwidth=1,  # Espessura da borda
        )

        # Estilo de botão ativo (quando pressionado)
        style.map(
            "Custom.TButton",
            background=[("active", cor_secundaria)],  # Cor de fundo ao pressionar
            foreground=[("active", cor_texto_pressionado)],  # Cor do texto ao pressionar
        )

        # Estilo dos botões gigantes
        style.configure(
            "Custom2.TButton",
            font=("Verdana", 12, "bold"),
            foreground=cor_texto,  # Cor do texto
            background="#363636",  # Cor de fundo
            padding=2,  # Espaçamento interno
            borderwidth=1,  # Espessura da borda
            anchor="center",
        )

        # Estilo de botão ativo (quando pressionado)
        style.map(
            "Custom2.TButton",
            background=[("active", cor_secundaria)],  # Cor de fundo ao pressionar
            foreground=[("active", cor_texto_pressionado)],  # Cor do texto ao pressionar
        )

        # funções
        # Função para chamar o menu principal
        self.tela_principal()
        #self.root.withdraw()

        # Inicializa o ícone da bandeja (Pystray)
        self.tray_icon = Icon("Generate Doc", self.criar_imagem())
        
        # Define o menu da bandeja
        self.tray_icon.menu = Menu(
            MenuItem("Abrir", self.mostrar_janela), 
            MenuItem("Fechar", self.fechar_aplicacao)
        )
        
        # Adiciona o tooltip
        self.tray_icon.tooltip = "Generate Doc V 1.0"
        
        # Inicia o ícone da bandeja
        self.tray_icon.run_detached()
        self.root.protocol("WM_DELETE_WINDOW", self.esconder_janela)
        self.root.mainloop()

    # Criar icone da barra de tarefas
    def criar_imagem(self):
        # Carregar o ícone a partir de um arquivo
        image = Image.open(icone_file_path)  # Substitua pelo caminho do seu ícone
        image = image.resize((32, 32))  # Redimensiona a imagem para 32x32 pixels (tamanho padrão para ícones)
        return image

    # função que dá withdrawn na janela
    def esconder_janela(self):
        # Esconde a janela ao invés de fechá-la
        self.root.withdraw()

    # função que mostra a janela
    def mostrar_janela(self, icon, item):
        # Mostra a janela ao clicar no ícone
        self.root.deiconify()
        self.root.state('zoomed')

    # Função para finalizar a aplicação e interface
    def fechar_aplicacao(self, icon, item):
        try:
            icon.visible = False
            icon.stop()
            self.root.quit()
        except Exception as e:
            print(f"Erro ao fechar: {e}")

    def selecionar_diretorio(self):
        path = filedialog.askdirectory()
        if path:
            self.path_var.set(path)

    def gerar_documentacao(self):
        selected_path = self.path_var.get().strip()
        if not selected_path:
            messagebox.showwarning("Aviso", "Por favor, selecione um diretório.")
            return

        try:
            sucesso = create_obsidian_notes(selected_path)
            if sucesso:
                messagebox.showinfo("Sucesso", "Documentação gerada com sucesso e Obsidian aberto.")
            else:
                messagebox.showwarning(
                    "Obsidian não instalado",
                    "Obsidian não está instalado ou não foi encontrado.\n"
                    "Por favor, instale o Obsidian e gere a documentação novamente."
                )
        except Exception as e:
            error_msg = f"Ocorreu um erro:\n{str(e)}"
            print(error_msg)
            traceback.print_exc()
            messagebox.showerror("Erro", error_msg)

    # Função que define a janela principal e chama a criação de dados dela        
    def tela_principal(self):
        self.root.title("Generate Doc: Criador de documentação SRC")
        self.root.geometry("1024x768")
        self.root.resizable(True, True)
        self.root.configure(bg="#000000")  # ou bg="#000000"
        self.root.maxsize(width= 1920 ,height= 1080)
        self.root.minsize(width= 1024 ,height= 768)
        self.root.state('zoomed')
        self.root.iconbitmap(icone_file_path)

        # Carregue e redimensione a imagem de fundo
        bg_image = Image.open(background_file_path)
        bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
        bg_photo = ImageTk.PhotoImage(bg_image)

        # Armazene a referência (senão a imagem desaparece)
        self.bg_photo = bg_photo

        # Coloque a imagem como fundo
        bg_label = tk.Label(self.root, image=self.bg_photo, bg="black")
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # === Continuar com a criação dos widgets ===
        self.setup_ui()

        # Chama a primeira janela        
        self.setup_ui()

    # Função que complementa os widgets da janela principal
    def setup_ui(self):
        # Frame principal dentro da janela root
        self.frame_main = tk.Frame(
            self.root,
            bd=4,
            bg="white",  # fundo branco para o frame
            highlightbackground=cor_detalhes,
            highlightcolor=cor_texto_pressionado,
            highlightthickness=0.1
        )
        self.frame_main.place(relx=0.5, rely=0.5, anchor="center", width=600, height=180)

        # Label explicativo
        label = tk.Label(
            self.frame_main,
            text="Selecione a sua pasta do canary, a mesma onde fica o executável e a pasta src...",
            font=("Arial", 12),
            bg="white"
        )
        label.pack(pady=(15, 10))

        # Entry para o caminho do diretório
        self.path_var = tk.StringVar()
        entry = tk.Entry(self.frame_main, textvariable=self.path_var, width=60)
        entry.pack(pady=5)

        # Botão para abrir diálogo de seleção de pasta
        browse_button = tk.Button(
            self.frame_main,
            text="Procurar Pasta",
            command=self.selecionar_diretorio,
            bg="#dcdcdc"
        )
        browse_button.pack(pady=5)

        # Botão para gerar documentação
        generate_button = tk.Button(
            self.frame_main,
            text="Gerar Documentação",
            command=self.gerar_documentacao,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 11, "bold")
        )
        generate_button.pack(pady=(10, 10))

if __name__ == "__main__":
    GenerateDocUI()
# Canary Neural Docs: Mapeamento Neural para OTServers  
**Visualização Estruturada do Código-Fonte do Canary em Obsidian**  

[![GitHub repo size](https://img.shields.io/github/repo-size/Habdel-Edenfield/canary-docs)](https://github.com/Habdel-Edenfield/canary-docs)
[![GitHub](https://img.shields.io/github/license/Habdel-Edenfield/canary-docs)](https://github.com/Habdel-Edenfield/canary-docs/blob/main/LICENSE)
[![Discord](https://img.shields.io/discord/1234567890123456789?label=Suporte&logo=discord)](https://discord.gg/your-invite-link)

Ferramenta de documentação automatizada para análise do código-fonte do Canary (OTServer), convertendo-o em documentos Markdown interconectados para uso no Obsidian. Ideal para aprendizado e integração com sistemas de IA.

Utilize agora a versão 1.0: para baixar é só [clicar aqui](https://github.com/Juanzitooh/Canary-Neural-Docs/releases/download/v1.0.0/Doc.Generator.rar)

---

## 👋 Sobre o Projeto

Olá! Sou **Habdel Edenfield** ([GitHub](https://github.com/Habdel-Edenfield) | Discord: `Habdel_Edenfield`) e desenvolvi esta solução para:
- Facilitar o entendimento da arquitetura do Canary
- Criar base de conhecimento para treinamento de IA/RAG
- Oferecer documentação dinâmica e navegável

---

## 🛠️ Funcionalidades

- **Análise Automática de Código**
  - Extração de classes, structs e enums com links internos
  - Detecção de métodos com parâmetros e tipos de retorno
  - Mapeamento hierárquico de diretórios

- **Suporte a ler funções de blind lua c++**
  - ?
  - ?
  - ?

- **Integração com Obsidian**
  - Links bidirecionais entre componentes
  - Visualização neural das relações internas
  - Base pronta para grafos de conhecimento

- **Suporte a Automação**
  - Saída em Markdown padronizado
  - Compatível com pipelines de CI/CD
  - Formatação otimizada para LLMs

---

![Preview](https://i.imgur.com/jNLfYwB.png)

---

## 🚀 Começando

### Pré-requisitos para desenvolver
- Python 3.8+
- Git instalado ( se não tiver, é só baixar o codigo no repositório)
- Obisidian

### Instalação Rápida
```bash
git clone https://github.com/Habdel-Edenfield/canary-docs.git

cd canary-docs

pip install -r requirements.txt

python main.py
```

Prefira usar ambientes virtuais para rodar o install requeriments

Ai é só seleciona a pasta do canary, apertar gerar documentação e ta gerado.

Caso tenha alguma idéia ou saiba algo que possamos acrescentar de informação abra um issue no repositório, agradecemos toda colaboração !

# Gerar realease (executável com pyinstaller)
```bash

pyinstaller --onefile --noconsole --name "Doc Generator" --distpath . --icon icone.ico --add-data "icone.ico;." --add-data "background.JPG;." --add-data ".obsidian;." main.py

```

## Estrutura de Pastas em qualquer servidor canary global ou canary custom
```bash
📁 Canary/ (pasta a ser selecionada)
└── 📁 src/
    └── ... (Codigo C++ canary)
📁 doc_generator/ (pasta aberta pelo obsidian)
└── 📁 .obsidian/(pasta que define a primeira vizualização no cofre, cores da wiki e afins)
└── 📁 hpp/
    ├── account.md
    ├── player.md
    └── ... (documentação gerada automaticamente)
```

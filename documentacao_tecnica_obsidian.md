# Documentação Técnica: Estrutura de Documentação Lua para Obsidian

## Visão Geral

Este documento explica tecnicamente como estruturar a documentação das funções Lua do Canary no Obsidian, aproveitando os recursos de links bidirecionais, tags e propriedades para criar uma base de conhecimento navegável e bem organizada.

## Estrutura Hierárquica

A estrutura hierárquica da API Lua do Canary pode ser representada da seguinte forma:

```
Classes (Action, Player, Item, etc.)
  └── Métodos (blockWalls, onUse, register, etc.)
```

No código C++, esta estrutura é implementada como:

```
ClasseFunctions (ActionFunctions, PlayerFunctions, etc.)
  └── Métodos estáticos (luaActionBlockWalls, luaActionOnUse, etc.)
```

E no ambiente Lua, é exposta como:

```lua
Action:blockWalls(true)
Player:addItem(itemId)
```

## Estrutura de Arquivos no Obsidian

Para representar esta hierarquia no Obsidian, usamos a seguinte estrutura de arquivos:

```
/Obsidian Vault/
  /Classes/
    Action.md
    Player.md
    Item.md
    ...
  /Métodos/
    Action.blockWalls.md
    Action.onUse.md
    Player.addItem.md
    ...
  index.md
```

### Arquivos de Classe

Cada arquivo de classe (ex: `Action.md`) contém:

1. **Metadados** - Tags e aliases para facilitar a pesquisa
2. **Descrição** - Explicação da finalidade da classe
3. **Lista de Métodos** - Links para todos os métodos da classe
4. **Exemplos de Uso** - Código Lua demonstrando como usar a classe
5. **Arquivos Relacionados** - Links para os arquivos C++ correspondentes

### Arquivos de Método

Cada arquivo de método (ex: `Action.blockWalls.md`) contém:

1. **Metadados** - Tags, classe pai e função C++ correspondente
2. **Assinatura** - Formato de chamada do método em Lua
3. **Parâmetros** - Descrição dos parâmetros aceitos
4. **Retorno** - Descrição dos valores retornados
5. **Descrição** - Explicação detalhada da funcionalidade
6. **Implementação C++** - Código fonte da implementação
7. **Exemplos de Uso** - Código Lua demonstrando como usar o método
8. **Notas** - Informações adicionais e considerações

## Mapeamento Técnico

O mapeamento entre o código C++ e a documentação Obsidian segue estas regras:

1. **Nome da Classe Lua**: 
   - Extraído de `Lua::registerSharedClass(L, "Action", "", ...)`
   - Torna-se o nome do arquivo em `/Classes/Action.md`

2. **Nome do Método Lua**:
   - Extraído de `Lua::registerMethod(L, "Action", "blockWalls", ...)`
   - Torna-se parte do nome do arquivo em `/Métodos/Action.blockWalls.md`

3. **Função C++ correspondente**:
   - Identificada como `ActionFunctions::luaActionBlockWalls`
   - Armazenada como metadado no arquivo do método

## Automação com Python

O script `generate_lua_docs.py` automatiza a geração desta documentação seguindo estes passos:

1. **Identificação de Classes**:
   - Procura arquivos `*_functions.hpp` e `*_functions.cpp`
   - Extrai o nome da classe a partir do padrão `class XYZFunctions`

2. **Extração de Métodos**:
   - Identifica métodos estáticos com padrão `luaXYZ`
   - Extrai o nome real do método removendo o prefixo `luaAction`

3. **Análise de Registros**:
   - Examina o método `init()` para encontrar como os métodos são registrados
   - Confirma os nomes reais usados no ambiente Lua

4. **Geração de Documentação**:
   - Cria arquivos Markdown para classes e métodos
   - Estabelece links bidirecionais entre eles
   - Adiciona metadados e tags apropriados

## Benefícios Técnicos

Esta abordagem oferece vários benefícios técnicos:

1. **Rastreabilidade**: Cada método Lua pode ser rastreado até sua implementação C++
2. **Navegabilidade**: Os links bidirecionais permitem navegar facilmente pela API
3. **Pesquisabilidade**: Tags e propriedades facilitam consultas complexas
4. **Visualização**: O gráfico do Obsidian mostra relações entre classes e métodos
5. **Manutenção**: A estrutura facilita atualizações quando o código muda
6. **Automação**: O processo pode ser totalmente automatizado

## Exemplo de Consultas no Obsidian

Com esta estrutura, é possível realizar consultas como:

```
tag:#lua-method AND class:[[Action]]
```

Para encontrar todos os métodos da classe Action, ou:

```
tag:#lua-method AND cpp-function:/^luaAction/
```

Para encontrar todos os métodos implementados em ActionFunctions.

## Conclusão

Esta estrutura de documentação para Obsidian oferece uma maneira técnica e organizada de documentar a API Lua do Canary, facilitando tanto o desenvolvimento quanto o uso da API por outros desenvolvedores. A automação com Python torna o processo de manutenção da documentação eficiente e consistente.
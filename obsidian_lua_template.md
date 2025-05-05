# Documentação Lua para Obsidian - Template

Este documento apresenta um modelo de como estruturar a documentação das funções Lua do Canary no Obsidian, aproveitando recursos como links internos, tags e propriedades.

## Estrutura de Arquivos

Para uma documentação eficiente no Obsidian, recomendamos a seguinte estrutura de arquivos:

```
/Lua API/
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

## Template para Classe

Cada classe deve ter seu próprio arquivo com o seguinte formato:

```md
---
tags: [lua-class]
aliases: [Action]
---

# Action

## Descrição
Classe que representa ações que podem ser executadas sobre itens no jogo.

## Métodos
- [[Action.onUse|onUse]] - Define o callback a ser executado quando o item é usado
- [[Action.register|register]] - Registra a ação no sistema
- [[Action.id|id]] - Define os IDs de itens associados à ação
- [[Action.aid|aid]] - Define os Action IDs associados
- [[Action.uid|uid]] - Define os Unique IDs associados
- [[Action.position|position]] - Define as posições onde a ação pode ser executada
- [[Action.allowFarUse|allowFarUse]] - Define se a ação pode ser usada à distância
- [[Action.blockWalls|blockWalls]] - Define se paredes bloqueiam a ação
- [[Action.checkFloor|checkFloor]] - Define se o chão deve ser verificado

## Exemplo de Uso
```lua
local action = Action()
action:id(2400) -- ID do item
action:allowFarUse(true)
action:register()
```

## Arquivo C++ Relacionado
- `action_functions.hpp`
- `action_functions.cpp`
```

## Template para Método

Cada método deve ter seu próprio arquivo com o seguinte formato:

```md
---
tags: [lua-method]
class: [[Action]]
cpp-function: luaActionBlockWalls
---

# Action.blockWalls

## Assinatura
```lua
Action:blockWalls(boolean)
```

## Parâmetros
- `boolean` - `true` para verificar linha de visão (paredes bloqueiam), `false` para ignorar paredes

## Retorno
- `boolean` - `true` se a operação foi bem-sucedida, `false` caso contrário

## Descrição
Define se paredes e outros obstáculos bloqueiam a linha de visão para esta ação.

## Implementação C++
```cpp
int ActionFunctions::luaActionBlockWalls(lua_State* L) {
    // action:blockWalls(bool)
    const auto &action = Lua::getUserdataShared<Action>(L, 1, "Action");
    if (action) {
        action->setCheckLineOfSight(Lua::getBoolean(L, 2));
        Lua::pushBoolean(L, true);
    } else {
        Lua::reportErrorFunc(Lua::getErrorDesc(LUA_ERROR_ACTION_NOT_FOUND));
        Lua::pushBoolean(L, false);
    }
    return 1;
}
```

## Exemplo de Uso
```lua
local action = Action()
action:id(2400)
action:blockWalls(true) -- Paredes bloqueiam a ação
action:register()
```

## Notas
- Esta função é registrada no ambiente Lua em `ActionFunctions::init()`
- Internamente, chama o método `setCheckLineOfSight()` da classe C++ `Action`
```

## Coleta Automática de Dados

Para coletar automaticamente esses dados dos arquivos de código fonte, podemos criar um script Python que:

1. Identifique todas as classes Lua (procurando por `registerSharedClass` ou `registerClass`)
2. Para cada classe, identifique todos os métodos (procurando por `registerMethod`)
3. Extraia a documentação e implementação de cada método
4. Gere os arquivos Markdown no formato adequado para o Obsidian

### Exemplo de Algoritmo

```python
# Pseudocódigo para coleta de dados
def coletar_classes_e_metodos():
    classes = {}
    
    # Percorrer todos os arquivos .cpp
    for arquivo_cpp in glob.glob("**/*_functions.cpp", recursive=True):
        with open(arquivo_cpp, 'r') as f:
            conteudo = f.read()
            
        # Encontrar o método init
        init_match = re.search(r'void (\w+)::init\(lua_State\* L\) {(.*?)}', conteudo, re.DOTALL)
        if not init_match:
            continue
            
        classe_cpp = init_match.group(1)
        init_body = init_match.group(2)
        
        # Encontrar registros de classe
        class_matches = re.findall(r'Lua::registerSharedClass\(L, "(\w+)"', init_body)
        for classe_lua in class_matches:
            classes[classe_lua] = {"methods": []}
            
        # Encontrar registros de métodos
        method_matches = re.findall(r'Lua::registerMethod\(L, "(\w+)", "(\w+)", (\w+)::(\w+)\)', init_body)
        for classe_lua, metodo_lua, classe_cpp, metodo_cpp in method_matches:
            if classe_lua in classes:
                classes[classe_lua]["methods"].append({
                    "name": metodo_lua,
                    "cpp_function": metodo_cpp
                })
    
    return classes

def gerar_documentacao_obsidian(classes):
    # Criar diretórios
    os.makedirs("Lua API/Classes", exist_ok=True)
    os.makedirs("Lua API/Métodos", exist_ok=True)
    
    # Gerar arquivos de classes
    for classe, info in classes.items():
        with open(f"Lua API/Classes/{classe}.md", 'w') as f:
            # Gerar conteúdo do arquivo de classe
            
        # Gerar arquivos de métodos
        for metodo in info["methods"]:
            with open(f"Lua API/Métodos/{classe}.{metodo['name']}.md", 'w') as f:
                # Gerar conteúdo do arquivo de método
```

## Benefícios desta Abordagem

1. **Hierarquia clara**: A estrutura de classes e métodos é facilmente navegável
2. **Links bidirecionais**: Obsidian mostrará automaticamente backlinks
3. **Pesquisa eficiente**: Tags e propriedades facilitam a filtragem
4. **Visualização de gráfico**: O Obsidian pode gerar um gráfico visual das relações
5. **Extensibilidade**: Fácil de adicionar novas classes e métodos
6. **Automação**: O processo pode ser automatizado com scripts

## Exemplo de Visualização no Obsidian

No Obsidian, esta estrutura permitirá:

1. Ver todas as classes em um único lugar
2. Navegar facilmente entre classes e seus métodos
3. Pesquisar por tags como `#lua-class` ou `#lua-method`
4. Visualizar a relação entre classes e métodos no gráfico
5. Usar consultas para listar, por exemplo, todos os métodos de uma classe específica
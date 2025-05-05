# Padrão de Nomenclatura das Funções Lua no Canary

## Visão Geral

Este documento serve como referência para entender o padrão de nomenclatura das funções Lua no código fonte do Canary, um emulador de servidor MMORPG de código aberto.

## Padrão Identificado

Ao analisar os arquivos de código fonte, identificamos um padrão consistente na nomenclatura das funções que são expostas ao ambiente Lua:

- As funções C++ que são expostas para Lua seguem o formato: `lua[Categoria][NomeFunção]`
- Exemplo: `luaActionBlockWalls` onde:
  - `lua` indica que é uma interface para o ambiente Lua
  - `Action` indica a categoria/classe da função
  - `BlockWalls` é o nome real da função como será chamada em Lua

## Mapeamento C++ para Lua

No código C++, estas funções são registradas no ambiente Lua através de métodos como:

```cpp
void ActionFunctions::init(lua_State* L) {
    Lua::registerMethod(L, "Action", "blockWalls", ActionFunctions::luaActionBlockWalls);
}
```

Isto significa que em scripts Lua, a função pode ser chamada como:

```lua
Action:blockWalls(true)
```

## Observações Importantes

1. **Filtro para coleta automática**: Para coletar automaticamente todas as funções Lua disponíveis, deve-se procurar por padrões como `lua[A-Z][a-zA-Z]+` nos arquivos .hpp.

2. **Nome real da função**: O nome real da função em Lua é sempre a parte após o prefixo "lua[Categoria]".

3. **Consistência**: Este padrão é consistente em todos os módulos do código fonte, não apenas nas funções de ação.

4. **Arquivos relevantes**: As declarações das funções estão sempre nos arquivos .hpp, enquanto as implementações estão nos arquivos .cpp correspondentes.

5. **Registro de funções**: Para entender como uma função é exposta para Lua, deve-se verificar o método `init()` na classe correspondente.

## Exemplo Completo

| Função C++ | Função Lua | Arquivo |
|------------|------------|---------|
| `luaActionBlockWalls` | `Action:blockWalls()` | action_functions.hpp |
| `luaActionCheckFloor` | `Action:checkFloor()` | action_functions.hpp |
| `luaActionOnUse` | `Action:onUse()` | action_functions.hpp |

---

*Este documento servirá como base para futuras análises e desenvolvimento de ferramentas para coleta automática de funções Lua no código fonte do Canary.*
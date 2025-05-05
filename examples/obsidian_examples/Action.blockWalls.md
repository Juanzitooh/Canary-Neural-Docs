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
Define se paredes e outros obstáculos bloqueiam a linha de visão para esta ação. Quando definido como `true`, o jogador não poderá usar o item se houver uma parede ou outro obstáculo bloqueando a linha de visão até o alvo.

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
- É comumente usada em conjunto com `allowFarUse()` para controlar como os itens podem ser usados à distância

## Relações
- Classe: [[Action]]
- Funções relacionadas: [[Action.allowFarUse]], [[Action.checkFloor]]
- Implementada em: `ActionFunctions::luaActionBlockWalls`
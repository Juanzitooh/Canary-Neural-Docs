---
tags: [lua-class]
aliases: [Action]
---

# Action

## Descrição
Classe que representa ações que podem ser executadas sobre itens no jogo. As ações são usadas para definir comportamentos quando itens são utilizados pelo jogador.

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
action:blockWalls(true)
action:register()
```

## Arquivo C++ Relacionado
- `action_functions.hpp`
- `action_functions.cpp`

## Notas Técnicas
Esta classe é registrada no ambiente Lua através da função `ActionFunctions::init()` usando `Lua::registerSharedClass()`. Todos os seus métodos são registrados usando `Lua::registerMethod()`.

## Relações
- Implementada em: [[ActionFunctions]]
- Usada em: Scripts de ações de itens
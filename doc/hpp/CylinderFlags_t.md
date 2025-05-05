# CylinderFlags_t

### Valores
- FLAG_NOLIMIT = 1 << 0
- // Bypass limits like capacity/container limits
- blocking items/creatures etc.
	FLAG_IGNOREBLOCKITEM = 1 << 1
- // Bypass movable blocking item checks
	FLAG_IGNOREBLOCKCREATURE = 1 << 2
- // Bypass creature checks
	FLAG_CHILDISOWNER = 1 << 3
- // Used by containers to query capacity of the carrier (player)
	FLAG_PATHFINDING = 1 << 4
- // An additional check is done for floor changing/teleport items
	FLAG_IGNOREFIELDDAMAGE = 1 << 5
- // Bypass field damage checks
	FLAG_IGNORENOTMOVABLE = 1 << 6
- // Bypass check for mobility
	FLAG_IGNOREAUTOSTACK = 1 << 7
- // queryDestination will not try to stack items together

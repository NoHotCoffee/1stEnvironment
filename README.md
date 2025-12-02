# 1stEnvironment

This repository contains a Tkinter-based fantasy terminal game, **Chronicles of the Caldera**. The GUI emulates its own terminal while tracking quests, travel, and gear placements for player, companion, weapon, and armor visuals.

## Running the game

Ensure Python 3 is available, then run:

```
python fantasy_game.py
```

Use the built-in command line inside the UI to explore locations, track multistep quests, equip items, and manage consumables.

### Commands

- `help` — show all commands.
- `look` — inspect your current location (discoveries show scavengeable loot).
- `travel <direction/location>` — move along connected paths.
- `map` — list reachable connections from where you stand.
- `quests` — list available quests and their steps.
- `track <quest name>` — toggle tracking a quest.
- `complete <quest name> <step#>` — mark a quest step done.
- `inventory` — list the items you carry.
- `equip <item>` — equip a weapon or armor.
- `use <item>` — use a consumable for its effects.
- `scavenge` — pick up loot available at the current location.
- `sheet` — view your character details, gear, and effects.

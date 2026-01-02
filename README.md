# Fantasy Glade (macOS-friendly Tkinter game)

This repository contains a lightweight fantasy adventure with a full GUI built using Tkinter. It is tuned for macOS with retina-friendly scaling but runs anywhere Python and Tk are available.

## Quick start

1. Ensure Python 3.10+ is installed (macOS already ships with Tk).
2. From the repo root, launch the game:

```bash
python -m fantasy_game
```

Use the on-screen controls or arrow/WASD keys to move, and **Space** to rest.

## Game overview

- **Heroic exploration**: Wander a 10x10 glade, collect glowing loot, and duel ambient spirits.
- **Simple combat**: Moving into an enemy triggers an immediate strike and counterstrike.
- **Rest anywhere**: Recover a bit of health and mana between encounters.
- **Event log**: The right column narrates recent actions in an easily scannable feed.

## macOS optimizations

- Uses `tk scaling 2.0` when running on macOS to improve clarity on Retina displays.
- Native window sizing (1100x760) fits comfortably on modern MacBooks while leaving room for the Dock and menu bar.

## Project layout

- `fantasy_game/app.py` – Tkinter GUI, screens, and widgets.
- `fantasy_game/state.py` – Core game logic and world state.
- `fantasy_game/__main__.py` – Enables `python -m fantasy_game` execution.

"""Core game state and logic for the Fantasy Game."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import random

Coord = Tuple[int, int]


@dataclass
class Hero:
    """Represents the player's hero."""

    name: str = "Astra the Wayfinder"
    max_hp: int = 30
    hp: int = 30
    max_mana: int = 12
    mana: int = 12
    gold: int = 10
    position: Coord = (0, 0)
    inventory: List[str] = field(default_factory=lambda: ["Traveler's Cloak", "Rusty Blade"])

    def heal(self, amount: int) -> int:
        before = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        return self.hp - before

    def restore_mana(self, amount: int) -> int:
        before = self.mana
        self.mana = min(self.max_mana, self.mana + amount)
        return self.mana - before


@dataclass
class Enemy:
    """Represents an enemy roaming the map."""

    name: str
    hp: int
    attack: int
    position: Coord

    @property
    def is_defeated(self) -> bool:
        return self.hp <= 0


@dataclass
class Loot:
    """Represents loot placed on the map."""

    description: str
    gold: int
    mana: int = 0
    healing: int = 0


class GameState:
    """Holds all mutable game data and core logic."""

    def __init__(self, map_size: int = 10, seed: Optional[int] = None) -> None:
        self.map_size = map_size
        self.rng = random.Random(seed)
        self.hero = Hero()
        self.enemies: List[Enemy] = []
        self.loot: Dict[Coord, Loot] = {}
        self.log: List[str] = []
        self.reset()

    def reset(self) -> None:
        """Return the game to its initial playable state."""
        self.hero = Hero(position=self.center_position())
        self.enemies = []
        self.loot = {}
        self.log = ["A whispering breeze carries rumors of hidden relics."]
        self._seed_world()

    def center_position(self) -> Coord:
        """Return a coordinate near the middle of the map."""
        mid = self.map_size // 2
        return (mid, mid)

    # World generation -----------------------------------------------------
    def _seed_world(self) -> None:
        for _ in range(4):
            self.spawn_enemy()
        for _ in range(3):
            self.place_loot()

    def spawn_enemy(self) -> None:
        """Create a new roaming enemy at a random open tile."""
        position = self._random_open_tile()
        enemy_kinds = [
            ("Moss Troll", 12, 4),
            ("Grove Wisp", 8, 3),
            ("Stone Sentinel", 18, 5),
            ("Thornling", 10, 3),
        ]
        name, hp, attack = self.rng.choice(enemy_kinds)
        self.enemies.append(Enemy(name=name, hp=hp, attack=attack, position=position))

    def place_loot(self) -> None:
        """Place a loot cache on an open tile."""
        position = self._random_open_tile()
        finds = [
            Loot("Moonpetal Draught", gold=8, healing=6),
            Loot("Sun-touched Crystal", gold=12, mana=4),
            Loot("Carved Oak Chest", gold=20, healing=2),
            Loot("Traveler's Satchel", gold=6, mana=2, healing=2),
        ]
        self.loot[position] = self.rng.choice(finds)

    def _random_open_tile(self) -> Coord:
        """Find a tile without enemies, loot, or the hero."""
        attempts = 0
        while True:
            x = self.rng.randint(0, self.map_size - 1)
            y = self.rng.randint(0, self.map_size - 1)
            coord = (x, y)
            if coord == self.hero.position:
                attempts += 1
                continue
            if any(enemy.position == coord for enemy in self.enemies):
                attempts += 1
                continue
            if coord in self.loot:
                attempts += 1
                continue
            return coord

    # Movement and interactions -------------------------------------------
    def move_hero(self, dx: int, dy: int) -> None:
        """Attempt to move the hero in the given direction."""
        x, y = self.hero.position
        new_x = min(max(0, x + dx), self.map_size - 1)
        new_y = min(max(0, y + dy), self.map_size - 1)
        new_position = (new_x, new_y)
        if new_position == self.hero.position:
            self.log.append("You press against the edge of the realm—no path lies beyond.")
            return

        self.hero.position = new_position
        self.log.append(f"You advance to tile {new_x + 1}-{new_y + 1}.")
        self._check_for_loot()
        self._check_for_encounter()
        self._maybe_spawn_new_threat()

    def _check_for_loot(self) -> None:
        if self.hero.position not in self.loot:
            return
        loot = self.loot.pop(self.hero.position)
        gained_hp = self.hero.heal(loot.healing)
        gained_mana = self.hero.restore_mana(loot.mana)
        self.hero.gold += loot.gold
        parts = [loot.description]
        if loot.gold:
            parts.append(f"+{loot.gold} gold")
        if gained_hp:
            parts.append(f"+{gained_hp} vitality")
        if gained_mana:
            parts.append(f"+{gained_mana} focus")
        self.log.append(f"You claim {', '.join(parts)}.")

    def _check_for_encounter(self) -> None:
        enemy = self._enemy_at(self.hero.position)
        if not enemy:
            return

        hero_burst = self.rng.randint(5, 9)
        enemy.hp -= hero_burst
        self.log.append(f"{enemy.name} takes {hero_burst} damage.")

        if enemy.is_defeated:
            self.enemies.remove(enemy)
            self.hero.gold += 5
            self.log.append(f"{enemy.name} crumbles. You gather 5 gold.")
            return

        retaliation = max(1, enemy.attack - self.rng.randint(1, 3))
        self.hero.hp -= retaliation
        self.log.append(f"{enemy.name} retaliates for {retaliation} damage.")
        if self.hero.hp <= 0:
            self.hero.hp = 0
            self.log.append("Your vision fades. The grove sleeps once more.")

    def _maybe_spawn_new_threat(self) -> None:
        roll = self.rng.random()
        if roll < 0.15:
            self.spawn_enemy()
            self.log.append("A distant rumble hints at a new foe nearby.")
        elif roll > 0.85:
            self.place_loot()
            self.log.append("Glimmering light suggests treasure has surfaced.")

    # Status helpers -------------------------------------------------------
    def _enemy_at(self, coord: Coord) -> Optional[Enemy]:
        for enemy in self.enemies:
            if enemy.position == coord:
                return enemy
        return None

    def tile_contents(self, coord: Coord) -> str:
        if coord == self.hero.position:
            return "hero"
        if coord in self.loot:
            return "loot"
        if self._enemy_at(coord):
            return "enemy"
        return "empty"

    def status_lines(self) -> List[str]:
        vitality = f"HP: {self.hero.hp}/{self.hero.max_hp}"
        focus = f"Mana: {self.hero.mana}/{self.hero.max_mana}"
        wealth = f"Gold: {self.hero.gold}"
        return [vitality, focus, wealth, f"Inventory: {', '.join(self.hero.inventory)}"]

    def is_game_over(self) -> bool:
        return self.hero.hp <= 0

    def rest(self) -> None:
        if self.is_game_over():
            self.log.append("The world is quiet. Rest offers no return.")
            return
        healed = self.hero.heal(4)
        restored = self.hero.restore_mana(2)
        self.log.append(f"You pause to rest (+{healed} vitality, +{restored} focus).")


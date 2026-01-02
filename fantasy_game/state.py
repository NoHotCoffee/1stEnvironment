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


@dataclass
class Companion:
    """A loyal ally supporting the hero."""

    name: str = "Lyra"
    title: str = "Grove Whisperer"
    bond: int = 3
    focus: int = 5
    note: str = "Guides you toward gentle paths and hidden blooms."


@dataclass
class NPC:
    """Non-player character inhabiting a location."""

    name: str
    role: str
    tone: str
    position: Coord


@dataclass
class Location:
    """Descriptor for a map tile."""

    name: str
    biome: str
    description: str
    features: List[str]
    actions: List[str]


class GameState:
    """Holds all mutable game data and core logic."""

    def __init__(self, map_size: int = 10, seed: Optional[int] = None) -> None:
        self.map_size = map_size
        self.rng = random.Random(seed)
        self.hero = Hero()
        self.companion = Companion()
        self.enemies: List[Enemy] = []
        self.loot: Dict[Coord, Loot] = {}
        self.locations: Dict[Coord, Location] = {}
        self.visited: set[Coord] = set()
        self.npcs: List[NPC] = []
        self.log: List[str] = []
        self.reset()

    def reset(self) -> None:
        """Return the game to its initial playable state."""
        self.hero = Hero(position=self.center_position())
        self.companion = Companion()
        self.enemies = []
        self.loot = {}
        self.locations = {}
        self.visited = set()
        self.npcs = []
        self.log = ["A whispering breeze carries rumors of hidden relics."]
        self._seed_world()
        self._describe_location()

    def center_position(self) -> Coord:
        """Return a coordinate near the middle of the map."""
        mid = self.map_size // 2
        return (mid, mid)

    # World generation -----------------------------------------------------
    def _seed_world(self) -> None:
        self._generate_locations()
        self._populate_npcs()
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

    def _generate_locations(self) -> None:
        groves = [
            ("Whisperleaf Clearing", "grove", "A gentle opening ringed with pale trees.", ["soft moss", "dappled light"], ["Rest", "Forage", "Search"]),
            ("Moonwell Verge", "spring", "A shallow pool reflects drifting clouds.", ["silver water", "stone runes"], ["Commune", "Search", "Chart"]),
            ("Thornwatch Rise", "ridge", "Low ridges hide alcoves of blooming briar.", ["wind-carved stones", "briar nests"], ["Search", "Scout", "Chart"]),
            ("Glimmerbank", "river", "A slow river glows with plankton at dusk.", ["pebbled shore", "luminous eddies"], ["Forage", "Commune", "Search"]),
            ("Sunlilt Meadow", "meadow", "Warm grasses ripple like waves.", ["swaying reeds", "skyward larks"], ["Rest", "Forage", "Chart"]),
            ("Warden's Steps", "ruin", "Ancient stairs lead nowhere but up.", ["broken columns", "etched stones"], ["Search", "Scout", "Commune"]),
        ]
        for x in range(self.map_size):
            for y in range(self.map_size):
                name, biome, desc, features, actions = self.rng.choice(groves)
                flourish = self.rng.choice(
                    [
                        "A stray firefly trails your path.",
                        "The air tastes of pine and rain.",
                        "Echoes hint at distant laughter.",
                        "Petals drift across the trail.",
                        "An owl watches from a high branch.",
                    ]
                )
                location = Location(
                    name=name,
                    biome=biome,
                    description=f"{desc} {flourish}",
                    features=features,
                    actions=actions,
                )
                self.locations[(x, y)] = location

    def _populate_npcs(self) -> None:
        roles = [
            ("Mira", "Lantern Keeper", "Warm but cautious"),
            ("Fen", "Wayfinder", "Soft-spoken and alert"),
            ("Sorrel", "Herbalist", "Curious and patient"),
            ("Brann", "Warden", "Calm and resolute"),
            ("Ilya", "Song Weaver", "Playful and bright"),
        ]
        for name, role, tone in roles:
            position = self._random_open_tile()
            self.npcs.append(NPC(name=name, role=role, tone=tone, position=position))

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
        self._describe_location()
        self._check_for_loot()
        self._check_for_encounter()
        self._maybe_spawn_new_threat()

    def _describe_location(self) -> None:
        loc = self.current_location()
        if loc is None:
            return
        if self.hero.position not in self.visited:
            self.visited.add(self.hero.position)
            seen = ", ".join(loc.features)
            self.log.append(f"You arrive at {loc.name}. {loc.description} Features: {seen}.")
        else:
            self.log.append(f"You return to {loc.name} ({loc.biome}).")

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

    def npcs_at(self, coord: Coord) -> List[NPC]:
        return [npc for npc in self.npcs if npc.position == coord]

    def npcs_here(self) -> List[NPC]:
        return self.npcs_at(self.hero.position)

    def current_location(self) -> Optional[Location]:
        return self.locations.get(self.hero.position)

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

    def location_summary(self) -> str:
        loc = self.current_location()
        if not loc:
            return "Unknown path"
        feats = ", ".join(loc.features)
        return f"{loc.name} — {loc.description} Features: {feats}."

    def is_game_over(self) -> bool:
        return self.hero.hp <= 0

    def rest(self) -> None:
        if self.is_game_over():
            self.log.append("The world is quiet. Rest offers no return.")
            return
        healed = self.hero.heal(4)
        restored = self.hero.restore_mana(2)
        self.log.append(f"You pause to rest (+{healed} vitality, +{restored} focus).")

    # Contextual actions ----------------------------------------------------
    def available_actions(self) -> List[str]:
        loc = self.current_location()
        if not loc:
            return []
        base = list(loc.actions)
        if self.npcs_here():
            base.append("Converse")
        if self.loot.get(self.hero.position):
            base.append("Collect")
        return sorted(set(base))

    def perform_action(self, action: str) -> None:
        if self.is_game_over():
            self.log.append("Silence hangs in the air; no actions remain.")
            return
        action = action.lower()
        if action == "rest":
            self.rest()
            return
        if action == "collect" and self.loot.get(self.hero.position):
            self._check_for_loot()
            return
        if action == "converse":
            self._speak_with_npc()
            return
        handlers = {
            "forage": self._action_forage,
            "search": self._action_search,
            "commune": self._action_commune,
            "chart": self._action_chart,
            "scout": self._action_scout,
        }
        if action in handlers:
            handlers[action]()
        else:
            self.log.append("You hesitate, unsure what to do here.")

    def _action_forage(self) -> None:
        healed = self.hero.heal(self.rng.randint(1, 4))
        mana = self.hero.restore_mana(1)
        self.hero.gold += 1
        self.log.append(f"You forage for herbs (+{healed} vitality, +{mana} focus, +1 gold).")

    def _action_search(self) -> None:
        if self.rng.random() < 0.4:
            finds = [
                Loot("Hidden Pouch", gold=5, mana=1, healing=1),
                Loot("Folded Map Scrap", gold=3, mana=2),
                Loot("Polished Charm", gold=7, healing=2),
            ]
            self.loot[self.hero.position] = self.rng.choice(finds)
            self.log.append("Your search reveals a tucked-away satchel at your feet.")
        else:
            self.log.append("You search the area but pocket only memories.")

    def _action_commune(self) -> None:
        gained = self.hero.restore_mana(self.rng.randint(2, 4))
        self.log.append(f"You attune to the glade (+{gained} focus).")

    def _action_chart(self) -> None:
        self.hero.gold += 3
        self.log.append("You sketch the terrain and mark safe paths (+3 gold from cartography).")

    def _action_scout(self) -> None:
        if self.enemies:
            spotted = self.rng.choice(self.enemies)
            self.log.append(f"You glimpse {spotted.name} near tile {spotted.position[0]+1}-{spotted.position[1]+1}.")
        else:
            self.log.append("The horizon is calm; no threats in sight.")

    def _speak_with_npc(self) -> None:
        locals_here = self.npcs_here()
        if not locals_here:
            self.log.append("No one answers your call.")
            return
        npc = self.rng.choice(locals_here)
        self.log.append(f"{npc.name} ({npc.role}) shares a hint: '{npc.tone}.'")
        self.hero.gold += 2
        self.hero.restore_mana(1)

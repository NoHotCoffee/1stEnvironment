import tkinter as tk
from tkinter import ttk
from dataclasses import dataclass, field
from typing import Dict, List, Optional


@dataclass
class Effect:
    name: str
    stat_changes: Dict[str, int]
    duration: int = 0
    description: str = ""


@dataclass
class Item:
    name: str
    description: str
    type: str
    power: int = 0
    effects: List[Effect] = field(default_factory=list)


@dataclass
class QuestStep:
    description: str
    completed: bool = False


@dataclass
class Quest:
    name: str
    summary: str
    steps: List[QuestStep]
    rewards: List[Item]
    active: bool = False
    completed: bool = False


@dataclass
class Location:
    name: str
    description: str
    connections: Dict[str, str]
    encounters: List[str] = field(default_factory=list)
    vendors: List[str] = field(default_factory=list)


@dataclass
class Character:
    name: str
    stats: Dict[str, int]
    inventory: List[Item] = field(default_factory=list)
    equipped_weapon: Optional[Item] = None
    equipped_armor: Optional[Item] = None
    companion: Optional[str] = None
    effects: List[Effect] = field(default_factory=list)

    def apply_effect(self, effect: Effect):
        self.effects.append(effect)
        for stat, delta in effect.stat_changes.items():
            self.stats[stat] = self.stats.get(stat, 0) + delta

    def remove_expired_effects(self):
        remaining_effects = []
        for effect in self.effects:
            if effect.duration > 0:
                effect.duration -= 1
                if effect.duration > 0:
                    remaining_effects.append(effect)
                else:
                    for stat, delta in effect.stat_changes.items():
                        self.stats[stat] = self.stats.get(stat, 0) - delta
        self.effects = remaining_effects


class GameState:
    def __init__(self):
        self.locations = self._create_locations()
        self.quests = self._create_quests()
        self.location_loot = self._create_loot()
        self.player = self._create_player()
        self.current_location = "Ironhaven"

    def _create_player(self) -> Character:
        starter_weapon = Item(
            name="Rusty Saber",
            description="A worn blade, but it still cuts.",
            type="weapon",
            power=4,
            effects=[Effect(name="Confidence", stat_changes={"spirit": 1}, duration=3)],
        )
        starter_armor = Item(
            name="Patched Leather",
            description="Leather armor reinforced with scrap metal.",
            type="armor",
            power=2,
            effects=[Effect(name="Resilience", stat_changes={"defense": 1}, duration=5)],
        )
        potion = Item(
            name="Sunleaf Tonic",
            description="Restores vitality and sharpens focus.",
            type="consumable",
            effects=[Effect(name="Healing", stat_changes={"vitality": 5}), Effect(name="Focus", stat_changes={"spirit": 2}, duration=2)],
        )
        invigorating_brew = Item(
            name="Invigorating Brew",
            description="A spiced drink that bolsters strength while dulling caution.",
            type="consumable",
            effects=[Effect(name="Might", stat_changes={"strength": 3}, duration=2), Effect(name="Reckless", stat_changes={"defense": -1}, duration=2)],
        )
        warding_charm = Item(
            name="Warding Charm",
            description="A small charm carved with sigils that deflect minor harm.",
            type="trinket",
            power=1,
            effects=[Effect(name="Ward", stat_changes={"defense": 2}, duration=3)],
        )
        player = Character(
            name="Arden",
            stats={"strength": 8, "defense": 6, "spirit": 5, "vitality": 20},
            inventory=[starter_weapon, starter_armor, potion, invigorating_brew, warding_charm],
            companion="Mistral the Fox",
        )
        player.equipped_weapon = starter_weapon
        player.equipped_armor = starter_armor
        return player

    def _create_locations(self) -> Dict[str, Location]:
        return {
            "Ironhaven": Location(
                name="Ironhaven",
                description="A fortress city built inside a caldera. Blacksmiths and engineers thrive here.",
                connections={"north": "Whispering Wilds", "east": "Glimmerfen", "travel gate": "Skyreach", "west": "Obsidian Coast", "tram": "Emberfall Forge"},
                encounters=["tinkers", "sparring guards", "runaway constructs"],
                vendors=["Forge of Dawns", "Clockwork Curios", "Inventor's Row"],
            ),
            "Whispering Wilds": Location(
                name="Whispering Wilds",
                description="Ancient forest with trees that carry echoes of old spells.",
                connections={"south": "Ironhaven", "east": "Frosted Peaks", "grove": "Starwell Oasis"},
                encounters=["moss wisps", "feral sprites", "rootbound beasts"],
                vendors=["Wanderer's Cache", "Listening Stone"],
            ),
            "Glimmerfen": Location(
                name="Glimmerfen",
                description="A luminous swamp where phosphor blooms and hidden ruins wait.",
                connections={"west": "Ironhaven", "north": "Skyreach", "ruins": "Hollow Warrens"},
                encounters=["swamp shamblers", "fog sirens", "luminous leeches"],
                vendors=["Floating Bazaar", "Boglight Ledger"],
            ),
            "Skyreach": Location(
                name="Skyreach",
                description="An aerial archipelago connected by rope bridges and zeppelin docks.",
                connections={"south": "Glimmerfen", "west": "Ironhaven", "summit": "Frosted Peaks", "east": "Zephyr Span"},
                encounters=["sky pirates", "wind drakes", "aether gulls"],
                vendors=["Cloudspire Emporium", "Ballast Market"],
            ),
            "Frosted Peaks": Location(
                name="Frosted Peaks",
                description="Icy mountains riddled with caves and a dormant observatory.",
                connections={"west": "Whispering Wilds", "summit": "Skyreach", "caverns": "Crystal Hollows"},
                encounters=["icebound golems", "aurora spirits", "frost wyrmlings"],
                vendors=["Crag Market", "Observatory Remnants"],
            ),
            "Obsidian Coast": Location(
                name="Obsidian Coast",
                description="Shoreline of black glass beaches and shipwrecked corsairs.",
                connections={"east": "Ironhaven", "cliffs": "Zephyr Span"},
                encounters=["glassed revenants", "corsair raiders", "tidal phantoms"],
                vendors=["Shattered Dock", "Driftwood Traders"],
            ),
            "Emberfall Forge": Location(
                name="Emberfall Forge",
                description="A subterranean foundry fueled by magma falls and rune vents.",
                connections={"elevator": "Ironhaven", "tunnel": "Hollow Warrens"},
                encounters=["ember drudges", "slag elementals", "molten mites"],
                vendors=["Great Crucible", "Ashen Market"],
            ),
            "Zephyr Span": Location(
                name="Zephyr Span",
                description="Wind-scoured bridge of stone arches suspended over the sea.",
                connections={"west": "Skyreach", "south": "Obsidian Coast", "arch": "Starwell Oasis"},
                encounters=["storm djinn", "bridge lurkers"],
                vendors=["Gale's Rest"],
            ),
            "Starwell Oasis": Location(
                name="Starwell Oasis",
                description="Desert grove surrounding a star-lit well said to whisper futures.",
                connections={"north": "Whispering Wilds", "arch": "Zephyr Span", "dunes": "Glass Dunes"},
                encounters=["sand shades", "oracle crows", "wayward pilgrims"],
                vendors=["Oasis Caravan", "Stargazer's Table"],
            ),
            "Hollow Warrens": Location(
                name="Hollow Warrens",
                description="Collapsed ruins beneath Glimmerfen crawling with echoing beasts.",
                connections={"surface": "Glimmerfen", "tunnel": "Emberfall Forge", "crawl": "Crystal Hollows"},
                encounters=["echo bats", "bonepickers", "rune gnawers"],
                vendors=["Shadowed Barter"],
            ),
            "Crystal Hollows": Location(
                name="Crystal Hollows",
                description="Iridescent caverns filled with resonant crystals and cold air.",
                connections={"crawl": "Hollow Warrens", "caverns": "Frosted Peaks"},
                encounters=["resonant spiders", "crystal golems"],
                vendors=["Glittering Nook"],
            ),
            "Glass Dunes": Location(
                name="Glass Dunes",
                description="Sweeping dunes of mirror-like sand that bend light and memory.",
                connections={"oasis": "Starwell Oasis"},
                encounters=["mirror lurkers", "sun wraiths", "glass scorpions"],
                vendors=["Nomad's Crossing"],
            ),
        }

    def _create_loot(self) -> Dict[str, List[Item]]:
        return {
            "Ironhaven": [
                Item(
                    name="Engineer Toolkit",
                    description="Tools that improve delicate work and gadget repairs.",
                    type="trinket",
                    effects=[Effect(name="Fine Tuning", stat_changes={"spirit": 1, "defense": 1}, duration=4)],
                )
            ],
            "Whispering Wilds": [
                Item(
                    name="Grove Pendant",
                    description="A pendant etched with leaf sigils that calm spirits.",
                    type="trinket",
                    effects=[Effect(name="Calm", stat_changes={"spirit": 2}, duration=3)],
                )
            ],
            "Glimmerfen": [
                Item(
                    name="Phosphor Vial",
                    description="Glowing swamp sample that heightens senses and attracts insects.",
                    type="consumable",
                    effects=[Effect(name="Senses", stat_changes={"spirit": 2}, duration=2), Effect(name="Irritation", stat_changes={"defense": -1}, duration=1)],
                )
            ],
            "Skyreach": [
                Item(
                    name="Zeppelin Rations",
                    description="Airship dried meats boosting vitality.",
                    type="consumable",
                    effects=[Effect(name="Hearty", stat_changes={"vitality": 6})],
                )
            ],
            "Frosted Peaks": [
                Item(
                    name="Froststeel Splinter",
                    description="Shard of metal that hardens armor when embedded.",
                    type="armor",
                    power=3,
                    effects=[Effect(name="Cold Ward", stat_changes={"defense": 2}, duration=4)],
                )
            ],
            "Obsidian Coast": [
                Item(
                    name="Corsair Cutlass",
                    description="Pirate blade balanced for swift strikes.",
                    type="weapon",
                    power=6,
                    effects=[Effect(name="Swagger", stat_changes={"strength": 2}, duration=3)],
                )
            ],
            "Emberfall Forge": [
                Item(
                    name="Emberglass Phial",
                    description="Liquid glass that courses like fire, energizing the bearer.",
                    type="consumable",
                    effects=[Effect(name="Blaze", stat_changes={"strength": 2, "spirit": 1}, duration=3)],
                )
            ],
            "Zephyr Span": [
                Item(
                    name="Windlash Cloak",
                    description="Billowing cloak that lets you lean into gales.",
                    type="armor",
                    power=4,
                    effects=[Effect(name="Gale Step", stat_changes={"defense": 1, "spirit": 1}, duration=4)],
                )
            ],
            "Starwell Oasis": [
                Item(
                    name="Starlit Sand",
                    description="Sand that refracts starlight and clears the mind.",
                    type="consumable",
                    effects=[Effect(name="Clarity", stat_changes={"spirit": 3}, duration=2)],
                )
            ],
            "Hollow Warrens": [
                Item(
                    name="Bonechime Blade",
                    description="Blade strung with bone chimes that disorient foes.",
                    type="weapon",
                    power=7,
                    effects=[Effect(name="Rattle", stat_changes={"spirit": 1}, duration=2)],
                )
            ],
            "Crystal Hollows": [
                Item(
                    name="Resonance Shard",
                    description="Crystal shard that vibrates with latent energy.",
                    type="trinket",
                    effects=[Effect(name="Echo Shield", stat_changes={"defense": 2}, duration=3)],
                )
            ],
            "Glass Dunes": [
                Item(
                    name="Sunmirror Draught",
                    description="Potion that reflects light to blind and energize.",
                    type="consumable",
                    effects=[Effect(name="Radiance", stat_changes={"strength": 1, "spirit": 2}, duration=3)],
                )
            ],
        }

    def _create_quests(self) -> Dict[str, Quest]:
        relic = Item(
            name="Aetheric Relic",
            description="A humming prism pulsing with blue energy.",
            type="quest",
            effects=[Effect(name="Attunement", stat_changes={"spirit": 3}, duration=4)],
        )
        glider_parts = Item(
            name="Sky Sail Components",
            description="Carbon-thread sails and buoyant crystals ready for assembly.",
            type="quest",
        )
        forge_seal = Item(
            name="Forge Seal",
            description="Symbol of master smiths, proves your worth in Ironhaven.",
            type="quest",
        )
        map_cache = Item(
            name="Skychart Cache",
            description="Hollow tubes of parchment mapping secret air currents.",
            type="quest",
            effects=[Effect(name="Navigator", stat_changes={"spirit": 2}, duration=5)],
        )
        obsidian_crest = Item(
            name="Obsidian Crest",
            description="Insignia of the coast's free captains granting sea passage.",
            type="quest",
            effects=[Effect(name="Authority", stat_changes={"strength": 1, "defense": 1}, duration=3)],
        )
        starwell_water = Item(
            name="Starwell Water",
            description="Glowing water rumored to heal any ailment.",
            type="quest",
            effects=[Effect(name="Renewal", stat_changes={"vitality": 10})],
        )
        return {
            "Echoes of the Forest": Quest(
                name="Echoes of the Forest",
                summary="Calm the whispering spirits and restore balance to the woods.",
                steps=[
                    QuestStep("Collect three bark runes from the Whispering Wilds"),
                    QuestStep("Banish the moss wisp near the rune circle"),
                    QuestStep("Return to the Ironhaven archivist with the stabilized runes"),
                ],
                rewards=[relic],
            ),
            "Skybound Repairs": Quest(
                name="Skybound Repairs",
                summary="Rebuild an old glider to explore the archipelago.",
                steps=[
                    QuestStep("Speak with the mechanic at the Glimmerfen docks"),
                    QuestStep("Recover buoyant crystals from the Skyreach drakes"),
                    QuestStep("Assemble the glider frame at the Ironhaven workshop"),
                ],
                rewards=[glider_parts],
            ),
            "Forge Master's Trial": Quest(
                name="Forge Master's Trial",
                summary="Prove yourself by crafting an alloy resistant to dragonfire.",
                steps=[
                    QuestStep("Mine froststeel ore in the Frosted Peaks"),
                    QuestStep("Gather emberglass from Glimmerfen vents"),
                    QuestStep("Smelt the alloy in the Ironhaven great forge"),
                ],
                rewards=[forge_seal],
            ),
            "Skychart Errand": Quest(
                name="Skychart Errand",
                summary="Collect charts to guide airships through unsteady currents.",
                steps=[
                    QuestStep("Gather drift charts from Zephyr Span couriers"),
                    QuestStep("Secure aether ink from Skyreach pirates"),
                    QuestStep("Deliver the completed sky map to Ironhaven's dockmaster"),
                ],
                rewards=[map_cache],
            ),
            "Corsair Detente": Quest(
                name="Corsair Detente",
                summary="Broker peace between the Obsidian Coast raiders and Ironhaven merchants.",
                steps=[
                    QuestStep("Recover the lost crest from corsair raiders"),
                    QuestStep("Escort trade envoy safely across Zephyr Span"),
                    QuestStep("Host a parley at the Shattered Dock without bloodshed"),
                ],
                rewards=[obsidian_crest],
            ),
            "Starwell Pilgrimage": Quest(
                name="Starwell Pilgrimage",
                summary="Retrieve sacred water to aid the city's ailing wardens.",
                steps=[
                    QuestStep("Navigate the Glass Dunes and avoid the sun wraiths"),
                    QuestStep("Answer the oasis oracle's riddle to draw the water"),
                    QuestStep("Return the Starwell Water to the Ironhaven infirmary"),
                ],
                rewards=[starwell_water],
            ),
        }

    def scavenge(self) -> str:
        loot = self.location_loot.get(self.current_location)
        if not loot:
            return "Nothing to pick up here."
        item = loot.pop(0)
        self.player.inventory.append(item)
        if not loot:
            self.location_loot.pop(self.current_location, None)
        return f"You recovered {item.name}: {item.description}"

    def travel(self, destination: str) -> str:
        location = self.locations[self.current_location]
        for direction, target in location.connections.items():
            if destination.lower() in {direction.lower(), target.lower()}:
                self.current_location = target
                self.player.remove_expired_effects()
                return f"You travel {direction} to {target}. {self.locations[target].description}"
        return "No clear path in that direction. Check your map."

    def look(self) -> str:
        location = self.locations[self.current_location]
        encounters = ", ".join(location.encounters) if location.encounters else "peaceful air"
        vendors = ", ".join(location.vendors) if location.vendors else "no vendors"
        connections = ", ".join([f"{k.title()} -> {v}" for k, v in location.connections.items()])
        lootable = len(self.location_loot.get(location.name, []))
        return (
            f"Location: {location.name}\n"
            f"{location.description}\n"
            f"Paths: {connections}\n"
            f"Encounters: {encounters}\n"
            f"Vendors: {vendors}\n"
            f"Discoveries: {lootable} item(s) can be scavenged here\n"
        )

    def describe_quests(self) -> str:
        lines = []
        for quest in self.quests.values():
            status = "Completed" if quest.completed else "Active" if quest.active else "Available"
            lines.append(f"{quest.name} — {status}\n  {quest.summary}")
            for idx, step in enumerate(quest.steps, start=1):
                mark = "✔" if step.completed else "✧"
                lines.append(f"    {mark} Step {idx}: {step.description}")
        return "\n".join(lines)

    def toggle_quest(self, quest_name: str) -> str:
        quest = self.quests.get(quest_name)
        if not quest:
            return "No quest by that name."
        quest.active = not quest.active
        state = "tracked" if quest.active else "untracked"
        return f"Quest '{quest.name}' is now {state}."

    def complete_step(self, quest_name: str, step_number: int) -> str:
        quest = self.quests.get(quest_name)
        if not quest:
            return "Quest not found."
        if step_number < 1 or step_number > len(quest.steps):
            return "Step does not exist."
        step = quest.steps[step_number - 1]
        if step.completed:
            return "Step already completed."
        step.completed = True
        if all(s.completed for s in quest.steps):
            quest.completed = True
            quest.active = False
            for reward in quest.rewards:
                self.player.inventory.append(reward)
            return f"Quest '{quest.name}' completed! Rewards added to inventory."
        return f"Marked step {step_number} complete for '{quest.name}'."

    def inventory_summary(self) -> str:
        lines = []
        for item in self.player.inventory:
            equipped = " (equipped)" if item in {self.player.equipped_weapon, self.player.equipped_armor} else ""
            lines.append(f"- {item.name} [{item.type}] power {item.power}{equipped}: {item.description}")
        return "\n".join(lines) if lines else "Inventory is empty."

    def equip(self, item_name: str) -> str:
        for item in self.player.inventory:
            if item.name.lower() == item_name.lower():
                if item.type == "weapon":
                    self.player.equipped_weapon = item
                    for effect in item.effects:
                        self.player.apply_effect(effect)
                    return f"Equipped weapon: {item.name}"
                if item.type == "armor":
                    self.player.equipped_armor = item
                    for effect in item.effects:
                        self.player.apply_effect(effect)
                    return f"Equipped armor: {item.name}"
                return "That item cannot be equipped."
        return "Item not found in inventory."

    def use_item(self, item_name: str) -> str:
        for idx, item in enumerate(self.player.inventory):
            if item.name.lower() == item_name.lower():
                if item.type != "consumable":
                    return "Only consumables can be used this way."
                for effect in item.effects:
                    self.player.apply_effect(effect)
                self.player.inventory.pop(idx)
                return f"Used {item.name}. Effects applied."
        return "Consumable not available."

    def character_sheet(self) -> str:
        weapon = self.player.equipped_weapon.name if self.player.equipped_weapon else "None"
        armor = self.player.equipped_armor.name if self.player.equipped_armor else "None"
        effects = ", ".join([f"{e.name} ({e.duration}t)" for e in self.player.effects]) or "None"
        stats = ", ".join([f"{k}: {v}" for k, v in self.player.stats.items()])
        return (
            f"Name: {self.player.name}\n"
            f"Companion: {self.player.companion}\n"
            f"Stats: {stats}\n"
            f"Weapon: {weapon}\n"
            f"Armor: {armor}\n"
            f"Effects: {effects}\n"
            f"Location: {self.current_location}\n"
        )


class FantasyTerminal:
    def __init__(self, root: tk.Tk, state: GameState):
        self.state = state
        self.root = root
        self.root.title("Chronicles of the Caldera")
        self._build_layout()
        self._print_intro()

    def _build_layout(self):
        self.root.geometry("1100x700")
        self.root.configure(bg="#0f131a")

        main_frame = ttk.Frame(self.root, padding=10)
        main_frame.pack(fill=tk.BOTH, expand=True)

        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)

        terminal_frame = ttk.LabelFrame(main_frame, text="Field Terminal", padding=10)
        terminal_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        self.output = tk.Text(terminal_frame, bg="#101820", fg="#e0f2ff", insertbackground="#7ad1f7", wrap=tk.WORD)
        self.output.pack(fill=tk.BOTH, expand=True)
        self.output.configure(state=tk.DISABLED)

        input_frame = ttk.Frame(main_frame)
        input_frame.grid(row=1, column=0, sticky="ew", padx=(0, 10), pady=(10, 0))
        input_frame.columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="Command:").grid(row=0, column=0, sticky="w")
        self.command_var = tk.StringVar()
        command_entry = ttk.Entry(input_frame, textvariable=self.command_var)
        command_entry.grid(row=0, column=1, sticky="ew")
        command_entry.bind("<Return>", self.execute_command)

        ttk.Button(input_frame, text="Send", command=self.execute_command).grid(row=0, column=2, padx=5)

        sidebar = ttk.LabelFrame(main_frame, text="Vitals & Placements", padding=10)
        sidebar.grid(row=0, column=1, rowspan=2, sticky="nsew")
        sidebar.columnconfigure(0, weight=1)

        self.player_image = tk.Canvas(sidebar, width=160, height=160, bg="#1d2733", highlightthickness=1, highlightbackground="#4b8cfc")
        self.player_image.create_text(80, 80, text="Player\nImage", fill="#7ad1f7")
        self.player_image.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        self.companion_image = tk.Canvas(sidebar, width=160, height=160, bg="#1d2733", highlightthickness=1, highlightbackground="#c084fc")
        self.companion_image.create_text(80, 80, text="Companion\nImage", fill="#e0e7ff")
        self.companion_image.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        gear_frame = ttk.Frame(sidebar)
        gear_frame.grid(row=2, column=0, sticky="ew", pady=(0, 10))
        gear_frame.columnconfigure(0, weight=1)

        self.weapon_slot = tk.Canvas(gear_frame, width=160, height=80, bg="#1a202c", highlightthickness=1, highlightbackground="#90cdf4")
        self.weapon_slot.create_text(80, 40, text="Weapon\nPlacement", fill="#c3dafe")
        self.weapon_slot.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        self.armor_slot = tk.Canvas(gear_frame, width=160, height=80, bg="#1a202c", highlightthickness=1, highlightbackground="#f6ad55")
        self.armor_slot.create_text(80, 40, text="Armor\nPlacement", fill="#fffaf0")
        self.armor_slot.grid(row=1, column=0, sticky="ew")

        self.stats_label = ttk.Label(sidebar, anchor="w", justify=tk.LEFT)
        self.stats_label.grid(row=3, column=0, sticky="ew")
        self._refresh_side_panel()

    def _print_intro(self):
        intro = (
            "Welcome to Chronicles of the Caldera!\n"
            "Type 'help' for commands. Plan quests, manage gear, and explore with your companion.\n"
        )
        self._write(intro)
        self._write(self.state.look())

    def _write(self, message: str):
        self.output.configure(state=tk.NORMAL)
        self.output.insert(tk.END, message + "\n")
        self.output.see(tk.END)
        self.output.configure(state=tk.DISABLED)

    def _refresh_side_panel(self):
        stats = self.state.character_sheet()
        self.stats_label.config(text=stats)
        self.weapon_slot.delete("all")
        weapon_text = self.state.player.equipped_weapon.name if self.state.player.equipped_weapon else "Weapon\nPlacement"
        self.weapon_slot.create_text(80, 40, text=weapon_text, fill="#c3dafe")
        self.armor_slot.delete("all")
        armor_text = self.state.player.equipped_armor.name if self.state.player.equipped_armor else "Armor\nPlacement"
        self.armor_slot.create_text(80, 40, text=armor_text, fill="#fffaf0")

    def execute_command(self, event=None):
        cmd = self.command_var.get().strip()
        if not cmd:
            return
        self.command_var.set("")
        self._write(f"> {cmd}")
        response = self._handle_command(cmd)
        self._write(response)
        self._refresh_side_panel()

    def _handle_command(self, cmd: str) -> str:
        parts = cmd.split()
        keyword = parts[0].lower()
        args = parts[1:]

        if keyword == "help":
            return (
                "Commands:\n"
                "  look — inspect current location\n"
                "  travel <direction/location> — move between locations\n"
                "  inventory — list items\n"
                "  equip <item> — equip weapon or armor\n"
                "  use <item> — use a consumable\n"
                "  scavenge — pick up loot in the area\n"
                "  quests — list quests and steps\n"
                "  track <quest name> — toggle quest tracking\n"
                "  complete <quest name> <step#> — mark a step done\n"
                "  sheet — show character details\n"
                "  map — list reachable locations from here\n"
            )
        if keyword == "look":
            return self.state.look()
        if keyword == "travel" and args:
            return self.state.travel(" ".join(args))
        if keyword == "inventory":
            return self.state.inventory_summary()
        if keyword == "equip" and args:
            return self.state.equip(" ".join(args))
        if keyword == "use" and args:
            return self.state.use_item(" ".join(args))
        if keyword == "scavenge":
            return self.state.scavenge()
        if keyword == "quests":
            return self.state.describe_quests()
        if keyword == "track" and args:
            return self.state.toggle_quest(" ".join(args))
        if keyword == "complete" and len(args) >= 2:
            try:
                step_no = int(args[-1])
                quest_name = " ".join(args[:-1])
            except ValueError:
                return "Usage: complete <quest name> <step number>"
            return self.state.complete_step(quest_name, step_no)
        if keyword == "sheet":
            return self.state.character_sheet()
        if keyword == "map":
            location = self.state.locations[self.state.current_location]
            return "Reachable: " + ", ".join([f"{d.title()} -> {t}" for d, t in location.connections.items()])
        return "Unrecognized command. Type 'help' to see options."


def main():
    root = tk.Tk()
    state = GameState()
    FantasyTerminal(root, state)
    root.mainloop()


if __name__ == "__main__":
    main()

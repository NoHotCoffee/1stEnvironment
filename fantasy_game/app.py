"""Tkinter application for the Fantasy Game."""

from __future__ import annotations

import platform
import tkinter as tk
from tkinter import ttk

from .state import GameState


class MapCanvas(tk.Canvas):
    """Render the world grid and its occupants."""

    TILE_COLORS = {
        "empty": "#1b2a1f",
        "hero": "#9cd67c",
        "enemy": "#d66f6f",
        "loot": "#f0d17b",
    }

    def __init__(self, master: tk.Misc, map_size: int, tile_size: int = 56) -> None:
        self.map_size = map_size
        self.tile_size = tile_size
        width = map_size * tile_size
        height = map_size * tile_size
        super().__init__(
            master,
            width=width,
            height=height,
            background="#0d1310",
            highlightthickness=0,
        )

    def draw(self, state: GameState) -> None:
        self.delete("all")
        for x in range(state.map_size):
            for y in range(state.map_size):
                self._draw_tile((x, y), state.tile_contents((x, y)))
        self._draw_grid_lines()

    def _draw_tile(self, coord, tile_type: str) -> None:
        x, y = coord
        x0 = x * self.tile_size
        y0 = y * self.tile_size
        x1 = x0 + self.tile_size
        y1 = y0 + self.tile_size
        color = self.TILE_COLORS[tile_type]
        border = "#0b0f0d"
        self.create_rectangle(x0, y0, x1, y1, fill=color, outline=border, width=2)
        if tile_type == "hero":
            self.create_text(
                x0 + self.tile_size / 2,
                y0 + self.tile_size / 2,
                text="★",
                fill="#10290f",
                font=("Helvetica", 20, "bold"),
            )
        elif tile_type == "enemy":
            self.create_text(
                x0 + self.tile_size / 2,
                y0 + self.tile_size / 2,
                text="⚔",
                fill="#2b0d0d",
                font=("Helvetica", 16, "bold"),
            )
        elif tile_type == "loot":
            self.create_text(
                x0 + self.tile_size / 2,
                y0 + self.tile_size / 2,
                text="✧",
                fill="#3c2a0b",
                font=("Helvetica", 16, "bold"),
            )

    def _draw_grid_lines(self) -> None:
        for i in range(self.map_size + 1):
            offset = i * self.tile_size
            self.create_line(offset, 0, offset, self.map_size * self.tile_size, fill="#18231c")
            self.create_line(0, offset, self.map_size * self.tile_size, offset, fill="#18231c")


class TitleScreen(ttk.Frame):
    """Intro screen with quick start actions."""

    def __init__(self, master: tk.Misc, start_callback) -> None:
        super().__init__(master, padding=36)
        self.start_callback = start_callback
        self._build()

    def _build(self) -> None:
        title = ttk.Label(self, text="Fantasy Glade", font=("Helvetica", 28, "bold"))
        subtitle = ttk.Label(
            self,
            text="A cozy macOS-friendly fantasy adventure.\nExplore the glade, collect relics, and duel woodland spirits.",
            font=("Helvetica", 12),
            justify="center",
        )
        start_btn = ttk.Button(self, text="Begin Journey", command=self.start_callback, padding=(20, 10))
        title.pack(pady=(10, 12))
        subtitle.pack(pady=(0, 24))
        start_btn.pack(pady=(4, 12))


class GameScreen(ttk.Frame):
    """Primary gameplay interface."""

    def __init__(self, master: tk.Misc, state: GameState, on_reset) -> None:
        super().__init__(master, padding=16)
        self.state = state
        self.on_reset = on_reset
        self.map_canvas = MapCanvas(self, map_size=state.map_size)
        self.log_box = tk.Text(self, height=12, width=50, wrap="word", background="#111511", foreground="#f7f7f7")
        self.log_box.configure(state=tk.DISABLED)
        self.status_labels: list[ttk.Label] = []
        self.companion_labels: list[ttk.Label] = []
        self.npc_list = tk.Listbox(self, height=6, background="#0f1410", foreground="#f4f4f4", selectbackground="#1f2b1f")
        self.inventory_list = tk.Listbox(self, height=6, background="#0f1410", foreground="#f4f4f4", selectbackground="#1f2b1f")
        self.action_buttons: list[ttk.Widget] = []
        self.location_name = ttk.Label(self, font=("Helvetica", 16, "bold"))
        self.location_desc = ttk.Label(self, font=("Helvetica", 11), wraplength=360, justify="left")
        self._build()
        self._bind_keys()
        self.refresh()

    def _build(self) -> None:
        # Left: map
        self.map_canvas.grid(row=0, column=0, rowspan=5, sticky="nsew", padx=(0, 12))

        # Right: status and controls
        status_frame = ttk.Frame(self)
        status_frame.grid(row=0, column=1, sticky="ew")
        header = ttk.Label(status_frame, text="Adventurer Status", font=("Helvetica", 16, "bold"))
        header.pack(anchor="w", pady=(0, 8))
        for _ in range(4):
            label = ttk.Label(status_frame, font=("Helvetica", 12))
            label.pack(anchor="w", pady=2)
            self.status_labels.append(label)

        controls = ttk.LabelFrame(self, text="Journey Controls", padding=10)
        controls.grid(row=1, column=1, sticky="ew", pady=8)
        btn_opts = {"width": 10}
        ttk.Button(controls, text="North", command=lambda: self._move(0, -1), **btn_opts).grid(row=0, column=1, pady=2)
        ttk.Button(controls, text="West", command=lambda: self._move(-1, 0), **btn_opts).grid(row=1, column=0, padx=4)
        ttk.Button(controls, text="East", command=lambda: self._move(1, 0), **btn_opts).grid(row=1, column=2, padx=4)
        ttk.Button(controls, text="South", command=lambda: self._move(0, 1), **btn_opts).grid(row=2, column=1, pady=2)
        ttk.Button(controls, text="Rest", command=self._rest, **btn_opts).grid(row=1, column=1, padx=4, pady=4)

        # Context area: location, companion, NPCs, inventory, actions
        context = ttk.Frame(self)
        context.grid(row=2, column=1, sticky="nsew")

        loc_frame = ttk.LabelFrame(context, text="Current Location", padding=10)
        loc_frame.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        self.location_name.pack(in_=loc_frame, anchor="w")
        self.location_desc.pack(in_=loc_frame, anchor="w", pady=(4, 0))

        grid = ttk.Frame(context)
        grid.grid(row=1, column=0, sticky="nsew")
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

        companion_frame = ttk.LabelFrame(grid, text="Companion", padding=10)
        companion_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 8), pady=(0, 8))
        for _ in range(4):
            label = ttk.Label(companion_frame, font=("Helvetica", 11))
            label.pack(anchor="w", pady=2)
            self.companion_labels.append(label)

        npc_frame = ttk.LabelFrame(grid, text="Nearby NPCs", padding=10)
        npc_frame.grid(row=0, column=1, sticky="nsew", pady=(0, 8))
        self.npc_list.pack(in_=npc_frame, fill="both", expand=True)
        ttk.Button(npc_frame, text="Converse", command=lambda: self._perform_action("Converse")).pack(pady=(6, 0))

        items_frame = ttk.LabelFrame(grid, text="Satchel", padding=10)
        items_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 8))
        self.inventory_list.pack(in_=items_frame, fill="both", expand=True)

        action_frame = ttk.LabelFrame(grid, text="Area Actions", padding=10)
        action_frame.grid(row=1, column=1, sticky="nsew")
        self.action_container = ttk.Frame(action_frame)
        self.action_container.pack(fill="both", expand=True)

        log_frame = ttk.LabelFrame(self, text="Whispers of the Glade", padding=10)
        log_frame.grid(row=3, column=1, sticky="nsew")
        self.log_box.pack(in_=log_frame, fill="both", expand=True)

        actions = ttk.Frame(self)
        actions.grid(row=4, column=1, sticky="ew", pady=(10, 0))
        ttk.Button(actions, text="Restart Journey", command=self.on_reset).pack(side="left", padx=(0, 8))
        ttk.Button(actions, text="Quit", command=self.winfo_toplevel().destroy).pack(side="left")

        self.columnconfigure(0, weight=3)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

    def _bind_keys(self) -> None:
        self.bind_all("<Up>", lambda event: self._move(0, -1))
        self.bind_all("<Down>", lambda event: self._move(0, 1))
        self.bind_all("<Left>", lambda event: self._move(-1, 0))
        self.bind_all("<Right>", lambda event: self._move(1, 0))
        self.bind_all("w", lambda event: self._move(0, -1))
        self.bind_all("s", lambda event: self._move(0, 1))
        self.bind_all("a", lambda event: self._move(-1, 0))
        self.bind_all("d", lambda event: self._move(1, 0))
        self.bind_all("<space>", lambda event: self._rest())

    def _move(self, dx: int, dy: int) -> None:
        if self.state.is_game_over():
            self._append_log("The hero can no longer move.")
            return
        self.state.move_hero(dx, dy)
        self.refresh()

    def _rest(self) -> None:
        self.state.rest()
        self.refresh()

    def _perform_action(self, action: str) -> None:
        self.state.perform_action(action)
        self.refresh()

    def _append_log(self, message: str) -> None:
        self.state.log.append(message)
        self.refresh_log()

    def refresh(self) -> None:
        self.map_canvas.draw(self.state)
        self._refresh_status()
        self._refresh_location()
        self._refresh_companion()
        self._refresh_npcs()
        self._refresh_inventory()
        self._refresh_actions()
        self.refresh_log()

    def _refresh_status(self) -> None:
        for label, text in zip(self.status_labels, self.state.status_lines()):
            label.configure(text=text)
        if self.state.is_game_over():
            self.status_labels[0].configure(text=f"{self.state.hero.name} has fallen.")

    def _refresh_location(self) -> None:
        loc = self.state.current_location()
        if not loc:
            self.location_name.configure(text="Unknown path")
            self.location_desc.configure(text="")
            return
        self.location_name.configure(text=f"{loc.name} ({loc.biome})")
        self.location_desc.configure(text=self.state.location_summary())

    def _refresh_companion(self) -> None:
        comp = self.state.companion
        lines = [
            f"{comp.name}, {comp.title}",
            f"Bond: {comp.bond}",
            f"Focus: {comp.focus}",
            comp.note,
        ]
        for label, text in zip(self.companion_labels, lines):
            label.configure(text=text)

    def _refresh_npcs(self) -> None:
        self.npc_list.delete(0, tk.END)
        for npc in self.state.npcs_here():
            self.npc_list.insert(tk.END, f"{npc.name} — {npc.role} ({npc.tone})")

    def _refresh_inventory(self) -> None:
        self.inventory_list.delete(0, tk.END)
        for item in self.state.hero.inventory:
            self.inventory_list.insert(tk.END, item)

    def _refresh_actions(self) -> None:
        for btn in self.action_buttons:
            btn.destroy()
        self.action_buttons = []
        actions = self.state.available_actions()
        if not actions:
            label = ttk.Label(self.action_container, text="No unique actions here.")
            label.pack(anchor="w")
            self.action_buttons.append(label)
            return
        for action in actions:
            btn = ttk.Button(self.action_container, text=action, command=lambda a=action: self._perform_action(a))
            btn.pack(anchor="w", pady=2, fill="x")
            self.action_buttons.append(btn)

    def refresh_log(self) -> None:
        self.log_box.configure(state=tk.NORMAL)
        self.log_box.delete("1.0", tk.END)
        for entry in self.state.log[-12:]:
            self.log_box.insert(tk.END, f"• {entry}\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state=tk.DISABLED)


class GameApp(tk.Tk):
    """Top-level application wrapper."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Fantasy Glade")
        self.geometry("1100x760")
        self._apply_macos_defaults()
        self.state = GameState()
        self._build_screens()

    def _build_screens(self) -> None:
        self.title_screen = TitleScreen(self, start_callback=self._start_game)
        self.game_screen = GameScreen(self, state=self.state, on_reset=self._start_game)
        self.title_screen.pack(fill="both", expand=True)

    def _start_game(self) -> None:
        self.state.reset()
        self.title_screen.pack_forget()
        self.game_screen.refresh()
        self.game_screen.pack(fill="both", expand=True)

    def _apply_macos_defaults(self) -> None:
        if platform.system() == "Darwin":
            # Improve clarity on Retina displays and adopt the aqua accent.
            self.tk.call("tk", "scaling", 2.0)


def main() -> None:
    app = GameApp()
    app.mainloop()


if __name__ == "__main__":
    main()

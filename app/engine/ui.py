import time
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
import random


console = Console()

NPC_COLOR_MAP = {}

AVAILABLE_COLORS = [
    "cyan",
    "magenta",
    "green",
    "yellow",
    "blue",
    "bright_red",
    "bright_cyan",
    "bright_magenta",
]

STREAM_DELAY = 0.015


def get_npc_color(npc_name: str):
    if npc_name not in NPC_COLOR_MAP:
        NPC_COLOR_MAP[npc_name] = random.choice(AVAILABLE_COLORS)
    return NPC_COLOR_MAP[npc_name]


def stream_panel(title: str, full_text: str, style: str):
    displayed_text = Text()
    
    with Live(refresh_per_second=30, console=console) as live:
        for char in full_text:
            displayed_text.append(char)
            panel = Panel(displayed_text, title=title, style=style)
            live.update(panel)
            time.sleep(STREAM_DELAY)

            # pausa dramática
            if char in [".", "!", "?"]:
                time.sleep(0.25)


def print_player(text: str):
    stream_panel("Jogador", text, "bold white")


def print_npc(npc_name: str, text: str):
    color = get_npc_color(npc_name)
    stream_panel(npc_name, text, color)


def print_world(text: str):
    stream_panel("Mundo", text, "bright_black")
    
'''
console = Console()

NPC_COLOR_MAP = {}

AVAILABLE_COLORS = [
    "cyan",
    "magenta",
    "green",
    "yellow",
    "blue",
    "bright_red",
    "bright_cyan",
    "bright_magenta",
]


def get_npc_color(npc_name: str):
    if npc_name not in NPC_COLOR_MAP:
        NPC_COLOR_MAP[npc_name] = random.choice(AVAILABLE_COLORS)
    return NPC_COLOR_MAP[npc_name]


def print_player(text: str):
    console.print(Panel(text, title="Jogador", style="bold white"))


def print_npc(npc_name: str, text: str):
    color = get_npc_color(npc_name)
    console.print(Panel(text, title=npc_name, style=color))


def print_world(text: str):
    console.print(Panel(text, title="Mundo", style="bright_black"))
'''
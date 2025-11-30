from backend.classes import Teleporter
from backend.classes import Player
from typing import List

import backend.classes as classes
import ui

# --- Get Player Count (with validation) --- 
# Written by Irfan, with editing from Daniel

def get_players(players_string: str) -> List[Player]:

    playercount = 0
    while True:
        if players_string.isdigit():
            playercount = int(players_string)
            if 1 <= playercount <= 4:
                break  # Valid input, exit the loop
            else:
                print("Please enter a number between 1 and 4.")
        else:
            print("That's not a number. try again!")

    # --- Get Player Names ---
    print(f"\nGreat! Let's get names for the {playercount} players.")
    players = []
    for i in range(playercount):
        name = input(f"Name for Player {i+1}: ")
        # Assign color from UI constants
        color = ui.PLAYER_COLORS[i]
        players.append(classes.Player(name, color))

    print("\nLet's begin! Our players are:")
    for player in players:
        print(f"- {player.name} (starting at {player.position})")

    print(players)
    return players

# --- BOARD DATA ---
# We return these lists so main.py can use them
def get_ladders():
    return [Teleporter(3,51), Teleporter(6,27), Teleporter(20,70), Teleporter(36,55), Teleporter(63,95), Teleporter(68,98)]

def get_snakes():
    return [Teleporter(25,5), Teleporter(34,1), Teleporter(47,19), Teleporter(65,52), Teleporter(87,57), Teleporter(91,61), Teleporter(99,69)]
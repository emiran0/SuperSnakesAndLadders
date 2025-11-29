from classes import Player
from typing import List

# --- Get Player Count (with validation) ---

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
    players = [] 

    print(f"\nGreat! Let's get names for the {playercount} players.")
    for i in range(playercount):
        # 'i + 1' makes it "Player 1", "Player 2", etc.
        name = input(f"Enter name for Player {i + 1}: ")
        players.append(Player(name))

    print("\nLet's begin! Our players are:")
    for player in players:
        print(f"- {player.name} (starting at {player.position})")

    print(players)
    return players
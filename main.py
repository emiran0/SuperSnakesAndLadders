import sys
import pygame
import game # Import our logic
import ui   # Import our graphics

#---------------------------------------1. setup Players-----------------------------------

print("Hello! Welcome to Super Snakes And Ladders!\n")

playercount = 0
while True:
    playercount_str = input("How many players are we having today? (1-4): ")
    if playercount_str.isdigit():
        playercount = int(playercount_str)
        if 1 <= playercount <= 4:
            break  # Valid input, exit the loop
        else:
            print("Please enter a number between 1 and 4.")
    else:
        print("That's not a number. try again!")

# while True:
#     try:
#         count = int(input("How many players? (1-4): "))
#         if 1 <= count <= 4: break
#     except: pass

# --- Get Player Names ---
players = []
for i in range(playercount):
    name = input(f"Name for Player {i+1}: ")
    # Assign color from UI constants
    color = ui.PLAYER_COLORS[i]
    players.append(game.Player(name, color))

# --- 2. GAME INIT ---
dice = game.Dice(1, 6)
ladders = game.get_ladders()
snakes = game.get_snakes()
display = ui.GameUI() # Start the UI window

current_idx = 0
game_message = f"{players[0].name}'s turn! Press SPACE."
game_over = False
running = True

# --- 3. MAIN LOOP ---
while running:
    # A. Input Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                # --- TURN LOGIC ---
                curr_player = players[current_idx]
                
                # Roll & Move
                roll = dice.dice_roll()
                curr_player.move(roll)
                game_message = f"{curr_player.name} rolled {roll}."

                # Check Snakes/Ladders
                hit_special = False
                for lad in ladders:
                    if curr_player.position == lad.start:
                        curr_player.teleport(lad.end)
                        game_message += " LADDER!"
                        hit_special = True
                
                for snk in snakes:
                    if curr_player.position == snk.start:
                        curr_player.teleport(snk.end)
                        game_message += " SNAKE!"
                        hit_special = True
                
                if not hit_special:
                    game_message += f" to {curr_player.position}."

                # Win Check or Next Turn
                if curr_player.position == 100:
                    game_message = f"{curr_player.name} WINS!"
                    game_over = True
                else:
                    current_idx = (current_idx + 1) % len(players)

    # B. Update Display
    # We pass the list of players and the current message to the UI
    display.draw(players, players[current_idx], game_message, game_over)

pygame.quit()
sys.exit()
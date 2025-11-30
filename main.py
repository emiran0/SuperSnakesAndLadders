# SUPER SNAKES AND LADDERS with UI v0.2
# Small Embedded Systems 25/26
# Main Module

import sys
import pygame # pygagme module
import classes # where our classes are in
import ui # where our graphics are
import time # for delays

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

# --- Get Player Names ---
players = []
for i in range(playercount):
    name = input(f"Name for Player {i+1}: ")
    # Assign color from UI constants
    color = ui.PLAYER_COLORS[i]
    players.append(classes.Player(name, color))

# --- 2. GAME INIT ---
dice = classes.Dice(1, 6)
ladders = classes.get_ladders()
snakes = classes.get_snakes()
display = ui.GameUI() # Start the UI window

current_idx = 0
game_message = f"{players[0].name}'s turn! Press SPACE."
game_over = False
running = True

# --- 3. MAIN LOOP ---
while running:
    
    # 1) Backend Side
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over and display.roll_button.button_clicked(event.pos):
                
                # --- TURN LOGIC ---
                current_player = players[current_idx]
                
                # Roll & Move
                roll = dice.dice_roll()
                current_player.move(roll)
                time.sleep(0.5)
                game_message = f"{current_player.name} rolled {roll}!"

                # Check Snakes/Ladders
                hit_object = False
                for ladder in ladders:
                    if current_player.position == ladder.start:
                        current_player.teleport(ladder.end)
                        game_message += f" Great! It's a LADDER! Moved to {current_player.position}."
                        hit_object = True
                
                for snake in snakes:
                    if current_player.position == snake.start:
                        current_player.teleport(snake.end)
                        game_message += f" Oh No! It's a SNAKE! Moved to {current_player.position}."
                        hit_object = True
                
                if not hit_object:
                    game_message += f" Moved to {current_player.position}."

                # Win Check or Next Turn
                if current_player.position == 100:
                    game_message = f"{current_player.name} WINS!"
                    game_over = True
                else:
                    current_idx = (current_idx + 1) % len(players)
                
                last_player = current_player

    # 2) Frontend Side
    # We pass the list of players and the current message to the UI Module's Draw Function
    display.draw(players, players[current_idx], game_message, game_over)

pygame.quit()
sys.exit()
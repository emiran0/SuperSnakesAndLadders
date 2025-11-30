# SUPER SNAKES AND LADDERS with UI v0.2
# Software and Systems 25/26
# Main Module

import sys
from backend import functions

import pygame # pygagme module
import backend.classes as classes # where our classes are in
import ui # where our graphics are
import time # for delays

#---------------------------------------1. setup Players-----------------------------------

print("Hello! Welcome to Super Snakes And Ladders!\n")
num_players = input("How many players? (1-4): ")

players = functions.get_players(num_players)

# --- 2. GAME INIT ---
dice = classes.Dice(1, 6)
ladders = functions.get_ladders()
snakes = functions.get_snakes()
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
        
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_SPACE:
                
                # --- TURN LOGIC ---
                current_player = players[current_idx]
                
                # Roll & Move
                roll = dice.dice_roll()
                time.sleep(0.5)
                game_message = f"{current_player.name} rolled {roll}!"

                # Code which checks if current_player has won - Daniel Cowen
                if current_player.position in range(94, 100):
                    if current_player.position + roll == 100:
                        current_player.move(roll)
                        game_message += f" 100 reached - {current_player.name} WINS!"
                        game_is_running = False
                        break
                    elif current_player.position + roll > 100:
                        game_message += f" {current_player.name} stays where they are - must land on 100 to win!"
                        current_idx = (current_idx + 1) % len(players)
                        continue
                    else:
                        pass

                current_player.move(roll)
                current_idx = (current_idx + 1) % len(players)

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
                
                last_player = current_player

    # 2) Frontend Side
    # We pass the list of players and the current message to the UI Module's Draw Function
    display.draw(players, players[current_idx], game_message, game_over)

pygame.quit()
sys.exit()
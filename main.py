# SUPER SNAKES AND LADDERS with UI v0.2
# Main Module (Modified)

import sys
import pygame   # pygagme module
import classes  # where our classes are in
import ui       # where our graphics are
import time     # for delays
import menus    # Import our new file（yanzhi ！！！）

display = ui.GameUI() 

'''         ！！！ After much consideration, if we were to replay it again, 
            ！！！ we'd need to add a major loop to support replayability.(yanzhi)      '''
while True:

    # --- 1. SETUP  ----(yanzhi)
    # The original input() has been replaced with calling the UI interface.
    players = menus.get_game_setup(display)
    
    if players is None: # If the window is closed in the settings interface
        break 

    # --- 2. GAME INIT  ---
    dice = classes.Dice(1, 6)
    ladders = classes.get_ladders()
    snakes = classes.get_snakes()
    
    current_idx = 0
    game_message = f"{players[0].name}'s turn! Press ROLL."
    game_over = False
    running = True 
    
    # --- 3. MAIN LOOP ---
    while running:
        
        # 1) Backend Side
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            # Only execute when button_clicked and the game is not over
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if display.roll_button.button_clicked(event.pos):
                    
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
                            game_message += f" LADDER! -> {current_player.position}."
                            hit_object = True

                    
                    for snake in snakes:
                        if current_player.position == snake.start:
                            current_player.teleport(snake.end)
                            game_message += f" SNAKE! -> {current_player.position}."
                            hit_object = True
                    
                    if not hit_object:
                        game_message += f" Moved to {current_player.position}."

                    # Win Check or Next Turn
                    if current_player.position == 100:
                        game_message = f"{current_player.name} WINS!"
                        game_over = True 
                        # Key Change: The original code here only performed a print statement. (yanzhi)
                        # Now we break out of the inner loop to display the settlement.
                        running = False 
                    else:
                        current_idx = (current_idx + 1) % len(players)
                    
                    last_player = current_player

        # 2) Frontend Side
        # We pass the list of players and the current message to the UI Module's Draw Function
        display.draw(players, players[current_idx], game_message, game_over)

    # --- 4. GAME OVER (yanzhi) ---
    # （running = False），The settlement screen is now displayed.
    winner_name = players[current_idx].name

    # #Pause briefly to allow players to see the last piece reach the end point.
    time.sleep(1) 

    play_again = menus.show_game_over(display, winner_name)
    
    if not play_again: 
        break 

pygame.quit()
sys.exit()
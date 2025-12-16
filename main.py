# SUPER SNAKES AND LADDERS v1.0
# Software and Systems 25/26
# Main Module (Modified)
# Daniel Cowen, Emirhan Kartal, Irfan Satria, Yanzhi Bao

import sys

import pygame   # pygame module
import backend.functions as functions
import backend.classes as classes # where our classes are in
import frontend.constants as constants
import frontend.ui as ui # where our graphics are
import time     # for delays
import menus    # Import our new file（yanzhi ！！！）

display = ui.GameUI() 

'''         ！！！ After much consideration, if we were to replay it again, 
            ！！！ we'd need to add a major loop to support replayability.(yanzhi)      '''


#======================================================================================================

'''DECLARE PLAYER TURN FUNCTION (Irfan)'''
def turnprocess(current_player, players, current_idx):
    # --- TURN LOGIC ---

    # Roll & Move
    roll = dice.dice_roll()
    start_pos = current_player.position
    current_player.move(roll)
    end_pos = current_player.position
    game_message = f"{current_player.name} rolled {roll}!" # Changed for better readability at the bottom bar (Emirhan)

    display.animate_player_move(players, current_idx, start_pos, end_pos, game_message) # Animation Function Call (Emirhan)
    
    # Check Snakes/Ladders (Irfan)
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

    # Win Check or Next Turn (Daniel Cowen, Modified by Irfan & Yanzhi)
    if current_player.position == 100:
        print(f"100 reached - {current_player.name} WINS!")
        game_message = f"{roll}! {current_player.name} WINS!"
        game_over = True 
        # Key Change: The original code here only performed a print statement. (yanzhi)
        # Now we break out of the inner loop to display the settlement.
        running = False
        
    elif current_player.position + roll > 100:
        print(f"{current_player.name} stays where they are - must land on 100 to win!")
        game_message = f"{roll}! {current_player.name} stays - must land on 100 to win!"
        game_over = False
        running = True
        
    else: 
        game_over = False
        running = True
    
    return game_over, game_message, running

#======================================================================================================

'''GAME SETUP, DISPLAY PYGAME WINDOW '''

while True:
     # --- 0. START MENU ---(Emirhan)
    start_game = menus.show_start_menu(display)
    if not start_game:
        break

    # --- 1. SETUP  ----(Yanzhi)
    # The original input() has been replaced with calling the UI interface.
    players = menus.get_game_setup(display)
    
    if players is None: # If the window is closed in the settings interface
        break 
    
    # AUTOMATICALLY ADD CPU PLAYER FOR SINGLE PLAYER GAME (IRFAN)
    if len(players) == 1:
        players.append(classes.Player("CPU", constants.PLAYER_COLORS[len(players)], "CPU"))
    
    # --- 2. GAME INIT  --- Irfan Satria, Modified by Yanzhi Bao and Daniel Cowen
    dice = classes.Dice(1, 6)
    ladders = functions.get_ladders()
    snakes = functions.get_snakes()
    
    current_idx = 0
    game_message = f"{players[0].name}'s turn! Press ROLL."
    game_over = False
    running = True 
    
    # --- 3. MAIN LOOP --- (Irfan Satria)
    while running:
        
        current_player = players[current_idx]
        
        # 1) Backend Side
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        #Execute different behavior depending on the player type whether it's a human or CPU. (Irfan)
    
            if(current_player.type != "CPU"): #HUMAN BEHAVIOR
            # Only execute when button_clicked and the game is not over
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over and running:
                    if display.roll_button.button_clicked(event.pos):
                        game_over, game_message, running = turnprocess(current_player, players, current_idx)
                        current_idx = (current_idx + 1) % len(players)
                        
        if current_player.type == "CPU" and not game_over and running: #CPU BEHAVIOR
            time.sleep(1.0)
            game_over, game_message, running = turnprocess(current_player, players, current_idx)
            current_idx = (current_idx + 1) % len(players)
                                    
        # 2) Frontend Side (Irfan Satria)
        # We pass the list of players and the current message to the UI Module's Draw Function
        display.draw(players, players[current_idx], game_message, game_over)

    # --- 4. GAME OVER (yanzhi) ---
    # （running = False），The settlement screen is now displayed.
    winner_name = players[(current_idx -1) % len(players)].name

    # #Pause briefly to allow players to see the last piece reach the end point.
    time.sleep(1) 

    play_again = menus.show_game_over(display, winner_name)
    
    if not play_again: 
        break 

pygame.quit()
sys.exit()
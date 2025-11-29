#SUPER SNAKES AND LADDERS CLI v0.1
#by irfanbstr

from classes import Dice
from functions import get_players
from constants import ladders, snakes
import time

#---------------------------------------setup Players-----------------------------------

print("Hello! Welcome to Super Snakes And Ladders!\n")
num_players = input("How many players? (1-4): ")

players = get_players(num_players)

#---------------------------------------setup Game board-----------------------------------
#Setup Game Board
mydice = Dice(2,6)  #this is a 2d6 die roll.
#Dice(a,b)
#a is the amount of dies, 
#and b is the sides.
#change the number if we want (a)d(b) dice, ex. (1,6) for 1d6, (2,10) for 2d10... etc

#---------------------------------------setup Game board DONE-----------------------------------

#---------------------------------------start game-----------------------------------

diceval = 0 #create a diceval variable to store the dicerolls

game_is_running = True
while game_is_running:
    for current_player in players:            
        print(f"\nIt's {current_player.name}'s turn.")
        print(f"{current_player.name} is now on square {current_player.position}.")
        # We ask the user to just press Enter
        user_action = input("Press ENTER to roll the dice (or type 'quit' to exit): ")

        if user_action == "":
            # The user pressed Enter
            print("Rolling the dice!")
            # The user pressed Enter
            diceval = mydice.dice_roll()
            time.sleep(0.5) # delay by 0.5s to simulate dice roll
            print(f"...{diceval}")
            
            # Code which checks if current_player has won - Daniel Cowen
            if current_player.position in range(94, 100):
                if current_player.position + diceval == 100:
                    current_player.move(diceval)
                    print(f"100 reached - {current_player.name} WINS!")
                    game_is_running = False
                    break
                elif current_player.position + diceval > 100:
                    print(f"{current_player.name} stays where they are - must land on 100 to win!")
                    continue
                else:
                    pass

            current_player.move(diceval)
            
            for ladder in ladders:
                if current_player.position == ladder.start:
                    print(f"Great! {current_player.name} found a ladder on square {current_player.position}!")
                    current_player.teleport(ladder.end)
                    break # end the for loop
            
            for snake in snakes:
                if current_player.position == snake.start:
                    print(f"Oh no! {current_player.name} found a snake on square {current_player.position}!")
                    current_player.teleport(snake.end)
                    break # end the for loop
            
        elif user_action == "quit":
            print("Thanks for playing!")
            game_is_running = False
            break # Exit the game
            
        else:
            # The user typed something else
            print(f"I don't understand '{user_action}'. Please just press ENTER.")


            

#---------------------------------------END game-----------------------------------
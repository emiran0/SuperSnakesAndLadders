#SUPER SNAKES AND LADDERS CLI v0.1
#by irfanbstr

import random

#---------------------------------------initialise Classes-----------------------------------
class Dice:
    def __init__(self,amount,number):
        self.amount = amount
        self.number = number
        self.value = 0
        print(f"{self.amount}d{self.number} (Dice) was created.")
    
    def dice_roll(self):
        self.value = random.randint(self.amount, self.number*self.amount)
        return self.value
# ---

#Player class will handle the position of each player and the move function
class Player:
    def __init__(self, name):
        self.name = name
        print(f"{self.name} (Player) was created.")
        self.position = 0  # Give it a starting value

    def move(self, steps):
        self.position += steps
        print(f"{self.name} moved to {self.position}")
        
    def teleport(self, endpos):
        self.position = endpos
        print(f"{self.name} teleported to {self.position}")
# ---

# Object serve as a superclass for our snake and ladder classes
class Object:
    def __init__(self, start, end):
        self.type = type
        self.start = start
        self.end = end
        print(f"{self.type} was created with start {start} and end {end}.")
# ---
class Ladder(Object): #child of object
    def __init__(self, start, end):
        self.start = start
        self.end = end
        print(f"Ladder was created with start {start} and end {end}.")
# ---
class Snake(Object): #child of object
    def __init__(self, start, end):
        self.start = start
        self.end = end
        print(f"Snake was created with start {start} and end {end}.")

#---------------------------------------initialise Classes DONE-----------------------------------

#---------------------------------------setup Players-----------------------------------

print("Hello! Welcome to Super Snakes And Ladders!\n")

# --- Get Player Count (with validation) ---
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

print(f"\nGreat! Let's get names for the {playercount} players.")
for i in range(playercount):
    # 'i + 1' makes it "Player 1", "Player 2", etc.
    name = input(f"Enter name for Player {i + 1}: ")
    players.append(Player(name))

print("\nLet's begin! Our players are:")
for player in players:
    print(f"- {player.name} (starting at {player.position})")
#---------------------------------------setup Players DONE-----------------------------------

#---------------------------------------setup Game board-----------------------------------
#Setup Game Board
mydice = Dice(2,6)  #this is a 2d6 die roll.
#Dice(a,b)
#a is the amount of dies, 
#and b is the sides.
#change the number if we want (a)d(b) dice, ex. (1,6) for 1d6, (2,10) for 2d10... etc

l1= Ladder(3,51) #start and end positions
l2= Ladder(6,27)
l3= Ladder(20,70)
l4= Ladder(36,55)
l5= Ladder(3,51)
l6= Ladder(6,27)

ladders = [l1,l2,l3,l4,l5,l6] #this is the list of ladders

s1= Snake(25,5) #start and end positions
s2= Snake(34,1)
s3= Snake(47,19)
s4= Snake(65,52)
s5= Snake(87,57)
s6= Snake(91,61)
s7= Snake(99,69)

snakes = [s1,s2,s3,s4,s5,s6,s7] #this is the list of snakes

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
            diceval = mydice.dice_roll()
            input("...The Result is...")
            # The user pressed Enter
            input(f"...{diceval}")
            # The user pressed Enter
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
            break # Exit the game
            
        else:
            # The user typed something else
            print(f"I don't understand '{user_action}'. Please just press ENTER.")
            
        if current_player.position >= 100:
           print(f"{current_player.name} WINS!")
           game_is_running = False #  end the while loop
           break # end the for loop

#---------------------------------------END game-----------------------------------
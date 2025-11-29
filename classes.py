# SUPER SNAKES AND LADDERS with UI v0.2
# Small Embedded Systems 25/26
# Classes Module

import random

#---------------------------------------initialise Classes-----------------------------------
#Dice class!
class Dice:
    def __init__(self, amount, number):
        self.amount = amount
        self.number = number
        self.value = 0 #initial value
        print(f"{self.amount}d{self.number} (Dice) was created.")
    
    def dice_roll(self):
        self.value = random.randint(self.amount, self.number*self.amount)
        return self.value
# ---

#Player class will handle the position of each player and the move function
class Player:
    def __init__(self, name, color):
        self.name = name
        print(f"{self.name} (Player) was created.")
        self.position = 0 # Give it a starting value
        self.color = color 

    def move(self, steps):
        
        #how the player moves. They cannot move forward if the diceroll steps exceed 100
        if (self.position + steps) <= 100:
            self.position += steps
            print(f"{self.name} moved to {self.position}")
        
        else:
            print(f"{self.name} Cannot move! Exceeding 100!")
        
    def teleport(self, endpos):
        self.position = endpos
        print(f"{self.name} teleported to {self.position}")
# ---

# Object serve as a superclass for our snake and ladder classes
class Object:
    def __init__(self, start, end):
        self.start = start
        self.end = end

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

# --- BOARD DATA ---
# We return these lists so main.py can use them
def get_ladders():
    return [Ladder(3,51), Ladder(6,27), Ladder(20,70), Ladder(36,55), Ladder(63,95), Ladder(68,98)]

def get_snakes():
    return [Snake(25,5), Snake(34,1), Snake(47,19), Snake(65,52), Snake(87,57), Snake(91,61), Snake(98,68)]
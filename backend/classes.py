# SUPER SNAKES AND LADDERS v1.0
# Software and Systems 25/26
# Classes Module
# Daniel Cowen, Irfan Satria

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

# Teleporter class created by Daniel Cowen
class Teleporter:
    '''
    A class which can create and represent either a Snake or a Ladder
    
    Attributes:
        start (int): the start coordinate of either the snake or ladder
        end (int): the end coordinate of either the snake or ladder
        type (str): a calculated variable which utilises attributes 'start' and 'end', which determines whether instance is 'Snake' or 'Ladder'
    '''
    def __init__(self, start: str, end: str):
        self.start = start
        self.end = end
        if self.end > self.start:
            self.type = "Ladder"
        elif self.end < self.start:
            self.type = "Snake"
        print(f"{self.type} was created with start {start} and end {end}.")
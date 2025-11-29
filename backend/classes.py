import random

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
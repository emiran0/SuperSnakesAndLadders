# SUPER SNAKES AND LADDERS v1.0
# Software and Systems 25/26
# UI Module
# Daniel Cowen, Irfan Satria, Emirhan


# Irfan:
# this is the graphics module.
# it contains a single Class called GameUI containing the UI Elements.

import pygame
import sys

from frontend.constants import BLACK, FPS, GRAY, SCREEN_HEIGHT, SCREEN_WIDTH, WHITE

# -------------------------GAME UI (by Irfan Satria, modified by Daniel, Emirhan)---------------------------------------------------

class GameUI: 
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        #Window Caption
        pygame.display.set_caption("Super Snakes & Ladders | Software & Systems 25/26")
        self.clock = pygame.time.Clock()
        
        # Load Font --------------------------------------------------------------------
        try:
            # Font is LCD BLock by Nimble Beasts (Royalty Free)
            # More suitable "Game-y" font
            #https://nimblebeastscollective.itch.io/nb-pixel-font-bundle
            self.font = pygame.font.Font("LCDBlock.ttf", 26)
            self.title_font = pygame.font.Font("LCDBlock.ttf", 64)
            self.button_font = pygame.font.Font("LCDBlock.ttf", 32)
            self.subtitle_font = pygame.font.Font("LCDBlock.ttf", 28)
        except:
            #Revert to Arial if Font not found
            self.font = pygame.font.SysFont("Arial", 24)
            self.title_font = pygame.font.SysFont("Arial", 64)
            self.button_font = pygame.font.SysFont("Arial", 32)
            self.subtitle_font = pygame.font.SysFont("Arial", 28)
        
        # Load Board Image -------------------------------------------------------------------
        try:
            self.board_img = pygame.image.load("board.jpg")
            self.board_img = pygame.transform.scale(self.board_img, (600, 600))
        except:
            self.board_img = None
            
        #------------------------------------------------------------------------------------
        # Create button for user to press 'roll' (Daniel Cowen)
        self.roll_button = Button(x=480, y=620, width=100, height=60, font=self.font, color=WHITE, text_color=BLACK, text="ROLL")

    # Converting gameplay into pixel coordinates for drawing onto screen (Irfan Satria)

    def get_pixel_coords(self, square_number):
        # This function Converts 1-100 square to x,y pixels
        
        idx = square_number - 1 # if the board shows 1, it's actually 0 on the code.
        row = idx // 10  # Floor division to get our row number. Example: 5 is row 0, 13 is row 1, 25 is row 2 because it starts with 2.
        col = idx % 10   # get our col number. Example: 25 is col 5 (remainder is 5)

        # each Cell Square is 60 pixels wide (600pixels/10 squares)
        cell_w = 600 / 10 
        cell_h = 600 / 10
        
        # get the pixel coordinates (XY) of the CENTER of each square.
        # this means half of the width and half the height
        # since our board starts at the bottom, Y is calculated in reverse (from the top of the screen)
        
        # for square 1 (0, 0) it's (30, 570)
        # for square 25 (2, 5) it's (330, 450) 
        x = (col * cell_w) + (cell_w // 2) # column number*60 (full square width) + 30 (half a square)
        y = ((9 - row) * cell_h) + (cell_h // 2) # (max row number - row number) *60 + 30
        
        return int(x), int(y)

   # This is the function that actually puts things on screen
   
    def draw(self, players, current_player, message, game_over):
        #Main render function called every frame
        
        self.screen.fill(BLACK)

        # 1) Draw the Board. Error handling was added in case the Board image was not loaded on the setup (line 45)
        if self.board_img != None:
            self.screen.blit(self.board_img, (0, 0)) #draw starting on X,Y (0,0)
            
        else:
            pygame.draw.rect(self.screen, GRAY, (0, 0, 600, 600))
            # Draw simple grid lines if image fails to load
            for x in range(0, 600, 60):
                pygame.draw.line(self.screen, WHITE, (x, 0), (x, 600))
            for y in range(0, 600, 60):
                pygame.draw.line(self.screen, WHITE, (0, y), (600, y))

        # 2) Draw Players
        for i, player in enumerate(players):
            # get the coordinates for the CENTER of a square 
            px, py = self.get_pixel_coords(player.position)
            # Add 10 pixel offset to each player so they don't overlap perfectly
            # player 1 (0) is shifted left 10 pixels and up 5 pixels
            # player 2 (1) is not shifted
            # player 3 (2) is shifted right 10 pixels and down 5 pixels
            # player 4 (3) is shifted right 20 pixels and down 10 pixels
            offset_x = (i * 10) - 10
            offset_y = (i * 5) - 5
            
            pygame.draw.circle(self.screen, BLACK, (px + offset_x, py + offset_y), 17)
            pygame.draw.circle(self.screen, player.color, (px + offset_x, py + offset_y), 15)

        # 3) Draw UI Text Area (Bottom 100px)
        pygame.draw.rect(self.screen, GRAY, (0, 600, 600, 100))
        
        msg_surf = self.font.render(message, True, WHITE)
        self.screen.blit(msg_surf, (20, 635))

        # Draws the button to 'Roll Dice' onto screen (Daniel Cowen)
        self.roll_button.draw(self.screen)

        if not game_over and current_player:
            turn_surf = self.font.render(f"Next: {current_player.name}", True, current_player.color)
            self.screen.blit(turn_surf, (20, 610))

        pygame.display.flip() # show image from buffer
        self.clock.tick(FPS)
    
    # Emirhan
    def animate_player_move(self, players, current_idx, start_pos, end_pos, message):
        """
        Simple linear animation of a single player's piece along board squares.
        Runs for 0.7 seconds total, regardless of distance. Not include delays for collision resulted events.
        """
        if start_pos == end_pos:
            return

        step = 1 if end_pos > start_pos else -1
        distance = abs(end_pos - start_pos)

        total_ms = 700
        delay_ms = total_ms // distance  # Dynamic delay to avoid too fast animation
        # print("Animating from", start_pos, "to", end_pos, "with delay", delay_ms, "ms")

        pos = start_pos
        while pos != end_pos:
            pos += step
            players[current_idx].position = pos

            # keep window responsive, allow quit while animating
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.draw(players, players[current_idx], message, False)
            pygame.time.delay(delay_ms)

# Button By Daniel Cowen
class Button:
    '''
    A class for creating a button on the screen - Created by Daniel Cowen

    Attributes:
        x - specifies the x coordinate of the button
        y - specifies the y coordinate of the button
        width - specifies the horizontal distance from the x coordinate
        height - specifies the vertical distance from the y coordinate
        font - specifies the typeface for the text in the button
        color - specifies the colour of the button itself
        text_color - specifies the colour of the text in the button
        text - allows the user to specify a short amount of text for placement in the button
        rect - a pygame object of type Rect, built with the attributes above

    Methods:
        .draw(self, screen) - renders the button on the screen
            args:  
            screen - the pygame display which the game is being run on. appears as a pop-up window

        .button_clicked(self, mouse_position) - method to determine whether the mouse has entered the borders of the button
            args:
            mouse_position - the location of the mouse on the screen. 
    '''
    def __init__(self, x, y, width, height, font, color, text_color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.font = font
        self.color = color
        self.text_color = text_color
        self.text = text
    
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height) # create button instance using Pygame's inbuilt Rect function

    def draw(self, screen):
        # Method to draw the button onto the screen
        text_surface = self.font.render(self.text, True, self.text_color) #render the text for inside the button

        # calculate center coordinates of the rect
        rect_center_x = self.x + self.width/2
        rect_center_y = self.y + self.height/2

        text_rect = text_surface.get_rect(center=(rect_center_x, rect_center_y)) # plot text on center coords of rectangle
        pygame.draw.rect(screen, self.color, self.rect) # draws the rectangle to screen
        screen.blit(text_surface, text_rect) # plot the rendered text (text_surface) with the destination text_rect onto the screen

    def button_clicked(self, mouse_position):
        # Method to check whether a button has been clicked or not
        if self.rect.collidepoint(mouse_position):
            return True
        else:
            return False
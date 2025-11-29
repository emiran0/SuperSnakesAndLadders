# SUPER SNAKES AND LADDERS with UI v0.2
# Small Embedded Systems 25/26
# UI Module

# Irfan:
# this is the graphics module.
# it contains a single Class called GameUI containing the UI Elements.

import pygame

# --- PYGAME SETUP ---
# Create a square window for our board plus extra vertical space for text.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700 # 600 for board + 100 for text
FPS = 60 # Capping the Frames per second. 
# Prevents performance issues, without it everything is executed as fast as the processor allows.
# 60 is selected as most monitors have a 60Hz refresh rate.

# DEFINE Colors ----------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
PLAYER_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)] # Red, Blue, Green, Yellow

# ---------------------------------------------------------------------------------------

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
        except:
            #Revert to Arial if Font not found
            self.font = pygame.font.SysFont("Arial", 24)
        
        # Load Board Image -------------------------------------------------------------------
        try:
            self.board_img = pygame.image.load("board.jpg")
            self.board_img = pygame.transform.scale(self.board_img, (600, 600))
        except:
            self.board_img = None
            
        #------------------------------------------------------------------------------------
      
    # Converting gameplay into pixel coordinates for drawing onto screen

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

        if not game_over and current_player:
            turn_surf = self.font.render(f"Next: {current_player.name}", True, current_player.color)
            self.screen.blit(turn_surf, (20, 610))

        pygame.display.flip() # show image from buffer
        self.clock.tick(FPS)
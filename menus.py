# SUPER SNAKES AND LADDERS v1.0
# Software and Systems 25/26
# Menus Module
# Yanzhi Bao
# Emirhan Kartal

# menus.py （yanzhi）
import pygame
import frontend.ui as ui
import frontend.constants as constants
import backend.classes as classes
'''
# menus py ! !
 I've created a new script containing the UI rendering logic for the start and restart buttons, 
 (along with the input field logic at the beginning). 
 I initially intended to integrate it into the UI,
 but that would make the code overly complex.
 So I created a new one. This won't change any UI or class script content.
'''

# Reuse the original project's color definitions
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)

class InputBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = ""                      # Initial content is empty
        self.font = font
        self.active = True                  # Mark the input field as active

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:       # If you press the [Enter key], all text entered so far will be returned
                return self.text            
            elif event.key == pygame.K_BACKSPACE:  # If you press the [Backspace key], it deletes the last character
                self.text = self.text[:-1]
            else:
                if len(self.text) < 10:            # Restrict name length to no more than 10 
                    self.text += event.unicode
        return None

    def draw(self, screen):
        
        pygame.draw.rect(screen, WHITE, self.rect, 2)    # Draw a white border
        
        surf = self.font.render(self.text, True, WHITE)  # Render text (Note: This will use the provided font, Arial)
      
        screen.blit(surf, (self.rect.x + 10, self.rect.y + 10))  # Slightly adjust the text position to center it.

# (Emirhan)
def show_start_menu(display):
    """
    Very simple start menu:
    - Shows 'SUPER SNAKES AND LADDERS' title
    - 'START' button -> return True
    - 'QUIT' button -> return False
    """
    screen = display.screen
    clock = display.clock
    title_font = display.title_font  # use same LCD-style font for theme
    button_font = display.button_font

    # Button sizing
    button_width = 250
    button_height = 60
    center_x = (screen.get_width() // 2) - (button_width // 2)

    start_y = 350
    quit_y = start_y + button_height + 20

    start_btn = ui.Button(center_x, start_y, button_width, button_height, button_font, WHITE, BLACK, "START")
    quit_btn = ui.Button(center_x, quit_y, button_width, button_height, button_font, WHITE, BLACK, "QUIT")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_btn.button_clicked(event.pos):
                    return True
                if quit_btn.button_clicked(event.pos):
                    return False

        screen.fill(BLACK)

        # Big title
        title_text = "SUPER SNAKES AND LADDERS"
        title_surf = title_font.render(title_text, True, WHITE)
        title_rect = title_surf.get_rect(center=(screen.get_width() // 2, 250))
        screen.blit(title_surf, title_rect)

        # Draw buttons
        start_btn.draw(screen)
        quit_btn.draw(screen)

        # Bottom small credit subtitle
        credit_text = "Made by Emirhan & Daniel & Yanzhi & Irfan"
        credit = display.subtitle_font.render(credit_text, True, GREEN)

        # Centered at the bottom (30 px above bottom edge)
        credit_rect = credit.get_rect(center=(screen.get_width() // 2, screen.get_height() - 30))
        screen.blit(credit, credit_rect)

        pygame.display.flip()
        # clock.tick(30)


def get_game_setup(display):
    """
    Replace the original `input()` code in the main function with the following, 
    which directly returns to Player list (List[Player])

    """
    font = display.font
    title_font = display.title_font # I fixed the font to be the same as the main font for consistency. (Emirhan)
    input_font = display.font # I fixed the font to be the same as the main font for consistency. (Emirhan)
    screen = display.screen
    clock = display.clock

    input_box = InputBox(200, 300, 200, 50, input_font)
    players = []
    prompt = "How many players? (1-4)"

    """
    step = 0 (Phase 0): The program is waiting for you to enter the number of players.

        Logic: Press Enter -> Check if input is a number -> If number, set step to 1.

    step = 1 (Phase 1): The program is waiting for you to enter player names.

        Logic: Press Enter -> Store name in list -> Check if names are sufficient -> If sufficient, exit.

    """
    step = 0 # 【Key State Machine】 0: Asking for number of people 1: Asking for names

    target_count = 0

    run_setup = True
    while run_setup:
        screen.fill(BLACK)     # Each loop begins by clearing the screen (blacking it out)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None    # Clicking the close button in the upper-right corner will break the code.
            
            result = input_box.handle_event(event)
            if result is not None:    
                # --- PHASE 0: NUMBER INPUT ---
                if step == 0:                                
                    if result.isdigit() and 1 <= int(result) <= 4:  # Check if the input is a number between 1 and 4
                        target_count = int(result)
                        step = 1
                        prompt = "Name for Player 1:"
                        input_box.text = ""
                
                # --- PHASE 1: NAME INPUT ---
                else:
                    if result.strip():                         # Name Input
                        color = constants.PLAYER_COLORS[len(players)]
                        players.append(classes.Player(result, color))
                        input_box.text = ""           
                        
                        if len(players) == target_count:
                            return players                     # All done. Return the list to main.py.
                        else:
                            prompt = f"Name for Player {len(players)+1}:"  # Not done yet. Prompted to enter the next person's name.
        # Render Title and Prompt
        title = title_font.render("SETUP PLAYERS", True, GREEN)
        title_rect = title.get_rect(center=(screen.get_width() // 2, 150)) # Centered title and moved up a bit for better aesthetics (Emirhan)
        prompt_surf = font.render(prompt, True, WHITE)
        screen.blit(title, title_rect) # Also here to center the title (Emirhan)
        screen.blit(prompt_surf, (150, 250))
        input_box.draw(screen)
        
        pygame.display.flip()
        clock.tick(30)

# ==========================================
# Function: show_game_over (Game Over Screen)
# Purpose: Display the winner and ask if the player wants to restart
# ==========================================
def show_game_over(display, winner_name):
    """
    Display the ending screen.
    Return: True (replay) or False (exit)
    """
    title_font = display.title_font # Changed fonts for consistency (Emirhan)
    button_font = display.button_font
    screen = display.screen
    
    # Reuse the Danny's Button class from ui.py
    replay_btn = ui.Button(200, 450, 200, 60, button_font, WHITE, BLACK, "PLAY AGAIN")
    
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False    # Close the window （no replay）
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_btn.button_clicked(event.pos):
                    return True # Clicked the button, returns True (replay)
                
        # Render Winning Text
        win_text = title_font.render(f"{winner_name} WINS!", True, GREEN)
        win_rect = win_text.get_rect(center=(screen.get_width() // 2, 150)) # Centered title and moved up a bit for better aesthetics (Emirhan)
        # Draw the text and buttons
        screen.blit(win_text, win_rect)
        replay_btn.draw(screen)
        pygame.display.flip()
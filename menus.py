# SUPER SNAKES AND LADDERS with UI v0.2
# Small Embedded Systems 25/26
# Menus Module
# Yanzhi Bao

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

def get_game_setup(display):
    """
    Replace the original `input()` code in the main function with the following, 
    which directly returns to Player list (List[Player])

    """
    font = display.font
    input_font = pygame.font.Font(None, 40) # ！！ I should mention that I can't use the previous font（LCD）, so I'm stuck with the default one. 
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
        title = font.render("SETUP GAME", True, GREEN)
        prompt_surf = font.render(prompt, True, WHITE)
        screen.blit(title, (220, 100))
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
    font = display.font
    screen = display.screen
    
    # Reuse the Danny's Button class from ui.py
    replay_btn = ui.Button(200, 450, 200, 60, font, WHITE, BLACK, "PLAY AGAIN")
    
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False    # Close the window （no replay）
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if replay_btn.button_clicked(event.pos):
                    return True # Clicked the button, returns True (replay)
                
        # Render Winning Text
        win_text = font.render(f"{winner_name} WINS!", True, GREEN)

        # Draw the text and buttons
        screen.blit(win_text, (200, 200))
        replay_btn.draw(screen)
        pygame.display.flip()
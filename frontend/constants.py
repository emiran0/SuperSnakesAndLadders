# SUPER SNAKES AND LADDERS v1.0
# Software and Systems 25/26
# Constants Module
# Daniel Cowen, Irfan Satria

# --- PYGAME SETUP ---
# Create a square window for our board plus extra vertical space for text.
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700 # 600 for board + 100 for text
FPS = 60 # Capping the Frames per second. 
# Prevents performance issues, without it everything is executed as fast as the processor allows.
# 60 is selected as most monitors have a 60Hz refresh rate.

# Background Music Volume
BG_MUSIC_VOLUME = 0.3  
WIN_MUSIC_VOLUME = 0.6 

# DEFINE Colors ----------------------------------------------------------------
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
PLAYER_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)] # Red, Blue, Green, Yellow
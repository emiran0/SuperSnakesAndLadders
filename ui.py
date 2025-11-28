import pygame

# --- CONFIGURATION ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 700 # 600 for board + 100 for text
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
PLAYER_COLORS = [(255, 0, 0), (0, 0, 255), (0, 255, 0), (255, 255, 0)] # Red, Blue, Green, Yellow

class GameUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Super Snakes & Ladders | Software & Systems 25/26")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 24)
        
        # Load Image
        try:
            self.board_img = pygame.image.load("board.jpg")
            self.board_img = pygame.transform.scale(self.board_img, (600, 600))
        except:
            self.board_img = None

    def get_pixel_coords(self, square_number):
        """Converts 1-100 square to x,y pixels"""
        if square_number < 1: square_number = 1
        if square_number > 100: square_number = 100
        
        idx = square_number - 1 
        row = idx // 10  
        col = idx % 10   

        cell_w = 600 / 10
        cell_h = 600 / 10
        
        x = (col * cell_w) + (cell_w // 2)
        y = ((9 - row) * cell_h) + (cell_h // 2)
        return int(x), int(y)

    def draw(self, players, current_player, message, game_over):
        """Main render function called every frame"""
        self.screen.fill(BLACK)

        # 1. Draw Board
        if self.board_img:
            self.screen.blit(self.board_img, (0, 0))
        # else:
        #     pygame.draw.rect(self.screen, GRAY, (0, 0, 600, 600))
        #     # Optional: Draw simple grid lines if image fails
        #     for x in range(0, 600, 60):
        #         pygame.draw.line(self.screen, WHITE, (x, 0), (x, 600))
        #     for y in range(0, 600, 60):
        #         pygame.draw.line(self.screen, WHITE, (0, y), (600, y))

        # 2. Draw Players
        for p in players:
            px, py = self.get_pixel_coords(p.position)
            # Add offset based on name length so they don't overlap perfectly
            offset_x = (len(p.name) * 3) % 20 - 10
            offset_y = (len(p.name) * 5) % 20 - 10
            
            pygame.draw.circle(self.screen, BLACK, (px + offset_x, py + offset_y), 17)
            pygame.draw.circle(self.screen, p.color, (px + offset_x, py + offset_y), 15)

        # 3. Draw UI Text Area (Bottom 100px)
        pygame.draw.rect(self.screen, BLACK, (0, 600, 600, 100))
        
        msg_surf = self.font.render(message, True, WHITE)
        self.screen.blit(msg_surf, (20, 635))

        if not game_over and current_player:
            turn_surf = self.font.render(f"Next: {current_player.name}", True, current_player.color)
            self.screen.blit(turn_surf, (20, 610))

        pygame.display.flip()
        self.clock.tick(FPS)
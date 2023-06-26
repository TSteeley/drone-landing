import pygame

class gameState:
    """ # Game State
    
    Carries important information about the game state
    """
    
    def __init__(self):
        self.dt = 0
        self.running = True
        self.target = []
        self.targetImage = pygame.transform.scale(
            pygame.image.load("red_dot.png"), (200,200))
        
    def set_dt(self, dt):
        self.dt = dt
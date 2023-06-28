import pygame
import random

class gameState:
    """ # Game State
    
    Carries important information about the game state
    """
    
    def __init__(self, screen):
        self.dt = 0
        self.points
        self.running = True
        self.screenSize = screen.get_size()
        self.set_randomTargetPos()
        self.targetImage = pygame.transform.scale(pygame.image.load("red_dot.png"), (200,200))
        
    def set_dt(self, dt):
        self.dt = dt
        
    def draw(self, screen):
        print(self.targetPos)
        screen.blit(self.targetImage, self.targetPos)
        
    def set_randomTargetPos(self):
        self.targetPos = (random.uniform(0,self.screenSize[0])//1,random.uniform(0,self.screenSize[1])//1)
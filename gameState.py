import pygame
import random
from brains import *

class gameState:
    """ # Game State
    
    Carries important information about the game state
    """
    
    def __init__(self, screenSize, player):
        self.dt = 0.017
        self.score = 0
        self.prevScore = 0
        self.withinTarget = 0
        self.prevDist = 0
        self.running = True
        self.screenSize = screenSize
        self.targetPos = tuple(player.pos)
        self.targetHome = tuple(player.pos)
        self.targetImage = pygame.transform.scale(pygame.image.load("red_dot.png"), (200,200))
        
    def set_dt(self, dt):
        self.dt = dt
        
    def draw(self, screen):
        screen.blit(self.targetImage, self.targetPos)
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render(f'Score: {self.score//1}', True, 'black', 'white')
        screen.blit(text, (200,600))
        
        
    def set_randomTargetPos(self):
        self.targetPos = (random.uniform(0,self.screenSize[0])//1,random.uniform(0,self.screenSize[1])//1)
        
    def update(self, player):
        # Scoring hyper parameters
        # [0] want drone to be within this radius to say it is close enough to count
        # [1] score for being with [0] distance of the target
        # [2] If drone is within target radius for [2] time it succeeds gets a bonus and target moves
        # [3] Points for succesfully being near target for target time
        # [4] score for approaching target
        # [5] penalty for leaving target
        # [6] out of bounds penalty
        score = [10, 1, 3, 200, 1, 1, -200]
        toTarg = dist(self.targetPos, tuple(player.pos))
        
        if any([player.pos.x//1 not in range(self.screenSize[0]), player.pos.y//1 not in range(self.screenSize[1])]):
            self.score = 0
            self.dScore = score[6]
            player.reset()
            # If you're confused about setting prevdist to 50 this is why. When the vehicle skips back to origin it frequently gets 
            # much closer to the target position. 
            self.prevDist = 50
            return True
        
        # Check if near target for longer than [2]
        if self.withinTarget > score[2]:
            self.score+=score[3]
            self.set_randomTargetPos()
        
        # Give points for being in radius of target update time near target and reset to 0 if away from target
        if toTarg < score[0]:
            self.score += score[1]
            self.withinTarget += self.dt
        else:
            self.withinTarget = 0
        
        # Give points for approaching target and remove for losing them
        if (self.prevDist - toTarg) >= 0:
            self.score += score[4]*(self.prevDist - toTarg)
        else:
            self.score += score[5]*(self.prevDist - toTarg)
            
        # update previous distance variable
        self.prevDist = toTarg
        self.dScore = self.score - self.prevScore
        self.prevScore = self.score
        return False
        
    def get_reward(self):
        return self.dScore

    def reset(self, seed = None):
        random.seed(seed)
        self.targetPos = self.targetHome
        self.score = 0
        self.prevScore = 0
        self.withinTarget = 0
        self.prevDist = 0
        
        
dist = lambda x,y: ((x[0]-y[0])**2+(x[1]-y[1])**2)**0.5
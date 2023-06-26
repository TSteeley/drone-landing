import pygame
import math as m
import numpy as np
from engine import engine

class player:
    """# Player class
    Super class which all palyers inherit from. The player is responsible for physics and position updates. 
    """
    def __init__(self) -> None:
        self.pos = []
        self.vel = np.array([0,0])
        self.acc = np.array([0,0])
        self.θ = 0
        self.ω = 0
        self.α = 0
        self.width  = 64
        self.height = 64
        self.engines = engine(number = 2, location =  [[-self.width/2,0], [self.width/2,0]], maxthrust=9, maxGimble=False)
        
        self.m = 1.38
        self.I = self.m/12 * (self.height**2 + self.width**2)
        self.g = [0,9.81]

        self.image = pygame.transform.scale(
            pygame.image.load('drone.png'), (64,64))
        
        
    def set_position(self, newPosition):
        self.pos = newPosition
        
    def display(self, screen):
        screen.blit(pygame.transform.rotate(self.image, self.θ), self.pos)
        
    def physics_update(self, dt):
        self.acc = np.matmul(self.engines.get_Thrust(), rotMat(self.θ))/ self.m + self.g 
        pos = 0.5 * self.acc * dt**2 + self.vel*dt + np.array(self.pos)
        self.vel = self.vel + self.acc * dt
        
        self.pos = pygame.Vector2(pos.tolist())
        
        self.α = self.engines.get_Torque()/self.I
        self.θ = self.θ + self.ω * dt + 0.5 * self.α * dt**2
        self.ω = self.α*dt + self.ω
         
        
        

class KeyBoard(player) :
    """ # KeyBoard class 
    
    Test your program from your keyboard
    """
    def __init__(self):
        super().__init__()
        self.thrustDiff = 0.10
        self.prevThrot = 0
        self.changed = False

        
    def key_updates(self, keys, state):
        if keys[pygame.K_w]:
            self.engines.set_Throttle(1)
        if keys[pygame.K_s]:
            self.engines.set_Throttle(0)
        if keys[pygame.K_a]:
            self.engines.increment_Throttle([0.01, -0.01])
        if keys[pygame.K_d]:
            self.engines.increment_Throttle([-0.01, 0.01])
        if keys[pygame.K_SPACE]:
            state.running = False
        if keys[pygame.K_LSHIFT]:
            self.engines.increment_Throttle(0.01)
        if keys[pygame.K_LCTRL]:
            self.engines.increment_Throttle(-0.01)
            
            
rotMat = lambda x: np.array([[m.cos(x), -m.sin(x)],[m.sin(x), m.cos(x)]])
import pygame
from brains import *
from gameState import gameState
from tensorflow import keras
import stable_baselines3

def pyGame2D(player: AI_player):
    # Initialise pygame environment
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()
    pygame.display.set_caption("AI drone")
    player.set_position(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
    state = gameState((1280,720), player)
    
    
    # Event Loop
    while state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        player.display(screen)
        
# If you're using an AI to play uncomment this line
        player.env_update(state)
        
        player.do_action()

        player.key_updates(pygame.key.get_pressed(), state)
        
        player.physics_update(state.dt)
        
        state.update(player)
        
        state.draw(screen)
        
        pygame.display.flip()

        print(player.engines.get_Throttle())
        
        state.set_dt(clock.tick(60) / 250)

    pygame.quit()

if __name__ == '__main__':
    # model = keras.models.load_model('DroneBrainV1')
    model = stable_baselines3.PPO.load("First PPO Model.zip")
    
    pyGame2D(AI_player(model))
    
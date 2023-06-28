import pygame
from brains import KeyBoard
from gameState import gameState


def pyGame2D(player: KeyBoard):
    # Initialise pygame environment
    pygame.init()
    screen = pygame.display.set_mode((1280,720))
    clock = pygame.time.Clock()
    pygame.display.set_caption("AI drone")
    print(pygame.display.get_surface())
    state = gameState(screen)
    
    player.set_position(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2))
    
    # Event Loop
    while state.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # fill the screen with a color to wipe away anything from last frame
        screen.fill("white")

        player.display(screen)

        player.key_updates(pygame.key.get_pressed(), state)
        
        player.physics_update(state.dt)
        
        state.draw(screen)
        
        
        
        pygame.display.flip()

        print(player.pos, player.engines.get_Throttle())
        
        state.set_dt(clock.tick(60) / 500)

    pygame.quit()

if __name__ == '__main__':
    pyGame2D(KeyBoard())
    
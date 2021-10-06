import pygame
import sys
import WORLD
import SHIP

pygame.init()


SCREEN_WIDTH = WORLD.SCREEN_WIDTH
SCREEN_HEIGHT = WORLD.SCREEN_HEIGHT

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


background_img = WORLD.load_image('./assets/background-black.png')
background_img = pygame.transform.scale2x(background_img)

# Object init
ship = SHIP.SHIP()

while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if WORLD.GAME_STATUS:
                pass
            else:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        ship.y -= ship.VELOCITY
    elif keys[pygame.K_DOWN]:
        ship.y += ship.VELOCITY
    elif keys[pygame.K_LEFT]:
        ship.x -= ship.VELOCITY
    elif keys[pygame.K_RIGHT]:
        ship.x += ship.VELOCITY
    # Draw background
    screen.blit(background_img, (0, 0))

    # Draw ship
    ship.draw(screen)

    pygame.display.update()

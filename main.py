import pygame
import sys
import random
from ENEMY import ENEMY
import WORLD
from PLAYER import PLAYER

pygame.init()


screen = pygame.display.set_mode((WORLD.SCREEN_WIDTH, WORLD.SCREEN_HEIGHT))

background_img = WORLD.load_image('./assets/background-black.png')
background_img = pygame.transform.scale2x(background_img)

# Object init
player = PLAYER(WORLD.SCREEN_WIDTH / 2, WORLD.SCREEN_HEIGHT * (4 / 5))
enemies = []


def main():
    run = True
    while run:
        screen.fill(WORLD.COLOR.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        # Create enemy
        if len(enemies) == 0:
            WORLD.GAME_LEVEL += 1
            WORLD.WAVE_LENGTH += 1
            for i in range(WORLD.WAVE_LENGTH):
                enemy_ = ENEMY(
                               # Random x position
                               random.randrange(player.get_width(), WORLD.SCREEN_WIDTH - player.get_width()),
                               # Random y position
                               random.randrange(-WORLD.SCREEN_HEIGHT, -500),
                               # Random color ship
                               random.choice(["red", "green", "blue"]))
                enemies.append(enemy_)

        keys = pygame.key.get_pressed()

        # Draw background
        screen.blit(background_img, (0, 0))
        WORLD.display_text(screen, f"Lives: {player.lives}", 80, 10)
        WORLD.display_text(screen, f"Level: {WORLD.GAME_LEVEL}", 630, 10)

        # Draw player ship
        player.draw(screen)
        player.move(keys)

        # Draw enemy ship
        for enemy_ in enemies:
            enemy_.draw(screen)
            enemy_.move(1)
            if enemy_.y + enemy_.get_height() > WORLD.SCREEN_HEIGHT:
                player.lives -= 1
                enemies.remove(enemy_)


        pygame.display.update()
        WORLD.clock.tick(WORLD.FPS)


if __name__ == "__main__":
    main()

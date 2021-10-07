import pygame
import sys
import WORLD
import PLAYER

pygame.init()


screen = pygame.display.set_mode((WORLD.SCREEN_WIDTH, WORLD.SCREEN_HEIGHT))

background_img = WORLD.load_image('./assets/background-black.png')
background_img = pygame.transform.scale2x(background_img)

# Object init
player = PLAYER.PLAYER(WORLD.SCREEN_WIDTH / 2, WORLD.SCREEN_HEIGHT * (4 / 5))


def main():
    while True:
        screen.fill(WORLD.COLOR.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        keys = pygame.key.get_pressed()

        # Draw background
        screen.blit(background_img, (0, 0))
        WORLD.display_text(screen, f"Lives: {player.lives}", 80, 10)
        WORLD.display_text(screen, f"Level: {1}", 630, 10)

        # Draw ship
        player.draw(screen)
        player.move(keys)

        pygame.display.update()
        WORLD.clock.tick(WORLD.FPS)


if __name__ == "__main__":
    main()

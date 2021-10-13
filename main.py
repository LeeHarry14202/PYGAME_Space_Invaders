import pygame
import sys
import random
import WORLD
from ENEMY import ENEMY
from PLAYER import PLAYER
from LASER import LASER

pygame.init()

screen = pygame.display.set_mode((WORLD.SCREEN_WIDTH, WORLD.SCREEN_HEIGHT))

# Load background image
background_img = WORLD.load_image('./assets/background-black.png')
background_img = pygame.transform.scale2x(background_img)

# Object init
player = PLAYER(WORLD.SCREEN_WIDTH / 2, WORLD.SCREEN_HEIGHT / 2)
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
                if WORLD.GAME_STATUS is False and WORLD.COUNT_TIME >= 400 :
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_SPACE:
                        # Reset game play
                        enemies.clear()

                    player.x = WORLD.SCREEN_WIDTH / 2
                    player.y = WORLD.SCREEN_HEIGHT / 2
                    player.lasers.clear()
                    player.health = 100

                    WORLD.GAME_LEVEL = 0
                    WORLD.WAVE_LENGTH = 1
                    WORLD.GAME_STATUS = True

        # Draw background
        screen.blit(background_img, (0, 0))

        if WORLD.GAME_STATUS:
            # 80, 10 is pos of x and y
            WORLD.display_text(screen, f"Lives: {player.lives}", 80, 10)
            # 630 , 10 is pos of x and y
            WORLD.display_text(screen, f"Level: {WORLD.GAME_LEVEL}", 630, 10)

            # Create enemy ship
            if len(enemies) == 0:
                WORLD.GAME_LEVEL += 1
                WORLD.WAVE_LENGTH += 1
                for i in range(WORLD.WAVE_LENGTH):
                    # Enemy init
                    enemy_ = ENEMY(
                                   # Random x position
                                   random.randrange(player.get_width(), WORLD.SCREEN_WIDTH - player.get_width()),
                                   # Random y position
                                   random.randrange(-WORLD.SCREEN_HEIGHT, -200),
                                   # Random color ship
                                   random.choice(["red", "green", "blue"]))
                    enemies.append(enemy_)

            # Draw enemy ship
            for enemy_ in enemies:
                enemy_.draw(screen)
                enemy_vel = random.randrange(1, 3)
                enemy_.move(enemy_vel)
                enemy_.move_laser(LASER.laser_vel, player)
                # Enemy wil shoot randomly
                if random.randrange(0, 2*WORLD.FPS) == 1:
                    # Enemy have 50% / FPS to shoot
                    enemy_.shoot()
                # Check if the enemy ship collide player ship
                if WORLD.collide(enemy_, player):
                    WORLD.GAME_STATUS = False
                # If the enemy ship go out off screen, player will lose lives
                elif enemy_.y + enemy_.get_height() > WORLD.SCREEN_HEIGHT:
                    player.lives -= 1
                    enemies.remove(enemy_)
                if player.health <= 0:
                    WORLD.GAME_STATUS = False

            keys = pygame.key.get_pressed()
            # Draw player ship
            player.draw(screen)
            player.move(keys)
            # Move and check if laser collide enemy ship
            player.move_laser(-LASER.laser_vel, enemies)
        else:
            WORLD.display_text(screen, f"YOU LOST", WORLD.SCREEN_WIDTH / 2, WORLD.SCREEN_HEIGHT / 2)
            WORLD.display_text(screen, f"TAB SPACE TO PLAY AGAIN", WORLD.SCREEN_WIDTH / 2, WORLD.SCREEN_HEIGHT / 2 + 50)
            WORLD.display_text(screen, f"TAB ESC TO EXIT", WORLD.SCREEN_WIDTH / 2, WORLD.SCREEN_HEIGHT / 2 + 100)
            WORLD.COUNT_TIME += 1
        pygame.display.update()
        WORLD.clock.tick(WORLD.FPS)


if __name__ == "__main__":
    main()

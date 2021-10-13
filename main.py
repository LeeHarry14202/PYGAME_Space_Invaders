import pygame
import sys
import random
import WORLD
# from ENEMY import ENEMY
# from PLAYER import PLAYER
# from LASER import LASER

pygame.init()

screen = pygame.display.set_mode((WORLD.SCREEN_WIDTH, WORLD.SCREEN_HEIGHT))

# Load background image
background_img = WORLD.load_image('./assets/background-black.png')
background_img = pygame.transform.scale2x(background_img)


class SHIP:
    COOLDOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.VELOCITY = 4
        self.cool_down_counter = 0

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def get_rect(self):
        return self.ship_img.get_rect(center=(self.x, self.y))

    def draw(self):
        # Draw ship
        screen.blit(self.ship_img, (self.x, self.y))
        # Draw laser
        for laser in self.lasers:
            laser.draw()

    def move_laser(self, vel, obj):
        self.cooldown()
        for laser_ in self.lasers:
            laser_.move(vel)
            # If the laser go out off screen, remove it
            if laser_.off_screen(WORLD.SCREEN_HEIGHT):
                self.lasers.remove(laser_)
            # If the laser collied obj(player), player will lose health
            elif laser_.collision(obj):
                obj.health -= 10
                # Check if laser have in list, remove it
                if laser_ in self.lasers:
                    self.lasers.remove(laser_)

    def move(self, keys):
        if keys[pygame.K_UP] and self.y - self.VELOCITY > 0:
            self.y -= self.VELOCITY
        elif keys[pygame.K_DOWN] and self.y + self.VELOCITY + self.get_height() + 20 < WORLD.SCREEN_HEIGHT:
            self.y += self.VELOCITY
        elif keys[pygame.K_LEFT] and self.x - self.VELOCITY > 0:
            self.x -= self.VELOCITY
        elif keys[pygame.K_RIGHT] and self.x + self.VELOCITY + self.get_width() < WORLD.SCREEN_WIDTH:
            self.x += self.VELOCITY
        elif keys[pygame.K_SPACE]:
            self.shoot()

    # Cool down laser shoot
    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = LASER(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1


class PLAYER(SHIP):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=100)
        self.ship_img = WORLD.load_image('./assets/pixel_ship_yellow.png')
        self.laser_img = WORLD.load_image('./assets/pixel_laser_yellow.png')
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.lives = 5

    def move_laser(self, vel, enemies_):
        self.cooldown()
        for laser_ in self.lasers:
            laser_.move(vel)
            if laser_.off_screen(WORLD.SCREEN_HEIGHT):
                self.lasers.remove(laser_)
            else:
                for enemy in enemies_:
                    if laser_.collision(enemy):
                        enemies_.remove(enemy)
                        if laser_ in self.lasers:
                            self.lasers.remove(laser_)

    def health_bar(self):
        healthbar_height = 10
        healthbar_y_pos = self.y + self.ship_img.get_height() + healthbar_height
        healthbar_width = self.ship_img.get_width()

        pygame.draw.rect(screen, WORLD.COLOR.RED, (self.x, healthbar_y_pos, healthbar_width, healthbar_height))
        pygame.draw.rect(screen, WORLD.COLOR.GREEN, (self.x, healthbar_y_pos, healthbar_width * (self.health / self.max_health), healthbar_height))

    def draw(self):
        # Draw player ship
        super().draw()
        # Draw health bar
        self.health_bar()


class ENEMY(SHIP):
    def __init__(self, x, y, color="red"):
        super().__init__(x, y)
        COLOR_MAP = {
            "red": (WORLD.load_image('./assets/pixel_ship_red_small.png'),
                    WORLD.load_image('./assets/pixel_laser_red.png')),
            "green": (WORLD.load_image('./assets/pixel_ship_green_small.png'),
                      WORLD.load_image('./assets/pixel_laser_green.png')),
            "blue": (WORLD.load_image('./assets/pixel_ship_blue_small.png'),
                     WORLD.load_image('./assets/pixel_laser_blue.png'))
            }
        self.ship_img, self.laser_img = COLOR_MAP[color]
        self.ship_img = pygame.transform.flip(self.ship_img, False, True)
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


class LASER:
    laser_vel = 4

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not 0 <= self.y <= height

    def collision(self, obj):
        return WORLD.collide(self, obj)


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
                if WORLD.GAME_STATUS is False and WORLD.COUNT_TIME >= 400:
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
                enemy_.draw()
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
            player.draw()
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

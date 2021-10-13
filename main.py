import pygame
import sys
import random
# import WORLD
# from ENEMY import ENEMY
# from PLAYER import PLAYER
# from LASER import LASER

pygame.init()

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

clock = pygame.time.Clock()
FPS = 120


def load_image(image_location):
    image = pygame.image.load(image_location). convert_alpha()
    return image


class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)


def display_text(text, x, y):
    # creating font object my_font
    my_font = pygame.font.SysFont('times new roman', 25)

    # creating a text surface on which text
    # will be drawn
    game_over_surface = my_font.render(text, True, COLOR.WHITE)

    # create a rectangular object for the text
    # surface object
    game_over_rect = game_over_surface.get_rect()

    # setting position of the text
    game_over_rect.midtop = (x, y)

    # blit wil draw the text on screen
    screen.blit(game_over_surface, game_over_rect)


def collide(obj_1, obj_2):
    offset_x = int(obj_2.x) - int(obj_1.x)
    offset_y = int(obj_2.y) - int(obj_1.y)
    # If not collide it will return None, else return (x,y)
    return obj_1.mask.overlap(obj_2.mask, (offset_x, offset_y)) is not None


# Load background image
background_img = load_image('./assets/background-black.png')
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
            if laser_.off_screen(SCREEN_HEIGHT):
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
        elif keys[pygame.K_DOWN] and self.y + self.VELOCITY + self.get_height() + 20 < SCREEN_HEIGHT:
            self.y += self.VELOCITY
        elif keys[pygame.K_LEFT] and self.x - self.VELOCITY > 0:
            self.x -= self.VELOCITY
        elif keys[pygame.K_RIGHT] and self.x + self.VELOCITY + self.get_width() < SCREEN_WIDTH:
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
        self.ship_img = load_image('./assets/pixel_ship_yellow.png')
        self.laser_img = load_image('./assets/pixel_laser_yellow.png')
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.lives = 5

    def move_laser(self, vel, enemies_):
        self.cooldown()
        for laser_ in self.lasers:
            laser_.move(vel)
            if laser_.off_screen(SCREEN_HEIGHT):
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

        pygame.draw.rect(screen, COLOR.RED, (self.x, healthbar_y_pos, healthbar_width, healthbar_height))
        pygame.draw.rect(screen, COLOR.GREEN, (self.x, healthbar_y_pos, int(healthbar_width * (self.health / self.max_health)), healthbar_height))

    def draw(self):
        # Draw player ship
        super().draw()
        # Draw health bar
        self.health_bar()


class ENEMY(SHIP):
    def __init__(self, x, y, color="red"):
        super().__init__(x, y)
        COLOR_MAP = {
            "red": (load_image('./assets/pixel_ship_red_small.png'),
                    load_image('./assets/pixel_laser_red.png')),
            "green": (load_image('./assets/pixel_ship_green_small.png'),
                      load_image('./assets/pixel_laser_green.png')),
            "blue": (load_image('./assets/pixel_ship_blue_small.png'),
                     load_image('./assets/pixel_laser_blue.png'))
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
        return collide(self, obj)


# Object init
player = PLAYER(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
enemies = []


def main():
    GAME_STATUS = True
    GAME_LEVEL = 0
    # Number of enemy ship
    WAVE_LENGTH = 1
    COUNT_TIME = 0
    run = True
    while run:
        screen.fill(COLOR.BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if GAME_STATUS is False and COUNT_TIME >= 400:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_SPACE:
                        COUNT_TIME = 0
                        # Reset game play
                        enemies.clear()

                        player.x = SCREEN_WIDTH / 2
                        player.y = SCREEN_HEIGHT / 2
                        player.lasers.clear()
                        player.health = 100

                        GAME_LEVEL = 0
                        WAVE_LENGTH = 1
                        GAME_STATUS = True

        # Draw background
        screen.blit(background_img, (0, 0))

        if GAME_STATUS:
            # 80, 10 is pos of x and y
            display_text(f"Lives: {player.lives}", 80, 10)
            # 630 , 10 is pos of x and y
            display_text(f"Level: {GAME_LEVEL}", 630, 10)

            # Create enemy ship
            if len(enemies) == 0:
                GAME_LEVEL += 1
                WAVE_LENGTH += 1
                for i in range(WAVE_LENGTH):
                    # Enemy init
                    enemy_ = ENEMY(
                                   # Random x position
                                   random.randrange(player.get_width(), SCREEN_WIDTH - player.get_width()),
                                   # Random y position
                                   random.randrange(-SCREEN_HEIGHT, -200),
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
                if random.randrange(0, 2*FPS) == 1:
                    # Enemy have 50% / FPS to shoot
                    enemy_.shoot()
                # Check if the enemy ship collide player ship
                if collide(enemy_, player) or player.health <= 0 or player.lives <= 0:
                    GAME_STATUS = False
                # If the enemy ship go out off screen, player will lose lives
                elif enemy_.y + enemy_.get_height() > SCREEN_HEIGHT:
                    player.lives -= 1
                    enemies.remove(enemy_)

            keys = pygame.key.get_pressed()
            # Draw player ship
            player.draw()
            player.move(keys)
            # Move and check if laser collide enemy ship
            player.move_laser(-LASER.laser_vel, enemies)
        else:
            display_text(f"YOU LOST", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            display_text(f"TAB SPACE TO PLAY AGAIN", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50)
            display_text(f"TAB ESC TO EXIT", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100)
            COUNT_TIME += 1
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

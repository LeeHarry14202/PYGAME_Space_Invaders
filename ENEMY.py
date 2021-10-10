import pygame.mask
from SHIP import SHIP
import WORLD


class ENEMY(SHIP):
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health=100)
        COLOR_MAP = {
            "red": (WORLD.load_image('./assets/pixel_ship_red_small.png'),
                    WORLD.load_image('./assets/pixel_laser_red.png')),
            "green": (WORLD.load_image('./assets/pixel_ship_green_small.png'),
                      WORLD.load_image('./assets/pixel_laser_green.png')),
            "blue": (WORLD.load_image('./assets/pixel_ship_blue_small.png'),
                     WORLD.load_image('./assets/pixel_laser_blue.png'))
            }
        self.ship_img, self.laser_img = COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.VELOCITY = 1
        self.enemies = []

    # def draw(self, screen):
    #     # for enemy in self.enemies:
    #         enemy.draw.(screen)

    def move(self, vel):
        if self.y + self.VELOCITY < WORLD.SCREEN_HEIGHT:
            self.VELOCITY = vel
            self.y += self.VELOCITY
        else:
            self.x += 50
            self.y = 0

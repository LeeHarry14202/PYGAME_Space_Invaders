import pygame.mask
from SHIP import SHIP
import WORLD


class ENEMY(SHIP):
    def __init__(self, x, y, color="red", health=100):
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
        self.ship_img = pygame.transform.flip(self.ship_img, False, True)
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel



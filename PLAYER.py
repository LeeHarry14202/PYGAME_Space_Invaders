import pygame
from SHIP import SHIP
import WORLD


class PLAYER(SHIP):
    def __init__(self, x, y, health=100):
        super().__init__(x, y, health=100)
        self.ship_img = WORLD.load_image('./assets/pixel_ship_yellow.png')
        self.laser_img = WORLD.load_image('./assets/pixel_laser_yellow.png')
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
        self.lives = 5

    def move_laser(self, vel, enemies):
        self.cooldown()
        for laser_ in self.lasers:
            laser_.move(vel)
            if laser_.off_screen(WORLD.SCREEN_HEIGHT):
                self.lasers.remove(laser_)
            else:
                for enemy in enemies:
                    if laser_.collision(enemy):
                        enemies.remove(enemy)
                        self.lasers.remove(laser_)

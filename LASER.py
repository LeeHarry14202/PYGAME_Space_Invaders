import pygame
from SHIP import SHIP
import WORLD


class LASER(SHIP):
    def __init__(self, x, y, img):
        super().__init__(x, y)
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return 0 <= self.y <= height

    def collision(self, obj):
        return WORLD.collide(self, obj)


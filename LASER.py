import pygame
import WORLD


class LASER:
    laser_vel = 4

    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def draw(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not 0 <= self.y <= height

    def collision(self, obj):
        return WORLD.collide(self, obj)

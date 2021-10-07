import WORLD
import pygame


class SHIP:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.laser = []
        self.VELOCITY = 3

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def get_rect(self):
        return self.ship_img.get_rect(center=(self.x, self.y))

    def draw(self, screen):
        screen.blit(self.ship_img, (self.x, self.y))

    def move(self, keys):
        if keys[pygame.K_UP] and self.y - self.VELOCITY > 0:
            self.y -= self.VELOCITY
        elif keys[pygame.K_DOWN] and self.y + self.VELOCITY + self.get_height() < WORLD.SCREEN_HEIGHT:
            self.y += self.VELOCITY
        elif keys[pygame.K_LEFT] and self.x - self.VELOCITY > 0:
            self.x -= self.VELOCITY
        elif keys[pygame.K_RIGHT] and self.x + self.VELOCITY + self.get_width() < WORLD.SCREEN_WIDTH:
            self.x += self.VELOCITY

import WORLD
import pygame
from LASER import LASER


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

    def draw(self, screen):
        # Draw ship
        screen.blit(self.ship_img, (self.x, self.y))
        # Draw laser
        for laser in self.lasers:
            laser.draw(screen)

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

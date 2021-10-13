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
                        if laser_ in self.lasers:
                            self.lasers.remove(laser_)

    def health_bar(self, screen):
        healthbar_height = 10
        healthbar_y_pos = self.y + self.ship_img.get_height() + healthbar_height
        healthbar_width = self.ship_img.get_width()

        pygame.draw.rect(screen, WORLD.COLOR.RED, (self.x, healthbar_y_pos, healthbar_width, healthbar_height))
        pygame.draw.rect(screen, WORLD.COLOR.GREEN, (self.x, healthbar_y_pos, healthbar_width * (self.health / self.max_health), healthbar_height))

    def draw(self, screen):
        # Draw player ship
        super().draw(screen)
        # Draw health bar
        self.health_bar(screen)

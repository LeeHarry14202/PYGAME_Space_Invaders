import WORLD


class SHIP:
    def __init__(self):
        self.x = WORLD.SCREEN_WIDTH / 2
        self.y = WORLD.SCREEN_HEIGHT * (4 / 5)
        self.img = WORLD.load_image('./assets/pixel_ship_red_small.png')
        self.rect = self.img.get_rect(center=(self.x, self.y))
        self.VELOCITY = 1
        self.direction = 'STAND'

    def draw(self, screen):
        # self.move_ship()
        self.rect = self.img.get_rect(center=(self.x, self.y))
        screen.blit(self.img, self.rect)

    def move_ship(self):
        if self.direction == 'UP':
            self.y -= self.VELOCITY
        elif self.direction == 'DOWN':
            self.y += self.VELOCITY
        elif self.direction == 'RIGHT':
            self.x += self.VELOCITY
        elif self.direction == 'LEFT':
            self.x -= self.VELOCITY
        else:
            self.x += 0
            self.y += 0
        self.rect = self.img.get_rect(center=(self.x, self.y))

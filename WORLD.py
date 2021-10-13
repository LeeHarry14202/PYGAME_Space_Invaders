import pygame

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

clock = pygame.time.Clock()
FPS = 120


GAME_STATUS = True
GAME_LEVEL = 0
# Number of enemy ship
WAVE_LENGTH = 1

COUNT_TIME = 0


def load_image(image_location):
    image = pygame.image.load(image_location). convert_alpha()
    return image


class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)


def display_text(screen, text, x, y):
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


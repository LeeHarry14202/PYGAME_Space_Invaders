import pygame

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

GAME_STATUS = True

clock = pygame.time.Clock()

FPS = 120

GAME_LEVEL = 0

WAVE_LENGTH = 5


def load_image(image_location):
    image = pygame.image.load(image_location). convert_alpha()
    return image


class COLOR:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)


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

import pygame

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600


GAME_STATUS = True


def load_image(image_location):
    image = pygame.image.load(image_location). convert_alpha()
    # image = pygame.transform(image)
    return image

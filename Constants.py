import pygame
from LoadTextures import *

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


FIELD_WIDTH = 7
FIELD_HEIGHT = 10


SCREEN_SIZE = pygame.display.get_window_size()


CELL_SIZE = int(SCREEN_SIZE[1] // FIELD_HEIGHT)
LEFT_INDENT = int((SCREEN_SIZE[0] - SCREEN_SIZE[1] * FIELD_WIDTH * 0.125) // 2)
TOP_INDENT = int(CELL_SIZE * 0.75)


placed_boxes = pygame.sprite.Group()
background = pygame.sprite.Group()
ground_border = pygame.sprite.Group()
falling_boxes = pygame.sprite.Group()
player_mark = pygame.sprite.Group()

menu_sprites = pygame.sprite.Group()


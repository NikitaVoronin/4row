import pygame
from LoadTextures import *

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


SCREEN_SIZE = pygame.display.get_window_size()

BOARD_HEIGHT = 6
BOARD_WIDTH = 7
BOTTOM_INTEND = SCREEN_SIZE[1] // 6
CELL_SIZE = (SCREEN_SIZE[1] - BOTTOM_INTEND) // (BOARD_HEIGHT + 2)
LEFT_INTEND = (SCREEN_SIZE[0] - CELL_SIZE * BOARD_WIDTH) // 2
TOP_INTEND = 2 * CELL_SIZE
LEN_OF_CHAIN = 4


placed_boxes = pygame.sprite.Group()
background = pygame.sprite.Group()
ground_border = pygame.sprite.Group()
falling_boxes = pygame.sprite.Group()
player_mark = pygame.sprite.Group()

menu_sprites = pygame.sprite.Group()



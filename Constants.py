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
rocks = pygame.sprite.Group()
falling_boxes = pygame.sprite.Group()
player_mark = pygame.sprite.Group()
menu_sprites = pygame.sprite.Group()
score_desk = pygame.sprite.Group()


back = pygame.sprite.Sprite(background)
back.image = pygame.transform.scale(load_image("Background.jpg"), SCREEN_SIZE)
back.rect = back.image.get_rect()
back.rect.x = 0
back.rect.y = 0


deskX = pygame.sprite.Sprite(score_desk)
deskX.image = pygame.transform.scale(load_image("Label3.png"), (SCREEN_SIZE[0] * 0.14, SCREEN_SIZE[1] * 0.1))
deskX.rect = deskX.image.get_rect()
deskX.rect.x = SCREEN_SIZE[0] * 0.83
deskX.rect.y = SCREEN_SIZE[1] * 0.15

deskO = pygame.sprite.Sprite(score_desk)
deskO.image = pygame.transform.scale(load_image("Label3.png"), (SCREEN_SIZE[0] * 0.14, SCREEN_SIZE[1] * 0.1))
deskO.rect = deskO.image.get_rect()
deskO.rect.x = SCREEN_SIZE[0] * 0.83
deskO.rect.y = SCREEN_SIZE[1] * 0.27

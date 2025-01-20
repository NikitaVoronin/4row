import pygame
from LoadTextures import *

pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


SCREEN_SIZE = pygame.display.get_window_size()


placed_boxes = pygame.sprite.Group()
background = pygame.sprite.Group()
ground_border = pygame.sprite.Group()
falling_boxes = pygame.sprite.Group()
player_mark = pygame.sprite.Group()

menu_sprites = pygame.sprite.Group()



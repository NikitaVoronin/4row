import pygame
from LoadTextures import *


class Box_O(pygame.sprite.Sprite):
    image = load_image('o.png')
    image = pygame.transform.scale(image, (135, 135))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Box_O.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Box_X(pygame.sprite.Sprite):
    image = load_image('x.png')
    image = pygame.transform.scale(image, (135, 135))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = Box_X.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

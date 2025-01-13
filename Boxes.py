import pygame
from LoadTextures import *


class BoxO(pygame.sprite.Sprite):
    image = load_image('O_Box.png')
    image_selected = load_image('O_AllocatedBox.png')
    image = pygame.transform.scale(image, (135, 135))
    image_selected = pygame.transform.scale(image_selected, (135, 135))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = BoxO.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 15

    def update(self, *args):
        self.rect = self.rect.move(0, self.velocity)
        if pygame.sprite.spritecollideany(self, args[1]) or pygame.sprite.spritecollideany(self, args[2]):
            self.kill()

        if args[0] is not None:
            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
                    self.rect.collidepoint(args[0].pos)):
                self.image = self.image_selected


class BoxX(pygame.sprite.Sprite):
    image = load_image('X_Box.png')
    image_selected = load_image('X_AllocatedBox.png')
    image = pygame.transform.scale(image, (135, 135))
    image_selected = pygame.transform.scale(image_selected, (135, 135))

    def __init__(self, x, y, *group):
        super().__init__(*group)
        self.image = BoxX.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 15

    def update(self, *args):
        self.rect = self.rect.move(0, self.velocity)
        if pygame.sprite.spritecollideany(self, args[1]) or pygame.sprite.spritecollideany(self, args[2]):
            self.kill()

        if args[0] is not None:
            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
                    self.rect.collidepoint(args[0].pos)):
                self.image = self.image_selected

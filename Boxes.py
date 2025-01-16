import pygame
from LoadTextures import *
from Constants import *


class BoxO(pygame.sprite.Sprite):
    image = load_image('O_Box.png')
    image_selected = load_image('O_AllocatedBox.png')
    image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
    image_selected = pygame.transform.scale(image_selected, (CELL_SIZE, CELL_SIZE))

    def __init__(self, x, y, selected, *group):
        super().__init__(*group)
        if selected:
            self.image = BoxO.image_selected
        else:
            self.image = BoxO.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 15

    def update(self, *args):
        self.rect = self.rect.move(0, self.velocity)
        if pygame.sprite.spritecollideany(self, args[1]) or pygame.sprite.spritecollideany(self, args[2]):
            self.kill()
            self.velocity = 0

        if args[0] is not None:
            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
                    self.rect.collidepoint(args[0].pos)):
                self.image = self.image_selected


class BoxX(pygame.sprite.Sprite):
    image = load_image('X_Box.png')
    image_selected = load_image('X_AllocatedBox.png')
    image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
    image_selected = pygame.transform.scale(image_selected, (CELL_SIZE, CELL_SIZE))

    def __init__(self, x, y, selected, *group):
        super().__init__(*group)
        if selected:
            self.image = BoxX.image_selected
        else:
            self.image = BoxX.image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 15

    def update(self, *args):
        self.rect = self.rect.move(0, self.velocity)
        if pygame.sprite.spritecollideany(self, args[1]) or pygame.sprite.spritecollideany(self, args[2]):
            self.kill()
            self.velocity = 0

        if args[0] is not None:
            if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
                    self.rect.collidepoint(args[0].pos)):
                self.image = self.image_selected

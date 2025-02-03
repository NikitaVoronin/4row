import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, image, function, *group):
        super().__init__(*group)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.function = function

    def update(self, *args):
        if (args and args[0].type == pygame.MOUSEBUTTONDOWN and
                self.rect.collidepoint(args[0].pos)):
            self.function()

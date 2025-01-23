import pygame
from LoadTextures import *
from Constants import *


class BoxO(pygame.sprite.Sprite):
    def __init__(self, x, y, size, selected, *group):
        super().__init__(*group)
        if selected:
            self.image = pygame.transform.scale(load_image('O_AllocatedBox.png'), (size, size))
        else:
            self.image = pygame.transform.scale(load_image('O_Box.png'), (size, size))
        self.selected = selected
        self.size = size
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 15

    def update(self, left, top,  *args):
        if len(args) == 3:
            if (pygame.sprite.spritecollideany(self, args[0]) or pygame.sprite.spritecollideany(self, args[1]) or
                    pygame.sprite.spritecollideany(self, args[2])):
                self.velocity = 0
                self.kill()
                cell_x, cell_y = (self.rect.x - left) // self.size, (self.rect.y - top) // self.size
                placed_boxes.add(BoxO(left + self.size * cell_x, top + self.size * cell_y, self.size, False))
            else:
                self.velocity = 15
                self.rect = self.rect.move(0, self.velocity)

        else:
            x, y = args
            screen_cords = left + self.size * x, top + self.size * y
            if self.rect.collidepoint(screen_cords):
                self.kill()
                placed_boxes.add(BoxO(screen_cords[0], screen_cords[1], self.size, not self.selected))


class BoxX(pygame.sprite.Sprite):
    def __init__(self, x, y, size, selected, *group):
        super().__init__(*group)
        if selected:
            self.image = pygame.transform.scale(load_image('X_AllocatedBox.png'), (size, size))
        else:
            self.image = pygame.transform.scale(load_image('X_Box.png'), (size, size))
        self.selected = selected
        self.size = size
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = 15

    def update(self, left, top,  *args):
        if len(args) == 3:
            if (pygame.sprite.spritecollideany(self, args[0]) or pygame.sprite.spritecollideany(self, args[1]) or
                    pygame.sprite.spritecollideany(self, args[2])):
                self.velocity = 0
                self.kill()
                cell_x, cell_y = (self.rect.x - left) // self.size, (self.rect.y - top) // self.size
                placed_boxes.add(BoxX(left + self.size * cell_x, top + self.size * cell_y, self.size, False, placed_boxes))
            else:
                self.velocity = 15
                self.rect = self.rect.move(0, self.velocity)

        else:
            x, y = args
            screen_cords = left + self.size * x, top + self.size * y
            if self.rect.collidepoint(screen_cords):
                self.kill()
                placed_boxes.add(BoxX(screen_cords[0], screen_cords[1], self.size, not self.selected))


class Rock(pygame.sprite.Sprite):
    def __init__(self, x, y, size, *group):
        super().__init__(*group)
        self.image = pygame.transform.scale(load_image('YEEEEE_ROOOCK.png'), (size, size))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


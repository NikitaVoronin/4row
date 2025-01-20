import pygame
from LoadTextures import *
from Constants import *


empty_checkbox = load_image('EmptyCheckbox1.png')
filled_checkbox = load_image('FilledCheckbox1.png')
label1 = load_image('Label1.png')
label2 = load_image('Label2.png')
up_arrow = load_image('Up.png')
right_arrow = load_image('Right.png')
left_arrow = load_image('Left.png')
down_arrow = load_image('Down.png')


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


class Menu:
    def __init__(self):
        self.width = SCREEN_SIZE[0]
        self.height = SCREEN_SIZE[1]
        self.buttons = []
        self.menu_flag = True
        self.play_button = Button(SCREEN_SIZE[0] - LEFT_INDENT * 1.1,
                                  SCREEN_SIZE[1] - TOP_INDENT * 1.3,
                                  pygame.transform.scale(load_image('Label1.png'),
                                                         (CELL_SIZE * 2, CELL_SIZE * 0.8)),
                                  self.start_game,
                                  menu_sprites)

    def render(self):
        background.draw(screen)
        menu_sprites.draw(screen)

    def start_game(self):
        self.menu_flag = False






import pygame
from LoadTextures import *
from Constants import *


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
        self.screen_width = SCREEN_SIZE[0]
        self.screen_height = SCREEN_SIZE[1]
        self.board_width = 7
        self.board_height = 6
        self.menu_flag = True
        self.font = pygame.font.Font('chinese.stxinwei.ttf', int(SCREEN_SIZE[0] * 0.025))

        self.mode_classic = True
        self.endless_height_flag = False

        self.text_mode_classic = self.font.render('Classic', True, (255, 255, 255))
        self.text_mode_score = self.font.render('Score', True, (255, 255, 255))
        self.text_endless_height = self.font.render('Endless height', True, (255, 255, 255))
        self.text_play = self.font.render('PLAY', True, (255, 255, 255))

        self.button_play_size = (SCREEN_SIZE[1] * 0.3, SCREEN_SIZE[1] * 0.12)
        self.button_play_intend = (SCREEN_SIZE[0] * 0.7, SCREEN_SIZE[1] * 0.8)
        self.button_play = Button(self.button_play_intend[0],
                                  self.button_play_intend[1],
                                  pygame.transform.scale(load_image('Label1.png'),
                                                         self.button_play_size),
                                  self.start_game,
                                  menu_sprites)

        self.button_mode_size = (SCREEN_SIZE[0] * 0.1125, SCREEN_SIZE[1] * 0.08)
        self.button_mode_classic_intend = (SCREEN_SIZE[0] * 0.1125, SCREEN_SIZE[1] * 0.08)
        self.button_mode_classic = Button(self.button_mode_classic_intend[0],
                                          self.button_mode_classic_intend[1],
                                          pygame.transform.scale(load_image('Label2.png'),
                                                                 self.button_mode_size),
                                          self.choose_mode_classic,
                                          menu_sprites)

        self.button_mode_score_intend = (SCREEN_SIZE[0] * 0.225, SCREEN_SIZE[1] * 0.08)
        self.button_mode_score = Button(self.button_mode_score_intend[0],
                                        self.button_mode_score_intend[1],
                                        pygame.transform.scale(load_image('Label1.png'),
                                                               self.button_mode_size),
                                        self.choose_mode_score,
                                        menu_sprites)

        self.checkbox_size = (SCREEN_SIZE[1] * 0.08, SCREEN_SIZE[1] * 0.08)
        self.checkbox_endless_height_intend = (self.button_mode_classic_intend[0] + self.text_endless_height.get_width() + self.checkbox_size[0], SCREEN_SIZE[1] * 0.2)
        self.checkbox_endless_height = Button(self.checkbox_endless_height_intend[0],
                                              self.checkbox_endless_height_intend[1],
                                              pygame.transform.scale(load_image('EmptyCheckbox1.png'),
                                                                     self.checkbox_size),
                                              self.endless_height,
                                              menu_sprites)

    def render(self):
        menu_sprites.draw(screen)

        text_mode_classic_intend = (self.button_mode_classic_intend[0] + (self.button_mode_size[0] - self.text_mode_classic.get_width()) // 2,
                                    self.button_mode_classic_intend[1] + (self.button_mode_size[1] - self.text_mode_classic.get_height()) // 2)
        screen.blit(self.text_mode_classic, text_mode_classic_intend)

        text_mode_score_intend = (self.button_mode_score_intend[0] + (self.button_mode_size[0] - self.text_mode_score.get_width()) // 2,
                                  self.button_mode_score_intend[1] + (self.button_mode_size[1] - self.text_mode_score.get_height()) // 2)
        screen.blit(self.text_mode_score, text_mode_score_intend)

        text_endless_height_intend = (self.button_mode_classic_intend[0],
                                      self.checkbox_endless_height_intend[1] + (self.checkbox_size[1] - self.text_endless_height.get_height()) // 2)
        screen.blit(self.text_endless_height, text_endless_height_intend)

        text_play_intend = (self.button_play_intend[0] + (self.button_play_size[0] - self.text_play.get_width()) // 2,
                            self.button_play_intend[1] + (self.button_play_size[1] - self.text_play.get_height()) // 2)
        screen.blit(self.text_play, text_play_intend)



    def start_game(self):
        self.menu_flag = False

    def choose_mode_classic(self):
        self.mode_classic = True
        self.button_mode_classic.image = pygame.transform.scale(load_image('Label2.png'),
                                                                (CELL_SIZE * 2, CELL_SIZE * 0.8))
        self.button_mode_score.image = pygame.transform.scale(load_image('Label1.png'),
                                                              (CELL_SIZE * 2, CELL_SIZE * 0.8))

    def choose_mode_score(self):
        self.mode_classic = False
        self.button_mode_classic.image = pygame.transform.scale(load_image('Label1.png'),
                                                                (CELL_SIZE * 2, CELL_SIZE * 0.8))
        self.button_mode_score.image = pygame.transform.scale(load_image('Label2.png'),
                                                              (CELL_SIZE * 2, CELL_SIZE * 0.8))

    def endless_height(self):
        self.endless_height_flag = not self.endless_height_flag
        if self.endless_height_flag:
            self.checkbox_endless_height.image = pygame.transform.scale(load_image('FilledCheckbox1.png'),
                                                                        (SCREEN_SIZE[1] * 0.08, SCREEN_SIZE[1] * 0.08))
        else:
            self.checkbox_endless_height.image = pygame.transform.scale(load_image('EmptyCheckbox1.png'),
                                                                        (SCREEN_SIZE[1] * 0.08, SCREEN_SIZE[1] * 0.08))






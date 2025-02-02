import pygame
import pprint
from Boxes import *
from Constants import *
from MatrixMaster import *
from Button import *


class Board:
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT
        self.left = LEFT_INTEND
        self.top = TOP_INTEND
        self.cell_size = CELL_SIZE

        self.relief_cords = []
        self.selected_boxes = []
        self.score_X = 0
        self.score_O = 0
        self.max_score = 10000

        self.font_size = int(SCREEN_SIZE[0] * 0.025)
        self.font = pygame.font.Font('chinese.stxinwei.ttf', self.font_size)

        self.winner = None
        self.mode_classic = True
        self.endless_height_flag = False
        self.relief_field_flag = False
        self.len_of_chain = 4
        self.pause_flag = False
        self.game_flag = False
        
        self.button_pause = Button(SCREEN_SIZE[0] * 0.02,
                                   SCREEN_SIZE[1] * 0.035,
                                   pygame.transform.scale(load_image('Pause.png'),
                                                          (SCREEN_SIZE[1] * 0.08, SCREEN_SIZE[1] * 0.08)),
                                   self.pause,
                                   game_sprites)

        self.button_restart = Button(SCREEN_SIZE[0] * 0.02,
                                     SCREEN_SIZE[1] * 0.2,
                                     pygame.transform.scale(load_image('label1.png'),
                                                            (SCREEN_SIZE[1] * 0.16, SCREEN_SIZE[1] * 0.08)),
                                     self.restart,
                                     pause_sprites)

        self.button_menu = Button(SCREEN_SIZE[0] * 0.02,
                                  SCREEN_SIZE[1] * 0.3,
                                  pygame.transform.scale(load_image('label1.png'),
                                                         (SCREEN_SIZE[1] * 0.16, SCREEN_SIZE[1] * 0.08)),
                                  self.to_menu,
                                  pause_sprites)

        self.error_text = self.font.render('', True, (255, 0, 0))

    def render(self, screen):
        self.change_player_mark()
        falling_boxes.draw(screen)
        placed_boxes.draw(screen)
        player_mark.draw(screen)
        rocks.draw(screen)
        falling_boxes.update(self.left, self.top, ground_border, placed_boxes, rocks)
        falling_rocks.update(self.left, self.top, ground_border)
        game_sprites.draw(screen)
        winner_sprite.draw(screen)

        # Отрисовка клеток на поле
        for i in range(self.height):
            for j in range(self.width):
                cords = (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 255), cords, 1)

        # Отрисовка комней на поле, если они есть
        if self.relief_cords and len(rocks.sprites()) == 0:
            for cord in self.relief_cords:
                x, y = cord
                screen_cords = (self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size)
                Rock(*screen_cords, rocks)

        # Отрисовка меню паузы
        if self.pause_flag:
            pause_sprites.draw(screen)
            text_restart = self.font.render('Restart', True, (255, 255, 255))
            text_menu = self.font.render('Menu', True, (255, 255, 255))

            screen.blit(text_restart, (SCREEN_SIZE[0] * 0.02 + (SCREEN_SIZE[1] * 0.16 - text_restart.get_width()) // 2,
                                       SCREEN_SIZE[1] * 0.2 + (SCREEN_SIZE[1] * 0.08 - text_restart.get_height()) // 2))
            screen.blit(text_menu, (SCREEN_SIZE[0] * 0.02 + (SCREEN_SIZE[1] * 0.16 - text_menu.get_width()) // 2,
                                    SCREEN_SIZE[1] * 0.3 + (SCREEN_SIZE[1] * 0.08 - text_menu.get_height()) // 2))

        # Отрисовка интерфейса для режима на очки
        if not self.mode_classic:
            score_sprites.draw(screen)
            text_score = self.font.render('SCORE', True, (255, 255, 255))
            text_X = self.font.render('X', True, (255, 255, 255))
            text_O = self.font.render('O', True, (255, 255, 255))
            text_score_X = self.font.render(str(self.score_X), True, (255, 255, 255))
            text_score_O = self.font.render(str(self.score_O), True, (255, 255, 255))
            text_get_score = self.font.render('Get score', True, (255, 255, 255))

            screen.blit(text_score, (SCREEN_SIZE[0] * 0.83 + (SCREEN_SIZE[0] * 0.14 - text_score.get_width()) // 2,
                                     SCREEN_SIZE[1] * 0.07))
            screen.blit(text_X, (SCREEN_SIZE[0] * 0.8,
                                 SCREEN_SIZE[1] * 0.15 + (SCREEN_SIZE[1] * 0.1 - text_X.get_height()) // 2))
            screen.blit(text_O, (SCREEN_SIZE[0] * 0.8,
                                 SCREEN_SIZE[1] * 0.27 + (SCREEN_SIZE[1] * 0.1 - text_O.get_height()) // 2))
            screen.blit(text_get_score, (SCREEN_SIZE[0] * 0.8 + (SCREEN_SIZE[0] * 0.16 - text_get_score.get_width()) // 2,
                                         SCREEN_SIZE[1] * 0.8 + (SCREEN_SIZE[1] * 0.12 - text_get_score.get_height()) // 2))
            screen.blit(self.error_text, ((SCREEN_SIZE[0] - self.error_text.get_width()) // 2,
                                          SCREEN_SIZE[1] * 0.91))

            screen.blit(text_score_X, (SCREEN_SIZE[0] * 0.83 + (SCREEN_SIZE[0] * 0.14 - text_score_X.get_width()) // 2,
                                       SCREEN_SIZE[1] * 0.15 + (SCREEN_SIZE[1] * 0.1 - text_score_X.get_height()) // 2))
            screen.blit(text_score_O, (SCREEN_SIZE[0] * 0.83 + (SCREEN_SIZE[0] * 0.14 - text_score_O.get_width()) // 2,
                                       SCREEN_SIZE[1] * 0.27 + (SCREEN_SIZE[1] * 0.1 - text_score_O.get_height()) // 2))

        # Выделение выигрывших клеток и отрисовка сообщения о победе
        if self.winner:
            for cell_cord in self.winner[1]:
                rect_cords = (self.left + self.cell_size * cell_cord[0], self.top + self.cell_size * cell_cord[1],
                              self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 75), rect_cords, int(SCREEN_SIZE[1] * 0.009))

            self.desk_winner = pygame.sprite.Sprite(winner_sprite)
            self.desk_winner.image = pygame.transform.scale(load_image("Label3.png"),
                                                            (SCREEN_SIZE[0] * 0.25, SCREEN_SIZE[1] * 0.18))
            self.desk_winner.rect = self.desk_winner.image.get_rect()
            self.desk_winner.rect.x = SCREEN_SIZE[0] * 0.02
            self.desk_winner.rect.y = SCREEN_SIZE[1] * 0.4

            text = self.font.render(self.winner[0].upper(), True, (255, 255, 255))
            screen.blit(text, (SCREEN_SIZE[0] * 0.02 + (SCREEN_SIZE[0] * 0.25 - text.get_width()) // 2,
                               SCREEN_SIZE[1] * 0.4 + (SCREEN_SIZE[1] * 0.18 - text.get_height()) // 2))

    def get_cell(self, mouse_pos):
        # Конвертация координат на экране в кординаты на поле
        x, y = mouse_pos
        if (0 <= (x - self.left) // self.cell_size <= self.width and
                0 <= (y - self.top) // self.cell_size <= self.height):
            return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size
        else:
            return None

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell_coords):
        # Обработка событий при нажатии
        if cell_coords is None or cell_coords[0] > self.width - 1 or cell_coords[1] > self.height - 1:
            return
        x, y = cell_coords

        if not self.pause_flag:
            if self.endless_height_flag:
                self.delete_last_row()

            if self.board[y][x][0] is None:
                self.spawn_new_box(x, y)

            elif self.board[y][x][0] == self.player and not self.mode_classic:
                placed_boxes.update(self.left, self.top, x, y)
                self.player = not self.player
                self.select_box(x, y)

            elif self.board[y][x][0] == (not self.player):
                self.player = not self.player

            self.player = not self.player

            self.change_player_mark()
            self.error_text = self.font.render('', True, (255, 0, 0))

    def spawn_new_box(self, x, y):
        if not self.mode_classic and self.selected_boxes:
            self.clear_select()

        # Создание нового ящика
        if self.player:
            BoxX(self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, self.board[y][x][1], falling_boxes)
        else:
            BoxO(self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, self.board[y][x][1], falling_boxes)

        # Падение ящика внутри матрицы
        while self.board[y][x][0] is None:
            if y == self.height - 1 or self.board[y + 1][x][0] is not None:
                break
            else:
                y += 1

        self.board[y][x][0] = self.player
        self.winner = self.matrix_master.new_trick((x, y))
        if self.winner:
            self.pause_flag = True

    def select_box(self, x, y):
        if (x, y) not in self.selected_boxes:
            self.selected_boxes.append((x, y))
        else:
            self.selected_boxes.remove((x, y))

        if not self.board[y][x][1]:
            self.board[y][x][1] = True
        else:
            self.board[y][x][1] = False
        return True

    def clear_select(self):
        for box in placed_boxes.sprites():
            box.deselect()
        self.selected_boxes = []

    def delete_last_row(self):
        # Проверка, достаточно ли заполнено поле, чтобы удалить ряд
        n = 0
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j][0] is not None:
                    n += 1

        if n >= int(self.width * self.height * 0.8):
            # Новое состояние матрицы
            self.board = self.matrix_master.del_last_row(self.board)

            # Удаление спрайтов нижней линии и падение остальных
            for box in placed_boxes.sprites():
                if box.rect.y == self.top + self.cell_size * (self.height - 1):
                    box.kill()
                else:
                    falling_boxes.add(box)
            else:
                placed_boxes.empty()

            if self.relief_field_flag:
                new_relief = []
                for cord in self.relief_cords:
                    if cord[1] == self.height - 1:
                        continue
                    else:
                        new_relief.append((cord[0], cord[1] + 1))
                self.relief_cords = new_relief

                for rock in rocks.sprites():
                    if rock.rect.y == self.top + self.cell_size * (self.height - 1):
                        rock.kill()
                    else:
                        falling_rocks.add(rock)
                else:
                    rocks.empty()

    def set_board(self):
        # Функция приводит список Board в начальное положение
        player_mark.empty()
        placed_boxes.empty()
        falling_boxes.empty()
        rocks.empty()
        falling_boxes.empty()

        # Создание пустой матрицы
        self.board = []
        for i in range(self.height):
            self.board.append([])
            for j in range(self.width):
                self.board[-1].append([None, False])

        if self.mode_classic is True:
            mode = 'classic'
        else:
            mode = 'score'

        # Обнуление доски в обработчике матрице
        self.matrix_master = MatrixMaster((self.width, self.height), mode, self.endless_height_flag,
                                          self.len_of_chain, self.relief_field_flag)

        if self.matrix_master.moving_now == 'X':
            self.player = True
            BoxX(self.left // 3, self.top // 3, self.cell_size, False, player_mark)
        else:
            self.player = False
            BoxO(self.left // 3, self.top // 3, self.cell_size, False, player_mark)

        # Создание нового рельефа на поле
        if self.relief_field_flag:
            self.relief_cords = self.matrix_master.relief
            for rock in self.relief_cords:
                x, y = rock
                self.board[y][x][0] = 0
                
        if not self.mode_classic:
            deskX = pygame.sprite.Sprite(score_sprites)
            deskX.image = pygame.transform.scale(load_image("Label3.png"), (SCREEN_SIZE[0] * 0.14, SCREEN_SIZE[1] * 0.1))
            deskX.rect = deskX.image.get_rect()
            deskX.rect.x = SCREEN_SIZE[0] * 0.83
            deskX.rect.y = SCREEN_SIZE[1] * 0.15

            deskO = pygame.sprite.Sprite(score_sprites)
            deskO.image = pygame.transform.scale(load_image("Label3.png"), (SCREEN_SIZE[0] * 0.14, SCREEN_SIZE[1] * 0.1))
            deskO.rect = deskO.image.get_rect()
            deskO.rect.x = SCREEN_SIZE[0] * 0.83
            deskO.rect.y = SCREEN_SIZE[1] * 0.27

            self.button_get_score = Button(SCREEN_SIZE[0] * 0.8,
                                           SCREEN_SIZE[1] * 0.8,
                                           pygame.transform.scale(load_image("Label1.png"),
                                                                  (SCREEN_SIZE[0] * 0.16, SCREEN_SIZE[1] * 0.12)),
                                           self.get_score,
                                           score_sprites)

    def get_score(self):
        try:
            score = self.matrix_master.scoring(self.selected_boxes)

            # Удаление выбранных ящиков из списка board
            for cord in self.selected_boxes:
                x, y = cord
                while y > 0 and self.board[y][x][0] is not None:
                    self.board[y][x][0] = self.board[y - 1][x][0]
                    y -= 1
                else:
                    self.board[y][x][0] = None

                x, y = cord

                for box in placed_boxes:
                    if (box.rect.x == self.left + self.cell_size * x and
                            box.rect.y == self.top + self.cell_size * y):
                        box.kill()

            # Начало падения ящиков
            for box in placed_boxes:
                box.kill()
                falling_boxes.add(box)
            else:
                placed_boxes.empty()

            # Проверка выигрыша
            if self.player:
                self.score_X += score
                if self.score_X >= self.max_score:
                    self.winner = 'crosses win'
            else:
                self.score_O += score
                if self.score_O >= self.max_score:
                    self.winner = 'nulls win'

            self.player = not self.player

            self.change_player_mark()
            self.selected_boxes = []

        except ModeError as e:
            self.error_text = self.font.render(str(e), True, (255, 0, 0))

        except TricksChoiceIsWrong as e:
            self.error_text = self.font.render(str(e), True, (255, 0, 0))

    def change_player_mark(self):
        # Изменение индикатора игрока, который сейчас делает ход
        player_mark.empty()
        if self.player:
            BoxX(self.left // 3, self.top // 3, SCREEN_SIZE[1] * 5 // 48, False, player_mark)
        else:
            BoxO(self.left // 3, self.top // 3, SCREEN_SIZE[1] * 5 // 48, False, player_mark)

    def pause(self):
        self.pause_flag = not self.pause_flag
        if self.pause_flag:
            self.button_pause.image = pygame.transform.scale(load_image('Play.png'),
                                                              (SCREEN_SIZE[1] * 0.08, SCREEN_SIZE[1] * 0.08))
        else:
            self.button_pause.image = pygame.transform.scale(load_image('Pause.png'),
                                   (SCREEN_SIZE[1] * 0.08, SCREEN_SIZE[1] * 0.08))

    def restart(self):
        # Обнуление констант
        winner_sprite.empty()
        self.set_board()
        self.pause_flag = False
        self.winner = None
        self.score_X = 0
        self.score_O = 0
        self.button_pause.image = pygame.transform.scale(load_image('Pause.png'),
                                                         (SCREEN_SIZE[1] * 0.08, SCREEN_SIZE[1] * 0.08))

    def to_menu(self):
        self.relief_cords = []
        self.pause_flag = False
        self.button_pause.image = pygame.transform.scale(load_image('Pause.png'),
                                                         (SCREEN_SIZE[1] * 0.08, SCREEN_SIZE[1] * 0.08))
        self.game_flag = False

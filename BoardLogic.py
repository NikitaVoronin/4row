import pygame
import pprint
from Boxes import *
from Constants import *
from MatrixMaster import *


class Board:
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT

        self.winner = None
        self.relief_cords = []
        self.selected_boxes = []
        self.score_X = 0
        self.score_O = 0

        self.left = LEFT_INTEND
        self.top = TOP_INTEND
        self.cell_size = CELL_SIZE
        self.font = pygame.font.Font('chinese.stxinwei.ttf', int(SCREEN_SIZE[0] * 0.025))

        self.mode_classic = True
        self.endless_height_flag = False
        self.relief_field_flag = False
        self.len_of_chain = 4

        self.text_score = self.font.render('SCORE', True, (255, 255, 255))
        self.text_X = self.font.render('X', True, (255, 255, 255))
        self.text_O = self.font.render('O', True, (255, 255, 255))
        self.text_score_X = self.font.render(str(self.score_X), True, (255, 255, 255))
        self.text_score_O = self.font.render(str(self.score_O), True, (255, 255, 255))

    def render(self, screen):
        falling_boxes.draw(screen)
        player_mark.draw(screen)
        rocks.draw(screen)
        falling_boxes.update(self.left, self.top, ground_border, placed_boxes, rocks)
        falling_rocks.update(self.left, self.top, ground_border)
        placed_boxes.draw(screen)

        for i in range(self.height):
            for j in range(self.width):
                cords = (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 255), cords, 1)

        if self.relief_cords and len(rocks.sprites()) == 0:
            for cord in self.relief_cords:
                x, y = cord
                screen_cords = (self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size)
                Rock(*screen_cords, rocks)

        if not self.mode_classic:
            score_desk.draw(screen)

            screen.blit(self.text_score, (SCREEN_SIZE[0] * 0.83 + (SCREEN_SIZE[0] * 0.14 - self.text_score.get_width()) // 2,
                                          SCREEN_SIZE[1] * 0.07))
            screen.blit(self.text_X, (SCREEN_SIZE[0] * 0.8,
                                      SCREEN_SIZE[1] * 0.15 + (SCREEN_SIZE[1] * 0.1 - self.text_X.get_height()) // 2))
            screen.blit(self.text_O, (SCREEN_SIZE[0] * 0.8,
                                      SCREEN_SIZE[1] * 0.27 + (SCREEN_SIZE[1] * 0.1 - self.text_O.get_height()) // 2))

            screen.blit(self.text_score_X, (SCREEN_SIZE[0] * 0.83 + (SCREEN_SIZE[0] * 0.14 - self.text_score_X.get_width()) // 2,
                                            SCREEN_SIZE[1] * 0.15 + (SCREEN_SIZE[1] * 0.1 - self.text_score_X.get_height()) // 2))
            screen.blit(self.text_score_O, (SCREEN_SIZE[0] * 0.83 + (SCREEN_SIZE[0] * 0.14 - self.text_score_O.get_width()) // 2,
                                            SCREEN_SIZE[1] * 0.27 + (SCREEN_SIZE[1] * 0.1 - self.text_score_O.get_height()) // 2))

        if self.winner:
            for cell_cord in self.winner[1]:
                rect_cords = (self.left + self.cell_size * cell_cord[0], self.top + self.cell_size * cell_cord[1],
                              self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 75), rect_cords, int(SCREEN_SIZE[1] * 0.009))

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        if (0 <= (x - self.left) // self.cell_size <= self.width and
                0 <= (y - self.top) // self.cell_size <= self.height):
            return (x - self.left) // self.cell_size, (y - self.top) // self.cell_size
        else:
            return None

    def on_click(self, cell_coords):
        if cell_coords is None or cell_coords[0] > self.width - 1 or cell_coords[1] > self.height - 1:
            return
        x, y = cell_coords

        if self.endless_height_flag:
            n = 0
            for i in range(len(self.board)):
                for j in range(len(self.board[0])):
                    if self.board[i][j][0] is not None:
                        n += 1
            if n >= int(self.width * self.height * 0.8):
                self.board = self.matrix_master.del_last_row(self.board)
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

        if self.board[y][x][0] is None:
            self.spawn_new_box(x, y)

        elif self.board[y][x][0] == self.player:
            if not self.mode_classic:
                placed_boxes.update(self.left, self.top, x, y)
                self.player = not self.player

        elif self.board[y][x][0] != self.player:
            self.player = not self.player

        self.player = not self.player

        player_mark.empty()
        if self.player:
            BoxX(self.left // 3, self.top // 3, SCREEN_SIZE[1] * 5 // 48, False, player_mark)
        else:
            BoxO(self.left // 3, self.top // 3, SCREEN_SIZE[1] * 5 // 48, False, player_mark)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def spawn_new_box(self, x, y):
        if self.player:
            BoxX(self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, self.board[y][x][1], falling_boxes)
        else:
            BoxO(self.left + self.cell_size * x, self.top + self.cell_size * y, self.cell_size, self.board[y][x][1], falling_boxes)

        while self.board[y][x][0] is None:
            if y == self.height - 1 or self.board[y + 1][x][0] is not None:
                break
            else:
                y += 1

        self.board[y][x][0] = self.player
        self.winner = self.matrix_master.new_trick((x, y))

    def select_box(self, x, y):
        self.board[y][x][1] = not self.board[y][x][1]
        return True

    def set_board(self, board):
        player_mark.empty()

        self.board = board
        if self.mode_classic is True:
            mode = 'classic'
        else:
            mode = 'score'

        self.matrix_master = MatrixMaster((self.width, self.height), mode, self.endless_height_flag,
                                          self.len_of_chain, self.relief_field_flag)

        if self.matrix_master.moving_now == 'X':
            self.player = True
            BoxX(self.left // 3, self.top // 3, self.cell_size, False, player_mark)
        else:
            self.player = False
            BoxO(self.left // 3, self.top // 3, self.cell_size, False, player_mark)

        if self.relief_field_flag:
            self.relief_cords = self.matrix_master.relief
            for rock in self.relief_cords:
                x, y = rock
                self.board[y][x][0] = 0

        if not self.mode_classic:
            pass

import pygame
from Boxes import *
from Constants import *
from MatrixMaster import *


class Board:
    def __init__(self):
        self.width = BOARD_WIDTH
        self.height = BOARD_HEIGHT

        self.winner = None

        self.left = LEFT_INTEND
        self.top = TOP_INTEND
        self.cell_size = CELL_SIZE

        self.mode_classic = True
        self.endless_height_flag = False
        self.relief_field_flag = False
        self.len_of_chain = 4

    def render(self, screen):
        falling_boxes.draw(screen)
        player_mark.draw(screen)
        rocks.draw(screen)
        falling_boxes.update(ground_border, placed_boxes)
        placed_boxes.draw(screen)

        for i in range(self.height):
            for j in range(self.width):
                cords = (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, (255, 255, 255), cords, 1)

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
            if n >= int(self.width * self.height * 0.5):
                self.board = self.matrix_master.del_last_row(self.board)
                print(self.board)

        if self.board[y][x][0] is None:
            self.spawn_new_box(x, y)

        elif self.board[y][x][0] == self.player:
            if self.select_box(x, y):
                self.player = not self.player

        self.player = not self.player
        player_mark.empty()
        if self.player:
            BoxX(self.left // 3, self.top // 3, self.cell_size, False, player_mark)
        else:
            BoxO(self.left // 3, self.top // 3, self.cell_size, False, player_mark)

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
            relief_cords = self.matrix_master.make_relief()
            for cord in relief_cords:
                i, j = cord
                screen_cords = (self.left + self.cell_size * j, self.top + self.cell_size * i, self.cell_size)
                Rock(*screen_cords, rocks)

